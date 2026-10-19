from src.strategies.base import Strategy
from src.engine.events import SignalEvent
from typing import Dict, List
import pandas as pd
from datetime import datetime

class MomentumStrategy(Strategy):
    """
    Relative Momentum Strategy (Rate of Change).
    Buy if ROC over lookback period is positive and above a threshold.
    Sell if ROC turns negative.
    """
    def __init__(self, lookback_period=20, threshold_pct=0.05):
        self.lookback_period = lookback_period
        self.threshold_pct = threshold_pct

    def generate_signals(self, current_date: datetime, data: Dict[str, pd.DataFrame], positions: Dict) -> List[SignalEvent]:
        signals = []
        for symbol, df in data.items():
            past_data = df[df['date'] <= current_date]
            if len(past_data) < self.lookback_period + 1:
                continue
                
            closes = past_data['close'].tail(self.lookback_period + 1).values
            
            price_today = closes[-1]
            price_n_days_ago = closes[-1 - self.lookback_period]
            
            roc = (price_today - price_n_days_ago) / price_n_days_ago
            
            if roc > self.threshold_pct:
                # FIX: Previous code emitted a BUY signal every day ROC stayed above threshold.
                # Added guard to only buy if there is no existing open position for this symbol.
                if symbol not in positions or positions[symbol].quantity == 0:
                    signals.append(SignalEvent(timestamp=current_date, symbol=symbol, signal_type=1))
            elif roc < 0:
                if symbol in positions and positions[symbol].quantity > 0:
                    signals.append(SignalEvent(timestamp=current_date, symbol=symbol, signal_type=-1))
                    
        return signals
