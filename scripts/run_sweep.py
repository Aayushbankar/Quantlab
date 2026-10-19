#!/usr/bin/env python3
"""
Parameter Sweep & Empirical PBO Experiment (FR-12 & D7).

Executes a grid of 120+ strategy configurations across the historical equity universe.
Computes daily return vectors, cross-trial variance, and Combinatorial Purged Cross-Validation (CPCV)
Probability of Backtest Overfitting (PBO) with 95% bootstrap confidence intervals.

Saves results to:
    - experiments/sweep_results.csv
    - experiments/sweep_returns.csv
    - experiments/sweep_summary.json
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.analytics.cpcv import CPCV  # noqa: E402
from src.api.db import record_trial  # noqa: E402
from src.data.clean import load_and_clean_all  # noqa: E402
from src.engine.backtest_engine import BacktestEngine  # noqa: E402
from src.strategies.bollinger_breakout import BollingerBreakoutStrategy  # noqa: E402
from src.strategies.momentum import MomentumStrategy  # noqa: E402
from src.strategies.rsi_mean_reversion import RSIMeanReversionStrategy  # noqa: E402
from src.strategies.sma_crossover import SMACrossoverStrategy  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("run_sweep")


def generate_configurations() -> list[dict[str, Any]]:
    """Generates 133 distinct strategy configurations."""
    configs: list[dict[str, Any]] = []

    # 1. SMA Crossover: fast < slow (48 configs)
    fast_windows = [5, 10, 15, 20, 25, 30]
    slow_windows = [35, 45, 55, 70, 85, 100, 150, 200]
    for f in fast_windows:
        for s in slow_windows:
            configs.append(
                {
                    "config_id": f"sma_{f}_{s}",
                    "strategy": "sma_crossover",
                    "params": {"fast_window": f, "slow_window": s},
                }
            )

    # 2. RSI Mean Reversion: 3 x 4 x 4 = 48 configs
    rsi_windows = [10, 14, 21]
    oversold_levels = [20, 25, 30, 35]
    overbought_levels = [65, 70, 75, 80]
    for w in rsi_windows:
        for os_lvl in oversold_levels:
            for ob_lvl in overbought_levels:
                configs.append(
                    {
                        "config_id": f"rsi_{w}_{os_lvl}_{ob_lvl}",
                        "strategy": "rsi_mean_reversion",
                        "params": {"period": w, "oversold": os_lvl, "overbought": ob_lvl},
                    }
                )

    # 3. Momentum: 5 x 5 = 25 configs
    lookbacks = [10, 20, 30, 45, 60]
    thresholds = [0.01, 0.02, 0.03, 0.05, 0.08]
    for lb in lookbacks:
        for th in thresholds:
            configs.append(
                {
                    "config_id": f"mom_{lb}_{int(th*100)}bps",
                    "strategy": "momentum",
                    "params": {"lookback_period": lb, "threshold_pct": th},
                }
            )

    # 4. Bollinger Breakout: 4 x 3 = 12 configs
    bb_windows = [15, 20, 25, 30]
    bb_stds = [1.5, 2.0, 2.5]
    for w in bb_windows:
        for std in bb_stds:
            configs.append(
                {
                    "config_id": f"bb_{w}_{str(std).replace('.', 'p')}",
                    "strategy": "bollinger_breakout",
                    "params": {"period": w, "num_std": std},
                }
            )

    return configs


def instantiate_strategy(strategy_name: str, params: dict[str, Any]):
    if strategy_name == "sma_crossover":
        return SMACrossoverStrategy(fast_window=params["fast_window"], slow_window=params["slow_window"])
    elif strategy_name == "rsi_mean_reversion":
        return RSIMeanReversionStrategy(
            period=params["period"], oversold=params["oversold"], overbought=params["overbought"]
        )
    elif strategy_name == "momentum":
        return MomentumStrategy(lookback_period=params["lookback_period"], threshold_pct=params["threshold_pct"])
    elif strategy_name == "bollinger_breakout":
        return BollingerBreakoutStrategy(period=params["period"], num_std=params["num_std"])
    else:
        raise ValueError(f"Unknown strategy: {strategy_name}")


def _eval_single_config(args: tuple[dict[str, Any], dict[str, pd.DataFrame]]) -> dict[str, Any] | None:
    """Worker task evaluating a single strategy configuration."""
    cfg, data = args
    cid = cfg["config_id"]
    try:
        strat_obj = instantiate_strategy(cfg["strategy"], cfg["params"])
        engine = BacktestEngine(data=data, strategy=strat_obj, initial_cash=100000.0, apply_costs=True)
        equity_df = engine.run()

        if equity_df.empty or len(equity_df) < 5:
            return None

        equity = equity_df["total_equity"].astype(float)
        daily_ret = equity.pct_change().dropna()
        dates = equity_df["date"].iloc[1:].reset_index(drop=True)

        total_return = float((equity.iloc[-1] / equity.iloc[0]) - 1.0)
        mean_ret = float(daily_ret.mean())
        std_ret = float(daily_ret.std())
        sharpe = (mean_ret / max(std_ret, 1e-8)) * np.sqrt(252.0)

        peak = equity.cummax()
        dd = (equity - peak) / peak
        max_dd = float(dd.min())

        return {
            "config_id": cid,
            "strategy": cfg["strategy"],
            "params": cfg["params"],
            "params_json": json.dumps(cfg["params"]),
            "total_return": round(total_return, 4),
            "sharpe": round(sharpe, 4),
            "max_drawdown": round(max_dd, 4),
            "start_date": str(equity_df["date"].iloc[0])[:10],
            "end_date": str(equity_df["date"].iloc[-1])[:10],
            "dates": list(dates),
            "returns": list(daily_ret.values),
        }
    except Exception as e:
        logger.warning(f"Error evaluating config {cid}: {e}")
        return None


def run_sweep(
    max_configs: int | None = None,
    record_to_db: bool = True,
    output_dir: Path | None = None,
    workers: int | None = None,
) -> dict[str, Any]:
    if output_dir is None:
        output_dir = REPO_ROOT / "experiments"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load data: prefer data/raw, fall back to tests/fixtures/data
    data_dir = REPO_ROOT / "data" / "raw"
    data = load_and_clean_all(str(data_dir))
    if not data:
        data_dir = REPO_ROOT / "tests" / "fixtures" / "data"
        logger.info(f"Using test fixtures data from {data_dir}")
        data = load_and_clean_all(str(data_dir))

    if not data:
        raise RuntimeError("No market data found for sweep. Run scripts/fetch_data.py or tests/fixtures/generate.py.")

    configs = generate_configurations()
    if max_configs is not None:
        configs = configs[:max_configs]

    num_workers = workers or min(os.cpu_count() or 4, 8)
    logger.info(
        f"Executing parameter sweep over {len(configs)} configurations across {len(data)} equities ({num_workers} parallel workers)..."
    )

    tasks = [(cfg, data) for cfg in configs]
    results_rows: list[dict[str, Any]] = []
    returns_series_dict: dict[str, pd.Series] = {}

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        for idx, res in enumerate(executor.map(_eval_single_config, tasks)):
            if res is None:
                continue

            results_rows.append(
                {
                    "config_id": res["config_id"],
                    "strategy": res["strategy"],
                    "params": res["params_json"],
                    "total_return": res["total_return"],
                    "sharpe": res["sharpe"],
                    "max_drawdown": res["max_drawdown"],
                }
            )

            ret_series = pd.Series(res["returns"], index=res["dates"])
            returns_series_dict[res["config_id"]] = ret_series

            if record_to_db:
                record_trial(
                    strategy=res["strategy"],
                    params=res["params"],
                    universe=list(data.keys()),
                    start_date=res["start_date"],
                    end_date=res["end_date"],
                    sharpe=res["sharpe"],
                    total_return=res["total_return"],
                    max_drawdown=res["max_drawdown"],
                )

            if (idx + 1) % 20 == 0 or (idx + 1) == len(configs):
                logger.info(f"Evaluated {idx + 1}/{len(configs)} configurations.")

    results_df = pd.DataFrame(results_rows)
    returns_df = pd.DataFrame(returns_series_dict).dropna()

    logger.info(f"Returns matrix shape for CPCV: {returns_df.shape}")

    # Compute CPCV and PBO with bootstrap CI
    cpcv = CPCV(n_splits=10, n_test_splits=2, embargo_pct=0.01)
    pbo_stats = cpcv.calculate_pbo_with_ci(returns_df, n_bootstraps=500, ci_level=0.95)

    all_sharpes = results_df["sharpe"].values
    cross_trial_var = float(np.var(all_sharpes, ddof=1)) if len(all_sharpes) > 1 else 0.0

    summary = {
        "n_configs_evaluated": len(results_df),
        "universe_symbols": sorted(list(data.keys())),
        "cross_trial_variance": round(cross_trial_var, 6),
        "mean_sharpe": round(float(np.mean(all_sharpes)), 4),
        "std_sharpe": round(float(np.std(all_sharpes, ddof=1)), 4),
        "max_sharpe": round(float(np.max(all_sharpes)), 4),
        "min_sharpe": round(float(np.min(all_sharpes)), 4),
        "pbo": pbo_stats.get("pbo"),
        "pbo_ci_lower_95": pbo_stats.get("ci_lower"),
        "pbo_ci_upper_95": pbo_stats.get("ci_upper"),
        "cpcv_paths": pbo_stats.get("n_paths"),
        "cpcv_overfit_paths": pbo_stats.get("overfit_paths"),
        "best_config": results_df.sort_values(by="sharpe", ascending=False).iloc[0].to_dict(),
    }

    # Save outputs
    results_path = output_dir / "sweep_results.csv"
    returns_path = output_dir / "sweep_returns.csv"
    summary_path = output_dir / "sweep_summary.json"

    results_df.to_csv(results_path, index=False)
    returns_df.to_csv(returns_path)
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    logger.info(
        f"Sweep completed. PBO: {summary['pbo']} (95% CI: [{summary['pbo_ci_lower_95']}, {summary['pbo_ci_upper_95']}])"
    )
    logger.info(f"Summary written to {summary_path}")

    return summary


def main():
    parser = argparse.ArgumentParser(description="Pramaan Multi-Strategy Parameter Sweep")
    parser.add_argument("--max-configs", type=int, default=None, help="Cap number of configs for quick runs")
    parser.add_argument("--no-db", action="store_true", help="Do not record to SQLite trials ledger")
    parser.add_argument("--workers", type=int, default=None, help="Number of parallel worker processes")
    args = parser.parse_args()

    run_sweep(max_configs=args.max_configs, record_to_db=not args.no_db, workers=args.workers)


if __name__ == "__main__":
    main()
