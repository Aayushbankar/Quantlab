import re
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

SYMBOL_REGEX = re.compile(r"^[A-Za-z0-9_\-\.]{1,30}$")

StrategyType = Literal[
    "sma_crossover",
    "sma_crossover_10_30",
    "rsi_mean_reversion",
    "momentum",
    "bollinger_breakout",
    "bh_and_hold",
    "buy_and_hold",
]


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Any = None


class ErrorResponse(BaseModel):
    error: ErrorDetail


class BacktestRequest(BaseModel):
    strategy: StrategyType = Field(
        default="sma_crossover",
        description="Strategy identifier: sma_crossover | sma_crossover_10_30 | rsi_mean_reversion | momentum | bollinger_breakout | bh_and_hold",
    )
    params: dict[str, Any] = Field(default_factory=dict, description="Strategy hyperparameters")
    universe: list[str] = Field(default=["RELIANCE.NS"], description="List of stock tickers from NIFTY-10 universe")
    start_date: str = Field(default="2019-01-01", description="Backtest start date (YYYY-MM-DD)")
    end_date: str = Field(default="2024-12-31", description="Backtest end date (YYYY-MM-DD)")
    initial_capital: float = Field(
        default=100000.0, ge=10000.0, le=100000000.0, description="Starting cash capital in INR"
    )
    apply_costs: bool = Field(default=True, description="Enable statutory Indian equity delivery cost stack & slippage")
    cost_profile: str = Field(default="standard_discount_2024", description="Cost profile ID: standard_discount_2024 | zerodha_delivery_2024 | zerodha_delivery_pre_oct2024")
    slippage_floor_bps: float = Field(default=0.0, ge=0.0, le=100.0, description="Minimum slippage/spread floor in basis points")
    demo_mode: bool = Field(default=False, description="Force offline replay mode from committed experiment artifacts")

    @model_validator(mode="after")
    def validate_request_bounds(self) -> "BacktestRequest":
        if self.start_date >= self.end_date:
            raise ValueError(f"start_date ({self.start_date}) must be strictly before end_date ({self.end_date}).")

        if not self.universe:
            raise ValueError("Universe cannot be empty; specify at least one equity symbol.")

        for sym in self.universe:
            if not SYMBOL_REGEX.match(sym):
                raise ValueError(
                    f"Invalid symbol '{sym}'. Symbols must be 1-20 alphanumeric characters (e.g. RELIANCE, TCS.NS)."
                )

        return self


class CostBreakdown(BaseModel):
    brokerage: float = 0.0
    stt: float = 0.0
    stamp_duty: float = 0.0
    turnover_fees: float = 0.0
    gst: float = 0.0
    dp_charges: float = 0.0
    sebi_fees: float = 0.0
    ipft: float = 0.0
    market_impact: float = 0.0
    total_friction: float = 0.0
    friction_drag_pct: float = 0.0


class TradeRecord(BaseModel):
    timestamp: str
    symbol: str
    side: str
    quantity: int
    raw_price: float
    fill_price: float
    total_cost: float
    status: str = "FILLED"
    reason: str | None = None


class PerformanceMetrics(BaseModel):
    total_return: float
    cagr: float
    sharpe_ratio: float
    sortino_ratio: float
    max_drawdown: float
    calmar_ratio: float
    average_exposure: float = 0.0
    alpha: float = 0.0
    beta: float = 0.0
    exposure_matched_return: float = 0.0


class OverfittingDiagnostics(BaseModel):
    dsr_p_value: float | None = None
    expected_max_sharpe: float | None = None
    pbo: float | None = None
    pbo_reason: str | None = None
    n_trials: int = 1


class BacktestResponse(BaseModel):
    run_id: str
    strategy: str
    is_cached: bool = False
    served_from: str = "live"  # "live" | "cache" | "replay"
    replay_reason: str | None = None
    engine_version: str = "1.0.0"
    data_hash: str = ""
    cost_profile: str = "1.0-indian-delivery-2024"
    execution_time_ms: float
    dates: list[str]
    gross_equity: list[float]
    net_equity: list[float]
    metrics: PerformanceMetrics
    costs: CostBreakdown
    trades: list[TradeRecord]
    diagnostics: OverfittingDiagnostics


class StrategyMetadata(BaseModel):
    id: str
    name: str
    description: str
    default_params: dict[str, Any]
    param_ranges: dict[str, Any]


class UniverseResponse(BaseModel):
    symbols: list[str]
    benchmark: str
    default_start: str
    default_end: str
    total_bars: int
    survivorship_bias_warning: str | None = None


class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    cost_model_version: str
    python_version: str
    numpy_version: str
    pandas_version: str
    demo_mode: bool


class TrialRecord(BaseModel):
    trial_id: int
    strategy: str
    params: dict[str, Any]
    universe: list[str]
    start_date: str
    end_date: str
    sharpe: float
    total_return: float
    max_drawdown: float
    run_id: str | None = None
    created_at: str


class TrialsResponse(BaseModel):
    total_trials: int
    trials: list[TrialRecord]
    cross_trial_variance: float


class SweepSummaryResponse(BaseModel):
    n_configs_evaluated: int
    universe_symbols: list[str]
    cross_trial_variance: float
    mean_sharpe: float
    std_sharpe: float
    max_sharpe: float
    min_sharpe: float
    pbo: float | None = None
    pbo_ci_lower_95: float | None = None
    pbo_ci_upper_95: float | None = None
    cpcv_paths: int = 0
    cpcv_overfit_paths: int = 0
    best_config: dict[str, Any] | None = None
