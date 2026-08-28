import pytest
import pandas as pd
from datetime import datetime, timedelta
from src.engine.backtest_engine import BacktestEngine
from src.strategies.base import Strategy
from src.engine.events import SignalEvent

class DummyStrategy(Strategy):
    def generate_signals(self, current_date, data, positions):
        # Always buy 1 share of RELIANCE on the first day
        if current_date == datetime(2023, 1, 1):
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
    
    engine = BacktestEngine(data, DummyStrategy(), initial_cash=1000.0, apply_costs=False)
    
    # Run backtest
    equity_history = engine.run()
    
    # 2023-01-01 Close: Signal generated (price ~ 101)
    # 2023-01-02 Open: Order executed at Open price 105.0
    assert "RELIANCE.NS" in engine.portfolio.positions
    pos = engine.portfolio.positions["RELIANCE.NS"]
    assert pos.average_entry_price == 105.0
