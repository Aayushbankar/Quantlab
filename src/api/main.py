import os
import sys
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from src.api.schemas import (
    BacktestRequest,
    BacktestResponse,
    HealthResponse,
    StrategyMetadata,
    UniverseResponse
)
from src.api.cache import compute_run_id
from src.api.db import get_cached_run, save_run, list_recent_runs
from src.api.replay import get_replay_run
from src.api.adapter import execute_backtest
from src.data.universe import get_universe, get_benchmark

app = FastAPI(
    title="Pramaan API",
    description="REST interface for the Pramaan backtesting engine & overfitting diagnostic platform (GTU DI05000341).",
    version="1.0.0"
)

# CORS configuration for Next.js frontend, LAN, remote forwards, and Tauri desktop shell
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        demo_mode=bool(os.environ.get("DEMO_DATA", False))
    )


@app.get("/strategies", response_model=List[StrategyMetadata])
def get_strategies():
    return [
        StrategyMetadata(
            id="sma_crossover",
            name="SMA Crossover",
            description="Classic moving average trend-following strategy with fast and slow windows.",
            default_params={"fast_window": 20, "slow_window": 50},
            param_ranges={"fast_window": [5, 50], "slow_window": [20, 200]}
        ),
        StrategyMetadata(
            id="sma_crossover_10_30",
            name="SMA Crossover (10, 30)",
            description="Aggressive short-horizon moving average crossover.",
            default_params={"fast_window": 10, "slow_window": 30},
            param_ranges={"fast_window": [5, 30], "slow_window": [15, 60]}
        ),
        StrategyMetadata(
            id="rsi_mean_reversion",
            name="RSI Mean Reversion",
            description="Wilder RSI mean-reversion with oversold buy and overbought sell thresholds.",
            default_params={"period": 14, "oversold": 30.0, "overbought": 70.0},
            param_ranges={"period": [5, 30], "oversold": [10.0, 45.0], "overbought": [55.0, 90.0]}
        ),
        StrategyMetadata(
            id="momentum",
            name="Momentum ROC",
            description="Rate of Change momentum strategy with duplicate-BUY invariant guard.",
            default_params={"lookback_period": 20, "threshold_pct": 0.05},
            param_ranges={"lookback_period": [5, 60], "threshold_pct": [0.01, 0.15]}
        ),
        StrategyMetadata(
            id="bollinger_breakout",
            name="Bollinger Band Breakout",
            description="Volatility channel expansion strategy (20-day SMA, 2 StdDev). Enters on upper-band breakthrough, exits on mean reversion.",
            default_params={"period": 20, "num_std": 2.0},
            param_ranges={"period": [10, 50], "num_std": [1.0, 3.0]}
        ),
        StrategyMetadata(
            id="bh_and_hold",
            name="Buy and Hold Benchmark",
            description="Passive investment control baseline. All active strategies are judged against this null hypothesis.",
            default_params={},
            param_ranges={}
        ),
    ]


@app.get("/universe", response_model=UniverseResponse)
def get_universe_info():
    symbols = get_universe()
    benchmark = get_benchmark()
    return UniverseResponse(
        symbols=symbols,
        benchmark=benchmark,
        default_start="2019-01-01",
        default_end="2024-12-30",
        total_bars=1480
    )


@app.get("/history")
def get_history(limit: int = 20):
    return list_recent_runs(limit=limit)


@app.get("/replay/{strategy}", response_model=BacktestResponse)
def replay_strategy(strategy: str, period: str = "full"):
    res = get_replay_run(strategy=strategy, period=period)
    if res:
        return BacktestResponse(**res)

    # Dynamic fallback: if strategy is new (e.g. bollinger_breakout), run on committed dataset
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
        apply_costs=True
    )
    return BacktestResponse(
        run_id=f"replay_{strategy}_{period}",
        strategy=strategy,
        is_cached=False,
        execution_time_ms=sim_res["execution_time_ms"],
        dates=sim_res["dates"],
        gross_equity=sim_res["gross_equity"],
        net_equity=sim_res["net_equity"],
        metrics=sim_res["metrics"],
        costs=sim_res["costs"],
        trades=sim_res["trades"],
        diagnostics=sim_res["diagnostics"]
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
        initial_cash=req.initial_capital
    )

    # 1. Tier 1: Check SQLite Cache
    cached = get_cached_run(run_id)
    if cached:
        return BacktestResponse(**cached)

    # 2. Tier 2: Check Offline Replay Mode
    if req.demo_mode or os.environ.get("DEMO_DATA") == "1":
        replay = get_replay_run(req.strategy)
        if replay:
            return BacktestResponse(**replay)

    # 3. Tier 3: In-Process Dual-Pass Execution
    try:
        sim_res = execute_backtest(
            strategy_name=req.strategy,
            params=req.params,
            universe_symbols=req.universe,
            start_date=req.start_date,
            end_date=req.end_date,
            initial_capital=req.initial_capital,
            apply_costs=req.apply_costs
        )
    except Exception as e:
        # Fallback to replay if simulation fails
        replay = get_replay_run(req.strategy)
        if replay:
            return BacktestResponse(**replay)
        raise HTTPException(status_code=500, detail=f"Simulation error: {str(e)}")

    response_data = {
        "run_id": run_id,
        "strategy": req.strategy,
        "is_cached": False,
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
        save_run(run_id, req.dict(), response_data)
    except Exception:
        pass

    return BacktestResponse(**response_data)
