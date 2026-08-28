from dataclasses import dataclass
from datetime import datetime

class Event:
    """Base class for all events."""
    pass

@dataclass
class MarketEvent(Event):
    """Signals that a new market bar has arrived."""
    timestamp: datetime
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: int

@dataclass
class SignalEvent(Event):
    """Signals a trading recommendation (1 for BUY, -1 for SELL, 0 for HOLD)."""
    timestamp: datetime
    symbol: str
    signal_type: int
    strength: float = 1.0

@dataclass
class OrderEvent(Event):
    """Signals an order to be executed by the broker/exchange."""
    timestamp: datetime
    symbol: str
    order_type: str # 'MKT' or 'LMT'
    side: str # 'BUY' or 'SELL'
    quantity: int
    limit_price: float = 0.0

@dataclass
class FillEvent(Event):
    """Signals a filled order with all cost components."""
    timestamp: datetime
    symbol: str
    side: str
    quantity: int
    raw_price: float
    fill_price: float
    commission: float
    stt: float
    stamp_duty: float
    gst: float
    turnover_fee: float
    total_cost: float
