import numpy as np
import pandas as pd
from scipy.stats import norm, skew, kurtosis

def expected_max_sharpe(N_trials: int, variance_sr: float, benchmark_sr: float = 0.0) -> float:
    """
    Approximates the Expected Maximum Sharpe Ratio (E[max(SR)]) across N independent trials
    using the Extreme Value Theory (Euler-Mascheroni constant approach).
    """
    if N_trials <= 1:
        return benchmark_sr
        
    emc = 0.5772156649 # Euler-Mascheroni constant
    Z = (1 - emc) * norm.ppf(1 - 1.0/N_trials) + emc * norm.ppf(1 - 1.0/(N_trials * np.e))
    return benchmark_sr + np.sqrt(variance_sr) * Z

def deflated_sharpe_ratio(observed_sr: float, returns: pd.Series, N_trials: int) -> float:
    """
    Calculates the Deflated Sharpe Ratio (DSR) which is the probabilistic Sharpe Ratio
    adjusted for selection bias (multiple testing).
    Returns the p-value.
    """
    if len(returns) < 3 or N_trials <= 1:
        return np.nan
        
    sk = skew(returns)
    ku = kurtosis(returns, fisher=False) # standard kurtosis (normal=3)
    
    # Calculate Variance of Sharpe Ratio in annualized units
    n = len(returns)
    # Convert annualized Sharpe to daily Sharpe for moment adjustment
    sr_daily = observed_sr / np.sqrt(252.0)
    var_sr_daily = (1.0 - sk * sr_daily + ((ku - 1.0) / 4.0) * (sr_daily ** 2)) / n
    var_sr_annual = var_sr_daily * 252.0
    
    # Expected Max Sharpe in annualized units
    ems_annual = expected_max_sharpe(N_trials, var_sr_annual, benchmark_sr=0.0)
    
    # Calculate DSR Z-score
    dsr_z = (observed_sr - ems_annual) / np.sqrt(var_sr_annual)
    
    # Return p-value
    return float(norm.cdf(dsr_z))
