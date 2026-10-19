import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from src.strategies.bollinger_breakout import BollingerBreakoutStrategy
from src.engine.portfolio import Position


def test_bollinger_breakout_signals():
    strat = BollingerBreakoutStrategy(period=5, num_std=1.0)
    dates = pd.date_range("2023-01-01", periods=10, freq="D")
    # Prices: 10, 10, 10, 10, 10, then breakout to 20
    prices = [10.0, 10.0, 10.0, 10.0, 10.0, 20.0, 21.0, 8.0, 7.0, 7.0]
    df = pd.DataFrame({"date": dates, "close": prices})
    data = {"RELIANCE": df}

    # At bar 5 (index 5, price 20), mean of prev 5 is 10, std is 0 -> price > band -> BUY
    # Note: past_data for 2023-01-06 includes price 20.0. Closes of tail(5) are [10, 10, 10, 10, 20]
    # mean is 12, std is 4, upper band = 16. Price 20 > 16 -> triggers BUY!
    signals = strat.generate_signals(dates[5], data, {})
    assert len(signals) == 1
    assert signals[0].signal_type == 1
    assert signals[0].symbol == "RELIANCE"

    # With open position, subsequent high price does not emit duplicate BUY
    pos_obj = Position("RELIANCE")
    pos_obj.update("BUY", 10, 20.0, 0.0)
    pos = {"RELIANCE": pos_obj}
    signals_dup = strat.generate_signals(dates[6], data, pos)
    assert len(signals_dup) == 0

    # At bar 7 (price 8.0), price drops below SMA -> emits SELL
    signals_exit = strat.generate_signals(dates[7], data, pos)
    assert len(signals_exit) == 1
    assert signals_exit[0].signal_type == -1
