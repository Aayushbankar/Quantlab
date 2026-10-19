from datetime import datetime

from src.engine.events import SignalEvent
from src.strategies.base import Strategy


class BuyAndHoldStrategy(Strategy):
    """
    Benchmark control: buy once on the first available bar, never sell.

    Not a trading strategy — it is the null hypothesis. Any active strategy
    that cannot beat this on a risk-adjusted basis has no edge: it is a
    friction tax disguised as alpha.
    """

    def __init__(self, skip_first: int = 1):
        self.skip_first = skip_first

    def generate_signals(self, current_date: datetime, data: dict, positions: dict) -> list[SignalEvent]:
        if self.skip_first > 0:
            self.skip_first -= 1
        else:
            return []

        signals = []
        for symbol in data:
            if symbol not in positions or positions[symbol].quantity == 0:
                signals.append(SignalEvent(timestamp=current_date, symbol=symbol, signal_type=1))
        return signals
