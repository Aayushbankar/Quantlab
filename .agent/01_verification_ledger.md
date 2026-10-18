---
title: "Master Verification Ledger — Pramaan"
date: 2026-10-16
project:
  - pramaan
tier:
  - engine
  - api
  - frontend
  - academic
tags:
  - verification-ledger
  - ssot
  - cost-model
  - dsr
  - cpcv
  - lookahead
  - pramaan
status: active
---

# Master Verification Ledger — Pramaan

This is the authoritative, machine-parseable SSOT mapping every verified Pramaan claim to its evidence, target, verification method, and raw artifact. Protocol: `00_overview.md`.

Legend: **PRM-VER** verification · **PRM-EXP** experiment · **PRM-GATE** gate record.

---

## §1 Repository Facts (static audit)

| Verification ID | Date & Timestamp (UTC) | Claim / Fact Description | Target (file:line) | Verification Method | Raw Evidence | Status |
|---|---|---|---|---|---|---|
| PRM-VER-001 | 2026-10-16 | `src/` is ~1,008 LOC across 18 Python modules | `src/**` | STATIC (source audit) | full source read | **VERIFIED** |
| PRM-VER-002 | 2026-10-16 | 4-layer decoupled architecture: Dashboard → Analytics → Engine → Data/Strategies | `src/dashboard`, `src/analytics`, `src/engine`, `src/data` | STATIC (source audit) | source read | **VERIFIED** |
| PRM-VER-003 | 2026-10-16 | pytest suite = **9 tests / 9 passed** at baseline, branch `feat/v2-architecture` | `tests/` (6 files) | STATIC (prior audit, `GTU_MINOR_PROJECT_REVIEW.md:215`) | `GTU_MINOR_PROJECT_REVIEW.md` §9 | **INCONCLUSIVE** — independent re-run pending, scheduled as PRM-EXP-001 |
| PRM-VER-004 | 2026-10-16 | `scipy` is imported by `deflated_sharpe.py:3` but **absent** from `requirements.txt` → fresh-clone install breaks DSR/CPCV | `src/analytics/deflated_sharpe.py:3` · `requirements.txt:1-7` | STATIC (source audit) | both files read | **VERIFIED** — release blocker, fix = PRM-EXP-002 |
| PRM-VER-005 | 2026-10-16 | `experiments/` and `data/raw/` are **empty on disk** — no real-data run artifact exists despite being the central result claim | `experiments/`, `data/raw/` | STATIC (filesystem) | directory listing | **VERIFIED (Negative Result)** — fix = PRM-EXP-003 |
| PRM-VER-006 | 2026-10-16 | Git history = **29 commits, single author** (`aayushbankar`) for a two-person team; `origin/meet` empty/unmerged | git shortlog | STATIC (git audit) | `GTU_MINOR_PROJECT_REVIEW.md:31` | **VERIFIED** — team-evidence risk PR-01 |
| PRM-VER-007 | 2026-10-16 | `.gitignore` covers `venv`, `data/raw/`, `data/processed/`, `__pycache__`, `.pytest_cache` — no `frontend/`, no `.agent/` | `.gitignore:1-6` | STATIC (source audit) | file read | **VERIFIED** — update during Phase 1 |

## §2 Engine Invariants

| Verification ID | Date & Timestamp (UTC) | Claim / Fact Description | Target (file:line) | Verification Method | Raw Evidence | Status |
|---|---|---|---|---|---|---|
| PRM-VER-010 | 2026-10-16 | **Zero-look-ahead enforced by construction**: SignalEvent generated at t Close → queued → filled at t+1 Open | `src/engine/backtest_engine.py:31-63` (`run`), `:65-101` (`_execute_pending_orders`) | STATIC (source audit) | source read | **VERIFIED** |
| PRM-VER-011 | 2026-10-16 | Look-ahead invariant is **tested** — dummy strategy signals 2023-01-01 Close, test asserts fill at Open 105.0 | `tests/test_engine.py:15-38` | STATIC (test audit) | file read | **VERIFIED** (pending PRM-EXP-001 re-run) |
| PRM-VER-012 | 2026-10-16 | Position sizing uses **10% of total equity**, not cash (documented bug fix) | `src/engine/backtest_engine.py:113-120` | STATIC (source audit) | source read | **VERIFIED** |
| PRM-VER-013 | 2026-10-16 | Total-equity sizing is **tested**: A@200 gives equity 11000 → B target 1100 → qty 110 asserted | `tests/test_engine.py:48-79` | STATIC (test audit) | file read | **VERIFIED** |
| PRM-VER-014 | 2026-10-16 | Cash≥0 is only **warned**, not enforced, inside `Portfolio` — pre-trade check lives in the engine | `src/engine/portfolio.py:34-36` · `backtest_engine.py:94-97` | STATIC (source audit) | source read | **VERIFIED** — invariant hardening = PRM-EXP-004 |
| PRM-VER-015 | 2026-10-16 | Momentum duplicate-BUY guard works — ROC>threshold with open position emits **0** signals | `src/strategies/momentum.py:34` · `tests/test_momentum.py:7-43` | STATIC (test audit) | file read | **VERIFIED** |
| PRM-VER-016 | 2026-10-16 | **Order-event duplication**: `src/engine/order.py` (`Order`) and `src/engine/events.py:27-35` (`OrderEvent`) carry the same fields; engine uses `OrderEvent` only | `src/engine/order.py` vs `src/engine/events.py` | STATIC (source audit) | both files read | **VERIFIED** — REMOVE candidate |

