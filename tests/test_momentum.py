import pytest
import pandas as pd
from datetime import datetime
from src.strategies.momentum import MomentumStrategy
from src.engine.position import Position

def test_momentum_no_duplicate_signals():
    strategy = MomentumStrategy(lookback_period=2, threshold_pct=0.10)
    
    dates = pd.date_range(start="2023-01-01", periods=5)
    data = {
        "AAPL": pd.DataFrame({
            "date": dates,
            # Prices: 100, 100, 120 (roc=0.2), 130 (roc=0.3), 140 (roc=0.16)
            # Day 3: ROC = (120 - 100)/100 = 0.20 > 0.10
            # Day 4: ROC = (130 - 100)/100 = 0.30 > 0.10
            # Day 5: ROC = (140 - 120)/120 = 0.166 > 0.10
            "close": [100.0, 100.0, 120.0, 130.0, 140.0],
        })
    }
    
    # Empty positions
    positions = {}
    
    # Day 3
    signals = strategy.generate_signals(dates[2], data, positions)
    assert len(signals) == 1
    assert signals[0].symbol == "AAPL"
    assert signals[0].signal_type == 1
    
    # Simulate execution: Add position
    pos = Position("AAPL")
    pos.update("BUY", 10, 120.0, 0.0)
    positions["AAPL"] = pos
    
    # Day 4
    # ROC is 0.30 > 0.10, but we already have an open position!
    signals = strategy.generate_signals(dates[3], data, positions)
    assert len(signals) == 0, "Should not generate duplicate BUY signal"
    
    # Day 5
    signals = strategy.generate_signals(dates[4], data, positions)
    assert len(signals) == 0, "Should not generate duplicate BUY signal"
