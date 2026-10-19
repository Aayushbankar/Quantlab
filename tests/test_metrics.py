import pytest
import pandas as pd
from src.analytics.metrics import MetricsEngine

def test_metrics_engine():
    # Construct a simple equity curve
    equity_history = pd.DataFrame({
        "date": pd.date_range("2023-01-01", periods=504), # 2 years
        "cash": [100.0] * 504,
        "total_equity": [100.0 * (1.001 ** i) for i in range(504)] # ~ 25% annual return
    })
    
    engine = MetricsEngine(equity_history, risk_free_rate=0.0)
    metrics = engine.compute_all()
    
    assert metrics["Total Return"] > 0
    assert metrics["CAGR"] > 0.20
    assert metrics["Max Drawdown"] == 0.0 # It only went up
    assert metrics["Sharpe Ratio"] > 0
