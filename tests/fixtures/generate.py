"""
Deterministic synthetic data generator for offline testing.

Uses numpy.random.Generator with seed=42 to produce reproducible OHLCV data
for three fictional Indian-equity-like symbols (TESTCO, SYNTH, FIXTR).
Data range: 2020-01-01 to 2023-12-31 (~1000 business days each).

The output matches the CSV format expected by ``src.data.clean.load_and_clean_all``:
columns = [date, open, high, low, close, volume, symbol].
"""

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SEED = 42
SYMBOLS = [
    "TESTCO",
    "SYNTH",
    "FIXTR",
    "RELIANCE",
    "TCS",
    "INFY",
    "HDFCBANK",
    "ICICIBANK",
    "SBIN",
    "ITC",
    "HINDUNILVR",
    "LT",
    "BHARTIARTL",
]
START_DATE = "2019-01-01"
END_DATE = "2024-12-31"
FIXTURE_DATA_DIR = Path(__file__).resolve().parent / "data"

# Per-symbol parameters (start price, daily drift, daily vol, vol range)
_SYMBOL_PARAMS: dict[str, dict[str, Any]] = {
    "TESTCO": {"start": 1200.0, "drift": 0.0004, "vol": 0.018, "vol_lo": 200_000, "vol_hi": 3_000_000},
    "SYNTH": {"start": 750.0, "drift": 0.0002, "vol": 0.022, "vol_lo": 150_000, "vol_hi": 2_500_000},
    "FIXTR": {"start": 2500.0, "drift": 0.0003, "vol": 0.015, "vol_lo": 100_000, "vol_hi": 5_000_000},
    "RELIANCE": {"start": 1300.0, "drift": 0.0005, "vol": 0.018, "vol_lo": 1_000_000, "vol_hi": 10_000_000},
    "TCS": {"start": 2000.0, "drift": 0.0004, "vol": 0.016, "vol_lo": 500_000, "vol_hi": 4_000_000},
    "INFY": {"start": 700.0, "drift": 0.0005, "vol": 0.020, "vol_lo": 1_000_000, "vol_hi": 8_000_000},
    "HDFCBANK": {"start": 1050.0, "drift": 0.0003, "vol": 0.015, "vol_lo": 1_500_000, "vol_hi": 12_000_000},
    "ICICIBANK": {"start": 360.0, "drift": 0.0006, "vol": 0.022, "vol_lo": 2_000_000, "vol_hi": 15_000_000},
    "SBIN": {"start": 300.0, "drift": 0.0004, "vol": 0.025, "vol_lo": 3_000_000, "vol_hi": 20_000_000},
    "ITC": {"start": 280.0, "drift": 0.0003, "vol": 0.016, "vol_lo": 2_000_000, "vol_hi": 15_000_000},
    "HINDUNILVR": {"start": 1800.0, "drift": 0.0003, "vol": 0.014, "vol_lo": 500_000, "vol_hi": 3_000_000},
    "LT": {"start": 1400.0, "drift": 0.0005, "vol": 0.019, "vol_lo": 400_000, "vol_hi": 3_500_000},
    "BHARTIARTL": {"start": 320.0, "drift": 0.0006, "vol": 0.021, "vol_lo": 1_000_000, "vol_hi": 8_000_000},
}


def _generate_symbol_df(
    rng: np.random.Generator,
    symbol: str,
    dates: pd.DatetimeIndex,
    params: dict[str, Any],
) -> pd.DataFrame:
    """Generate a single symbol's OHLCV DataFrame with realistic Indian-equity properties."""
    n = len(dates)
    # Geometric Brownian Motion for close prices
    log_returns = rng.normal(params["drift"], params["vol"], n)
    log_returns[0] = 0.0  # first day starts at the seed price
    close = params["start"] * np.cumprod(np.exp(log_returns))

    # Clamp prices to 500-3000 range (Indian equity band)
    close = np.clip(close, 500.0, 3000.0)

    # Open: slight gap from previous close
    open_ = np.empty(n)
    open_[0] = close[0] * (1 + rng.normal(0, 0.003))
    open_[1:] = close[:-1] * (1 + rng.normal(0, 0.003, n - 1))

    # High >= max(open, close);  Low <= min(open, close)
    intraday_range = np.abs(rng.normal(0, params["vol"] * 0.6, n))
    high = np.maximum(open_, close) * (1 + intraday_range)
    low = np.minimum(open_, close) * (1 - intraday_range)

    # Volume: log-normal within specified range
    raw_vol = rng.lognormal(mean=np.log(1_000_000), sigma=0.6, size=n)
    volume = np.clip(raw_vol, params["vol_lo"], params["vol_hi"]).astype(int)

    df = pd.DataFrame(
        {
            "date": dates,
            "open": np.round(open_, 4),
            "high": np.round(high, 4),
            "low": np.round(low, 4),
            "close": np.round(close, 4),
            "volume": volume,
            "symbol": f"{symbol}.NS",
        }
    )
    return df


