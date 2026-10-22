from datetime import datetime

import pytest

from src.engine.cost_model import (
    IndianCostModel,
    get_effective_profile,
    list_available_profiles,
    load_cost_profile,
)
from src.engine.events import OrderEvent


def test_indian_cost_model_buy():
    """Baseline test for standard discount broker buy trade."""
    model = IndianCostModel(apply_costs=True, gamma=0.1)

    order = OrderEvent(
        timestamp=datetime(2023, 1, 1),
        symbol="RELIANCE.NS",
        order_type="MKT",
        side="BUY",
        quantity=100,
    )

    raw_price = 1000.0
    fill = model.process_order(order, raw_price, volatility=0.02, adv=1000000)

    # impact_pct = 0.1 * 0.02 * sqrt(100/1000000) = 0.00002
    # fill_price = 1000 * 1.00002 = 1000.02
    assert fill.fill_price == pytest.approx(1000.02)

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
    assert fill.dp_charge == 0.0


def test_zerodha_delivery_buy_golden_master():
    """Golden master test for Zerodha equity delivery buy against published rate card."""
    model = IndianCostModel(apply_costs=True, gamma=0.0, profile="zerodha_delivery_2024")

    # Buy 100 shares of Reliance at Rs 2500.00 -> Trade Value = Rs 2,50,000.00
    order = OrderEvent(
        timestamp=datetime(2024, 10, 15),
        symbol="RELIANCE.NS",
        order_type="MKT",
        side="BUY",
        quantity=100,
    )
    fill = model.process_order(order, raw_price=2500.0, volatility=0.0, adv=1000000)

    assert fill.fill_price == 2500.0
    assert fill.commission == 0.0  # Zerodha delivery is Rs 0 brokerage

    # STT: 0.1% of 250,000 = 250.0 (CBDT Rule 5 nearest integer)
    assert fill.stt == 250.0

    # Stamp duty: 0.015% of 250,000 = 37.50 (BUY only)
    assert fill.stamp_duty == pytest.approx(37.50)

    # NSE turnover: 0.00297% = 7.425
    # SEBI fee: 0.0001% = 0.25
    # IPFT: 0.0001% = 0.25
    # Total turnover charges = 7.925
    assert fill.sebi_fee == pytest.approx(0.25)
    assert fill.ipft == pytest.approx(0.25)
    assert fill.turnover_fee == pytest.approx(7.925)

    # DP charge is 0 on BUY
    assert fill.dp_charge == 0.0

    # GST: 18% of (0 + 7.925 + 0) = 1.4265
    assert fill.gst == pytest.approx(1.4265)

    expected_total = 0.0 + 250.0 + 37.50 + 7.925 + 1.4265
    assert fill.total_cost == pytest.approx(expected_total)


def test_zerodha_delivery_sell_golden_master_with_dp_charge():
    """Golden master test for Zerodha equity delivery sell including CDSL DP charges."""
    model = IndianCostModel(apply_costs=True, gamma=0.0, profile="zerodha_delivery_2024")

    # Sell 100 shares of Reliance at Rs 2600.00 -> Trade Value = Rs 2,60,000.00
    order = OrderEvent(
        timestamp=datetime(2024, 10, 16),
        symbol="RELIANCE.NS",
        order_type="MKT",
        side="SELL",
        quantity=100,
    )
    fill = model.process_order(order, raw_price=2600.0, volatility=0.0, adv=1000000)

    assert fill.commission == 0.0

    # STT: 0.1% on sell = 260.0
    assert fill.stt == 260.0

    # Stamp duty: 0 on SELL
    assert fill.stamp_duty == 0.0

    # NSE turnover: 0.00297% = 7.722, SEBI = 0.26, IPFT = 0.26 -> Total = 8.242
    assert fill.turnover_fee == pytest.approx(8.242)

    # DP charge: Rs 13.50 on sell
    assert fill.dp_charge == 13.50

    # GST: 18% on (Turnover + DP Charge) = 0.18 * (8.242 + 13.50) = 0.18 * 21.742 = 3.91356
    assert fill.gst == pytest.approx(3.91356)

    expected_total = 0.0 + 260.0 + 0.0 + 8.242 + 13.50 + 3.91356
    assert fill.total_cost == pytest.approx(expected_total)


def test_slippage_floor_dominates_small_orders():
    """Verifies that an explicit slippage floor in bps enforces a spread minimum on small retail orders."""
    # 5 bps floor = 0.0005
    model = IndianCostModel(apply_costs=True, gamma=0.1, slippage_floor_bps=5.0)

    # 1 share with huge ADV -> Almgren-Chriss impact is near zero (< 0.000001)
    order = OrderEvent(
        timestamp=datetime(2024, 1, 1),
        symbol="INFY.NS",
        order_type="MKT",
        side="BUY",
        quantity=1,
    )
    fill = model.process_order(order, raw_price=1000.0, volatility=0.01, adv=10000000)

    # Fill price must reflect the 5 bps (0.05%) floor: 1000 * 1.0005 = 1000.50
    assert fill.fill_price == pytest.approx(1000.50)
    assert fill.slippage == pytest.approx(0.50)


def test_effective_profile_date_resolution():
    """Verifies date-based resolution of rate cards across SEBI Oct 2024 True-to-Label boundary."""
    pre_oct_profile = get_effective_profile("2024-05-15", broker="zerodha")
    post_oct_profile = get_effective_profile("2024-10-15", broker="zerodha")

    assert pre_oct_profile.profile_id == "zerodha_delivery_pre_oct2024"
    assert pre_oct_profile.exchange_turnover_rate == 0.0000345

    assert post_oct_profile.profile_id == "zerodha_delivery_2024"
    assert post_oct_profile.exchange_turnover_rate == 0.0000297


def test_unverified_profile_flagging():
    """Verifies that unverified cost profiles are transparently flagged."""
    profile = load_cost_profile("traditional_full_service")
    assert profile.unverified is True
    assert profile.brokerage_percent == 0.0050

    available = list_available_profiles()
    assert "zerodha_delivery_2024" in available
    assert "traditional_full_service" in available
