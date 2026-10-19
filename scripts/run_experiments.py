"""
Real-data experiment matrix for Pramaan.

Produces the ONE artifact that every results claim now depends on:
    experiments/experiment_log.csv   -- the reproducible run matrix
    experiments/oos_decay.csv        -- in-sample vs out-of-sample decay
    experiments/equity_curves/*.csv  -- raw engine output, for chart regeneration
    experiments/data_manifest.csv    -- what was actually fetched

Every number reported in the README, report and slides must trace back to a
row in experiment_log.csv, with the parameters recorded in the same row.
"""

import os
import json
import hashlib
import time
import sys

import numpy as np
import pandas as pd
import yfinance as yf

from src.data.universe import get_universe
from src.data.clean import clean_data
from src.engine.backtest_engine import BacktestEngine
from src.engine.cost_model import IndianCostModel
from src.analytics.metrics import MetricsEngine

GAMMA = IndianCostModel().gamma
COST_MODEL_VERSION = "1.0-indian-delivery-2024"
INITIAL_CAPITAL = 100000.0
SIZE_FRACTION = 0.10

STRATEGIES = {
    "sma_crossover":          {"fast_window": 20, "slow_window": 50},
    "sma_crossover_10_30":    {"fast_window": 10, "slow_window": 30},
    "rsi_mean_reversion":     {"period": 14, "oversold": 30, "overbought": 70},
    "momentum":               {"lookback_period": 20, "threshold_pct": 0.05},
    "bh_and_hold":            {},
}

PERIODS = {
    "full":  ("2019-01-01", "2024-12-31"),
    "IS":    ("2019-01-01", "2022-12-31"),
    "OOS":   ("2023-01-01", "2024-12-31"),
}

OUT_DIR = "experiments"
CURVE_DIR = os.path.join(OUT_DIR, "equity_curves")


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def make_strategy(name, kwargs):
    if name.startswith("sma_crossover"):
        from src.strategies.sma_crossover import SMACrossoverStrategy
        return SMACrossoverStrategy(**kwargs)
    if name == "rsi_mean_reversion":
        from src.strategies.rsi_mean_reversion import RSIMeanReversionStrategy
        return RSIMeanReversionStrategy(**kwargs)
    if name == "momentum":
        from src.strategies.momentum import MomentumStrategy
        return MomentumStrategy(**kwargs)
    if name == "bh_and_hold":
        from src.strategies.bh_and_hold import BuyAndHoldStrategy
        return BuyAndHoldStrategy()
    raise ValueError(f"unknown strategy {name}")


def fetch_universe(start, end):
    symbols = get_universe()
    data = {}
    for sym in symbols:
        raw = yf.Ticker(sym).history(start=start, end=end)
        if raw is None or len(raw) == 0:
            log(f"  !! no data for {sym}")
            continue
        raw = raw.reset_index()
        raw["Date"] = pd.to_datetime(raw["Date"]).dt.tz_localize(None)
        raw = raw[["Date", "Open", "High", "Low", "Close", "Volume"]]
        raw.columns = ["date", "open", "high", "low", "close", "volume"]
        raw["symbol"] = sym
        data[sym] = clean_data(raw)
    return data


def slice_period(data, start, end):
    out = {}
    for sym, df in data.items():
        mask = (df["date"] >= pd.Timestamp(start)) & (df["date"] <= pd.Timestamp(end))
        if mask.any():
            out[sym] = df.loc[mask].reset_index(drop=True)
    return out


