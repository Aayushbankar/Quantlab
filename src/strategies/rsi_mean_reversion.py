from src.strategies.base import Strategy
from src.engine.events import SignalEvent
from typing import Dict, List
import pandas as pd
import numpy as np
from datetime import datetime

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

    def _calculate_rsi(self, closes: np.ndarray) -> float:
        deltas = np.diff(closes)
        seed = deltas[:self.period]
        up = seed[seed >= 0].sum()/self.period
        down = -seed[seed < 0].sum()/self.period
        rs = up/down if down != 0 else 0
        rsi = np.zeros_like(closes)
        rsi[:self.period] = 100. - 100./(1. + rs)

        for i in range(self.period, len(closes)):
            delta = deltas[i - 1]
            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta

            up = (up*(self.period - 1) + upval)/self.period
            down = (down*(self.period - 1) + downval)/self.period
            rs = up/down if down != 0 else 0
            rsi[i] = 100. - 100./(1. + rs)
        return rsi[-1], rsi[-2]

    def generate_signals(self, current_date: datetime, data: Dict[str, pd.DataFrame], positions: Dict) -> List[SignalEvent]:
        signals = []
        for symbol, df in data.items():
            past_data = df[df['date'] <= current_date]
            if len(past_data) < self.period * 2:
                continue
                
            # Need a decent buffer to calculate Wilder's smoothing accurately
            closes = past_data['close'].tail(self.period * 5).values
            rsi_today, rsi_yest = self._calculate_rsi(closes)
            
            # Oversold -> Buy
            if rsi_yest >= self.oversold and rsi_today < self.oversold:
                signals.append(SignalEvent(timestamp=current_date, symbol=symbol, signal_type=1))
                
            # Overbought -> Sell
            elif rsi_yest <= self.overbought and rsi_today > self.overbought:
                if symbol in positions and positions[symbol].quantity > 0:
                    signals.append(SignalEvent(timestamp=current_date, symbol=symbol, signal_type=-1))
                    
        return signals
