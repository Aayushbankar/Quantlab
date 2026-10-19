from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from src.engine.events import FillEvent, OrderEvent

if TYPE_CHECKING:
    from datetime import datetime

COST_PROFILES_DIR = Path(__file__).resolve().parent.parent.parent / "cost_profiles"


@dataclass
class CostProfile:
    """Versioned rate card for statutory Indian cash equity delivery costs."""

    profile_id: str
    name: str
    broker: str
    exchange: str
    effective_date: str
    unverified: bool
    source: str
    brokerage_percent: float
    brokerage_cap: float
    brokerage_flat: float
    stt_rate: float
    stamp_duty_rate: float
    exchange_turnover_rate: float
    sebi_turnover_rate: float
    ipft_rate: float
    dp_charge: float
    gst_rate: float
    slippage_floor_bps: float
    notes: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CostProfile:
        return cls(
            profile_id=data.get("profile_id", "custom"),
            name=data.get("name", "Custom Profile"),
            broker=data.get("broker", "Generic"),
            exchange=data.get("exchange", "NSE"),
            effective_date=data.get("effective_date", "2024-10-01"),
            unverified=bool(data.get("unverified", False)),
            source=data.get("source", ""),
            brokerage_percent=float(data.get("brokerage_percent", 0.0003)),
            brokerage_cap=float(data.get("brokerage_cap", 20.0)),
            brokerage_flat=float(data.get("brokerage_flat", 0.0)),
            stt_rate=float(data.get("stt_rate", 0.0010)),
            stamp_duty_rate=float(data.get("stamp_duty_rate", 0.00015)),
            exchange_turnover_rate=float(data.get("exchange_turnover_rate", 0.0000297)),
            sebi_turnover_rate=float(data.get("sebi_turnover_rate", 0.0000010)),
            ipft_rate=float(data.get("ipft_rate", 0.0)),
            dp_charge=float(data.get("dp_charge", 13.50)),
            gst_rate=float(data.get("gst_rate", 0.18)),
            slippage_floor_bps=float(data.get("slippage_floor_bps", 0.0)),
            notes=data.get("notes", ""),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "profile_id": self.profile_id,
            "name": self.name,
            "broker": self.broker,
            "exchange": self.exchange,
            "effective_date": self.effective_date,
            "unverified": self.unverified,
            "source": self.source,
            "brokerage_percent": self.brokerage_percent,
            "brokerage_cap": self.brokerage_cap,
            "brokerage_flat": self.brokerage_flat,
            "stt_rate": self.stt_rate,
            "stamp_duty_rate": self.stamp_duty_rate,
            "exchange_turnover_rate": self.exchange_turnover_rate,
            "sebi_turnover_rate": self.sebi_turnover_rate,
            "ipft_rate": self.ipft_rate,
            "dp_charge": self.dp_charge,
            "gst_rate": self.gst_rate,
            "slippage_floor_bps": self.slippage_floor_bps,
            "notes": self.notes,
        }


_DEFAULT_PROFILE = CostProfile(
    profile_id="standard_discount_2024",
    name="Standard Retail Discount Broker (w.e.f. Oct 2024)",
    broker="Standard Discount",
    exchange="NSE",
    effective_date="2024-10-01",
    unverified=False,
    source="Standard retail broker rate card: min(Rs 20, 0.03%) brokerage, SEBI True-to-label NSE charges",
    brokerage_percent=0.0003,
    brokerage_cap=20.0,
    brokerage_flat=0.0,
    stt_rate=0.0010,
    stamp_duty_rate=0.00015,
    exchange_turnover_rate=0.0000297,
    sebi_turnover_rate=0.0000010,
    ipft_rate=0.0,
    dp_charge=13.50,
    gst_rate=0.18,
    slippage_floor_bps=0.0,
    notes="Baseline retail discount broker model with DP charge on sell.",
)


def load_cost_profile(name_or_path: str | Path | None = None) -> CostProfile:
    """Loads a CostProfile by id, filename, or file path. Falls back to default if None."""
    if name_or_path is None:
        return _DEFAULT_PROFILE

    if isinstance(name_or_path, CostProfile):
        return name_or_path

    path = Path(name_or_path)
    if not path.is_file():
        # Check in COST_PROFILES_DIR
        candidate = COST_PROFILES_DIR / f"{name_or_path}.json"
        if candidate.is_file():
            path = candidate
        else:
            candidate_raw = COST_PROFILES_DIR / str(name_or_path)
            if candidate_raw.is_file():
                path = candidate_raw
            else:
                raise FileNotFoundError(f"Cost profile not found: {name_or_path} in {COST_PROFILES_DIR}")

    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return CostProfile.from_dict(data)


def list_available_profiles() -> list[str]:
    """Returns available cost profile IDs in the cost_profiles directory."""
    if not COST_PROFILES_DIR.is_dir():
        return [_DEFAULT_PROFILE.profile_id]
    return sorted([p.stem for p in COST_PROFILES_DIR.glob("*.json")])


