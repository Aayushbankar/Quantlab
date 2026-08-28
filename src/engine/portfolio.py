from typing import Dict, List
from src.engine.events import FillEvent, MarketEvent
from src.engine.position import Position

class Portfolio:
    """
    Maintains the state of cash and positions, enforcing invariants.
    """
    def __init__(self, initial_cash: float = 100000.0):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions: Dict[str, Position] = {}
        self.equity_history: List[dict] = []
        
    def apply_fill(self, fill: FillEvent):
        """
        Updates cash and positions based on a filled order.
        Enforces Cash >= 0 invariant (in a real system, the order manager would preemptively check, 
        but here we assume the sizing logic is correct. We will log a warning if cash goes negative).
        """
        if fill.symbol not in self.positions:
            self.positions[fill.symbol] = Position(fill.symbol)
            
        position = self.positions[fill.symbol]
        
        # Calculate cash flow
        if fill.side == 'BUY':
            cash_flow = -(fill.quantity * fill.fill_price) - fill.total_cost
        else: # SELL
            cash_flow = (fill.quantity * fill.fill_price) - fill.total_cost
            
        self.cash += cash_flow
        
        if self.cash < 0:
            print(f"WARNING: Cash balance dropped below zero: {self.cash}")
            
        position.update(fill.side, fill.quantity, fill.fill_price, fill.total_cost)
        
    def update_timeindex(self, event: MarketEvent):
        """
        Records the current total equity at the given market event timestamp.
        """
        total_equity = self.cash
        for symbol, position in self.positions.items():
            if position.quantity > 0:
                # We use the closing price of the event to mark-to-market
                total_equity += position.quantity * event.close
                
        self.equity_history.append({
            'date': event.timestamp,
            'cash': self.cash,
            'total_equity': total_equity
        })
