import pandas as pd
from typing import Dict, List
from src.engine.events import MarketEvent, SignalEvent, OrderEvent
from src.engine.portfolio import Portfolio
from src.engine.cost_model import IndianCostModel

class BacktestEngine:
    """
    Event-driven simulation loop enforcing Zero Look-Ahead.
    Signal on day T Close -> Executed on day T+1 Open.
    """
    def __init__(self, data: Dict[str, pd.DataFrame], strategy, initial_cash=100000.0, apply_costs=True):
        self.data = data
        self.strategy = strategy
        self.portfolio = Portfolio(initial_cash=initial_cash)
        self.cost_model = IndianCostModel(apply_costs=apply_costs)
        
        # Internal state
        self.pending_orders: List[OrderEvent] = []
        self._align_data()

    def _align_data(self):
        """Creates a sorted master timeline of all dates across the universe."""
        dates = set()
        for df in self.data.values():
            dates.update(df['date'].tolist())
        self.timeline = sorted(list(dates))

    def run(self):
        """Executes the backtest."""
        print("Starting backtest...")
        
        for i, current_date in enumerate(self.timeline):
            # 1. T+1 OPEN: Execute pending orders from previous day (T)
            self._execute_pending_orders(current_date)
            
            # 2. T CLOSE: Update MTM (Mark-to-Market) and generate new signals
            daily_events = []
            for symbol, df in self.data.items():
                # Get data up to current date (inclusive)
                # In a real system, we'd feed row by row. Here we simulate it efficiently
                mask = df['date'] == current_date
                if not mask.any():
                    continue
                    
                row = df[mask].iloc[0]
                market_event = MarketEvent(
                    timestamp=current_date, symbol=symbol,
                    open=row['open'], high=row['high'],
                    low=row['low'], close=row['close'], volume=row['volume']
                )
                daily_events.append(market_event)
                
                # Update portfolio timeindex (MTM based on close)
                self.portfolio.update_timeindex(market_event)

            # Generate signals on T Close
            signals = self.strategy.generate_signals(current_date, self.data, self.portfolio.positions)
            
            # Convert signals to pending orders for T+1 Open
            self._process_signals(signals, current_date)

        print("Backtest completed.")
        return pd.DataFrame(self.portfolio.equity_history)

    def _execute_pending_orders(self, current_date):
        """Fills orders at the OPEN price of the current date."""
        executed = []
        for order in self.pending_orders:
            df = self.data.get(order.symbol)
            mask = df['date'] == current_date
            if mask.any():
                row = df[mask].iloc[0]
                open_price = row['open']
                
                # Apply cost model to get exact fill event
                fill_event = self.cost_model.process_order(order, open_price)
                fill_event.timestamp = current_date
                
                # Apply to portfolio
                self.portfolio.apply_fill(fill_event)
                executed.append(order)
                
        # Remove executed orders
        self.pending_orders = [o for o in self.pending_orders if o not in executed]

    def _process_signals(self, signals: List[SignalEvent], current_date):
        """Converts signals to pending orders."""
        for signal in signals:
            # Simplistic sizing: invest 10% of current equity per signal
            # In a real system, a dedicated PositionSizer would handle this
            current_equity = self.portfolio.cash # simplified, should use total equity
            target_value = current_equity * 0.10
            
            # Get latest close price to estimate quantity
            df = self.data[signal.symbol]
            row = df[df['date'] == current_date].iloc[0]
            est_price = row['close']
            
            if est_price <= 0: continue
            
            qty = int(target_value / est_price)
            if qty <= 0: continue
            
            side = 'BUY' if signal.signal_type == 1 else 'SELL'
            
            # Check if we have position to sell
            if side == 'SELL':
                pos = self.portfolio.positions.get(signal.symbol)
                if not pos or pos.quantity <= 0:
                    continue # Ignore sell if no long position
                qty = min(qty, pos.quantity) # Don't short
                
            order = OrderEvent(
                timestamp=current_date,
                symbol=signal.symbol,
                order_type='MKT',
                side=side,
                quantity=qty
            )
            self.pending_orders.append(order)
