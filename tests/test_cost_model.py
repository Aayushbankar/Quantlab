import pytest
from datetime import datetime
from src.engine.events import OrderEvent
from src.engine.cost_model import IndianCostModel

def test_indian_cost_model_buy():
    model = IndianCostModel(apply_costs=True, gamma=0.1)
    
    order = OrderEvent(
        timestamp=datetime(2023, 1, 1),
        symbol="RELIANCE.NS",
        order_type="MKT",
        side="BUY",
        quantity=100
    )
    
    raw_price = 1000.0
    # Simulate process_order with vol=0.02 and adv=1000000
    fill = model.process_order(order, raw_price, volatility=0.02, adv=1000000)
    
    # impact_pct = 0.1 * 0.02 * sqrt(100/1000000) = 0.00002
    # fill_price = 1000 * 1.00002 = 1000.02
    assert fill.fill_price == pytest.approx(1000.02)
    
    trade_value = 1000.02 * 100 # 100002.0
    
    # Brokerage min(20, 100002 * 0.0003) = 20.0
    assert fill.commission == 20.0
    
    # STT: 100002 * 0.0010 = 100.002 -> rounded to 100.0
    assert fill.stt == 100.0
    
    # Stamp Duty: 100002 * 0.00015 = 15.0003
    assert fill.stamp_duty == pytest.approx(15.0003)
    
    # Turnover = 100002 * 0.0000307 (0.00297% NSE + 0.0001% SEBI)
    assert fill.turnover_fee == pytest.approx(100002.0 * 0.0000307)
    
    # GST = (20 + Turnover) * 0.18
    assert fill.gst == pytest.approx((20.0 + (100002.0 * 0.0000307)) * 0.18)
