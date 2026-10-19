import numpy as np
import pandas as pd

# This module previously could not be imported in the reproduction environment:
# scipy was imported by src/analytics/deflated_sharpe.py but absent from
# requirements.txt (and from the venv). PRM-VER-004.
from src.analytics.deflated_sharpe import deflated_sharpe_ratio, expected_max_sharpe


def test_expected_max_sharpe_increases_with_trials():
    low = expected_max_sharpe(N_trials=2, variance_sr=0.01)
    high = expected_max_sharpe(N_trials=500, variance_sr=0.01)
    assert high > low, "more trials must inflate the expected maximum Sharpe"


def test_expected_max_sharpe_single_trial_returns_benchmark():
    assert expected_max_sharpe(N_trials=1, variance_sr=0.01, benchmark_sr=0.0) == 0.0


def test_dsr_returns_valid_pvalue_for_noise():
    rng = np.random.default_rng(11)
    returns = pd.Series(rng.normal(0.0, 1.0, 252))
    p = deflated_sharpe_ratio(observed_sr=1.0, returns=returns, N_trials=50)
    assert 0.0 <= p <= 1.0


def test_dsr_punishes_single_trial_less_than_many():
    rng = np.random.default_rng(11)
    returns = pd.Series(rng.normal(0.0, 1.0, 252))

    p_honest = deflated_sharpe_ratio(1.5, returns, N_trials=2)
    p_fished = deflated_sharpe_ratio(1.5, returns, N_trials=2000)

    assert p_fished <= p_honest, "the same Sharpe must look less credible after many trials"


def test_dsr_rejects_insufficient_data():
    rng = np.random.default_rng(3)
    short = pd.Series(rng.normal(0, 1, 2))
    assert np.isnan(deflated_sharpe_ratio(1.0, short, N_trials=10))


def test_dsr_rejects_single_trial():
    returns = pd.Series(np.random.default_rng(3).normal(0, 1, 252))
    assert np.isnan(deflated_sharpe_ratio(1.0, returns, N_trials=1))


def test_dsr_high_true_sharpe_is_credible():
    rng = np.random.default_rng(21)
    returns = pd.Series(rng.normal(0.05, 0.01, 756))  # strong genuine edge
    p = deflated_sharpe_ratio(observed_sr=4.0, returns=returns, N_trials=50)
    assert p > 0.5, f"a genuine edge should survive deflation, got p={p}"
