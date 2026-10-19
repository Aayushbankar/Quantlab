import json
import os
import sys

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.adapter import execute_backtest
from src.api.cache import compute_run_id
from src.api.db import (
    get_cached_run,
    get_trial_sharpes,
    get_trials_count,
    init_db,
    list_recent_runs,
    list_trials,
    save_run,
)
from src.api.replay import get_replay_run
from src.api.schemas import (
    BacktestRequest,
    BacktestResponse,
    ErrorResponse,
    HealthResponse,
    StrategyMetadata,
    SweepSummaryResponse,
    TrialsResponse,
    UniverseResponse,
)
from src.data.universe import get_benchmark, get_universe

app = FastAPI(
    title="Pramaan API",
    description="REST interface for the Pramaan backtesting engine & overfitting diagnostic platform (GTU DI05000341).",
    version="1.0.0",
    responses={422: {"model": ErrorResponse}},
)

# CORS configuration (D12: env-configurable origins, no wildcard credentials)
allowed_origins_env = os.environ.get(
    "PRAMAAN_ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000,http://127.0.0.1:8000",
)
allowed_origins = [orig.strip() for orig in allowed_origins_env.split(",") if orig.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc: RequestValidationError):
    error_details = []
    messages = []
    for e in exc.errors():
        msg = str(e.get("msg", ""))
        messages.append(msg)
        error_details.append({"loc": [str(x) for x in e.get("loc", ())], "msg": msg, "type": str(e.get("type", ""))})
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request parameters: " + "; ".join(messages),
                "details": error_details,
            }
        },
    )


@app.exception_handler(ValueError)
def value_error_handler(request, exc: ValueError):
    return JSONResponse(
        status_code=422, content={"error": {"code": "INVALID_ARGUMENT", "message": str(exc), "details": None}}
    )


def is_demo_mode_active() -> bool:
    val = os.environ.get("DEMO_DATA")
    if val is None:
        return False
    return val.strip().lower() in ("1", "true", "yes", "on")


@app.api_route("/health", methods=["GET", "HEAD"], response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="healthy",
        engine="Pramaan Event-Driven Simulation Core",
        version="1.0.0",
        cost_model_version="1.0-indian-delivery-2024",
        python_version=sys.version.split()[0],
        numpy_version=np.__version__,
        pandas_version=pd.__version__,
        demo_mode=is_demo_mode_active(),
    )


@app.get("/strategies", response_model=list[StrategyMetadata])
def get_strategies():
    return [
        StrategyMetadata(
            id="sma_crossover",
            name="SMA Crossover",
            description="Classic moving average trend-following strategy with fast and slow windows.",
            default_params={"fast_window": 20, "slow_window": 50},
            param_ranges={"fast_window": [5, 50], "slow_window": [20, 200]},
        ),
        StrategyMetadata(
            id="sma_crossover_10_30",
            name="SMA Crossover (10, 30)",
            description="Aggressive short-horizon moving average crossover.",
            default_params={"fast_window": 10, "slow_window": 30},
            param_ranges={"fast_window": [5, 30], "slow_window": [15, 60]},
        ),
        StrategyMetadata(
            id="rsi_mean_reversion",
            name="RSI Mean Reversion",
            description="Wilder RSI mean-reversion with oversold buy and overbought sell thresholds.",
            default_params={"period": 14, "oversold": 30.0, "overbought": 70.0},
            param_ranges={"period": [5, 30], "oversold": [10.0, 45.0], "overbought": [55.0, 90.0]},
        ),
        StrategyMetadata(
            id="momentum",
            name="Momentum ROC",
            description="Rate of Change momentum strategy with duplicate-BUY invariant guard.",
            default_params={"lookback_period": 20, "threshold_pct": 0.05},
            param_ranges={"lookback_period": [5, 60], "threshold_pct": [0.01, 0.15]},
        ),
        StrategyMetadata(
            id="bollinger_breakout",
            name="Bollinger Band Breakout",
            description="Volatility channel expansion strategy (20-day SMA, 2 StdDev). Enters on upper-band breakthrough, exits on mean reversion.",
            default_params={"period": 20, "num_std": 2.0},
            param_ranges={"period": [10, 50], "num_std": [1.0, 3.0]},
        ),
        StrategyMetadata(
            id="bh_and_hold",
            name="Buy and Hold Benchmark",
            description="Passive investment control baseline. All active strategies are judged against this null hypothesis.",
            default_params={},
            param_ranges={},
        ),
    ]


@app.get("/universe", response_model=UniverseResponse)
def get_universe_info():
    symbols = get_universe()
    benchmark = get_benchmark()
    return UniverseResponse(
        symbols=symbols, benchmark=benchmark, default_start="2019-01-01", default_end="2024-12-30", total_bars=1480
    )


@app.get("/history")
def get_history(limit: int = 20):
    return list_recent_runs(limit=limit)


@app.get("/ready")
def get_readiness():
    init_db()
    return {"status": "ready", "engine": "Pramaan", "version": "1.0.0"}


