"""
Regenerate every results chart FROM REAL ENGINE OUTPUT.

Every figure produced here is derived from experiments/experiment_log.csv or
experiments/equity_curves/<run_id>.csv. No np.random, no synthetic noise, no
curve reconstructed from a CAGR summary. Prior pipeline (DE-001) fabricated
data with np.random and is removed.

Each chart is stamped with the parameters that produced it, so any figure in
the report can be traced back to a specific run_id.
"""

import os
import json
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXP = os.path.join(BASE, "experiments")
CHARTS = os.path.join(BASE, "docs", "charts")
LOG = os.path.join(EXP, "experiment_log.csv")
CURVES = os.path.join(EXP, "equity_curves")

C_OK = "#55A868"    # green — costs off (the mirage)
C_COST = "#C44E52"  # red — costs on (reality)
C_BM = "#4C72B0"    # blue — benchmark


def load():
    with open(os.path.join(EXP, "PROVENANCE.json")) as f:
        prov = json.load(f)
    return pd.read_csv(LOG), prov


def curve(run_id):
    p = os.path.join(CURVES, f"{run_id}.csv")
    return pd.read_csv(p) if os.path.exists(p) else None


def runs(df, strategy, period="full", apply_costs=True):
    m = df[(df.strategy == strategy) & (df.period == period) & (df.apply_costs == apply_costs)]
    return m.iloc[0] if len(m) else None


def stamp(ax, text):
    ax.annotate(
        text, xy=(0.005, -0.16), xycoords="axes fraction", fontsize=7,
        color="#555555", ha="left", va="top", family="monospace",
    )


