import numpy as np
import pandas as pd

from src.data.clean import clean_data


def _raw_frame(n=12, nan_indices=(), dup_index=None):
    dates = pd.date_range("2023-01-01", periods=n)
    base = [100.0 + i for i in range(n)]
    frame = pd.DataFrame(
        {
            "date": list(dates),
            "open": base,
            "high": [v + 1 for v in base],
            "low": [v - 1 for v in base],
            "close": base,
            "volume": [1000] * n,
        }
    )
    for idx in nan_indices:
        frame.loc[idx, "close"] = np.nan
    if dup_index is not None:
        frame = pd.concat([frame, frame.iloc[[dup_index]]], ignore_index=True)
    return frame


def test_clean_drops_missing_ohlc_rows_not_forward_filled():
    df = _raw_frame(nan_indices=(5,))
    cleaned = clean_data(df)

    assert len(cleaned) == 11, "row with missing close must be dropped"
    assert cleaned["close"].isna().sum() == 0


def test_clean_does_not_forward_fill():
    # Forward-filling would silently invent a price and become a lookahead proxy.
    df = _raw_frame(n=6, nan_indices=(3,))
    cleaned = clean_data(df)

    assert len(cleaned) == 5
    assert 103.0 not in cleaned["close"].values, "the dropped day's price must not reappear"


def test_clean_sorts_chronologically():
    df = _raw_frame().sample(frac=1.0, random_state=3)  # shuffle rows
    cleaned = clean_data(df)
    assert cleaned["date"].is_monotonic_increasing


def test_clean_rejects_duplicate_dates():
    df = _raw_frame(dup_index=7)
    cleaned = clean_data(df)
    assert cleaned["date"].is_unique, "duplicate trading days corrupt return calculation"


def test_clean_accepts_empty_frame_without_crashing():
    df = pd.DataFrame(columns=["date", "open", "high", "low", "close", "volume"])
    cleaned = clean_data(df)
    assert cleaned.empty


def test_clean_handles_datetime_string_column():
    df = _raw_frame()
    df["date"] = df["date"].astype(str)
    cleaned = clean_data(df)
    assert pd.api.types.is_datetime64_any_dtype(cleaned["date"])