def get_effective_profile(trade_date: str | datetime, broker: str = "zerodha") -> CostProfile:
    """
    Resolves the applicable cost profile based on the trade execution date.
    E.g. Zerodha delivery rates shifted on 2024-10-01 following SEBI True-to-Label circular.
    """
    if isinstance(trade_date, str):
        t_date = trade_date[:10]
    else:
        t_date = trade_date.strftime("%Y-%m-%d")

    broker_lower = broker.lower()
    if "zerodha" in broker_lower:
        if t_date < "2024-10-01":
            try:
                return load_cost_profile("zerodha_delivery_pre_oct2024")
            except FileNotFoundError:
                pass
        try:
            return load_cost_profile("zerodha_delivery_2024")
        except FileNotFoundError:
            pass

    return _DEFAULT_PROFILE


class IndianCostModel:
    """
    Implements statutory Indian equity delivery costs and slippage.
    Enforces SEBI, NSE, CBDT, and State Stamp Duty rules.
    """

    def __init__(
        self,
        apply_costs: bool = True,
        gamma: float = 0.1,
        slippage_floor_bps: float = 0.0,
        profile: CostProfile | str | Path | dict | None = None,
        auto_date_resolution: bool = False,
    ):
        self.apply_costs = apply_costs
        self.gamma = gamma  # Market impact calibration constant
        self.slippage_floor_bps = slippage_floor_bps
        self.auto_date_resolution = auto_date_resolution

        if profile is None:
            self.profile = _DEFAULT_PROFILE
        elif isinstance(profile, CostProfile):
            self.profile = profile
        elif isinstance(profile, dict):
            self.profile = CostProfile.from_dict(profile)
        else:
            self.profile = load_cost_profile(profile)

        # Slippage floor can override or be overridden by profile
        if slippage_floor_bps > 0.0:
            self.slippage_floor_bps = slippage_floor_bps
        else:
            self.slippage_floor_bps = self.profile.slippage_floor_bps

    def process_order(
        self,
        order: OrderEvent,
        raw_price: float,
        volatility: float = 0.02,
        adv: int = 1000000,
    ) -> FillEvent:
        """
        Calculates slippage using Almgren-Chriss Square Root Model (with optional slippage floor)
        and applies statutory Indian cash delivery fees.
        """
        if not self.apply_costs:
            return FillEvent(
                timestamp=order.timestamp,
                symbol=order.symbol,
                side=order.side,
                quantity=order.quantity,
                raw_price=raw_price,
                fill_price=raw_price,
                commission=0.0,
                stt=0.0,
                stamp_duty=0.0,
                gst=0.0,
                turnover_fee=0.0,
                total_cost=0.0,
                dp_charge=0.0,
                sebi_fee=0.0,
                ipft=0.0,
                slippage=0.0,
            )

        # Active cost profile (resolve by trade date if requested)
        profile = self.profile
        if self.auto_date_resolution and order.timestamp is not None:
            profile = get_effective_profile(order.timestamp, broker=self.profile.broker)

        # Almgren-Chriss Square Root Impact Model
        # dP = gamma * sigma * sqrt(Q / V)
        q_v_ratio = order.quantity / max(adv, 1)  # Prevent div by zero
        market_impact_pct = self.gamma * volatility * (q_v_ratio**0.5)

        # Apply slippage floor (spread / market depth floor in basis points)
        floor_pct = self.slippage_floor_bps / 10000.0
        effective_impact_pct = max(market_impact_pct, floor_pct)

        # Cap impact to prevent absurd prices in illiquid edge cases (500 bps = 5%)
        effective_impact_pct = min(effective_impact_pct, 0.05)

        # Apply slippage (worse execution price)
        if order.side == "BUY":
            fill_price = raw_price * (1 + effective_impact_pct)
        else:
            fill_price = raw_price * (1 - effective_impact_pct)

        slippage = abs(fill_price - raw_price)
        trade_value = fill_price * order.quantity

        # 1. Brokerage: min(cap, trade_value * pct) or flat
        if profile.brokerage_cap > 0.0:
            brokerage = min(profile.brokerage_cap, trade_value * profile.brokerage_percent)
        elif profile.brokerage_percent > 0.0:
            brokerage = trade_value * profile.brokerage_percent
        else:
            brokerage = profile.brokerage_flat

        # 2. STT: 0.1% on both Buy & Sell (Delivery) - CBDT Rule 5 round to nearest integer
        stt = float(round(trade_value * profile.stt_rate))

        # 3. Stamp Duty: 0.015% (Buy only)
        stamp_duty = (trade_value * profile.stamp_duty_rate) if order.side == "BUY" else 0.0

        # 4. Exchange Turnover, SEBI Fee & IPFT
        nse_turnover = trade_value * profile.exchange_turnover_rate
        sebi_turnover = trade_value * profile.sebi_turnover_rate
        ipft = trade_value * profile.ipft_rate
        total_turnover = nse_turnover + sebi_turnover + ipft

        # 5. Depository Participant (DP) Charge: Levied only on SELL delivery
        dp_charge = profile.dp_charge if order.side == "SELL" else 0.0

        # 6. GST: 18% on (Brokerage + Turnover charges + DP Charge)
        # Note: STT and Stamp Duty are taxes and strictly exempt from GST.
        taxable_base = brokerage + total_turnover + dp_charge
        gst = taxable_base * profile.gst_rate

        total_cost = brokerage + stt + stamp_duty + total_turnover + dp_charge + gst

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
            total_cost=total_cost,
            dp_charge=dp_charge,
            sebi_fee=sebi_turnover,
            ipft=ipft,
            slippage=slippage,
        )
