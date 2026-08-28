from dataclasses import dataclass
from datetime import datetime

@dataclass
class Order:
    """Represents an order in the system."""
    symbol: str
    side: str # 'BUY' or 'SELL'
    quantity: int
    timestamp: datetime
    order_type: str = 'MKT'
    limit_price: float = 0.0
    price: float = 0.0 # Will be populated upon execution if MKT
    status: str = 'PENDING' # PENDING, FILLED, REJECTED
