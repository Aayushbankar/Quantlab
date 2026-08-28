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
