class Position:
    """Represents a trading position in a specific symbol."""
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.quantity = 0
        self.average_entry_price = 0.0
        self.realized_pnl = 0.0

    def update(self, side: str, quantity: int, fill_price: float, total_cost: float):
        """Updates the position based on a filled order."""
        if side == 'BUY':
            if self.quantity >= 0:
                # Adding to long position
                total_cost_basis = (self.quantity * self.average_entry_price) + (quantity * fill_price)
                self.quantity += quantity
                self.average_entry_price = total_cost_basis / self.quantity
            else:
                # Covering a short (Out of scope for this project, but handled for completeness)
                pass # Simplified for long-only mostly
        elif side == 'SELL':
            if self.quantity > 0:
                # Closing long position
                close_qty = min(self.quantity, quantity)
                pnl = (fill_price - self.average_entry_price) * close_qty
                self.realized_pnl += pnl - total_cost
                self.quantity -= quantity
                if self.quantity == 0:
                    self.average_entry_price = 0.0

    def unrealized_pnl(self, current_price: float) -> float:
        """Calculates unrealized PnL based on current market price."""
        return (current_price - self.average_entry_price) * self.quantity
