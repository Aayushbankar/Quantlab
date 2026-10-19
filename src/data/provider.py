"""Data provider abstraction for Pramaan.

Supports local CSV / Parquet repositories, synthetic fixture generation, and
optional Yahoo Finance network retrieval.
"""

import hashlib
import json
import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import pandas as pd

from src.data.clean import clean_data

logger = logging.getLogger(__name__)


class DataProvider(ABC):
    """Abstract interface for retrieving market historical data."""

    @abstractmethod
    def get_symbol_data(
        self, symbol: str, start_date: str | None = None, end_date: str | None = None
    ) -> pd.DataFrame:
        """Fetch cleaned OHLCV DataFrame for a single symbol."""
        pass

    @abstractmethod
    def get_universe_data(
        self, symbols: list[str], start_date: str | None = None, end_date: str | None = None
    ) -> dict[str, pd.DataFrame]:
        """Fetch cleaned OHLCV DataFrames for a list of symbols."""
        pass

    @abstractmethod
    def get_available_symbols(self) -> list[str]:
        """List symbols currently available in the provider's store."""
        pass


class LocalCSVDataProvider(DataProvider):
    """Loads and cleans daily equity data from local CSV storage."""

    def __init__(self, data_dir: str | Path):
        self.data_dir = Path(data_dir)

    def get_available_symbols(self) -> list[str]:
        if not self.data_dir.exists():
            return []
        symbols = []
        for p in self.data_dir.glob("*.csv"):
            if not p.name.startswith("replay_"):
                symbols.append(p.stem)
        return sorted(symbols)

    def get_symbol_data(
        self, symbol: str, start_date: str | None = None, end_date: str | None = None
    ) -> pd.DataFrame:
        clean_sym = symbol.replace(".NS", "").strip()
        candidates = [
            self.data_dir / f"{clean_sym}.csv",
            self.data_dir / f"{clean_sym}.NS.csv",
        ]
        file_path = None
        for cand in candidates:
            if cand.exists():
                file_path = cand
                break

        if not file_path:
            raise FileNotFoundError(f"Symbol {symbol} not found in {self.data_dir}")

        df = pd.read_csv(file_path)
        cleaned = clean_data(df)

        if start_date:
            cleaned = cleaned[cleaned["date"] >= pd.to_datetime(start_date)]
        if end_date:
            cleaned = cleaned[cleaned["date"] <= pd.to_datetime(end_date)]

        return cleaned.reset_index(drop=True)

    def get_universe_data(
        self, symbols: list[str], start_date: str | None = None, end_date: str | None = None
    ) -> dict[str, pd.DataFrame]:
        result = {}
        for sym in symbols:
            try:
                result[sym] = self.get_symbol_data(sym, start_date, end_date)
            except FileNotFoundError:
                logger.warning(f"Could not load symbol {sym} from {self.data_dir}")
        return result


class SyntheticDataProvider(DataProvider):
    """Generates synthetic fixture data deterministically in-memory."""

    def __init__(self, seed: int = 42):
        from tests.fixtures.generate import generate_fixture_data

        self.seed = seed
        self._cache = generate_fixture_data(seed=seed)

    def get_available_symbols(self) -> list[str]:
        return sorted(list(self._cache.keys()))

    def get_symbol_data(
        self, symbol: str, start_date: str | None = None, end_date: str | None = None
    ) -> pd.DataFrame:
        clean_sym = symbol.replace(".NS", "").strip()
        if clean_sym not in self._cache:
            raise KeyError(f"Symbol {symbol} not in synthetic universe {self.get_available_symbols()}")
        df = self._cache[clean_sym].copy()
        if start_date:
            df = df[df["date"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["date"] <= pd.to_datetime(end_date)]
        return df.reset_index(drop=True)

    def get_universe_data(
        self, symbols: list[str], start_date: str | None = None, end_date: str | None = None
    ) -> dict[str, pd.DataFrame]:
        result = {}
        for sym in symbols:
            result[sym] = self.get_symbol_data(sym, start_date, end_date)
        return result


class YahooDataProvider(DataProvider):
    """Fetches real-time / historical data from Yahoo Finance via yfinance."""

    def __init__(self, cache_dir: str | Path | None = None):
        self.cache_dir = Path(cache_dir) if cache_dir else None
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_available_symbols(self) -> list[str]:
        if self.cache_dir and self.cache_dir.exists():
            return sorted([p.stem for p in self.cache_dir.glob("*.csv")])
        return []

    def get_symbol_data(
        self, symbol: str, start_date: str | None = None, end_date: str | None = None
    ) -> pd.DataFrame:
        from src.data.fetch import fetch_stock_data

        # Check local cache first
        clean_sym = symbol.replace(".NS", "").strip()
        if self.cache_dir:
            cache_file = self.cache_dir / f"{clean_sym}.csv"
            if cache_file.exists():
                df = pd.read_csv(cache_file)
                cleaned = clean_data(df)
                if start_date:
                    cleaned = cleaned[cleaned["date"] >= pd.to_datetime(start_date)]
                if end_date:
                    cleaned = cleaned[cleaned["date"] <= pd.to_datetime(end_date)]
                return cleaned.reset_index(drop=True)

        s_date = start_date or "2019-01-01"
        e_date = end_date or "2024-12-31"
        df = fetch_stock_data(symbol if symbol.endswith(".NS") else f"{symbol}.NS", s_date, e_date)
        if df is None or df.empty:
            raise RuntimeError(f"Yahoo Finance returned no data for symbol {symbol}")
        cleaned = clean_data(df)
        if self.cache_dir:
            cleaned.to_csv(self.cache_dir / f"{clean_sym}.csv", index=False)
        return cleaned

    def get_universe_data(
        self, symbols: list[str], start_date: str | None = None, end_date: str | None = None
    ) -> dict[str, pd.DataFrame]:
        result = {}
        for sym in symbols:
            result[sym] = self.get_symbol_data(sym, start_date, end_date)
        return result


def verify_manifest(
    manifest_path: str | Path = "data/manifest.json", data_dir: str | Path = "tests/fixtures/data"
) -> dict[str, bool]:
    """Verifies that committed fixture data matches the SHA-256 hashes recorded in the manifest."""
    manifest_p = Path(manifest_path)
    data_p = Path(data_dir)
    if not manifest_p.exists():
        raise FileNotFoundError(f"Manifest not found at {manifest_p}")

    with open(manifest_p) as f:
        manifest: dict[str, Any] = json.load(f)

    results = {}
    for fname, meta in manifest.get("files", {}).items():
        file_path = data_p / fname
        if not file_path.exists():
            results[fname] = False
            continue
        with open(file_path, "rb") as f:
            computed_sha = hashlib.sha256(f.read()).hexdigest()
        results[fname] = computed_sha == meta["sha256"]

    return results


def get_data_provider(provider_type: str = "local", **kwargs) -> DataProvider:
    """Factory creating the appropriate DataProvider."""
    if provider_type == "local":
        data_dir = kwargs.get("data_dir", "data/raw" if os.path.exists("data/raw") else "tests/fixtures/data")
        return LocalCSVDataProvider(data_dir=data_dir)
    elif provider_type == "synthetic":
        return SyntheticDataProvider(seed=kwargs.get("seed", 42))
    elif provider_type == "yahoo":
        return YahooDataProvider(cache_dir=kwargs.get("cache_dir", "data/raw"))
    else:
        raise ValueError(f"Unknown data provider type: {provider_type}")
