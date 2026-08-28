import pytest
import pandas as pd
from datetime import datetime, timedelta
from src.engine.backtest_engine import BacktestEngine
from src.strategies.base import Strategy
from src.engine.events import SignalEvent

class DummyStrategy(Strategy):
    def generate_signals(self, current_date, data, positions):
        # Always buy 1 share of RELIANCE on the first day
        if current_date == pd.Timestamp("2023-01-01"):
            return [SignalEvent(timestamp=current_date, symbol="RELIANCE.NS", signal_type=1)]
        return []

def test_engine_zero_look_ahead():
    # Setup dummy data
    dates = pd.date_range(start="2023-01-01", periods=3)
    data = {
        "RELIANCE.NS": pd.DataFrame({
            "date": dates,
            "open": [100.0, 105.0, 110.0],
            "high": [102.0, 107.0, 112.0],
            "low": [98.0, 103.0, 108.0],
            "close": [101.0, 106.0, 111.0],
            "volume": [1000, 1000, 1000]
        })
    }
    
    engine = BacktestEngine(data, DummyStrategy(), initial_cash=10000.0, apply_costs=False)
    
    # Run backtest
    equity_history = engine.run()
    
    # 2023-01-01 Close: Signal generated (price ~ 101)
    # 2023-01-02 Open: Order executed at Open price 105.0
    assert "RELIANCE.NS" in engine.portfolio.positions
    pos = engine.portfolio.positions["RELIANCE.NS"]
    assert pos.average_entry_price == 105.0

class SizingTestStrategy(Strategy):
    def generate_signals(self, current_date, data, positions):
        if current_date == pd.Timestamp("2023-01-01"):
            return [SignalEvent(timestamp=current_date, symbol="A", signal_type=1)]
        if current_date == pd.Timestamp("2023-01-02"):
            return [SignalEvent(timestamp=current_date, symbol="B", signal_type=1)]
        return []

def test_engine_position_sizing_uses_total_equity():
    dates = pd.date_range(start="2023-01-01", periods=3)
    data = {
        "A": pd.DataFrame({
            "date": dates,
            "open": [100.0, 100.0, 200.0],
            "high": [100.0, 200.0, 200.0],
            "low": [100.0, 100.0, 200.0],
            "close": [100.0, 200.0, 200.0],
            "volume": [1000, 1000, 1000]
        }),
        "B": pd.DataFrame({
            "date": dates,
            "open": [10.0, 10.0, 10.0],
            "high": [10.0, 10.0, 10.0],
            "low": [10.0, 10.0, 10.0],
            "close": [10.0, 10.0, 10.0],
            "volume": [1000, 1000, 1000]
        })
    }
    
    engine = BacktestEngine(data, SizingTestStrategy(), initial_cash=10000.0, apply_costs=False)
    engine.run()
    
    # Day 1: A closes at 100. Equity = 10000. Sizing 10% = 1000. qty = 10.
    # Day 2: open B closes at 10.
    # Day 2: A price is 200. Cash = 10000 - 10*100 = 9000. Total equity = 9000 + 10*200 = 11000.
    # Target size for B = 10% of 11000 = 1100. qty = 110.
    
    assert "B" in engine.portfolio.positions
    pos_b = engine.portfolio.positions["B"]
    assert pos_b.quantity == 110, f"Expected 110, got {pos_b.quantity}"
