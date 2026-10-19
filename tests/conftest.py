"""
Pramaan test configuration and shared fixtures.

Deterministic synthetic fixtures enable clean-clone offline test execution
without external network access or dependency on gitignored raw market data.
"""

from pathlib import Path

import pandas as pd
import pytest

from tests.fixtures.generate import FIXTURE_DATA_DIR, generate_fixture_data


@pytest.fixture(scope="session")
def fixture_data_dir() -> Path:
    """Path to the directory containing committed synthetic fixture CSVs."""
    return FIXTURE_DATA_DIR


@pytest.fixture(scope="session")
def synthetic_data() -> dict[str, pd.DataFrame]:
    """In-memory dictionary of synthetic OHLCV DataFrames ready for engine execution."""
    return generate_fixture_data()


@pytest.fixture(autouse=True)
def ensure_offline_safe_data_dir(monkeypatch):
    """
    Ensure tests never touch external network or fail when data/raw is missing.
    If data/raw has no CSVs, redirects adapter.RAW_DATA_DIR to tests/fixtures/data.
    """
    raw_dir = Path("data/raw")
    has_csvs = raw_dir.exists() and any(raw_dir.glob("*.csv"))
    if not has_csvs:
        monkeypatch.setattr("src.api.adapter.RAW_DATA_DIR", str(FIXTURE_DATA_DIR))