def run_id_for(strategy_name, kwargs, period, apply_costs):
    payload = json.dumps(
        {
            "strategy": strategy_name,
            "params": kwargs,
            "period": period,
            "initial_cash": INITIAL_CAPITAL,
            "size": SIZE_FRACTION,
            "cost": COST_MODEL_VERSION,
            "apply_costs": bool(apply_costs),
            "universe": get_universe(),
            "lib": {"numpy": np.__version__, "pandas": pd.__version__},
        },
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()[:12]


def main():
    os.makedirs(CURVE_DIR, exist_ok=True)

    start_date, end_date = PERIODS["full"]
    log(f"Fetching {len(get_universe())} NSE symbols {start_date} -> {end_date}")
    data = fetch_universe(start_date, end_date)
    if not data:
        log("ERROR: no data fetched — cannot produce the matrix")
        sys.exit(1)

    manifest = pd.DataFrame([
        {"symbol": s, "rows": len(d), "first": d["date"].min().date(), "last": d["date"].max().date()}
        for s, d in data.items()
    ])
    manifest.to_csv(os.path.join(OUT_DIR, "data_manifest.csv"), index=False)
    log(f"Fetched {len(data)} symbols; bars per symbol: "
        f"{manifest['rows'].min()}–{manifest['rows'].max()}")

    # Total portfolio PnL across the full run, for PBO
    strategy_returns = {}
    rows = []

    for name, kwargs in STRATEGIES.items():
        for period_name, (p_start, p_end) in PERIODS.items():
            pdata = slice_period(data, p_start, p_end)
            if not pdata:
                continue

            for apply_costs in (True, False):
                # bh_and_hold is the control case: costs always ON, never patched
                settings = [True] if name == "bh_and_hold" else [apply_costs]
                for costs_on in settings:
                    t0 = time.time()
                    strategy = make_strategy(name, kwargs)
                    engine = BacktestEngine(
                        pdata, strategy,
                        initial_cash=INITIAL_CAPITAL,
                        apply_costs=costs_on,
                    )
                    equity = engine.run()
                    elapsed = time.time() - t0

                    metrics = MetricsEngine(equity).compute_all()
                    trades = len(engine.portfolio.positions)

                    rid = run_id_for(name, kwargs, period_name, costs_on)
                    rows.append({
                        "run_id": rid,
                        "strategy": name,
                        "params": json.dumps(kwargs, sort_keys=True),
                        "universe": "10 NSE equities",
                        "period": period_name,
                        "date_range": f"{p_start}..{p_end}",
                        "apply_costs": costs_on,
                        "initial_capital": INITIAL_CAPITAL,
                        "total_return": metrics.get("Total Return", np.nan),
                        "cagr": metrics.get("CAGR", np.nan),
                        "sharpe": metrics.get("Sharpe Ratio", np.nan),
                        "sortino": metrics.get("Sortino Ratio", np.nan),
                        "max_drawdown": metrics.get("Max Drawdown", np.nan),
                        "calmar": metrics.get("Calmar Ratio", np.nan),
                        "final_equity": equity["total_equity"].iloc[-1] if len(equity) else np.nan,
                        "days": len(equity),
                        "symbols": len(pdata),
                        "gamma": GAMMA,
                        "cost_model_version": COST_MODEL_VERSION,
                        "seconds": round(elapsed, 3),
                    })

                    curve_path = os.path.join(CURVE_DIR, f"{rid}.csv")
                    equity.to_csv(curve_path, index=False)

                    if name == "bh_and_hold" and period_name == "full":
                        r = equity["total_equity"].pct_change().dropna()
                        strategy_returns["bh_and_hold"] = r

                    log(f"  {name}{'('+json.dumps(kwargs,sort_keys=True)+')' if kwargs else ''} "
                        f"{period_name} costs={costs_on} "
                        f"sharpe={metrics.get('Sharpe Ratio', float('nan')):.3f} "
                        f"cagr={metrics.get('CAGR', float('nan'))*100:.2f}% "
                        f"({elapsed:.1f}s)")

    log_df = pd.DataFrame(rows)
    log_df.to_csv(os.path.join(OUT_DIR, "experiment_log.csv"), index=False)
    log(f"Wrote {len(log_df)} rows to {OUT_DIR}/experiment_log.csv")

    # ---- In-sample / out-of-sample decay ----
    is_oos = log_df[log_df["period"].isin(["IS", "OOS"])].pivot_table(
        index=["strategy", "params", "apply_costs"],
        columns="period",
        values=["sharpe", "cagr", "total_return"],
        aggfunc="first",
    )
    is_oos.columns = ["_".join(map(str, c)) for c in is_oos.columns]
    is_oos = is_oos.reset_index()

    def decay(row, metric):
        i, o = row.get(metric + "_IS"), row.get(metric + "_OOS")
        if pd.isna(i) or pd.isna(o):
            return np.nan
        if abs(i) < 1e-12:
            return np.nan
        return (i - o) / abs(i)

    for metric in ("sharpe", "cagr", "total_return"):
        is_oos[f"{metric}_decay"] = is_oos.apply(lambda r: decay(r, metric), axis=1)

    is_oos.to_csv(os.path.join(OUT_DIR, "oos_decay.csv"), index=False)
    log(f"Wrote IS/OOS decay table with {len(is_oos)} configurations")

    # ---- PBO across every full-period strategy pair, costs ON ----
    from src.analytics.cpcv import CPCV
    full = log_df[(log_df["period"] == "full") & (log_df["apply_costs"])]
    pbo_payload = {}
    for run_id, curve_file in [
        (r.run_id, os.path.join(CURVE_DIR, f"{r.run_id}.csv")) for r in full.itertuples()
    ]:
        eq = pd.read_csv(curve_file)
        r = eq["total_equity"].pct_change().dropna().reset_index(drop=True)
        pbo_payload[run_id] = r

    if len(pbo_payload) >= 2:
        pbo_df = pd.DataFrame(pbo_payload)
        cpcv = CPCV(n_splits=8, n_test_splits=2, embargo_pct=0.01)
        pbo = cpcv.calculate_pbo(pbo_df)
        log(f"CPCV PBO (splits=8 test=2 embargo=1%) = {pbo:.4f} ({pbo*100:.2f}%)")
        pbo_summary = {
            "pbo": float(pbo) if pd.notna(pbo) else None,
            "n_strategies": int(len(pbo_payload)),
            "n_splits": 8, "n_test_splits": 2, "embargo_pct": 0.01,
            "cost_model_version": COST_MODEL_VERSION,
            "interpretation": (
                "PBO is the probability that the strategy which ranks best "
                "in-sample falls to or below the median out-of-sample."
            ),
        }
    else:
        pbo_summary = {"pbo": None, "n_strategies": len(pbo_payload)}
        log("WARNING: fewer than 2 strategies — PBO not computed")

    with open(os.path.join(OUT_DIR, "pbo.json"), "w") as f:
        json.dump(pbo_summary, f, indent=2)

    # ---- Provenance summary ----
    prov = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "data_source": "yfinance (Yahoo Finance) alpha-vantage free API",
        "fetch_window": f"{start_date}..{end_date}",
        "universe_size": len(data),
        "universe": sorted(data.keys()),
        "bar_interval": "1d",
        "adjustment": "yfinance auto-adjusted close",
        "initial_capital": INITIAL_CAPITAL,
        "position_size_fraction": SIZE_FRACTION,
        "cost_model_version": COST_MODEL_VERSION,
        "gamma": GAMMA,
        "n_runs": len(log_df),
        "pbo": pbo_summary,
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "python": sys.version.split()[0],
    }
    with open(os.path.join(OUT_DIR, "PROVENANCE.json"), "w") as f:
        json.dump(prov, f, indent=2)

    log(f"Done. Artifacts in {OUT_DIR}/")


if __name__ == "__main__":
    main()
