from typing import Any

from pydantic import BaseModel, Field


class BacktestRequest(BaseModel):
    strategy: str = Field(default="sma_crossover", description="Strategy identifier: sma_crossover | sma_crossover_10_30 | rsi_mean_reversion | momentum | bh_and_hold")
    params: dict[str, Any] = Field(default_factory=dict, description="Strategy hyperparameters")
    universe: list[str] = Field(default=["RELIANCE.NS"], description="List of stock tickers from NIFTY-10 universe")
    start_date: str = Field(default="2019-01-01", description="Backtest start date (YYYY-MM-DD)")
    end_date: str = Field(default="2024-12-31", description="Backtest end date (YYYY-MM-DD)")
    initial_capital: float = Field(default=100000.0, ge=10000.0, description="Starting cash capital in INR")
    apply_costs: bool = Field(default=True, description="Enable statutory Indian equity delivery cost stack & slippage")
    demo_mode: bool = Field(default=False, description="Force offline replay mode from committed experiment artifacts")


class CostBreakdown(BaseModel):
    brokerage: float = 0.0
    stt: float = 0.0
    stamp_duty: float = 0.0
    turnover_fees: float = 0.0
    gst: float = 0.0
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


class PerformanceMetrics(BaseModel):
    total_return: float
    cagr: float
    sharpe_ratio: float
    sortino_ratio: float
    max_drawdown: float
    calmar_ratio: float


class OverfittingDiagnostics(BaseModel):
    dsr_p_value: float | None = None
    expected_max_sharpe: float | None = None
    pbo: float | None = None
    n_trials: int = 30


class BacktestResponse(BaseModel):
    run_id: str
    strategy: str
    is_cached: bool = False
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


class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    cost_model_version: str
    python_version: str
    numpy_version: str
    pandas_version: str
    demo_mode: bool
