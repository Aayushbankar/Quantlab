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
    assert data["total_bars"] >= 1000


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
        "demo_mode": False,
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
        "demo_mode": False,
    }
    res1 = client.post("/run", json=req).json()
    res2 = client.post("/run", json=req).json()
    assert res1["run_id"] == res2["run_id"]
    assert res1["metrics"] == res2["metrics"]


def test_ready_endpoint():
    res = client.get("/ready")
    assert res.status_code == 200
    assert res.json()["status"] == "ready"


def test_trials_endpoint():
    res = client.get("/trials")
    assert res.status_code == 200
    data = res.json()
    assert "total_trials" in data
    assert "trials" in data
    assert "cross_trial_variance" in data
    assert data["total_trials"] >= 1


def test_sweep_summary_endpoint():
    res = client.get("/sweep")
    assert res.status_code == 200
    data = res.json()
    assert data["n_configs_evaluated"] >= 100
    assert "pbo" in data
    assert 0.0 <= data["pbo"] <= 1.0
    assert data["pbo_ci_lower_95"] <= data["pbo"] <= data["pbo_ci_upper_95"]


def test_universe_survivorship_warning():
    res = client.get("/universe")
    assert res.status_code == 200
    data = res.json()
    assert data["total_bars"] > 500
    assert "survivorship_bias_warning" in data
    assert "SURVIVORSHIP BIAS WARNING" in data["survivorship_bias_warning"]


def test_async_jobs_workflow():
    req = {
        "strategy": "sma_crossover",
        "params": {"fast_window": 10, "slow_window": 30},
        "universe": ["RELIANCE.NS"],
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "initial_capital": 100000.0,
        "apply_costs": True,
    }
    # 1. Submit job
    res = client.post("/jobs", json=req)
    assert res.status_code == 200
    job_id = res.json()["job_id"]
    assert job_id.startswith("job_")

    # 2. Poll job status
    import time
    for _ in range(30):
        time.sleep(0.2)
        poll_res = client.get(f"/jobs/{job_id}")
        assert poll_res.status_code == 200
        poll_data = poll_res.json()
        if poll_data["status"] in ("completed", "failed"):
            break

    assert poll_data["status"] == "completed"
    assert poll_data["result"] is not None
    assert "metrics" in poll_data["result"]


def test_honesty_report_html_generation():
    # First ensure a run exists in cache
    req = {
        "strategy": "sma_crossover",
        "params": {"fast_window": 20, "slow_window": 50},
        "universe": ["RELIANCE.NS"],
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "initial_capital": 100000.0,
        "apply_costs": True,
    }
    run_res = client.post("/run", json=req)
    assert run_res.status_code == 200
    run_id = run_res.json()["run_id"]

    # Request HTML honesty report
    rep_res = client.get(f"/report/{run_id}")
    assert rep_res.status_code == 200
    assert "text/html" in rep_res.headers["content-type"]
    html = rep_res.text
    assert "Pramaan Honesty Report" in html
    assert run_id in html
    assert "Statutory Friction Tollgate Waterfall" in html
    assert "Academic &amp; Regulatory Disclaimer" in html


def test_frontend_workstation_serving():
    res_root = client.get("/")
    assert res_root.status_code == 200
    assert "text/html" in res_root.headers["content-type"]
    assert "Pramaan" in res_root.text

    res_landing = client.get("/landing")
    assert res_landing.status_code == 200
    assert "text/html" in res_landing.headers["content-type"]

    res_app = client.get("/app")
    assert res_app.status_code == 200
    assert "text/html" in res_app.headers["content-type"]

