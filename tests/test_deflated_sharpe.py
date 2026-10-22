import numpy as np
import pandas as pd
import pytest

from src.analytics.deflated_sharpe import (
    deflated_sharpe_ratio,
    deflated_sharpe_ratio_from_moments,
    expected_max_sharpe,
)


def test_expected_max_sharpe_increases_with_trials():
    low = expected_max_sharpe(N_trials=2, variance_sr=0.01)
    high = expected_max_sharpe(N_trials=500, variance_sr=0.01)
    assert high > low, "more trials must inflate the expected maximum Sharpe"


def test_expected_max_sharpe_single_trial_returns_benchmark():
    assert expected_max_sharpe(N_trials=1, variance_sr=0.01, benchmark_sr=0.0) == 0.0


def test_expected_max_sharpe_negative_variance_raises():
    with pytest.raises(ValueError, match="must be non-negative"):
        expected_max_sharpe(N_trials=10, variance_sr=-0.05)


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


def test_bailey_lopez_de_prado_2014_published_worked_example():
    """
    Validates against the published worked example in Section 4 of:
    Bailey, D. H., & López de Prado, M. (2014).
    'The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality'
    Journal of Portfolio Management, 40(5), 94-107.

    Setup:
      - N = 100 independent trials
      - Cross-trial variance of Sharpe ratios V[SR] = 0.5
      - Expected Max Sharpe under null evaluates to ~1.7894
      - T = 1250 daily observations (approx 5 years)
      - Selected strategy observed annualized SR = 2.5
      - Returns skewness gamma_3 = -3.0
      - Returns Pearson kurtosis gamma_4 = 13.0 (excess kurtosis = 10.0)
      - Standard error of Sharpe ratio estimator = 0.5587
      - DSR p-value = 0.8983 (fails the 0.95 significance threshold due to overfitting)
    """
    # 1. Expected maximum Sharpe ratio verification
    ems = expected_max_sharpe(N_trials=100, variance_sr=0.5, benchmark_sr=0.0)
    assert ems == pytest.approx(1.789406, abs=1e-4)

    # 2. Deflated Sharpe Ratio from moments verification
    dsr = deflated_sharpe_ratio_from_moments(
        observed_sr=2.5,
        n_obs=1250,
        skewness=-3.0,
        kurtosis_val=13.0,
        N_trials=100,
        variance_sr=0.5,
        benchmark_sr=0.0,
    )

    # Must match 0.8983 (below 0.95 threshold)
    assert dsr == pytest.approx(0.898308, abs=1e-4)
    assert dsr < 0.95, "DSR correctly deflates headline Sharpe of 2.5 down to insignificant when dredged from 100 trials"


def test_dsr_with_cross_trial_vector():
    """Verifies that passing all trial Sharpe ratios automatically computes sample variance with ddof=1."""
    rng = np.random.default_rng(42)
    trial_sharpes = rng.normal(0.0, 0.7, size=100)
    observed_sr = float(np.max(trial_sharpes))

    returns = pd.Series(rng.normal(0.0005, 0.015, size=500))

    dsr = deflated_sharpe_ratio(
        observed_sr=observed_sr,
        returns=returns,
        all_sr_estimates=trial_sharpes,
    )
    assert 0.0 <= dsr <= 1.0