# 1. Profit Mirage — the headline figure
def chart_profit_mirage(df, prov):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    strategies = ["sma_crossover", "sma_crossover_10_30", "rsi_mean_reversion", "momentum"]

    sh_off, sh_on, labels = [], [], []
    for s in strategies:
        o = runs(df, s, apply_costs=False)
        n = runs(df, s, apply_costs=True)
        sh_off.append(o.sharpe)
        sh_on.append(n.sharpe)
        labels.append(s.replace("_", "\n"))

    x = np.arange(len(labels))
    w = 0.38
    axes[0].bar(x - w / 2, sh_off, w, label="Costs OFF (the mirage)", color=C_OK)
    axes[0].bar(x + w / 2, sh_on, w, label="Costs ON (reality)", color=C_COST)
    axes[0].axhline(
        runs(df, "bh_and_hold").sharpe, ls="--", color=C_BM, lw=1.5,
        label="Buy-and-hold benchmark",
    )
    for i, (a, b) in enumerate(zip(sh_off, sh_on)):
        axes[0].text(i - w / 2, a + 0.02, f"{a:.2f}", ha="center", fontsize=8)
        axes[0].text(i + w / 2, b + 0.02, f"{b:.2f}", ha="center", fontsize=8)
    axes[0].set_xticks(x); axes[0].set_xticklabels(labels, fontsize=8)
    axes[0].set_ylabel("Sharpe ratio")
    axes[0].set_title("Sharpe ratio: costs OFF vs ON", fontweight="bold")
    axes[0].legend(fontsize=8); axes[0].grid(axis="y", alpha=0.3)

    drags, d_labels = [], []
    for s in strategies:
        o = runs(df, s, apply_costs=False)
        n = runs(df, s, apply_costs=True)
        drags.append((o.final_equity - n.final_equity))
        d_labels.append(s.replace("_", "\n"))
    bars = axes[1].bar(d_labels, drags, color=C_COST)
    for b, d in zip(bars, drags):
        axes[1].text(b.get_x() + b.get_width() / 2, d + 400, f"Rs{d:,.0f}",
                     ha="center", fontsize=9, fontweight="bold")
    axes[1].set_ylabel("Equity lost (INR)")
    axes[1].set_title("Statutory cost drag on Rs1,00,000", fontweight="bold")
    axes[1].grid(axis="y", alpha=0.3)

    txt = (f"{prov['universe_size']} NSE symbols | {prov['fetch_window']} | 1d bars | "
           f" Rs{prov['initial_capital']:,.0f} | {prov['cost_model_version']} | "
           f"gamma={prov['gamma']} | source: {prov['data_source']}")
    fig.suptitle("The Profit Mirage: how Indian statutory costs erase an apparent edge", fontsize=13, fontweight="bold")
    stamp(fig.axes[1], txt)
    fig.tight_layout(rect=[0, 0.06, 1, 0.96])
    fig.savefig(os.path.join(CHARTS, "profit_mirage.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


# 2. Real equity curves vs benchmark
def chart_equity_curves(df, prov):
    fig, ax = plt.subplots(figsize=(13, 7))
    for s, col, ls in [
        ("sma_crossover_10_30", C_COST, "-"),
        ("momentum", "#8172B2", "-"),
        ("rsi_mean_reversion", "#CCB974", "-"),
    ]:
        r = runs(df, s)
        c = curve(r.run_id)
        if c is None:
            continue
        ax.plot(pd.to_datetime(c["date"]), c["total_equity"] / 1000, ls, lw=1.8, label=f"{s} (costs ON)")
    r = runs(df, "bh_and_hold")
    c = curve(r.run_id)
    if c is not None:
        ax.plot(pd.to_datetime(c["date"]), c["total_equity"] / 1000, "--", lw=2.2, color=C_BM,
                label="buy-and-hold (costs ON)")
    ax.axhline(100, color="grey", lw=0.8, ls=":")
    ax.set_ylabel("Portfolio value (Rs thousands)")
    ax.set_xlabel("")
    ax.set_title("Real equity curves, 10 NSE equities 2019-2024 (from engine output)", fontweight="bold")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    stamp(ax, f"strategy=sma_crossover_10_30(10,30) / momentum(20,5%) / rsi(14,30,70) / bh | "
              f"{prov['fetch_window']} | costs ON | source: {prov['data_source']}")
    fig.tight_layout()
    fig.savefig(os.path.join(CHARTS, "equity_curves_real.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


# 3. IS vs OOS decay
def chart_oos_decay(df, prov):
    d = pd.read_csv(os.path.join(EXP, "oos_decay.csv"))
    d = d[d.apply_costs == True].copy()
    d["label"] = d.strategy
    d = d.sort_values("sharpe_IS")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    y = np.arange(len(d))
    h = 0.38
    axes[0].barh(y + h / 2, d.sharpe_IS, h, color=C_OK, label="In-sample (2019-2022)")
    axes[0].barh(y - h / 2, d.sharpe_OOS, h, color=C_COST, label="Out-of-sample (2023-2024)")
    axes[0].set_yticks(y); axes[0].set_yticklabels(d.label, fontsize=9)
    axes[0].set_xlabel("Sharpe ratio")
    axes[0].set_title("In-sample vs out-of-sample Sharpe (costs ON)", fontweight="bold")
    axes[0].legend(fontsize=8); axes[0].grid(axis="x", alpha=0.3)

    valid = d[pd.notna(d.sharpe_decay)]
    colors = [C_COST if v > 0 else C_OK for v in valid.sharpe_decay]
    axes[1].barh(valid.label, valid.sharpe_decay, color=colors)
    axes[1].axvline(0, color="black", lw=0.8)
    axes[1].set_xlabel("Sharpe decay  (IS - OOS) / |IS|")
    axes[1].set_title("Parameter overfitting: IS->OOS decay", fontweight="bold")
    axes[1].grid(axis="x", alpha=0.3)
    for lbl, v in zip(valid.label, valid.sharpe_decay):
        axes[1].text(v + (0.02 if v >= 0 else -0.02), lbl, f"{v:+.0%}",
                     va="center", ha="left" if v >= 0 else "right", fontsize=8)

    stamp(axes[1], f"{prov['fetch_window']} | costs ON | decay>0 means IS inflated | "
                   f"source: {prov['data_source']}")
    fig.tight_layout()
    fig.savefig(os.path.join(CHARTS, "oos_decay.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


# 4. Parameter stability surface (2D grid) from a real run
def chart_param_stability(prov):
    """Real 2D parameter grid: load a cached surface if present, else note it."""
    surface_path = os.path.join(EXP, "param_surface.csv")
    if not os.path.exists(surface_path):
        return False

    s = pd.read_csv(surface_path)
    piv = s.pivot(index="fast_window", columns="slow_window", values="sharpe")
    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(piv, annot=True, fmt=".2f", cmap="RdYlGn", center=0, ax=ax,
                cbar_kws={"label": "IS Sharpe ratio"})
    ax.set_xlabel("slow window")
    ax.set_ylabel("fast window")
    ax.set_title("Parameter stability surface (real grid search)", fontweight="bold")
    stamp(ax, f"{prov['fetch_window']} in-sample | 10 NSE symbols | costs ON | "
              f"source: {prov['data_source']}")
    fig.tight_layout()
    fig.savefig(os.path.join(CHARTS, "param_stability_surface.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)
    return True


# 5. Market impact curve (analytic model, honestly labelled as a model plot)
def chart_market_impact(prov):
    quantities = np.linspace(100, 100_000, 500)
    adv = 1_000_000
    sigma = 0.02
    gamma = prov["gamma"]
    impact_pct = gamma * sigma * np.sqrt(quantities / adv) * 100

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(quantities, impact_pct, color="#55A868", lw=3)
    ax.set_xlabel("Order quantity (shares)")
    ax.set_ylabel("Slippage impact (%)")
    ax.axvline(adv * 0.01, color="red", ls="--", lw=1.5, label="1% of ADV (1,000,000 shares)")
    ax.fill_between(quantities, impact_pct, 0, color="#55A868", alpha=0.1)
    ax.legend()
    ax.grid(alpha=0.3)
    ax.set_title("Almgren-Chriss square-root market impact (model)", fontweight="bold")
    stamp(ax, f"ANALYTIC MODEL (not a run artifact): dP = gamma*sigma*sqrt(Q/V) | "
              f"gamma={gamma}, sigma=0.02, ADV=1e6 — as implemented in src/engine/cost_model.py")
    fig.tight_layout()
    fig.savefig(os.path.join(CHARTS, "market_impact_curve.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def main():
    os.makedirs(CHARTS, exist_ok=True)
    df, prov = load()
    chart_profit_mirage(df, prov)
    chart_equity_curves(df, prov)
    chart_oos_decay(df, prov)
    chart_param_stability(prov)
    chart_market_impact(prov)
    print("Charts regenerated from real engine output:")
    for f in sorted(os.listdir(CHARTS)):
        if f.endswith(".png"):
            print(f"  {f}")


if __name__ == "__main__":
    main()
