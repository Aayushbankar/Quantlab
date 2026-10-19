from abc import ABC, abstractmethod
from typing import List, Dict
import pandas as pd
from src.engine.events import SignalEvent
from datetime import datetime

class Strategy(ABC):
    """Base interface for all trading strategies."""
    
    @abstractmethod
    def generate_signals(self, current_date: datetime, data: Dict[str, pd.DataFrame], positions: Dict) -> List[SignalEvent]:
        """
        Evaluates data up to current_date and returns a list of SignalEvents.
        """
        pass
