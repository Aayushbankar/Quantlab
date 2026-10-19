import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List
from src.strategies.base import Strategy
from src.engine.events import SignalEvent


class BollingerBreakoutStrategy(Strategy):
    """
    Bollinger Band Volatility Breakout Strategy.
    Buys when price breaks above the Upper Bollinger Band (20-day SMA + 2 StdDev).
    Exits when price falls back below the 20-day middle moving average.
    Avoids duplicate BUY signals while a position is active.
    """
    def __init__(self, period: int = 20, num_std: float = 2.0):
        self.period = int(period)
        self.num_std = float(num_std)

    def generate_signals(self, current_date: datetime, data: Dict[str, pd.DataFrame], positions: Dict) -> List[SignalEvent]:
        signals = []
        for symbol, df in data.items():
            past_data = df[df['date'] <= current_date]
            if len(past_data) < self.period + 1:
                continue

            closes = past_data['close'].tail(self.period).values
            mean = np.mean(closes)
            std = np.std(closes)
            if std == 0:
                continue

            upper_band = mean + (self.num_std * std)
            current_close = past_data['close'].iloc[-1]

            # Long Entry: Price closes above Upper Band with no existing position
            if current_close > upper_band:
                if symbol not in positions or positions[symbol].quantity == 0:
                    signals.append(SignalEvent(timestamp=current_date, symbol=symbol, signal_type=1))
            # Long Exit: Price falls back below Middle SMA
            elif current_close < mean:
                if symbol in positions and positions[symbol].quantity > 0:
                    signals.append(SignalEvent(timestamp=current_date, symbol=symbol, signal_type=-1))

        return signals
