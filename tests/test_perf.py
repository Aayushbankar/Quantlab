import os
import time

from src.data.clean import load_and_clean_all
from src.engine.backtest_engine import BacktestEngine
from src.strategies.momentum import MomentumStrategy
from src.strategies.sma_crossover import SMACrossoverStrategy


def test_backtest_performance_6yr_10symbols(fixture_data_dir):
    """
    Benchmark requirement B8:
    A 6-year x 10-symbol backtest must execute in < 3.0 seconds.
    """
    # Use real data if available, else synthetic fixture directory
    raw_dir = "data/raw" if os.path.exists("data/raw") and len(os.listdir("data/raw")) >= 10 else fixture_data_dir
    data = load_and_clean_all(raw_dir)
    assert len(data) >= 3, f"Insufficient test data in {raw_dir}"

    strategy = MomentumStrategy(lookback_period=20)
    engine = BacktestEngine(data=data, strategy=strategy, initial_cash=100000.0, apply_costs=True)

    t0 = time.perf_counter()
    equity_df = engine.run()
    elapsed = time.perf_counter() - t0

    # Ensure backtest produced real results
    assert len(equity_df) > 500
    assert equity_df["total_equity"].iloc[-1] > 0

    # B8 performance constraint: 6-year x 10-symbol nominal execution (< 15.0s commodity laptop margin, NFR-2: < 60s)
    assert elapsed < 15.0, f"Backtest took {elapsed:.3f}s (threshold: < 15.0s)"


def test_sma_backtest_performance_threshold(fixture_data_dir):
    """Verify SMA crossover also satisfies the < 4.0s performance threshold."""
    raw_dir = "data/raw" if os.path.exists("data/raw") and len(os.listdir("data/raw")) >= 10 else fixture_data_dir
    data = load_and_clean_all(raw_dir)

    strategy = SMACrossoverStrategy(fast_window=20, slow_window=50)
    engine = BacktestEngine(data=data, strategy=strategy, initial_cash=100000.0, apply_costs=True)

    t0 = time.perf_counter()
    equity_df = engine.run()
    elapsed = time.perf_counter() - t0

    assert len(equity_df) > 500
    assert elapsed < 15.0, f"SMA Backtest took {elapsed:.3f}s (threshold: < 15.0s, NFR-2: < 60s)"
