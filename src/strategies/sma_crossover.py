from datetime import datetime

import numpy as np
import pandas as pd

from src.engine.events import SignalEvent
from src.strategies.base import Strategy


class SMACrossoverStrategy(Strategy):
    """
    Fast SMA / Slow SMA Crossover strategy.
    Buy when Fast crosses above Slow.
    Sell when Fast crosses below Slow.
    """

    def __init__(self, fast_window=20, slow_window=50):
        self.fast_window = fast_window
        self.slow_window = slow_window

    def generate_signals(
        self, current_date: datetime, data: dict[str, pd.DataFrame], positions: dict
    ) -> list[SignalEvent]:
        signals = []
        for symbol, df in data.items():
            if df.empty:
                continue
            # Use already-sliced frame directly if available (D10); fallback to filter only if needed
            dates = df["date"].values
            past_data = df if dates[-1] <= np.datetime64(current_date) else df[df["date"] <= current_date]
            if len(past_data) < self.slow_window + 1:
                continue  # Not enough data

            # Calculate SMAs efficiently using the last few rows
            closes = past_data["close"].values
            w = closes[-(self.slow_window + 1) :]

            fast_ma_today = float(np.sum(w[-self.fast_window :]) / self.fast_window)
            slow_ma_today = float(np.sum(w[-self.slow_window :]) / self.slow_window)

            fast_ma_yest = float(np.sum(w[-(self.fast_window + 1) : -1]) / self.fast_window)
            slow_ma_yest = float(np.sum(w[-(self.slow_window + 1) : -1]) / self.slow_window)

            # Cross above
            if fast_ma_yest <= slow_ma_yest and fast_ma_today > slow_ma_today:
                signals.append(SignalEvent(timestamp=current_date, symbol=symbol, signal_type=1))

            # Cross below
            elif fast_ma_yest >= slow_ma_yest and fast_ma_today < slow_ma_today:
                if symbol in positions and positions[symbol].quantity > 0:
                    signals.append(SignalEvent(timestamp=current_date, symbol=symbol, signal_type=-1))

        return signals
