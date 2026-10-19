from __future__ import annotations

import hashlib
import json
from typing import Any

import numpy as np
import pandas as pd


def compute_run_id(
    strategy: str,
    params: dict[str, Any],
    start: str,
    end: str,
    universe: list[str],
    apply_costs: bool,
    initial_cash: float = 100000.0,
    cost_profile: str = "standard_discount_2024",
    engine_version: str = "1.0.0",
    data_hash: str = "",
) -> str:
    """
    Computes a deterministic SHA-256 hash identifying the exact simulation state.
    Enforces AGENTS.md Rule 7: hash(strategy+params+universe+dates+cost_version+lib_versions).
    """
    payload = json.dumps(
        {
            "strategy": strategy,
            "params": params,
            "period": f"{start}..{end}",
            "initial_cash": float(initial_cash),
            "size": 0.10,
            "cost": str(cost_profile),
            "apply_costs": bool(apply_costs),
            "universe": sorted(universe),
            "engine_version": str(engine_version),
            "data_hash": str(data_hash),
            "lib": {"numpy": np.__version__, "pandas": pd.__version__},
        },
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()[:12]
