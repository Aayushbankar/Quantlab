import numpy as np
import pandas as pd
import pytest

from src.strategies.rsi_mean_reversion import RSIMeanReversionStrategy


def _strategy():
    return RSIMeanReversionStrategy(period=14, oversold=30, overbought=70)


def test_rsi_100_when_all_gains():
    # Every delta positive -> average loss is exactly zero.
    # Prior implementation returned RSI 0 (max oversold) here, emitting the
    # exact opposite signal from the one the price action implies.
    closes = np.linspace(100.0, 200.0, 60)  # 59 strictly positive deltas
    rsi_today, rsi_yest = _strategy()._calculate_rsi(closes)

    assert rsi_today == pytest.approx(100.0), f"all-gains window must saturate at 100, got {rsi_today}"
    assert rsi_yest == pytest.approx(100.0)


def test_rsi_0_when_all_losses():
    closes = np.linspace(200.0, 100.0, 60)
    rsi_today, _ = _strategy()._calculate_rsi(closes)
    assert rsi_today == pytest.approx(0.0), f"all-losses window must floor at 0, got {rsi_today}"


def test_rsi_neutral_on_flat_series():
    closes = np.full(60, 150.0)
    rsi_today, _ = _strategy()._calculate_rsi(closes)
    assert rsi_today == pytest.approx(50.0), f"no movement must be neutral 50, got {rsi_today}"


def test_rsi_bounded_zero_to_hundred_on_random_walk():
    rng = np.random.default_rng(7)
    for _ in range(20):
        closes = 100 * np.cumprod(1 + rng.normal(0, 0.02, 80))
        rsi_today, rsi_yest = _strategy()._calculate_rsi(closes)
        assert 0.0 <= rsi_today <= 100.0
        assert 0.0 <= rsi_yest <= 100.0


def test_rsi_all_gains_does_not_emit_oversold_buy():
    # Guards the original signal-inversion bug end-to-end through the strategy API.
    strategy = RSIMeanReversionStrategy(period=3, oversold=30, overbought=70)
    dates = pd.date_range("2023-01-01", periods=10)
    df = pd.DataFrame({
        "date": dates,
        "open": np.linspace(100, 130, 10),
        "high": np.linspace(100, 130, 10),
        "low": np.linspace(100, 130, 10),
        "close": np.linspace(100, 130, 10),  # monotonically rising
        "volume": [1000] * 10,
    })

    signals = [strategy.generate_signals(d, {"RELIANCE.NS": df}, {}) for d in dates]

    buys = [s for day in signals for s in day if s.signal_type == 1]
    assert buys == [], f"rising market must not emit an oversold BUY, got {buyer_symbols(buys)}"


def buyer_symbols(signals):
    return [s.symbol for s in signals]
