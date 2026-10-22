"""
Deflated Sharpe Ratio (DSR) and Multiple Testing Overfitting Diagnostics.

References:
    Bailey, D. H., & López de Prado, M. (2014).
    The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality.
    The Journal of Portfolio Management, 40(5), 94-107.
    DOI: 10.3905/jpm.2014.40.5.094

    López de Prado, M. (2018).
    Advances in Financial Machine Learning.
    John Wiley & Sons, Chapter 8.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from scipy.stats import kurtosis, norm, skew

if TYPE_CHECKING:
    import pandas as pd

# Euler-Mascheroni constant
EULER_MASCHERONI = 0.57721566490153286060651209008240243104215933593992


def expected_max_sharpe(N_trials: int, variance_sr: float, benchmark_sr: float = 0.0) -> float:
    """
    Approximates the Expected Maximum Sharpe Ratio (E[max(SR)]) across N independent trials
    under the Null Hypothesis using Extreme Value Theory (EVT).

    Formula (Bailey & López de Prado, 2014, Eq. 8):
        E[max_N] = benchmark_sr + sqrt(variance_sr) * ( (1 - gamma)*Z^{-1}[1 - 1/N] + gamma*Z^{-1}[1 - 1/(N*e)] )
    where gamma is the Euler-Mascheroni constant and Z^{-1} is the inverse Gaussian CDF.
    """
    if N_trials <= 1:
        return float(benchmark_sr)

    if variance_sr < 0.0:
        raise ValueError(f"variance_sr must be non-negative, got {variance_sr}")

    if variance_sr == 0.0:
        return float(benchmark_sr)

    # EVT approximation
    z_term = (1.0 - EULER_MASCHERONI) * norm.ppf(1.0 - 1.0 / N_trials) + EULER_MASCHERONI * norm.ppf(
        1.0 - 1.0 / (N_trials * np.e)
    )
    return float(benchmark_sr + np.sqrt(variance_sr) * z_term)


def deflated_sharpe_ratio_from_moments(
    observed_sr: float,
    n_obs: int,
    skewness: float,
    kurtosis_val: float,
    N_trials: int,
    variance_sr: float,
    benchmark_sr: float = 0.0,
) -> float:
    """
    Calculates Deflated Sharpe Ratio (DSR) directly from sample moments.

    Parameters:
        observed_sr: Annualized Sharpe ratio of the selected strategy.
        n_obs: Number of daily return observations (T).
        skewness: Skewness of the return distribution (gamma_3).
        kurtosis_val: Pearson kurtosis of the return distribution (gamma_4, normal = 3.0).
        N_trials: Number of strategy variations/trials evaluated.
        variance_sr: Cross-trial variance of Sharpe ratios across all N trials.
        benchmark_sr: Benchmark Sharpe ratio under the null hypothesis (default 0.0).

    Returns:
        float: DSR p-value (probability that the observed Sharpe exceeds the expected max).
    """
    if n_obs < 3 or N_trials <= 1:
        return float(np.nan)

    # 1. Variance of the Sharpe ratio estimator with (T - 1) degrees of freedom
    # Mertens (2002) / Lo (2002) / Bailey & López de Prado (2014, Eq. 5)
    sr_daily = observed_sr / np.sqrt(252.0)
    var_sr_daily = (1.0 - skewness * sr_daily + ((kurtosis_val - 1.0) / 4.0) * (sr_daily**2)) / (n_obs - 1)
    var_sr_annual = var_sr_daily * 252.0
    std_sr_annual = np.sqrt(max(1e-12, var_sr_annual))

    # 2. Expected maximum Sharpe ratio across N trials with cross-trial variance
    ems_annual = expected_max_sharpe(N_trials=N_trials, variance_sr=variance_sr, benchmark_sr=benchmark_sr)

    # 3. Deflated Sharpe Ratio Z-statistic and normal CDF
    dsr_z = (observed_sr - ems_annual) / std_sr_annual
    return float(norm.cdf(dsr_z))


def deflated_sharpe_ratio(
    observed_sr: float,
    returns: pd.Series | np.ndarray,
    N_trials: int = 1,
    variance_sr: float | None = None,
    all_sr_estimates: list[float] | np.ndarray | None = None,
    benchmark_sr: float = 0.0,
) -> float:
    """
    Calculates the Deflated Sharpe Ratio (DSR) adjusted for multi-testing selection bias
    and non-normality (skewness and kurtosis).

    Parameters:
        observed_sr: Annualized Sharpe ratio of the selected strategy.
        returns: Daily returns of the strategy.
        N_trials: Number of trials/parameter sets tested.
        variance_sr: Variance of Sharpe ratios across the N trials (cross-trial variance).
        all_sr_estimates: Optional array of Sharpe ratios from all N trials (computes variance_sr).
        benchmark_sr: Benchmark Sharpe ratio (default 0.0).

    Returns:
        float: DSR p-value in [0, 1], or NaN if invalid sample.
    """
    # Resolve N_trials and cross-trial variance if vector of trials provided
    if all_sr_estimates is not None and len(all_sr_estimates) > 1:
        N_trials = len(all_sr_estimates)
        variance_sr = float(np.var(all_sr_estimates, ddof=1))

    if len(returns) < 3 or N_trials <= 1:
        return float(np.nan)

    # Calculate empirical sample moments
    sk = float(skew(returns))
    ku = float(kurtosis(returns, fisher=False))  # Pearson kurtosis (normal = 3.0)
    n = len(returns)

    # If variance_sr not explicitly provided, estimate from strategy estimation variance
    # for backwards compatibility, but document that cross-trial variance is preferred.
    if variance_sr is None:
        sr_daily = observed_sr / np.sqrt(252.0)
        var_sr_daily = (1.0 - sk * sr_daily + ((ku - 1.0) / 4.0) * (sr_daily**2)) / (n - 1)
        variance_sr = var_sr_daily * 252.0

    return deflated_sharpe_ratio_from_moments(
        observed_sr=observed_sr,
        n_obs=n,
        skewness=sk,
        kurtosis_val=ku,
        N_trials=N_trials,
        variance_sr=variance_sr,
        benchmark_sr=benchmark_sr,
    )