## §3 Cost Model & Statistics

| Verification ID | Date & Timestamp (UTC) | Claim / Fact Description | Target (file:line) | Verification Method | Raw Evidence | Status |
|---|---|---|---|---|---|---|
| PRM-VER-020 | 2026-10-16 | **Full Indian statutory stack implemented**: brokerage min(20, 0.03%), STT 0.1% both sides, stamp duty 0.015% **buy-only**, NSE turnover 0.00297%, SEBI 0.0001%, GST 18% on brokerage+turnover | `src/engine/cost_model.py:36-55` | STATIC (source audit) | source read | **VERIFIED** — the moat |
| PRM-VER-021 | 2026-10-16 | Cost components are **unit-tested** to the paisa: fill 1000.02, brokerage 20, STT 100, stamp 15.0003, turnover 100002×0.0000307, GST derived | `tests/test_cost_model.py:6-40` | STATIC (test audit) | file read | **VERIFIED** |
| PRM-VER-022 | 2026-10-16 | Market impact = **Almgren-Chriss square-root** `γ·σ·√(Q/ADV)`, capped at 5% | `src/engine/cost_model.py:22-28` | STATIC (source audit) | source read | **VERIFIED** |
| PRM-VER-023 | 2026-10-16 | Volatility and ADV estimated from a trailing 20-bar window, with NaN guards | `src/engine/backtest_engine.py:84-89` | STATIC (source audit) | source read | **VERIFIED** |
| PRM-VER-024 | 2026-10-16 | DSR implements skew/kurtosis-adjusted variance and E[max SR] via Euler-Mascheroni extreme-value approximation | `src/analytics/deflated_sharpe.py:5-15, 17-43` | STATIC (source audit) | source read | **VERIFIED** |
| PRM-VER-025 | 2026-10-16 | CPCV purges train/test leakage at block boundaries with a configurable embargo | `src/analytics/cpcv.py:20-45` | STATIC (source audit) | source read | **VERIFIED** |
| PRM-VER-026 | 2026-10-16 | Embargo effect is **tested**: AR(1) φ=0.95 series, PBO with embargo > PBO without embargo (claim of leakage) | `tests/test_cpcv.py:35-59` | STATIC (test audit) | file read | **VERIFIED** (pending PRM-EXP-001 re-run) |
| PRM-VER-027 | 2026-10-16 | Strategies re-filter with `df[df['date'] <= current_date]` each symbol each day → **O(N) rescan**; correctness unaffected (still causal) but the "near-compiled speeds" claim is overstated | `sma_crossover.py:21` · `rsi_mean_reversion.py:46` · `momentum.py:20` | STATIC (source audit) | source read | **VERIFIED (Negative Result)** — do not claim O(1) end-to-end |

## §4 Data, Docs & Claims Integrity

