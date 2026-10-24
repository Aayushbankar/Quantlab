"""Throwaway: recompute sweep DSR statistics under rf=6% (report convention)
and reproduce the rf=0 numbers. Uses repo functions; does NOT modify artifacts."""
import json, sys
import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis

sys.path.insert(0, "/mnt/work/projects/Quantlab")
from src.analytics.deflated_sharpe import (expected_max_sharpe,
                                            deflated_sharpe_ratio_from_moments)

RF = 0.06
ANN = np.sqrt(252.0)

ret = pd.read_csv("/mnt/work/projects/Quantlab/experiments/sweep_returns.csv", index_col=0)
T = len(ret)
print(f"configs={ret.shape[1]}  T={T}  dates {ret.index[0]}..{ret.index[-1]}")

# --- Sharpe, both conventions (MetricsEngine style: excess = r - rf/252, pandas std ddof=1)
s0 = (ret.mean() / ret.std()) * ANN                      # rf = 0 (run_sweep.py:141)
s6 = ((ret.mean() - RF/252) / ret.std()) * ANN           # rf = 6% (MetricsEngine)

# --- validate against committed artifacts
res = pd.read_csv("/mnt/work/projects/Quantlab/experiments/sweep_results.csv").set_index("config_id")
chk = pd.concat([s0.rename("s0"), res["sharpe"].rename("artifact")], axis=1)
chk["d"] = (chk.s0 - chk.artifact).abs()
print(f"[validate] rf=0 vs sweep_results.csv: max abs diff = {chk.d.max():.6f} "
      f"(rounding to 4dp explains diff<=5e-5: {(chk.d <= 5.1e-5).all()})")
summ = json.load(open("/mnt/work/projects/Quantlab/experiments/sweep_summary.json"))
print(f"[validate] rf=0 mean {s0.mean():.4f} (summary {summ['mean_sharpe']}) | "
      f"var {s0.var(ddof=1):.6f} (summary {summ['cross_trial_variance']}) | "
      f"max {s0.max():.4f} (summary {summ['max_sharpe']}) argmax={s0.idxmax()}")

# --- statistics, both conventions
N = ret.shape[1]
def stats(s, tag):
    v = float(s.var(ddof=1))
    ems = expected_max_sharpe(N, v, 0.0)
    print(f"[{tag}] mean={s.mean():.4f} var={v:.6f} std={np.sqrt(v):.4f} "
          f"max={s.max():.4f} ({s.idxmax()}) min={s.min():.4f} E[max]={ems:.4f}")
    return v, ems

v0, ems0 = stats(s0, "rf=0")
v6, ems6 = stats(s6, "rf=6%")

# --- DSR for every config under rf=6%
def moments(col):
    x = ret[col]
    return float(skew(x)), float(kurtosis(x, fisher=False))

dsr6, dsr0 = {}, {}
for c in ret.columns:
    sk, ku = moments(c)
    dsr6[c] = deflated_sharpe_ratio_from_moments(s6[c], T, sk, ku, N, v6, 0.0)
    dsr0[c] = deflated_sharpe_ratio_from_moments(s0[c], T, sk, ku, N, v0, 0.0)

d6 = pd.Series(dsr6); d0 = pd.Series(dsr0)
best6 = s6.idxmax(); best0 = s0.idxmax()
sk, ku = moments(best6)
print(f"\n[best config rf=6%] {best6}: SR6={s6[best6]:.4f} SR0={s0[best6]:.4f} "
      f"skew={sk:.4f} kurt={ku:.4f} T={T} DSR6={d6[best6]:.4f} (1-DSR={1-d6[best6]:.4f})")
sk0, ku0 = moments(best0)
print(f"[best config rf=0] {best0}: SR0={s0[best0]:.4f} SR6={s6[best0]:.4f} "
      f"skew={sk0:.4f} kurt={ku0:.4f} DSR0={d0[best0]:.4f} (old-convention reproduction)")
print(f"[counts] rf=6%: DSR>=0.95: {(d6>=0.95).sum()}  DSR>=0.5: {(d6>=0.5).sum()}  "
      f"max DSR={d6.max():.4f} ({d6.idxmax()})")
print(f"[counts] rf=0:  DSR>=0.95: {(d0>=0.95).sum()}  max DSR={d0.max():.4f} ({d0.idxmax()})")
print(f"[sma_5_45] SR0={s0['sma_5_45']:.4f} SR6={s6['sma_5_45']:.4f} DSR6={d6['sma_5_45']:.4f} DSR0={d0['sma_5_45']:.4f}")

# --- baseline: committed SMA(20,50) full-period cost-on run bf3f93a2fb4a (legacy profile)
eq = pd.read_csv("/mnt/work/projects/Quantlab/experiments/equity_curves/bf3f93a2fb4a.csv")
rb = eq["total_equity"].pct_change().dropna()
sr6 = float((rb.mean() - RF/252) / rb.std() * ANN)
sr0 = float(rb.mean() / rb.std() * ANN)
skb, kub = float(skew(rb)), float(kurtosis(rb, fisher=False))
log_row = pd.read_csv("/mnt/work/projects/Quantlab/experiments/experiment_log.csv").set_index("run_id").loc["bf3f93a2fb4a"]
print(f"\n[baseline bf3f93a2fb4a] T={len(rb)} SR6={sr6:.4f} (experiment_log {float(log_row['sharpe']):.4f}) "
      f"SR0={sr0:.4f} skew={skb:.4f} kurt={kub:.4f}")
print(f"[baseline DSR rf=6% hurdle] DSR={deflated_sharpe_ratio_from_moments(sr6, len(rb), skb, kub, N, v6, 0.0):.4f}")
print(f"[baseline DSR rf=0  hurdle] DSR={deflated_sharpe_ratio_from_moments(sr0, len(rb), skb, kub, N, v0, 0.0):.4f} "
      f"(old mixed-convention bullet said 0.260 using ANOTHER config's moments)")
