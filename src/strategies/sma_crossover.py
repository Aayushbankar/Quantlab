from src.strategies.base import Strategy
from src.engine.events import SignalEvent
from typing import Dict, List
import pandas as pd
from datetime import datetime

class SMACrossoverStrategy(Strategy):
    """
    Fast SMA / Slow SMA Crossover strategy.
    Buy when Fast crosses above Slow.
    Sell when Fast crosses below Slow.
    """
    def __init__(self, fast_window=20, slow_window=50):
        self.fast_window = fast_window
        self.slow_window = slow_window

    def generate_signals(self, current_date: datetime, data: Dict[str, pd.DataFrame], positions: Dict) -> List[SignalEvent]:
        signals = []
        for symbol, df in data.items():
            # Get data up to current date
            past_data = df[df['date'] <= current_date]
            if len(past_data) < self.slow_window + 1:
                continue # Not enough data
                
            # Calculate SMAs efficiently using the last few rows
            closes = past_data['close'].tail(self.slow_window + 1).values
            
            fast_ma_today = closes[-self.fast_window:].mean()
            slow_ma_today = closes[-self.slow_window:].mean()
            
            fast_ma_yest = closes[-(self.fast_window+1):-1].mean()
            slow_ma_yest = closes[-(self.slow_window+1):-1].mean()
            
            # Cross above
            if fast_ma_yest <= slow_ma_yest and fast_ma_today > slow_ma_today:
                signals.append(SignalEvent(timestamp=current_date, symbol=symbol, signal_type=1))
            
            # Cross below
            elif fast_ma_yest >= slow_ma_yest and fast_ma_today < slow_ma_today:
                if symbol in positions and positions[symbol].quantity > 0:
                    signals.append(SignalEvent(timestamp=current_date, symbol=symbol, signal_type=-1))
                    
        return signals
