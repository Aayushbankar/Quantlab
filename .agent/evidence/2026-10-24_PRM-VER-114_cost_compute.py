"""T5: round-trip cost on standard_discount_2024 with the repo's own cost model."""
import sys
from datetime import datetime
sys.path.insert(0, "/mnt/work/projects/Quantlab")
from src.engine.cost_model import IndianCostModel
from src.engine.events import OrderEvent

def mk(side, qty, price):
    return OrderEvent(timestamp=datetime(2024, 10, 15), symbol="RELIANCE",
                      order_type="MKT", side=side, quantity=qty, limit_price=0.0)

model = IndianCostModel(apply_costs=True, profile="standard_discount_2024")
p = model.profile
print("profile_id:", p.profile_id, "| unverified:", p.unverified)

qty, px = 100, 1000.0
V = qty * px
for side in ("BUY", "SELL"):
    fill = model.process_order(mk(side, qty, px), raw_price=px, volatility=0.0, adv=10**9)
    print(f"--- {side} {qty} x {px} = Rs {V:,.2f} ---")
    for k in ["slippage","fill_price","commission","stt","stamp_duty","sebi_fee","turnover_fee","dp_charge","gst","total_cost"]:
        print(f"  {k:14s} = {getattr(fill,k):.4f}")
    if side == "BUY": tb = fill
    else: ts = fill
rt = tb.total_cost + ts.total_cost
print(f"ROUND TRIP = Rs {rt:.4f} = {rt/V*10000:.2f} bps of Rs 1,00,000 notional")
print(f"GST check: buy 0.18*(20+3.07+0)={0.18*(tb.commission+tb.turnover_fee+tb.dp_charge):.4f}; "
      f"sell 0.18*(20+3.07+13.50)={0.18*(ts.commission+ts.turnover_fee+ts.dp_charge):.4f}")
