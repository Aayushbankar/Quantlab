from abc import ABC, abstractmethod
from datetime import datetime

import pandas as pd

from src.engine.events import SignalEvent


class Strategy(ABC):
    """Base interface for all trading strategies."""

    @abstractmethod
    def generate_signals(
        self, current_date: datetime, data: dict[str, pd.DataFrame], positions: dict
    ) -> list[SignalEvent]:
        """
        Evaluates data up to current_date and returns a list of SignalEvents.
        """
        pass
