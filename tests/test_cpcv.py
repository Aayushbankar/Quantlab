import pytest
import numpy as np
import pandas as pd
from src.analytics.cpcv import CPCV

def test_calculate_pbo_random_returns():
    np.random.seed(42)
    # 1000 days, 50 random strategies
    returns_data = {f"strat_{i}": np.random.normal(0, 1, 1000) for i in range(50)}
    df = pd.DataFrame(returns_data)
    
    # 10 splits, 2 test splits (45 paths)
    cpcv = CPCV(n_splits=10, n_test_splits=2)
    pbo = cpcv.calculate_pbo(df)
    
    # Pure random strategies should yield a PBO around 0.5 (50%)
    assert 0.4 <= pbo <= 0.6, f"Expected PBO ~0.5 for random data, got {pbo}"

def test_calculate_pbo_real_signal():
    np.random.seed(42)
    # 1000 days, 50 random strategies
    returns_data = {f"strat_{i}": np.random.normal(0, 1, 1000) for i in range(50)}
    
    # Introduce a strategy with genuine persistent signal (higher mean)
    returns_data["genuine_strat"] = np.random.normal(0.5, 1, 1000)
    
    df = pd.DataFrame(returns_data)
    
    cpcv = CPCV(n_splits=10, n_test_splits=2)
    pbo = cpcv.calculate_pbo(df)
    
    # Genuine strategy should consistently be chosen IS and perform well OOS, PBO should be very low
    assert pbo < 0.1, f"Expected low PBO for genuine signal, got {pbo}"

def test_cpcv_embargo_ar1():
    np.random.seed(42)
    # Generate strongly autocorrelated returns (AR(1) process)
    n = 1000
    phi = 0.95
    returns = np.zeros((n, 20))
    for i in range(20):
        eps = np.random.normal(0, 1, n)
        for t in range(1, n):
            returns[t, i] = phi * returns[t-1, i] + eps[t]
            
    df = pd.DataFrame(returns, columns=[f"strat_{i}" for i in range(20)])
    
    # Run with NO embargo
    cpcv_no_embargo = CPCV(n_splits=10, n_test_splits=2, embargo_pct=0.0)
    pbo_no_embargo = cpcv_no_embargo.calculate_pbo(df)
    
    # Run WITH embargo
    cpcv_embargo = CPCV(n_splits=10, n_test_splits=2, embargo_pct=0.05)
    pbo_embargo = cpcv_embargo.calculate_pbo(df)
    
    # With highly autocorrelated returns, lack of embargo causes OOS performance
    # to be artificially predictable from adjacent IS performance, lowering PBO artificially.
    # Proper embargo breaks this leakage, so PBO should be higher with embargo.
    assert pbo_embargo > pbo_no_embargo, f"Embargo did not increase PBO: {pbo_no_embargo} vs {pbo_embargo}"
