import pytest
import pandas as pd
from src.analytics.cpcv import CPCV

def test_calculate_pbo_raises_not_implemented():
    cpcv = CPCV(n_splits=3, n_test_splits=1)
    df = pd.DataFrame()
    with pytest.raises(NotImplementedError, match="PBO calculation is not yet implemented"):
        cpcv.calculate_pbo(df)
