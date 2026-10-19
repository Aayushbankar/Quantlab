import os
import time
from typing import Any

import pandas as pd

from src.analytics.deflated_sharpe import deflated_sharpe_ratio, expected_max_sharpe
from src.analytics.metrics import MetricsEngine
from src.data.clean import load_and_clean_all
from src.engine.backtest_engine import BacktestEngine
from src.engine.events import FillEvent
from src.strategies.bh_and_hold import BuyAndHoldStrategy
from src.strategies.bollinger_breakout import BollingerBreakoutStrategy
from src.strategies.momentum import MomentumStrategy
from src.strategies.rsi_mean_reversion import RSIMeanReversionStrategy
from src.strategies.sma_crossover import SMACrossoverStrategy

RAW_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "raw")


def make_strategy(name: str, params: dict):
    if name == "sma_crossover":
        return SMACrossoverStrategy(
            fast_window=int(params.get("fast_window", 20)), slow_window=int(params.get("slow_window", 50))
        )
    elif name == "sma_crossover_10_30":
        return SMACrossoverStrategy(
            fast_window=int(params.get("fast_window", 10)), slow_window=int(params.get("slow_window", 30))
        )
    elif name == "rsi_mean_reversion":
        return RSIMeanReversionStrategy(
            period=int(params.get("period", 14)),
            oversold=float(params.get("oversold", 30.0)),
            overbought=float(params.get("overbought", 70.0)),
        )
    elif name == "momentum":
        return MomentumStrategy(
            lookback_period=int(params.get("lookback_period", 20)),
            threshold_pct=float(params.get("threshold_pct", 0.05)),
        )
    elif name == "bollinger_breakout":
        return BollingerBreakoutStrategy(
            period=int(params.get("period", 20)), num_std=float(params.get("num_std", 2.0))
        )
    elif name in ("bh_and_hold", "buy_and_hold"):
        return BuyAndHoldStrategy()
    else:
        raise ValueError(
            f"Unknown strategy '{name}'. Valid strategies are: sma_crossover, "
            "sma_crossover_10_30, rsi_mean_reversion, momentum, bollinger_breakout, bh_and_hold."
        )


