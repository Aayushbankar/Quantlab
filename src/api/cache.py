import json
import hashlib
import numpy as np
import pandas as pd


def compute_run_id(
    strategy: str,
    params: dict,
    start: str,
    end: str,
    universe: list,
    apply_costs: bool,
    initial_cash: float = 100000.0,
) -> str:
    """
    Computes a deterministic SHA-256 hash identifying the exact simulation state.
    Matches the specification in scripts/run_experiments.py and AGENTS.md Rule 7.
    """
    payload = json.dumps({
        "strategy": strategy,
        "params": params,
        "period": f"{start}..{end}",
        "initial_cash": float(initial_cash),
        "size": 0.10,
        "cost": "1.0-indian-delivery-2024",
        "apply_costs": bool(apply_costs),
        "universe": sorted(universe),
        "lib": {"numpy": np.__version__, "pandas": pd.__version__}
    }, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()[:12]
