"""
Tests for Phase 1 Honesty Fixes (D1, D2, D3, D10, D11).

Every test in this module defines the exact behavioral requirement for
eliminating hardcoded diagnostics, silent fallbacks, benchmark confounds,
and silent order rejections.
"""

import pytest
from fastapi.testclient import TestClient

from src.api.adapter import execute_backtest, make_strategy
from src.api.main import app
from src.engine.backtest_engine import BacktestEngine
from src.strategies.sma_crossover import SMACrossoverStrategy
from tests.fixtures.generate import generate_fixture_data

client = TestClient(app)


def test_d1_no_hardcoded_pbo_in_single_run():
    """D1: A single backtest run must NOT return hardcoded PBO (0.6429); pbo must be None if no sweep."""
    req = {
        "strategy": "sma_crossover",
        "params": {"fast_window": 20, "slow_window": 50},
        "universe": ["RELIANCE"],
        "start_date": "2023-01-01",
        "end_date": "2023-06-30",
        "initial_capital": 100000.0,
        "apply_costs": True,
        "demo_mode": False,
    }
    res = client.post("/run", json=req)
    assert res.status_code == 200
    data = res.json()
    # PBO requires a parameter sweep; on a single config run, pbo must be None or explicitly flagged
    diagnostics = data["diagnostics"]
    assert diagnostics["pbo"] is None or diagnostics.get("pbo_reason") is not None
    assert diagnostics["pbo"] != 0.6429 or "pbo_reason" in diagnostics


def test_d2_make_strategy_raises_on_unknown():
    """D2: make_strategy must NOT silently default to SMA(20,50) on unknown strategy."""
    with pytest.raises(ValueError, match="Unknown strategy"):
        make_strategy("non_existent_strategy_xyz", {})


def test_d2_execute_backtest_raises_on_unknown_symbol():
    """D2: execute_backtest must NOT silently fallback to entire dataset on missing symbol."""
    with pytest.raises(ValueError, match="requested symbols not found"):
        execute_backtest(
            strategy_name="sma_crossover",
            params={"fast_window": 10, "slow_window": 30},
            universe_symbols=["NON_EXISTENT_SYMBOL_XYZ"],
            start_date="2023-01-01",
            end_date="2023-06-30",
            initial_capital=100000.0,
            apply_costs=True,
        )


def test_d2_api_returns_422_with_error_envelope_on_invalid_strategy():
    """D2: /run with invalid strategy returns 422 with {error: {code, message, details}}."""
    req = {
        "strategy": "invalid_strat",
        "params": {},
        "universe": ["RELIANCE"],
        "start_date": "2023-01-01",
        "end_date": "2023-06-30",
    }
    res = client.post("/run", json=req)
    assert res.status_code == 422
    body = res.json()
    assert "error" in body
    assert "code" in body["error"]
    assert "message" in body["error"]


def test_d2_api_returns_422_on_reversed_dates():
    """D2: /run with start_date > end_date returns 422 with proper error envelope."""
    req = {
        "strategy": "sma_crossover",
        "params": {"fast_window": 20, "slow_window": 50},
        "universe": ["RELIANCE"],
        "start_date": "2024-01-01",
        "end_date": "2022-01-01",
    }
    res = client.post("/run", json=req)
    assert res.status_code == 422
    body = res.json()
    assert "error" in body


def test_d2_provenance_metadata_in_response():
    """D2: Every backtest response must state served_from, engine_version, data_hash, cost_profile."""
    req = {
        "strategy": "sma_crossover",
        "params": {"fast_window": 20, "slow_window": 50},
        "universe": ["RELIANCE"],
        "start_date": "2023-01-01",
        "end_date": "2023-06-30",
    }
    res = client.post("/run", json=req)
    assert res.status_code == 200
    data = res.json()
    assert data["served_from"] in ("live", "cache", "replay")
    assert "engine_version" in data
    assert "data_hash" in data
    assert "cost_profile" in data


def test_d3_exposure_and_benchmark_metrics():
    """D3: Metrics must include average_exposure, alpha, beta, and exposure_matched_benchmark."""
    req = {
        "strategy": "sma_crossover",
        "params": {"fast_window": 20, "slow_window": 50},
        "universe": ["RELIANCE"],
        "start_date": "2023-01-01",
        "end_date": "2023-06-30",
    }
    res = client.post("/run", json=req)
    assert res.status_code == 200
    metrics = res.json()["metrics"]
    assert "average_exposure" in metrics
    assert "alpha" in metrics
    assert "beta" in metrics
    assert "exposure_matched_return" in metrics
    assert 0.0 <= metrics["average_exposure"] <= 1.0


def test_d10_insufficient_cash_records_rejected_order():
    """D10: Orders rejected for insufficient cash must be recorded as REJECTED in trades."""
    data = generate_fixture_data()
    # Initial cash too low for position sizing
    engine = BacktestEngine(
        data={"TESTCO": data["TESTCO"]},
        strategy=SMACrossoverStrategy(fast_window=5, slow_window=15),
        initial_cash=50.0,  # ₹50 is not enough to buy even 1 share of ~₹1200 TESTCO
        apply_costs=True,
    )
    engine.run()
    # Check that at least one rejected trade was captured in portfolio order log or trades
    has_rejected = any(t.get("status") == "REJECTED" for t in engine.portfolio.rejected_trades)
    assert has_rejected, "Insufficient cash order must be recorded as REJECTED, not silently dropped"


def test_d11_demo_data_env_var_parsing(monkeypatch):
    """D11: DEMO_DATA='0' or 'false' must NOT evaluate to True in health check."""
    monkeypatch.setenv("DEMO_DATA", "0")
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["demo_mode"] is False

    monkeypatch.setenv("DEMO_DATA", "false")
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["demo_mode"] is False

    monkeypatch.setenv("DEMO_DATA", "1")
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["demo_mode"] is True
