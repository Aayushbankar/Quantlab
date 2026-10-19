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
| PRM-VER-003 | 2026-10-19 | pytest suite = **9 tests / 9 passed** at baseline; **independently re-run this cycle**, then expanded to 35 | `tests/` | RUNTIME (pytest) | `9 passed in 1.63s` (baseline) · `35 passed in 5.49s` (final) | **VERIFIED** — baseline confirmed by direct re-run |
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

---

## §6 Ralph Cycle — Verification Records (2026-10-19)

| Verification ID | Date & Timestamp (UTC) | Claim / Fact Description | Target | Verification Method | Raw Evidence | Status |
|---|---|---|---|---|---|---|
| PRM-VER-060 | 2026-10-19 | `scipy` absent from `requirements.txt` **and** from the venv → `deflated_sharpe.py` unimportable; **no test imported the module**, so the defect was invisible | `src/analytics/deflated_sharpe.py:3`, `requirements.txt` | RUNTIME (import) | `ModuleNotFoundError: No module named 'scipy'` | **VERIFIED** — resolved R02 |
| PRM-VER-061 | 2026-10-19 | After pinning `scipy==1.17.1` (numpy held at 1.26.4), the DSR import path and its statistics are covered by 7 tests | `tests/test_deflated_sharpe.py` | RUNTIME (pytest) | `35 passed in 5.49s` | **VERIFIED** |
| PRM-VER-062 | 2026-10-19 | Test suite baseline 9/9 → **35 passed** after adding SMA, RSI, data, DSR and determinism coverage | `tests/` | RUNTIME (pytest) | `35 passed in 5.49s` | **VERIFIED** |
| PRM-VER-063 | 2026-10-19 | RSI all-gains bug reproduced and fixed: `rs=0` → RSI 0; now saturates at 100; guarded by 5 tests incl. an end-to-end rising-market assertion | `src/strategies/rsi_mean_reversion.py` | RUNTIME (pytest) | `tests/test_rsi.py` 5 passed | **VERIFIED** |
| PRM-VER-064 | 2026-10-19 | Duplicate-date bug in `clean_data` found by a newly written test, then fixed (dedupe after NaN-drop so complete rows win) | `src/data/clean.py` | RUNTIME (pytest) | `test_clean_rejects_duplicate_dates` fails before fix, passes after | **VERIFIED** |
| PRM-VER-065 | 2026-10-19 | Determinism holds: two independent runs produce a byte-identical equity curve (SHA-256 of serialised equity equal) | `tests/test_determinism.py` | RUNTIME (pytest) + digest compare | 3 passed | **VERIFIED** — NFR-1 satisfied |
| PRM-VER-066 | 2026-10-19 | Real-data matrix executed: 10 symbols, 1480 bars each, 2019-01-01…2024-12-30, 30 runs, costs on/off × {full, IS, OOS} | `experiments/experiment_log.csv` | RUNTIME (engine) | 30 rows; log + `oos_decay.csv` + `PROVENANCE.json` + `pbo.json` | **VERIFIED** |
| PRM-VER-067 | 2026-10-19 | **Buy-and-hold benchmark Sharpe 0.746 (CAGR 19.07%) beat every active strategy**; best active SMA(10,30) at 0.685; 0 of 4 active beat it | `experiments/experiment_log.csv` | RUNTIME (engine) | full-period table | **VERIFIED (Negative Result)** — central finding |
| PRM-VER-068 | 2026-10-19 | Cost stack removes 48.2% of momentum Sharpe (0.359→0.186) and ₹12,995 of terminal equity on ₹1,00,000 | `experiments/experiment_log.csv` | RUNTIME (engine) | full-period rows | **VERIFIED** — the Profit Mirage |
| PRM-VER-069 | 2026-10-19 | CPCV PBO = **64.29%** (8 splits, 2 test, 1% embargo, 5 configurations, real returns) | `experiments/pbo.json` | RUNTIME (engine) | pbo.json | **VERIFIED** |
| PRM-VER-070 | 2026-10-19 | Momentum Sharpe decays 52.0% IS→OOS with costs on | `experiments/oos_decay.csv` | RUNTIME (engine) | decay table | **VERIFIED** |
| PRM-VER-071 | 2026-10-19 | Fabricated chart pipeline removed: `generate_advanced_charts.py`, `generate_report_charts.py`, `build_report.py` deleted; `np.random` no longer produces any chart data | `scripts/`, `docs/charts/` | STATIC (grep) | `grep -rn "np.random" scripts/` → only prose comments | **VERIFIED** |
| PRM-VER-072 | 2026-10-19 | All remaining charts derive from `experiments/` only: `equity_curves_real.png` (312 KB), `oos_decay.png`, `profit_mirage.png` from real runs; `market_impact_curve.png` explicitly stamped as an analytic model | `scripts/generate_real_charts.py` | STATIC + RUNTIME (regenerate) | charts present with parameter stamps | **VERIFIED** |
| PRM-VER-073 | 2026-10-19 | Report compiles with `pdflatex`, 0 errors, 0 undefined references, 40 pages, all department-format front matter and Ch.1–5 present | `docs/Pramaan_Report.pdf` | RUNTIME (build) | `Output written on Pramaan_Report.pdf (40 pages)` · `pdftotext` confirms each required section | **VERIFIED** |
| PRM-VER-074 | 2026-10-19 | Two per-member PDFs, 40 pages each, body byte-identical from page 2 (50,562 chars), deposit line and roles correct | `docs/Pramaan_Report_{Aayush_Avinash_Bankar,Meet_Jayeshbhai_Patel}.pdf` | RUNTIME (build) + text diff | page counts equal; extracted bodies equal | **VERIFIED** |
| PRM-VER-075 | 2026-10-19 | PPTX: exactly 10 slides, no empty slides, no placeholder text, zero shapes overflowing the canvas | `Pramaan_Presentation.pptx` | RUNTIME (python-pptx inspection) | enumeration output | **VERIFIED** |
| PRM-VER-076 | 2026-10-19 | All slide figures are read from the experiment artifacts at generation time — the deck cannot drift from the data | `scripts/build_presentation.py` | STATIC (source audit) | script consumes log + decay CSVs | **VERIFIED** |
| PRM-VER-077 | 2026-10-19 | NSE turnover reconciled to 0.00297% across code, Thesis.tex, market copy and domain deep-dive — zero un-reconciled `0.00345` remain in deliverable paths | `src/engine/cost_model.py:48`, `docs/`, `scripts/` | STATIC (grep) | `grep -rn "0.00345"` → 0 in deliverable paths | **VERIFIED** — C-01 closed |
| PRM-VER-078 | 2026-10-19 | `risk_free_rate` default corrected 0.05 → 0.06 to match the mathematical specification | `src/analytics/metrics.py:7` | STATIC + RUNTIME (tests) | 35 passed | **VERIFIED** — C-03 closed |

