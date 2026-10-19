from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["cost_model_version"] == "1.0-indian-delivery-2024"
    assert "engine" in data


def test_strategies_catalog():
    res = client.get("/strategies")
    assert res.status_code == 200
    strats = res.json()
    assert len(strats) >= 4
    strat_ids = [s["id"] for s in strats]
    assert "sma_crossover" in strat_ids
    assert "rsi_mean_reversion" in strat_ids
    assert "momentum" in strat_ids
    assert "bh_and_hold" in strat_ids


def test_universe_endpoint():
    res = client.get("/universe")
    assert res.status_code == 200
    data = res.json()
    assert len(data["symbols"]) == 10
    assert data["benchmark"] == "^NSEI"
    assert data["total_bars"] == 1480


def test_replay_endpoint():
    res = client.get("/replay/sma_crossover")
    assert res.status_code == 200
    data = res.json()
    assert data["strategy"] == "sma_crossover"
    assert len(data["net_equity"]) > 100
    assert len(data["gross_equity"]) > 100
    assert data["metrics"]["sharpe_ratio"] > 0.0
    assert data["costs"]["total_friction"] > 0.0


def test_run_backtest_with_caching():
    req = {
        "strategy": "sma_crossover",
        "params": {"fast_window": 20, "slow_window": 50},
        "universe": ["RELIANCE.NS"],
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "initial_capital": 100000.0,
        "apply_costs": True,
        "demo_mode": False
    }
    # First call: executes simulation
    res1 = client.post("/run", json=req)
    assert res1.status_code == 200
    data1 = res1.json()
    assert "run_id" in data1
    assert len(data1["net_equity"]) > 50

    # Second call: served from SQLite cache
    res2 = client.post("/run", json=req)
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["run_id"] == data1["run_id"]
    assert data2["is_cached"] is True
    assert data2["net_equity"] == data1["net_equity"]


def test_api_determinism():
    req = {
        "strategy": "momentum",
        "params": {"lookback_period": 20, "threshold_pct": 0.05},
        "universe": ["TCS.NS"],
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "initial_capital": 100000.0,
        "apply_costs": True,
        "demo_mode": False
    }
    res1 = client.post("/run", json=req).json()
    res2 = client.post("/run", json=req).json()
    assert res1["run_id"] == res2["run_id"]
    assert res1["metrics"] == res2["metrics"]