def execute_backtest(
    strategy_name: str,
    params: dict,
    universe_symbols: list[str],
    start_date: str,
    end_date: str,
    initial_capital: float = 100000.0,
    apply_costs: bool = True,
) -> dict[str, Any]:
    t0 = time.time()

    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)
    if start_dt >= end_dt:
        raise ValueError(f"start_date ({start_date}) must be strictly before end_date ({end_date}).")

    if not universe_symbols:
        raise ValueError("universe_symbols cannot be empty.")

    # Validate symbols
    import hashlib
    import re

    symbol_regex = re.compile(r"^[A-Za-z0-9_\-\.]{1,30}$")
    for sym in universe_symbols:
        if not symbol_regex.match(sym):
            raise ValueError(
                f"Invalid symbol '{sym}'. Symbols must be 1-20 alphanumeric characters (e.g. RELIANCE, TCS.NS)."
            )

    all_data = load_and_clean_all(RAW_DATA_DIR)
    if not all_data:
        fixture_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "tests", "fixtures", "data"
        )
        if os.path.exists(fixture_dir):
            all_data = load_and_clean_all(fixture_dir)

    # Attempt on-demand fetching for any new tickers if not offline
    clean_symbols = [s.replace(".NS", "") for s in universe_symbols]
    missing_symbols = [s for s in clean_symbols if s not in all_data and f"{s}.NS" not in all_data]
    if missing_symbols and os.environ.get("PRAMAAN_OFFLINE") != "1":
        for sym in missing_symbols:
            csv_path = os.path.join(RAW_DATA_DIR, f"{sym}.csv")
            try:
                from src.data.fetch import fetch_stock_data

                fetch_sym = sym if ".NS" in sym else f"{sym}.NS"
                df_live = fetch_stock_data(fetch_sym, start_date="2019-01-01", end_date="2024-12-31")
                if df_live is not None and not df_live.empty:
                    df_live.to_csv(csv_path, index=False)
                    all_data[sym] = df_live
            except Exception:
                pass

    # Filter universe
    filtered_data = {}
    for sym, df in all_data.items():
        if sym in clean_symbols or f"{sym}.NS" in universe_symbols:
            mask = (df["date"] >= start_dt) & (df["date"] <= end_dt)
            sub_df = df[mask].reset_index(drop=True)
            if not sub_df.empty:
                filtered_data[sym] = sub_df

    if not filtered_data:
        raise ValueError(
            f"No data available: requested symbols not found in dataset for dates {start_date} to {end_date}. "
            f"Requested: {universe_symbols}."
        )

    # Compute provenance data hash
    hasher = hashlib.sha256()
    for sym in sorted(filtered_data.keys()):
        df_sym = filtered_data[sym]
        hasher.update(sym.encode())
        hasher.update(str(len(df_sym)).encode())
        if not df_sym.empty:
            hasher.update(str(df_sym["close"].iloc[0]).encode())
            hasher.update(str(df_sym["close"].iloc[-1]).encode())
    data_hash = hasher.hexdigest()[:16]

    # 1. Primary Run (Net simulation with costs)
    strat_net = make_strategy(strategy_name, params)
    engine_net = BacktestEngine(
        data=filtered_data, strategy=strat_net, initial_cash=initial_capital, apply_costs=apply_costs
    )

    captured_trades: list[dict[str, Any]] = []
    total_costs_accum = {
        "brokerage": 0.0,
        "stt": 0.0,
        "stamp_duty": 0.0,
        "turnover_fees": 0.0,
        "gst": 0.0,
        "market_impact": 0.0,
    }

    orig_apply_fill = engine_net.portfolio.apply_fill

    def hooked_apply_fill(fill: FillEvent):
        captured_trades.append(
            {
                "timestamp": str(fill.timestamp)[:10],
                "symbol": fill.symbol,
                "side": fill.side,
                "quantity": int(fill.quantity),
                "raw_price": round(float(fill.raw_price), 2),
                "fill_price": round(float(fill.fill_price), 2),
                "total_cost": round(float(fill.total_cost), 2),
                "status": "FILLED",
            }
        )
        total_costs_accum["brokerage"] += float(fill.commission)
        total_costs_accum["stt"] += float(fill.stt)
        total_costs_accum["stamp_duty"] += float(fill.stamp_duty)
        total_costs_accum["turnover_fees"] += float(fill.turnover_fee)
        total_costs_accum["gst"] += float(fill.gst)
        total_costs_accum["market_impact"] += float(fill.quantity * abs(fill.fill_price - fill.raw_price))
        return orig_apply_fill(fill)

    engine_net.portfolio.apply_fill = hooked_apply_fill
    net_equity_df = engine_net.run()

    # Append any rejected trades
    captured_trades.extend(engine_net.portfolio.rejected_trades)

    # 2. Counterfactual Gross Run (Unpenalized compounding simulation)
    strat_gross = make_strategy(strategy_name, params)
    engine_gross = BacktestEngine(
        data=filtered_data, strategy=strat_gross, initial_cash=initial_capital, apply_costs=False
    )
    gross_equity_df = engine_gross.run()

    dates = net_equity_df["date"].astype(str).tolist()
    net_equity = net_equity_df["total_equity"].astype(float).tolist()
    gross_equity = gross_equity_df["total_equity"].astype(float).tolist()

    # Benchmark analytics (against first available index or equity)
    bm_series = None
    first_sym = next(iter(filtered_data.keys()))
    if first_sym in filtered_data:
        bm_series = filtered_data[first_sym].set_index("date")["close"].pct_change().dropna()

    metrics_calc = MetricsEngine(net_equity_df, benchmark_returns=bm_series)
    metrics_dict = metrics_calc.compute_all()

    # DSR calculation
    daily_returns = net_equity_df["total_equity"].pct_change().dropna().values
    dsr_p_val = None
    expected_max_sr = None
    if len(daily_returns) > 30:
        try:
            obs_sr = float(metrics_dict.get("Sharpe Ratio", 0.0))
            returns_series = pd.Series(daily_returns)
            dsr_p_val = float(deflated_sharpe_ratio(observed_sr=obs_sr, returns=returns_series, N_trials=30))
            expected_max_sr = float(expected_max_sharpe(N_trials=30, variance_sr=0.01, benchmark_sr=0.0))
        except Exception:
            pass

    cost_drag = max(0.0, gross_equity[-1] - net_equity[-1])
    friction_pct = (cost_drag / initial_capital) * 100.0

    return {
        "dates": dates,
        "gross_equity": gross_equity,
        "net_equity": net_equity,
        "metrics": {
            "total_return": round(float(metrics_dict.get("Total Return", 0.0)), 4),
            "cagr": round(float(metrics_dict.get("CAGR", 0.0)), 4),
            "sharpe_ratio": round(float(metrics_dict.get("Sharpe Ratio", 0.0)), 4),
            "sortino_ratio": round(float(metrics_dict.get("Sortino Ratio", 0.0)), 4),
            "max_drawdown": round(float(metrics_dict.get("Max Drawdown", 0.0)), 4),
            "calmar_ratio": round(float(metrics_dict.get("Calmar Ratio", 0.0)), 4),
            "average_exposure": round(float(metrics_dict.get("Average Exposure", 1.0)), 4),
            "alpha": round(float(metrics_dict.get("Alpha", 0.0)), 4),
            "beta": round(float(metrics_dict.get("Beta", 1.0)), 4),
            "exposure_matched_return": round(float(metrics_dict.get("Exposure Matched Return", 0.0)), 4),
        },
        "costs": {
            "brokerage": round(total_costs_accum["brokerage"], 2),
            "stt": round(total_costs_accum["stt"], 2),
            "stamp_duty": round(total_costs_accum["stamp_duty"], 2),
            "turnover_fees": round(total_costs_accum["turnover_fees"], 2),
            "gst": round(total_costs_accum["gst"], 2),
            "market_impact": round(total_costs_accum["market_impact"], 2),
            "total_friction": round(cost_drag, 2),
            "friction_drag_pct": round(friction_pct, 2),
        },
        "trades": captured_trades,
        "diagnostics": {
            "dsr_p_value": round(dsr_p_val, 4) if dsr_p_val is not None else None,
            "expected_max_sharpe": round(expected_max_sr, 4) if expected_max_sr is not None else None,
            "pbo": None,
            "pbo_reason": "PBO requires a combinatorial parameter sweep; run /sweep to compute empirical PBO",
            "n_trials": 1,
        },
        "data_hash": data_hash,
        "engine_version": "1.0.0",
        "cost_profile": "1.0-indian-delivery-2024",
        "execution_time_ms": round((time.time() - t0) * 1000.0, 2),
    }