## Ralph Cycle Retractions

| PRM-VER ID | Date Retracted | Reason |
|---|---|---|
| _R-001_ | 2026-10-19 | **Retracted:** "the submitted cost-degradation charts are derived from real backtest runs." Retracted by PRM-VER-030/031 and now fully superseded by PRM-VER-071/072 — the synthetic pipeline is deleted and every surviving chart is generated from `experiments/` with a parameter stamp. |

## Evolution Notes (Ralph cycle)

| EVO ID | Date | Note |
|---|---|---|
| EVO-002 | 2026-10-19 | **The most consequential finding of the cycle:** the flagship statistic (DSR) was silently non-functional in the reproduction environment — `scipy` missing from both `requirements.txt` and the venv, and **no test imported it**. A clean-install reviewer would have hit an `ImportError` on the project's headline feature. Lesson recorded: an untested import is a broken import. |
| EVO-003 | 2026-10-19 | The results are **against the project's own premise** — 0 of 4 strategies beat a passive benchmark. Reported as the central finding rather than reframed, per the steering rule that negative results are logged loudly. |
| EVO-004 | 2026-10-19 | Requirement pins were drifted from reality (`yfinance==0.2.37` vs 1.7.0 installed). Corrected to the versions actually verified; `python-pptx` added for the presentation build. |
| PRM-VER-079 | 2026-10-19 | **Defect found during review and fixed:** the report (module inventory §3.1, Source Map, Ch.5 deployment) and README claimed a REST API (`src/api/`) and Next.js web UI that **do not exist**; README even gave run instructions (`python -m src.api.main`, `cd frontend && npm install`) for modules never built, and referenced a `.env.example` that does not ship. The verifier had checked the engine directories but not whether every module named in the documents exists. All documents now describe only the shipped surface (headless engine + CLI + Streamlit fallback); API/frontend/desktop are explicitly marked *planned* with FR-15 retained as a requirement, not a claim. Both member PDFs rebuilt (40 pages, bodies identical, 0 LaTeX errors) | `docs/Pramaan_Report.tex`, `README.md` | STATIC (path audit) + RUNTIME (rebuild) | `ls src/api frontend` → absent; rebuilt PDFs verified | **VERIFIED (Negative Result)** — self-caught defect, corrected |
| PRM-VER-080 | 2026-10-19 | `src/api/` implemented with FastAPI: endpoints `/health`, `/strategies`, `/universe`, `/replay`, `/history`, and `/run` with dual-pass Gross/Net simulation and SQLite run caching | `src/api/` | RUNTIME (pytest) | 6 passed in `tests/test_api.py` | **VERIFIED** — Phase 1 complete |
| PRM-VER-081 | 2026-10-19 | Pytest test suite expanded from 35 to **41 passed** across 13 test modules in 5.40s | `tests/` | RUNTIME (pytest) | `41 passed in 5.40s` | **VERIFIED** |
| PRM-VER-082 | 2026-10-19 | `data/raw/` populated with 10 liquid NSE equities (1,480 bars each, 2019-2024); unblocks Streamlit fallback UI and enables in-process offline execution | `data/raw/` | RUNTIME (`download_universe`) | 10 CSVs present, 1.5MB total on disk | **VERIFIED** |
| PRM-VER-083 | 2026-10-19 | GTU syllabus unit folders backfilled with formal documentation: `docs/03_unit3_testing/test_plan_and_results.md` and `docs/04_unit4_redesign/engineering_redesigns.md` | `docs/03_unit3_testing/`, `docs/04_unit4_redesign/` | STATIC (audit) | files present and non-trivial | **VERIFIED** |
| PRM-VER-084 | 2026-10-19 | Syllabus 5.4 "Student Reflections and Learning Experience" added to `docs/Pramaan_Report.tex` for both Aayush and Meet; all 3 PDFs rebuilt (42 pages, 0 LaTeX errors); Slide 10 in `Pramaan_Presentation.pptx` regenerated | `docs/Pramaan_Report.tex`, `Pramaan_Presentation.pptx` | RUNTIME (build) | 3 PDFs at 42 pages; pptx with 10 slides | **VERIFIED** |
| PRM-VER-085 | 2026-10-19 | Pandas round warning in `tests/test_determinism.py` eliminated | `tests/test_determinism.py` | RUNTIME (pytest) | zero warnings in test_determinism | **VERIFIED** |
| PRM-VER-086 | 2026-10-19 | Bollinger Band Volatility Breakout strategy implemented (`src/strategies/bollinger_breakout.py`), registered in API adapter and `/strategies` endpoint; unit test passing | `src/strategies/bollinger_breakout.py`, `tests/test_bollinger.py` | RUNTIME (pytest) | `42 passed in 8.46s` | **VERIFIED** |
| PRM-VER-087 | 2026-10-19 | Frontend elevated with institutional Slate-Navy palette, interactive Methodology Guide modal, one-click examiner presets, metric tooltips, and animated execution progress stepper with toast feedback; production build clean | `frontend/src/` | RUNTIME (build) | `npm run build` static generation 5/5, 0 errors | **VERIFIED** |
| PRM-VER-088 | 2026-10-19 | Full desktop workspace overhaul: replaced 1280px constrained container with expansive 2-column layout (sticky 340px command rail + full-bleed workspace), 1200x420 widescreen SVG dissector, multi-view tabs (Profit Mirage, Statutory Tollgate, Overfitting, Ledger, Unified), and instant dual-theme engine (Obsidian Dark & Institutional Light) | `frontend/src/` | RUNTIME (build) | `npm run build` static generation 5/5, 0 errors | **VERIFIED** |
| PRM-VER-089 | 2026-10-19 | Headless Chromium browser audit conducted; user palette implemented (Deep Crimson #931621, Dark Slate Grey #28464B, Stormy Teal #326771, Pacific Cyan #2C8C99, Turquoise #42D9C8); layout converted to 100vw/100vh app-shell with zero dead viewport space; verified via screenshot inspection | `frontend/src/`, `/tmp/screen_vibrant.png` | RUNTIME (browser screenshot) | Chromium 1920x1080 capture verified | **VERIFIED** |
| PRM-VER-090 | 2026-10-19 | Complete Master Quant Station frontend rebuilt from scratch: exact user palette (Dark Slate Grey #28464B cards, Stormy Teal #326771 borders, Pacific Cyan #2C8C99 Gross curve, Turquoise #42D9C8 Net curve, Deep Crimson #931621 Evaporation fill), gradient masthead ribbon, $1400 \times 460$ widescreen SVG dissector, and 100vw/100vh app-shell verified via headless browser screenshot `/tmp/screen_master.png` | `frontend/src/`, `/tmp/screen_master.png` | RUNTIME (browser screenshot + build) | `npm run build` static generation 5/5, 0 errors | **VERIFIED** |
| PRM-VER-091 | 2026-10-19 | Interactive trading workstation elevated: custom-styled Trading Model combobox (`CustomStrategySelect.tsx`), dynamic strategy hyperparameter sliders (SMA, RSI, Momentum, Bollinger), tweakable starting capital input with INR quick pills (₹50K–₹50L), interactive NSE stock universe chips + on-demand live ticker fetching (`src/api/adapter.py`), and FillEvent statutory cost bugfix; verified with production build (5/5 static routes, 0 errors), 42/42 pytest tests passing, and 1920x1080 screenshot `/tmp/screen_pramaan_master.png` | `frontend/src/`, `src/api/adapter.py`, `/tmp/screen_pramaan_master.png` | RUNTIME (build + pytest + screenshot) | `npm run build` clean, 42 passed in 4.30s, screenshot verified | **VERIFIED** |
| PRM-VER-092 | 2026-10-19 | Complete UX overhaul & visual feedback system: eliminated left-sidebar clutter via progressive disclosure (3-step setup with collapsible parameter and universe drawers), eliminated developer/code jargon (Python subprocess, T+1 invariant, raw hex codes), added prominent first-time user primer guide banner, added run-completion & delta summary HUD banner (`✓ Backtest Results Updated`), and added visual ring-pulse feedback on KPI cards and charts; verified via Next.js production build (5/5 static routes clean, 0 errors) and Chromium screenshot `/tmp/screen_pramaan_guided.png` | `frontend/src/`, `/tmp/screen_pramaan_guided.png` | RUNTIME (build + screenshot) | `npm run build` clean, 1920x1080 screenshot verified | **VERIFIED** |
| PRM-VER-093 | 2026-10-19 | Curated harmonic theming & interactive concept orientation: re-engineered Dark ("Abyssal Slate & Teal" #10191B canvas) and Light ("Fine Paper & Maritime Teal" #F1F6F7 vellum) modes to eliminate extreme harshness and weave user's slate-teal-crimson palette harmoniously; added `InteractiveTourHUD.tsx` with 3 interactive concept cards (Paper Mirage, Indian Tax Tollgate, Bankable Net Alpha) with live syllabus links; added URL `?theme=` support; verified via Next.js production build (0 errors), 42/42 pytest tests passing, and 1920x1080 screenshots `/tmp/screen_curated_dark_v2.png` and `/tmp/screen_curated_light_v3.png` | `frontend/src/app/globals.css`, `frontend/src/components/InteractiveTourHUD.tsx`, `/tmp/screen_curated_dark_v2.png`, `/tmp/screen_curated_light_v3.png` | RUNTIME (build + screenshots) | `npm run build` clean, 42 passed in 5.01s, both themes verified | **VERIFIED** |
| PRM-VER-094 | 2026-10-19 | Phase 0 scaffolding: `pyproject.toml` created with `pramaan` package definition, `pythonpath=['.']` eliminating manual PYTHONPATH, ruff/mypy/pyright configurations, and `.pre-commit-config.yaml` | `pyproject.toml`, `.pre-commit-config.yaml` | STATIC + RUNTIME (ruff, pytest) | `ruff check src/ tests/` clean (0 errors), `pytest` collects and passes without PYTHONPATH | **VERIFIED** — Task A1 complete |
| PRM-VER-095 | 2026-10-19 | Seeded synthetic fixture system (`tests/fixtures/`) implemented with generator and 13 equity CSVs; entire 42-test suite passes 100% offline with `data/raw/` deleted/hidden; fixes D4 clean-clone failure | `tests/fixtures/`, `tests/conftest.py`, `src/api/replay.py`, `src/api/adapter.py` | RUNTIME (pytest without data/raw) | `42 passed in 2.71s` with `data/raw` absent | **VERIFIED** — Task A2 / D4 complete |
| PRM-VER-096 | 2026-10-19 | GitHub Actions CI configured (`.github/workflows/ci.yml`) for Python (pytest+cov, ruff) and Frontend (lint, typecheck, build); README updated with CI badge, corrected 42 test counts, real clone URL, Bollinger strategy listed; D5, D16 (LaTeX artifacts untracked, strategy docs moved to `docs/strategy/`), and D17 (`.mailmap` resolving single author identity) closed | `.github/workflows/ci.yml`, `README.md`, `.mailmap`, `docs/strategy/` | RUNTIME (pytest, ruff, npm build, git shortlog) | `git shortlog -sne` single author, 42 tests green, build clean | **VERIFIED** — Task A3 / Gate P0 complete |
| PRM-VER-097 | 2026-10-19 | Honesty fixes D1 & D2: removed hardcoded 0.6429 PBO from `adapter.py` (now `None` with `pbo_reason` explaining sweep requirement); eliminated silent fallbacks in `make_strategy` (raises `ValueError`), `execute_backtest` (raises on missing symbol/dates), and `/run` (never returns unrelated replay on error); added strict Pydantic v2 validation with standardized `{error: {code, message, details}}` envelope; added `served_from`, `engine_version`, `data_hash`, `cost_profile` provenance fields | `src/api/adapter.py`, `src/api/schemas.py`, `src/api/main.py`, `tests/test_honesty.py` | RUNTIME (pytest) | `grep -rn "0.6429" src/` → 0 matches; `test_d1`, `test_d2` passing | **VERIFIED** — D1, D2 complete |
| PRM-VER-098 | 2026-10-19 | Benchmark confound fix D3: added `average_exposure` (0.0 to 1.0), `alpha`, `beta`, and `exposure_matched_return` to `MetricsEngine` and API schemas; tests verify exposure is tracked and bounded | `src/analytics/metrics.py`, `src/api/schemas.py`, `src/api/adapter.py`, `tests/test_honesty.py` | RUNTIME (pytest) | `test_d3_exposure_and_benchmark_metrics` passed; exposure within [0, 1] | **VERIFIED** — D3 complete |
| PRM-VER-099 | 2026-10-19 | Engine and env bugfixes D10 & D11: orders rejected for insufficient cash or minimum share sizing are recorded as `REJECTED` in portfolio and returned in trade ledger; replaced `print()` with Python `logging`; fixed `bool(os.environ.get("DEMO_DATA"))` truthy string bug using `is_demo_mode_active()`; eliminated O(N²) quadratic date filtering in strategies | `src/engine/portfolio.py`, `src/engine/backtest_engine.py`, `src/api/main.py`, `tests/test_honesty.py` | RUNTIME (pytest) | `test_d10`, `test_d11` passed; all 51 tests green | **VERIFIED** — D10, D11 / Gate P1 complete |
| PRM-VER-100 | 2026-10-19 | Versioned cost profile subsystem (D8): created `cost_profiles/` with `zerodha_delivery_2024.json`, `zerodha_delivery_pre_oct2024.json`, `standard_discount_2024.json`, and `traditional_full_service.json` (unverified: true); added DP charge (CDSL flat Rs 13.50 + 18% GST on sell), IPFT, date-based rate resolution across SEBI Oct 2024 boundary, user-configurable `slippage_floor_bps`, and golden-master tests verifying every statutory fee line down to exact paisa | `cost_profiles/`, `src/engine/cost_model.py`, `src/engine/events.py`, `src/api/schemas.py`, `src/api/adapter.py`, `tests/test_cost_model.py` | RUNTIME (pytest) | 6 golden-master tests passed in `tests/test_cost_model.py`; 56 total tests green | **VERIFIED** — Task B1 / D8 complete |
| PRM-VER-101 | 2026-10-19 | Deflated Sharpe Ratio mathematical correction (D6): updated `deflated_sharpe.py` to use true cross-trial variance of Sharpe ratios instead of single-strategy estimator variance; corrected estimator variance degrees of freedom to $(T - 1)$; added `deflated_sharpe_ratio_from_moments`; validated against Bailey & López de Prado (2014) Section 4 published worked example ($N=100, V=0.5, T=1250, SR=2.5 \rightarrow DSR=0.8983$) | `src/analytics/deflated_sharpe.py`, `tests/test_deflated_sharpe.py` | RUNTIME (pytest) | 10 passed in `tests/test_deflated_sharpe.py`; published worked example verified | **VERIFIED** — Task B2 / D6 complete |
