import pytest
import pandas as pd
import numpy as np
from src.engine.backtest_engine import BacktestEngine
from src.strategies.sma_crossover import SMACrossoverStrategy


def _data():
    rng = np.random.default_rng(5)
    dates = pd.date_range("2019-01-01", periods=300, freq="B")
    closes = 100 * np.cumprod(1 + rng.normal(0.0005, 0.015, 300))
    df = pd.DataFrame({
        "date": dates,
        "open": closes,
        "high": closes * 1.005,
        "low": closes * 0.995,
        "close": closes,
        "volume": [500_000] * 300,
    })
    return {"RELIANCE.NS": df}


def _run():
    engine = BacktestEngine(_data(), SMACrossoverStrategy(20, 50), initial_cash=100000.0, apply_costs=True)
    return engine.run()


def test_backtest_is_byte_identical_across_runs():
    a = _run()[["date", "total_equity"]].copy()
    a["total_equity"] = a["total_equity"].round(10)
    b = _run()[["date", "total_equity"]].copy()
    b["total_equity"] = b["total_equity"].round(10)

    pd.testing.assert_frame_equal(a, b, check_exact=True)


def test_backtest_equity_hash_stable():
    h = _run()["total_equity"].round(6).to_csv(index=False)
    digest = __import__("hashlib").sha256(h.encode()).hexdigest()

    h2 = _run()["total_equity"].round(6).to_csv(index=False)
    digest2 = __import__("hashlib").sha256(h2.encode()).hexdigest()

    assert digest == digest2, "same request must yield byte-identical equity curve"


def test_costs_change_the_outcome():
    free = _run()["total_equity"].iloc[-1]
    engine = BacktestEngine(_data(), SMACrossoverStrategy(20, 50), initial_cash=100000.0, apply_costs=False)
    paid = engine.run()["total_equity"].iloc[-1]
    assert free < paid, "statutory costs must reduce terminal equity"
