from pathlib import Path

import pandas as pd
import pytest

from src.data.provider import (
    LocalCSVDataProvider,
    SyntheticDataProvider,
    get_data_provider,
    verify_manifest,
)


def test_local_csv_data_provider(fixture_data_dir):
    provider = LocalCSVDataProvider(data_dir=fixture_data_dir)
    symbols = provider.get_available_symbols()
    assert len(symbols) >= 3
    assert "TESTCO" in symbols

    df = provider.get_symbol_data("TESTCO", start_date="2020-01-01", end_date="2021-12-31")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "open" in df.columns
    assert "close" in df.columns
    assert df["date"].min() >= pd.to_datetime("2020-01-01")
    assert df["date"].max() <= pd.to_datetime("2021-12-31")


def test_synthetic_data_provider():
    provider = SyntheticDataProvider(seed=42)
    symbols = provider.get_available_symbols()
    assert "TESTCO" in symbols
    assert "SYNTH" in symbols

    df = provider.get_symbol_data("SYNTH")
    assert len(df) > 1000
    assert (df["high"] >= df["low"]).all()


def test_manifest_checksum_integrity(fixture_data_dir):
    manifest_path = Path("data/manifest.json")
    assert manifest_path.exists(), "data/manifest.json must exist"

    results = verify_manifest(manifest_path=manifest_path, data_dir=fixture_data_dir)
    assert len(results) > 0
    # Every committed fixture file must match its SHA-256 hash exactly
    for fname, is_valid in results.items():
        assert is_valid, f"SHA-256 checksum mismatch for {fname}"


def test_provider_factory():
    local_p = get_data_provider("local")
    assert isinstance(local_p, LocalCSVDataProvider)

    synth_p = get_data_provider("synthetic", seed=123)
    assert isinstance(synth_p, SyntheticDataProvider)

    with pytest.raises(ValueError, match="Unknown data provider type"):
        get_data_provider("unknown_type")
