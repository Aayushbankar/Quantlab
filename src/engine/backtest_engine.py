import logging

import numpy as np
import pandas as pd

from src.engine.cost_model import IndianCostModel
from src.engine.events import OrderEvent, SignalEvent
from src.engine.portfolio import Portfolio

logger = logging.getLogger(__name__)


class BacktestEngine:
    """
    Event-driven simulation loop enforcing Zero Look-Ahead.
    Signal on day T Close -> Executed on day T+1 Open.
    """

    def __init__(
        self,
        data: dict[str, pd.DataFrame],
        strategy,
        initial_cash=100000.0,
        apply_costs=True,
        cost_model: IndianCostModel | None = None,
    ):
        self.data = data
        self.strategy = strategy
        self.portfolio = Portfolio(initial_cash=initial_cash)
        self.cost_model = cost_model if cost_model is not None else IndianCostModel(apply_costs=apply_costs)

        # Internal state
        self.pending_orders: list[OrderEvent] = []
        self._align_data()

    def _align_data(self):
        """Creates a sorted master timeline of all dates across the universe."""
        dates = set()
        self.idx_trackers = {}
        self._date_arrays = {}
        self._close_arrays = {}
        self._open_arrays = {}
        self._high_arrays = {}
        self._low_arrays = {}
        self._vol_arrays = {}

        for symbol, df in self.data.items():
            dates.update(df["date"].tolist())
            self.idx_trackers[symbol] = 0  # Track row index for O(1) slicing
            self._date_arrays[symbol] = df["date"].to_numpy()
            self._close_arrays[symbol] = df["close"].to_numpy()
            self._open_arrays[symbol] = df["open"].to_numpy()
            self._high_arrays[symbol] = df["high"].to_numpy()
            self._low_arrays[symbol] = df["low"].to_numpy()
            self._vol_arrays[symbol] = df["volume"].to_numpy()

        self.timeline = sorted(list(dates))

    def run(self):
        """Executes the backtest."""
        logger.info("Starting High-Performance Event Loop...")
        sliced_data = {s: self.data[s].iloc[:0] for s in self.data}
        prev_indices = {s: 0 for s in self.data}

        for current_date in self.timeline:
            c_date_np = np.datetime64(current_date)

            # 1. T+1 OPEN: Execute pending orders
            self._execute_pending_orders(current_date, c_date_np)

            # Update trackers using fast numpy comparison
            for symbol, arr in self._date_arrays.items():
                idx = self.idx_trackers[symbol]
                if idx < len(arr) and arr[idx] <= c_date_np:
                    self.idx_trackers[symbol] = idx + 1

            # 2. T CLOSE: MTM and signal generation
            current_prices = {}
            for symbol, arr in self._date_arrays.items():
                idx = self.idx_trackers[symbol] - 1
                if idx >= 0 and arr[idx] == c_date_np:
                    current_prices[symbol] = self._close_arrays[symbol][idx]

            self.portfolio.update_timeindex(current_date, current_prices)

            # Fast O(1) Data Slicing (only re-slice if index advanced)
            for symbol, idx in self.idx_trackers.items():
                if idx != prev_indices[symbol]:
                    sliced_data[symbol] = self.data[symbol][:idx]
                    prev_indices[symbol] = idx

            signals = self.strategy.generate_signals(current_date, sliced_data, self.portfolio.positions)
            self._process_signals(signals, current_date, sliced_data)

        logger.info("Backtest completed.")
        return pd.DataFrame(self.portfolio.equity_history)

    def _execute_pending_orders(self, current_date, c_date_np=None):
        """Fills orders with Trade-Through Limit Logic and Market Impact."""
        if not self.pending_orders:
            return
        if c_date_np is None:
            c_date_np = np.datetime64(current_date)
        executed = []
        for order in self.pending_orders:
            sym = order.symbol
            idx = self.idx_trackers[sym]
            dates = self._date_arrays.get(sym)
            if dates is not None and idx < len(dates) and dates[idx] == c_date_np:
                low_val = self._low_arrays[sym][idx]
                high_val = self._high_arrays[sym][idx]
                open_val = self._open_arrays[sym][idx]

                # Trade-Through Limit Order Logic
                if order.order_type == "LMT":
                    if order.side == "BUY" and low_val >= order.limit_price:
                        continue  # Price never reached limit
                    if order.side == "SELL" and high_val <= order.limit_price:
                        continue
                    exec_price = order.limit_price  # Executed exactly at limit
                else:
                    exec_price = open_val  # MKT executes at Open

                # Estimate Volatility and ADV for Almgren-Chriss Impact via fast numpy
                start_k = max(0, idx - 20)
                if idx - start_k > 2:
                    c_window = self._close_arrays[sym][start_k:idx]
                    rets = np.diff(c_window) / c_window[:-1]
                    vol = float(np.std(rets, ddof=1))
                    adv = float(np.mean(self._vol_arrays[sym][start_k:idx]))
                else:
                    vol = 0.02
                    adv = 1000000.0

                vol = vol if not (np.isnan(vol) or vol == 0) else 0.02
                adv = adv if not (np.isnan(adv) or adv == 0) else 1000000.0

                fill_event = self.cost_model.process_order(order, exec_price, volatility=vol, adv=adv)

                if order.side == "BUY":
                    estimated_cost = (fill_event.quantity * fill_event.fill_price) + fill_event.total_cost
                    if estimated_cost > self.portfolio.cash:
                        self.portfolio.record_rejected(
                            timestamp=str(current_date)[:10],
                            symbol=order.symbol,
                            side=order.side,
                            quantity=order.quantity,
                            price=exec_price,
                            reason=f"Insufficient cash (required ₹{estimated_cost:.2f}, available ₹{self.portfolio.cash:.2f})",
                        )
                        executed.append(order)
                        continue

                fill_event.timestamp = current_date
                self.portfolio.apply_fill(fill_event)
                executed.append(order)

        self.pending_orders = [o for o in self.pending_orders if o not in executed]

    def _process_signals(self, signals: list[SignalEvent], current_date, sliced_data):
        for signal in signals:
            side = "BUY" if signal.signal_type == 1 else "SELL"

            if side == "BUY":
                # FIX: Original code sized based on raw cash (self.portfolio.cash).
                # This causes position sizing to artificially shrink as more capital is deployed.
                # Correct sizing is 10% of total portfolio equity (cash + open positions MTM).
                current_equity = (
                    self.portfolio.equity_history[-1]["total_equity"]
                    if self.portfolio.equity_history
                    else self.portfolio.cash
                )
                target_value = current_equity * 0.10

                df = sliced_data[signal.symbol]
                est_price = df["close"].iloc[-1]

                if est_price <= 0:
                    continue
                qty = int(target_value / est_price)
                if qty <= 0:
                    self.portfolio.record_rejected(
                        timestamp=str(current_date)[:10],
                        symbol=signal.symbol,
                        side="BUY",
                        quantity=1,
                        price=est_price,
                        reason=f"Insufficient capital to buy 1 share (allocated ₹{target_value:.2f}, share price ₹{est_price:.2f})",
                    )
                    continue
            else:
                pos = self.portfolio.positions.get(signal.symbol)
                if not pos or pos.quantity <= 0:
                    continue
                qty = pos.quantity

            order = OrderEvent(
                timestamp=current_date,
                symbol=signal.symbol,
                order_type="MKT",  # Extensible to LMT in advanced strategies
                side=side,
                quantity=qty,
            )
            self.pending_orders.append(order)
