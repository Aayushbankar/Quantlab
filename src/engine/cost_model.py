from src.engine.events import OrderEvent, FillEvent

class IndianCostModel:
    """
    Implements statutory Indian equity delivery costs and slippage.
    """
    def __init__(self, apply_costs: bool = True, gamma: float = 0.1):
        self.apply_costs = apply_costs
        self.gamma = gamma # Market impact calibration constant

    def process_order(self, order: OrderEvent, raw_price: float, volatility: float = 0.02, adv: int = 1000000) -> FillEvent:
        """
        Calculates slippage using Almgren-Chriss Square Root Model and applies statutory fees.
        """
        if not self.apply_costs:
            return FillEvent(
                timestamp=order.timestamp, symbol=order.symbol, side=order.side, 
                quantity=order.quantity, raw_price=raw_price, fill_price=raw_price,
                commission=0, stt=0, stamp_duty=0, gst=0, turnover_fee=0, total_cost=0
            )

        # Almgren-Chriss Square Root Impact Model
        # dP = gamma * sigma * sqrt(Q / V)
        q_v_ratio = order.quantity / max(adv, 1) # Prevent div by zero
        market_impact_pct = self.gamma * volatility * (q_v_ratio ** 0.5)
        
        # Cap impact to prevent absurd prices in illiquid edge cases
        market_impact_pct = min(market_impact_pct, 0.05) 

        # Apply slippage (worse execution price)
        if order.side == 'BUY':
            fill_price = raw_price * (1 + market_impact_pct)
        else:
            fill_price = raw_price * (1 - market_impact_pct)
            
        trade_value = fill_price * order.quantity
        
        # 1. Brokerage: min(20, 0.03% of trade value)
        brokerage = min(20.00, trade_value * 0.0003)
        
        # 2. STT: 0.1% on both Buy & Sell (Delivery) - CBDT Rule 5 round to nearest integer
        stt = float(round(trade_value * 0.0010))
        
        # 3. Stamp Duty: 0.015% (Buy only)
        stamp_duty = (trade_value * 0.00015) if order.side == 'BUY' else 0.0
        
        # 4. NSE Turnover Fee: 0.00297% (SEBI True-to-Label w.e.f. Oct 2024) + SEBI fee 0.0001%
        nse_turnover = trade_value * 0.0000297
        sebi_turnover = trade_value * 0.000001
        total_turnover = nse_turnover + sebi_turnover
        
        # 5. GST: 18% on (Brokerage + Turnover)
        gst = (brokerage + total_turnover) * 0.18
        
        total_cost = brokerage + stt + stamp_duty + total_turnover + gst
        
        return FillEvent(
            timestamp=order.timestamp, 
            symbol=order.symbol, 
            side=order.side, 
            quantity=order.quantity, 
            raw_price=raw_price, 
            fill_price=fill_price,
            commission=brokerage, 
            stt=stt, 
            stamp_duty=stamp_duty, 
            gst=gst, 
            turnover_fee=total_turnover, 
            total_cost=total_cost
        )