| Verification ID | Date & Timestamp (UTC) | Claim / Fact Description | Target (file:line) | Verification Method | Raw Evidence | Status |
|---|---|---|---|---|---|---|
| PRM-VER-030 | 2026-10-16 | **`scripts/generate_advanced_charts.py` fabricates data** — monthly returns heatmap and equity/drawdown curves use `np.random`, explicitly labelled *"Illustrative, not derived from live backtest run"* | `scripts/generate_advanced_charts.py:16-55` | STATIC (source audit) | source read | **VERIFIED (Negative Result)** |
| PRM-VER-031 | 2026-10-16 | **`scripts/generate_report_charts.py` simulates the equity curve** from stored CAGR rather than replaying engine output | `scripts/generate_report_charts.py:53-79` | STATIC (source audit) | source read | **VERIFIED (Negative Result)** |
| PRM-VER-032 | 2026-10-16 | Entry-point scripts fetch only **2022–2024 (2 years)** — the "5-year NIFTY-50 dataset" claim is not currently supported by any script | `scripts/run_experiments.py:18` · `run_pbo_experiment.py:15` | STATIC (source audit) | source read | **DISPROVED** until PRM-EXP-003 |
| PRM-VER-033 | 2026-10-16 | Universe is **10 symbols**, not 50 — "NIFTY-50" framing overstates the universe | `src/data/universe.py:3-14` | STATIC (source audit) | file read | **VERIFIED** — relabel to "10 large-cap NSE equities" unless expanded |
| PRM-VER-034 | 2026-10-16 | `plot_2d_heatmap` is implemented but **never called** from the dashboard | `src/dashboard/components.py:21-31` · `app.py:63-64` | STATIC (source audit) | source read | **VERIFIED** |
| PRM-VER-035 | 2026-10-16 | Dashboard **hard-fails** via `st.stop()` when `data/raw/` is missing, with no empty state | `src/dashboard/app.py:24-26` | STATIC (source audit) | source read | **VERIFIED** — UX blocker |
| PRM-VER-036 | 2026-10-16 | **RSI all-gains bug confirmed**: `rs = up/down if down != 0 else 0` returns rs=0 → RSI=0 (max **oversold**) when every delta is positive; correct value is RSI=100 | `src/strategies/rsi_mean_reversion.py:23-24, 39` | STATIC (source audit) | source read | **VERIFIED** — no test survives this; fix = PRM-EXP-005 |
| PRM-VER-037 | 2026-10-16 | **Risk-free rate mismatch**: code defaults 0.05, mathematical spec says 0.06 | `src/analytics/metrics.py:7` | STATIC (source audit) | source read | **VERIFIED** — fix = PRM-EXP-002 |
| PRM-VER-038 | 2026-10-16 | NSE turnover fee stated as **0.00297%** in code but **0.00345%** in `QUANTLAB_DOMAIN_DEEP_DIVE.md` — documents disagree | `cost_model.py:48` vs `QUANTLAB_DOMAIN_DEEP_DIVE.md:95` | STATIC (source audit) | both files read | **VERIFIED** — contradiction C-01 |
| PRM-VER-039 | 2026-10-16 | Adjusted-close contradiction: clean.py relies on yfinance-adjusted closes; report text claims adjusted close is *"strictly prohibited"* | `src/data/clean.py:23` vs `QuantLab_Thesis.tex:419` | STATIC (source audit) | both files read | **VERIFIED** — contradiction C-02 |
| PRM-VER-040 | 2026-10-16 | LMT trade-through path (`BUY fills only if low < limit`) is implemented but **unreachable** — engine emits only MKT orders | `backtest_engine.py:75-80, 131` | STATIC (source audit) | source read | **VERIFIED** — dead path, document or wire |
| PRM-VER-041 | 2026-10-16 | `validator.py` 2D grid search requires **exactly 2** parameters; N-dimensional sweeps impossible | `src/analytics/validation.py:30-32` | STATIC (source audit) | source read | **VERIFIED** |

## §5 Build Environment (Product Track)

| Verification ID | Date & Timestamp (UTC) | Claim / Fact Description | Target | Verification Method | Raw Evidence | Status |
|---|---|---|---|---|---|---|
| PRM-VER-050 | 2026-10-16 | Node **v26.7.0** available — satisfies Next.js 15 / Tauri toolchain requirements | host | RUNTIME (`node --version`) | terminal output | **VERIFIED** |
| PRM-VER-051 | 2026-10-16 | Python **3.11.16** available — satisfies pandas 2.2.2 / numpy 1.26.4 pins | host | RUNTIME (`python3 --version`) | terminal output | **VERIFIED** |
| PRM-VER-052 | 2026-10-16 | Working tree has 1 untracked review doc; no uncommitted engine changes present | git status | STATIC (git audit) | `git status` | **VERIFIED** |

---

## Retraction Log

| PRM-VER ID | Date Retracted | Reason |
|---|---|---|
| _PRM-VER-R001_ | 2026-10-16 | **Retracted upstream claim:** "the submitted cost-degradation charts are derived from real backtest runs." Retracted because PRM-VER-030/031 prove `generate_advanced_charts.py` and `generate_report_charts.py` synthesise data with `np.random` and label it *illustrative*. The reports' figures therefore do **not** currently evidence the engine on real data. Resolution requires PRM-EXP-003 (regenerate from a real run with parameters recorded). |

## Evolution Notes

| EVO ID | Date | Note |
|---|---|---|
| EVO-001 | 2026-10-16 | Strategy docs migrated from free-form `progress.md` to this ledger, adopting the CypherMatrix VER/EXP/EVO protocol. Rationale: Pramaan's thesis demands that its own build be auditable — `00_overview.md`. |

## Nearest Unverified Claims (must be attempted before submission)

| ID | Blocker | Scheduled |
|---|---|---|
| PRM-VER-003 | pytest 9/9 never independently re-run this branch | PRM-EXP-001 |
| PRM-VER-032 | no real 2019–2024 dataset or log on disk | PRM-EXP-003 |
| PRM-VER-038/039 | two documented contradictions in the report | PRM-EXP-002 |
