import pytest
from datetime import datetime
from src.engine.portfolio import Portfolio
from src.engine.events import FillEvent

def test_portfolio_cash_flow():
    portfolio = Portfolio(initial_cash=100000.0)
    
    fill = FillEvent(
        timestamp=datetime(2023, 1, 1),
        symbol="TCS.NS",
        side="BUY",
        quantity=10,
        raw_price=3000.0,
        fill_price=3000.0,
        commission=20.0,
        stt=30.0,
        stamp_duty=0.0,
        gst=0.0,
        turnover_fee=0.0,
        total_cost=50.0
    )
    
    portfolio.apply_fill(fill)
    
    # Cash should be 100000 - (10 * 3000) - 50 = 69950.0
    assert portfolio.cash == 69950.0
    
    pos = portfolio.positions["TCS.NS"]
    assert pos.quantity == 10
    assert pos.average_entry_price == 3000.0
