import pytest
from datetime import datetime
from src.engine.events import OrderEvent
from src.engine.cost_model import IndianCostModel

def test_indian_cost_model_buy():
    model = IndianCostModel(apply_costs=True, slippage_pct=0.0005) # 0.05%
    
    order = OrderEvent(
        timestamp=datetime(2023, 1, 1),
        symbol="RELIANCE.NS",
        order_type="MKT",
        side="BUY",
        quantity=100
    )
    
    raw_price = 1000.0
    fill = model.process_order(order, raw_price)
    
    # Fill price should be raw_price * (1 + 0.0005)
    assert fill.fill_price == 1000.5
    
    trade_value = 1000.5 * 100 # 100050.0
    
    # Brokerage min(20, 100050 * 0.0003) = min(20, 30.015) = 20.0
    assert fill.commission == 20.0
    
    # STT: 100050 * 0.0010 = 100.05
    assert fill.stt == 100.05
    
    # Stamp Duty: 100050 * 0.00015 = 15.0075
    assert fill.stamp_duty == 15.0075
    
    # Turnover = 100050 * 0.0000307 = 3.0715
    assert fill.turnover_fee == 100050.0 * 0.0000307
    
    # GST = (20 + 3.0715) * 0.18 = 4.15287
    assert fill.gst == pytest.approx((20.0 + (100050.0 * 0.0000307)) * 0.18)
