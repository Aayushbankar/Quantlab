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
        self.idx_trackers = {}
        for symbol, df in self.data.items():
            dates.update(df['date'].tolist())
            self.idx_trackers[symbol] = 0 # Track row index for O(1) slicing
        self.timeline = sorted(list(dates))

    def run(self):
        """Executes the backtest."""
        print("Starting High-Performance Event Loop...")
        
        for current_date in self.timeline:
            # 1. T+1 OPEN: Execute pending orders
            self._execute_pending_orders(current_date)
            
            # Update trackers
            for symbol, df in self.data.items():
                idx = self.idx_trackers[symbol]
                if idx < len(df) and df['date'].iloc[idx] <= current_date:
                    self.idx_trackers[symbol] += 1
            
            # 2. T CLOSE: MTM and signal generation
            current_prices = {}
            for symbol, df in self.data.items():
                idx = self.idx_trackers[symbol] - 1
                if idx >= 0 and df['date'].iloc[idx] == current_date:
                    current_prices[symbol] = df['close'].iloc[idx]
                
            self.portfolio.update_timeindex(current_date, current_prices)

            # Fast O(1) Data Slicing (Eliminates O(N^2) memory thrashing)
            sliced_data = {}
            for symbol, df in self.data.items():
                sliced_data[symbol] = df.iloc[:self.idx_trackers[symbol]]

            signals = self.strategy.generate_signals(current_date, sliced_data, self.portfolio.positions)
            self._process_signals(signals, current_date, sliced_data)

        print("Backtest completed.")
        return pd.DataFrame(self.portfolio.equity_history)

    def _execute_pending_orders(self, current_date):
        """Fills orders with Trade-Through Limit Logic and Market Impact."""
        executed = []
        for order in self.pending_orders:
            df = self.data.get(order.symbol)
            idx = self.idx_trackers[order.symbol]
            if idx < len(df) and df['date'].iloc[idx] == current_date:
                row = df.iloc[idx]
                
                # Trade-Through Limit Order Logic
                if order.order_type == 'LMT':
                    if order.side == 'BUY' and row['low'] >= order.limit_price:
                        continue # Price never reached limit
                    if order.side == 'SELL' and row['high'] <= order.limit_price:
                        continue
                    exec_price = order.limit_price # Executed exactly at limit
                else:
                    exec_price = row['open'] # MKT executes at Open
                
                # Estimate Volatility and ADV for Almgren-Chriss Impact
                past_data = df.iloc[max(0, idx-20):idx]
                vol = past_data['close'].pct_change().std() if len(past_data) > 2 else 0.02
                adv = past_data['volume'].mean() if len(past_data) > 2 else 1000000
                vol = vol if not pd.isna(vol) else 0.02
                adv = adv if not pd.isna(adv) else 1000000

                fill_event = self.cost_model.process_order(order, exec_price, volatility=vol, adv=adv)
                
                if order.side == 'BUY':
                    estimated_cost = (fill_event.quantity * fill_event.fill_price) + fill_event.total_cost
                    if estimated_cost > self.portfolio.cash:
                        executed.append(order)
                        continue

                fill_event.timestamp = current_date
                self.portfolio.apply_fill(fill_event)
                executed.append(order)
                
        self.pending_orders = [o for o in self.pending_orders if o not in executed]

    def _process_signals(self, signals: List[SignalEvent], current_date, sliced_data):
        for signal in signals:
            side = 'BUY' if signal.signal_type == 1 else 'SELL'
            
            if side == 'BUY':
                current_equity = self.portfolio.cash
                target_value = current_equity * 0.10
                
                df = sliced_data[signal.symbol]
                est_price = df['close'].iloc[-1]
                
                if est_price <= 0: continue
                qty = int(target_value / est_price)
                if qty <= 0: continue
            else:
                pos = self.portfolio.positions.get(signal.symbol)
                if not pos or pos.quantity <= 0:
                    continue
                qty = pos.quantity
                
            order = OrderEvent(
                timestamp=current_date,
                symbol=signal.symbol,
                order_type='MKT', # Extensible to LMT in advanced strategies
                side=side,
                quantity=qty
            )
            self.pending_orders.append(order)
