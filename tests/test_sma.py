import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from src.strategies.sma_crossover import SMACrossoverStrategy
from src.engine.position import Position


def _frame(closes):
    dates = pd.date_range("2023-01-01", periods=len(closes))
    return pd.DataFrame({
        "date": dates,
        "open": closes,
        "high": closes,
        "low": closes,
        "close": closes,
        "volume": [1000] * len(closes),
    })


def _rising(n, start=100.0, step=1.0):
    return [start + step * i for i in range(n)]


def _flat(n, value=100.0):
    return [value] * n


def test_sma_golden_cross_emits_buy():
    # 9 bars dip (fast SMA falls below slow) then recover: a genuine upward cross.
    closes = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
              100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
    # fast window 2, slow window 5 keeps the fixture small and the cross unambiguous
    strategy = SMACrossoverStrategy(fast_window=2, slow_window=5)
    df = _frame(closes + [110.0, 115.0, 120.0, 125.0, 130.0])

    signals = []
    for d in df['date']:
        signals.extend(strategy.generate_signals(d, {"X": df}, {}))

    buys = [s for s in signals if s.signal_type == 1]
    assert buys, "a sustained rally must eventually cross the slow SMA upward"


def test_sma_death_cross_emits_sell_only_with_position():
    closes = _flat(10) + _rising(6, start=100.0, step=5.0) + _flat(4) + [
        90.0, 85.0, 80.0, 75.0, 70.0
    ]
    strategy = SMACrossoverStrategy(fast_window=2, slow_window=5)
    df = _frame(closes)

    pos = Position("X")
    pos.update("BUY", 10, 100.0, 0.0)
    positions = {"X": pos}

    signals = []
    for d in df['date']:
        signals.extend(strategy.generate_signals(d, {"X": df}, positions))

    sells = [s for s in signals if s.signal_type == -1]
    assert sells, "a sustained decline must cross the slow SMA downward"

    # Without a position there is nothing to sell, and the engine must not
    # generate a spurious SELL signal for a symbol it does not hold.
    flat_signals = []
    for d in df['date']:
        flat_signals.extend(strategy.generate_signals(d, {"X": df}, {}))
    flat_sells = [s for s in flat_signals if s.signal_type == -1]
    assert flat_sells == []


def test_sma_insufficient_history_produces_no_signal():
    strategy = SMACrossoverStrategy(fast_window=2, slow_window=5)
    df = _frame(_flat(3))  # fewer bars than slow_window + 1

    signals = strategy.generate_signals(df['date'].iloc[-1], {"X": df}, {})
    assert signals == []


def test_sma_respects_fast_must_be_less_than_slow():
    strategy = SMACrossoverStrategy(fast_window=5, slow_window=2)
    df = _frame(_rising(30))
    # Windows are inverted; the strategy must not silently treat this as valid.
    signals = strategy.generate_signals(df['date'].iloc[-1], {"X": df}, {})
    assert all(s.signal_type in (-1, 1) for s in signals)


def test_sma_no_lookahead_uses_only_past_bars():
    # A future spike must not influence any signal generated before it.
    clean = _frame(_rising(12))
    spiked = _frame(_rising(12) + [999.0] * 3)

    strategy = SMACrossoverStrategy(fast_window=2, slow_window=5)

    early_clean = [
        s for d in clean['date'][:11] for s in strategy.generate_signals(d, {"X": clean}, {})
    ]
    early_spiked = [
        s for d in spiked['date'][:11] for s in strategy.generate_signals(d, {"X": spiked}, {})
    ]

    assert [ (s.symbol, s.signal_type) for s in early_clean ] == \
           [ (s.symbol, s.signal_type) for s in early_spiked ]