@app.get("/trials", response_model=TrialsResponse)
def get_trials(strategy: str | None = None, limit: int = 50, offset: int = 0):
    count = get_trials_count(strategy=strategy)
    items = list_trials(strategy=strategy, limit=limit, offset=offset)
    sharpes = get_trial_sharpes(strategy=strategy)
    var = float(np.var(sharpes, ddof=1)) if len(sharpes) > 1 else 0.0
    return TrialsResponse(
        total_trials=count,
        trials=items,
        cross_trial_variance=round(var, 6),
    )


@app.get("/sweep", response_model=SweepSummaryResponse)
def get_sweep_summary():
    summary_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "experiments",
        "sweep_summary.json",
    )
    if os.path.exists(summary_path):
        with open(summary_path, encoding="utf-8") as f:
            data = json.load(f)
        return SweepSummaryResponse(**data)
    raise HTTPException(status_code=404, detail="No sweep summary found. Run scripts/run_sweep.py first.")


@app.post("/sweep", response_model=SweepSummaryResponse)
def trigger_sweep(max_configs: int = 50):
    from scripts.run_sweep import run_sweep

    summary = run_sweep(max_configs=max_configs, record_to_db=True)
    return SweepSummaryResponse(**summary)


@app.get("/replay/{strategy}", response_model=BacktestResponse)
def replay_strategy(strategy: str, period: str = "full"):
    res = get_replay_run(strategy=strategy, period=period)
    if res:
        res["served_from"] = "replay"
        res["replay_reason"] = f"Verified replay artifact for {strategy} ({period})"
        res.setdefault("engine_version", "1.0.0")
        res.setdefault("cost_profile", "1.0-indian-delivery-2024")
        res.setdefault("data_hash", "committed-replay")
        return BacktestResponse(**res)

    # Dynamic fallback: run on committed dataset
    start_date = "2019-01-01"
    end_date = "2022-12-31" if period == "IS" else "2024-12-30"
    if period == "OOS":
        start_date = "2023-01-01"

    sim_res = execute_backtest(
        strategy_name=strategy,
        params={},
        universe_symbols=["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"],
        start_date=start_date,
        end_date=end_date,
        initial_capital=100000.0,
        apply_costs=True,
    )
    return BacktestResponse(
        run_id=f"replay_{strategy}_{period}",
        strategy=strategy,
        is_cached=False,
        served_from="replay",
        replay_reason=f"Dynamic replay calculation on committed fixture dataset for {strategy} ({period})",
        engine_version=sim_res.get("engine_version", "1.0.0"),
        data_hash=sim_res.get("data_hash", ""),
        cost_profile=sim_res.get("cost_profile", "1.0-indian-delivery-2024"),
        execution_time_ms=sim_res["execution_time_ms"],
        dates=sim_res["dates"],
        gross_equity=sim_res["gross_equity"],
        net_equity=sim_res["net_equity"],
        metrics=sim_res["metrics"],
        costs=sim_res["costs"],
        trades=sim_res["trades"],
        diagnostics=sim_res["diagnostics"],
    )


@app.post("/run", response_model=BacktestResponse)
def run_backtest(req: BacktestRequest):
    run_id = compute_run_id(
        strategy=req.strategy,
        params=req.params,
        start=req.start_date,
        end=req.end_date,
        universe=req.universe,
        apply_costs=req.apply_costs,
        initial_cash=req.initial_capital,
        cost_profile=req.cost_profile,
    )

    # 1. Tier 1: Check SQLite Cache
    cached = get_cached_run(run_id)
    if cached:
        cached["is_cached"] = True
        cached["served_from"] = "cache"
        cached["replay_reason"] = "Retrieved byte-identical run from SQLite cache"
        return BacktestResponse(**cached)

    # 2. Tier 2: Check Offline Replay Mode
    if req.demo_mode or is_demo_mode_active():
        replay = get_replay_run(req.strategy)
        if replay:
            replay["served_from"] = "replay"
            replay["replay_reason"] = f"Demo mode enabled: served verified precomputed run for {req.strategy}"
            return BacktestResponse(**replay)

    # 3. Tier 3: In-Process Dual-Pass Execution (Strict: no silent fallbacks on failure)
    sim_res = execute_backtest(
        strategy_name=req.strategy,
        params=req.params,
        universe_symbols=req.universe,
        start_date=req.start_date,
        end_date=req.end_date,
        initial_capital=req.initial_capital,
        apply_costs=req.apply_costs,
        cost_profile=req.cost_profile,
        slippage_floor_bps=req.slippage_floor_bps,
    )

    response_data = {
        "run_id": run_id,
        "strategy": req.strategy,
        "is_cached": False,
        "served_from": "live",
        "replay_reason": None,
        "engine_version": sim_res.get("engine_version", "1.0.0"),
        "data_hash": sim_res.get("data_hash", ""),
        "cost_profile": sim_res.get("cost_profile", "1.0-indian-delivery-2024"),
        "execution_time_ms": sim_res["execution_time_ms"],
        "dates": sim_res["dates"],
        "gross_equity": sim_res["gross_equity"],
        "net_equity": sim_res["net_equity"],
        "metrics": sim_res["metrics"],
        "costs": sim_res["costs"],
        "trades": sim_res["trades"],
        "diagnostics": sim_res["diagnostics"],
    }

    # Save to SQLite
    try:
        save_run(run_id, req.model_dump(), response_data)
    except Exception:
        pass

    return BacktestResponse(**response_data)