def generate_fixture_data() -> dict[str, pd.DataFrame]:
    """
    Generate deterministic synthetic OHLCV data for all fixture symbols.

    Returns
    -------
    Dict[str, pd.DataFrame]
        Mapping of symbol name (without .NS suffix) to a cleaned DataFrame
        ready for the backtest engine.  Columns: date, open, high, low, close, volume.
    """
    rng = np.random.default_rng(SEED)
    dates = pd.bdate_range(start=START_DATE, end=END_DATE)

    data: dict[str, pd.DataFrame] = {}
    for symbol in SYMBOLS:
        params = _SYMBOL_PARAMS[symbol]
        df = _generate_symbol_df(rng, symbol, dates, params)
        # Drop the 'symbol' column for engine consumption (engine keys by dict key)
        engine_df = df.drop(columns=["symbol"]).copy()
        data[symbol] = engine_df

    return data


def save_fixture_csvs(output_dir: str | Path | None = None) -> Path:
    """
    Generate and persist CSVs in the fixture data directory.

    The CSVs include the ``symbol`` column so they match the format
    produced by ``src.data.fetch.download_universe`` and consumed by
    ``src.data.clean.load_and_clean_all``.
    """
    out = Path(output_dir) if output_dir else FIXTURE_DATA_DIR
    out.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(SEED)
    dates = pd.bdate_range(start=START_DATE, end=END_DATE)

    for symbol in SYMBOLS:
        params = _SYMBOL_PARAMS[symbol]
        df = _generate_symbol_df(rng, symbol, dates, params)
        csv_path = out / f"{symbol}.csv"
        df.to_csv(csv_path, index=False)

    return out


def generate_replay_fixture() -> dict[str, Any]:
    """
    Produce a minimal replay JSON blob that the ``/replay/<strategy>``
    endpoint can serve without touching experiments/ or the network.

    Runs an actual SMA crossover backtest on fixture data so all numbers
    are internally consistent.
    """
    from src.analytics.metrics import MetricsEngine
    from src.engine.backtest_engine import BacktestEngine
    from src.strategies.sma_crossover import SMACrossoverStrategy

    data = generate_fixture_data()
    strategy = SMACrossoverStrategy(20, 50)

    # Net run
    engine_net = BacktestEngine(data=data, strategy=strategy, initial_cash=100000.0, apply_costs=True)
    net_eq = engine_net.run()

    # Gross run
    strategy_gross = SMACrossoverStrategy(20, 50)
    engine_gross = BacktestEngine(data=data, strategy=strategy_gross, initial_cash=100000.0, apply_costs=False)
    gross_eq = engine_gross.run()

    metrics_calc = MetricsEngine(net_eq)
    metrics = metrics_calc.compute_all()

    dates = net_eq["date"].astype(str).tolist()
    net_equity = net_eq["total_equity"].astype(float).tolist()
    gross_equity = gross_eq["total_equity"].astype(float).tolist()

    cost_drag = max(0.0, gross_equity[-1] - net_equity[-1])

    return {
        "run_id": "fixture_replay_sma_crossover",
        "strategy": "sma_crossover",
        "is_cached": True,
        "execution_time_ms": 0.0,
        "dates": dates,
        "gross_equity": gross_equity,
        "net_equity": net_equity,
        "metrics": {
            "total_return": round(float(metrics.get("Total Return", 0.0)), 4),
            "cagr": round(float(metrics.get("CAGR", 0.0)), 4),
            "sharpe_ratio": round(float(metrics.get("Sharpe Ratio", 0.0)), 4),
            "sortino_ratio": round(float(metrics.get("Sortino Ratio", 0.0)), 4),
            "max_drawdown": round(float(metrics.get("Max Drawdown", 0.0)), 4),
            "calmar_ratio": round(float(metrics.get("Calmar Ratio", 0.0)), 4),
        },
        "costs": {
            "brokerage": round(cost_drag * 0.15, 2),
            "stt": round(cost_drag * 0.45, 2),
            "stamp_duty": round(cost_drag * 0.05, 2),
            "turnover_fees": round(cost_drag * 0.03, 2),
            "gst": round(cost_drag * 0.07, 2),
            "market_impact": round(cost_drag * 0.25, 2),
            "total_friction": round(cost_drag, 2),
            "friction_drag_pct": round((cost_drag / 100000.0) * 100.0, 2),
        },
        "trades": [],
        "diagnostics": {
            "dsr_p_value": 0.52,
            "expected_max_sharpe": 0.746,
            "pbo": 0.6429,
            "n_trials": 30,
        },
    }


def save_replay_fixture(output_dir: str | Path | None = None) -> Path:
    """Generate the replay JSON and save it alongside the CSVs."""
    out = Path(output_dir) if output_dir else FIXTURE_DATA_DIR
    out.mkdir(parents=True, exist_ok=True)
    replay = generate_replay_fixture()
    path = out / "replay_sma_crossover.json"
    with open(path, "w") as f:
        json.dump(replay, f, indent=2)
    return path


# ---------------------------------------------------------------------------
# CLI entry-point — ``python -m tests.fixtures.generate``
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"Generating fixture CSVs in {FIXTURE_DATA_DIR} ...")
    save_fixture_csvs()
    print("Generating replay fixture ...")
    save_replay_fixture()
    print("Done.")
