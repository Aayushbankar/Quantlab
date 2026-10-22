from datetime import datetime

import numpy as np
import pandas as pd

from src.engine.events import SignalEvent
from src.strategies.base import Strategy


class RSIMeanReversionStrategy(Strategy):
    """
    RSI Mean Reversion (Wilder's RSI).
    Buy when RSI crosses below oversold (e.g. 30).
    Sell when RSI crosses above overbought (e.g. 70).
    """

    def __init__(self, period=14, oversold=30, overbought=70):
        self.period = period
        self.oversold = oversold
        self.overbought = overbought

    def _calculate_rsi(self, closes: np.ndarray):
        deltas = np.diff(closes)
        seed = deltas[: self.period]
        up = float(seed[seed >= 0].sum() / self.period)
        down = float(-seed[seed < 0].sum() / self.period)
        rs = self._relative_strength(up, down)
        curr_rsi = 100.0 - 100.0 / (1.0 + rs)
        prev_rsi = curr_rsi

        p_minus_1 = self.period - 1
        p_float = float(self.period)

        for i in range(self.period, len(closes)):
            delta = float(deltas[i - 1])
            if delta > 0:
                upval = delta
                downval = 0.0
            else:
                upval = 0.0
                downval = -delta

            up = (up * p_minus_1 + upval) / p_float
            down = (down * p_minus_1 + downval) / p_float
            rs = self._relative_strength(up, down)
            prev_rsi = curr_rsi
            curr_rsi = 100.0 - 100.0 / (1.0 + rs)
        return curr_rsi, prev_rsi

    @staticmethod
    def _relative_strength(up: float, down: float) -> float:
        if down > 0:
            return up / down
        if up > 0:
            # All gains: RSI must saturate at 100, not collapse to 0
            return float("inf")
        # No price movement: neutral convention
        return 1.0

    def generate_signals(
        self, current_date: datetime, data: dict[str, pd.DataFrame], positions: dict
    ) -> list[SignalEvent]:
        signals = []
        for symbol, df in data.items():
            if df.empty:
                continue
            dates = df["date"].values
            past_data = df if dates[-1] <= np.datetime64(current_date) else df[df["date"] <= current_date]
            if len(past_data) < self.period * 2:
                continue

            # Need a decent buffer to calculate Wilder's smoothing accurately
            closes = past_data["close"].values[-(self.period * 5) :]
            rsi_today, rsi_yest = self._calculate_rsi(closes)

            # Oversold -> Buy
            if rsi_yest >= self.oversold and rsi_today < self.oversold:
                signals.append(SignalEvent(timestamp=current_date, symbol=symbol, signal_type=1))

            # Overbought -> Sell
            elif rsi_yest <= self.overbought and rsi_today > self.overbought:
                if symbol in positions and positions[symbol].quantity > 0:
                    signals.append(SignalEvent(timestamp=current_date, symbol=symbol, signal_type=-1))

        return signals
