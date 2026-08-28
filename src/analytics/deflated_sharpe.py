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
    
    # Calculate Variance of Sharpe Ratio
    n = len(returns)
    var_sr = (1 - sk * observed_sr + ((ku - 1) / 4) * (observed_sr ** 2)) / n
    
    # Expected Max Sharpe
    ems = expected_max_sharpe(N_trials, var_sr)
    
    # Calculate DSR Z-score
    dsr_z = (observed_sr - ems) / np.sqrt(var_sr)
    
    # Return p-value
    return norm.cdf(dsr_z)
