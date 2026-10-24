---
title: "Decision Records — Pramaan"
date: 2026-10-16
project:
  - pramaan
tier:
  - meta
tags:
  - decisions
  - architecture
  - pramaan
status: active
---

# Decision Records — Pramaan

Dated, justified decisions. If a rule is broken, a decision note is written **here** — never silently. Protocol: `00_overview.md` §7.

| ID | Date | Decision | Justification | Status |
|---|---|---|---|---|
| DEC-001 | 2026-10-16 | **No backend / no cloud compute for v1.** Computation stays 100% local | Public data source, no broker integration, daily bars on ~10 symbols; a laptop is sufficient. A server adds cost, latency and ops surface for zero functional gain. | Ratified |
| DEC-002 | 2026-10-16 | **SQLite + Parquet for the demo path; Supabase deferred** to the product phase | The Oct 26 demo must never depend on a network. Supabase (auth/sync/history) enters after the submission. | Ratified |
| DEC-003 | 2026-10-16 | **No live trading / broker integration** | Out of scope by rule; adds SEBI regulatory burden, liability and ops a diploma project cannot carry; there is no execution revenue path. | Ratified |
| DEC-004 | 2026-10-16 | **Engine is never rewritten** — `src/engine`, `src/analytics`, `src/strategies`, `src/data` are the contribution; bugs fixed with regression tests | It is the only viva-defensible artifact. Rebuilding it destroys the marks. | Ratified (non-negotiable) |
| DEC-005 | 2026-10-16 | **Desktop-first distribution** via PyInstaller/Briefcase wrapping the existing Python UI; no native mobile in v1 | Reuses the Python engine directly. Native mobile (Kotlin/Dart) or Python-on-mobile (Kivy/BeeWare) either forces an engine rewrite or uses immature tooling. | Ratified; revisit post-PMF |
| DEC-006 | 2026-10-16 | **Product name = Pramaan** (प्रमाण, "proof"). Tagline *"Prove your edge before you deploy a rupee."* | Indian-native (examiner-friendly), states the thesis in one word, distinct from Western competitors. "QuantLab" retained only as the legacy engine/repo name. | Ratified |
| DEC-007 | 2026-10-16 | **Apache 2.0 retained** for the engine | Permissive: allows commercial use and proprietary derivatives with notice preservation. Keeps the OSS adoption + academic path open. | Ratified |
| DEC-008 | 2026-10-16 | **FastAPI exposes the engine**; frontend consumes only the API contract | One codebase, three surfaces (CLI/GUI/web). The contract is frozen in `docs/api-contract.md` before UI work starts. | Ratified — critical path |
| DEC-009 | 2026-10-16 | **Web frontend = Next.js + TypeScript + Tailwind + shadcn/ui + Recharts**; desktop via Tauri; PWA for mobile-browser reach | Charts and dashboard quality are the product's face, and TS is the fastest language to build them in. Flutter was rejected for v1 (Dart rewrite, weaker charting, slower ramp) — see `03_dead_ends.md`. | Ratified |
| DEC-010 | 2026-10-16 | **Streamlit dashboard kept** as the demo fallback until Phase 4 | Zero-cost insurance. If the rebirth fails at the G4 gate the submission still has a working demo. | Active until Oct 22 |
| DEC-011 | 2026-10-19 | **Dual-Pass Gross Counterfactual Formulation:** Unpenalized independent compounding run for Gross curve rather than shadow sizing | Illustrates the true idealized "Profit Mirage" that traps naive traders, where capital compounds friction-free. Reconciled against Net via statutory tollgate. | Ratified |
| DEC-012 | 2026-10-19 | **SSE / Live Progress Bar Emission Throttle at 50 bars** | Emitting every single bar saturates client event loops and DOM re-renders. 50 bars provides sub-10ms latency and smooth visual feedback for 1,480-bar runs. | Ratified |
| DEC-013 | 2026-10-19 | **Tiered Offline Replay Resolution (`DEMO_DATA=1` fail-safe)** | Viva demo must never crash on network failure: Tier 1 SQLite cache -> Tier 2 `experiments/` pre-computed artifacts -> Tier 3 local `data/raw/` offline simulation. | Ratified |
| DEC-014 | 2026-10-19 | **Attribution & Shared Defense Protocol for GTU DI05000341** | Mitigate 40-1 commit split risk by formalizing per-member subsystem ownership in report Ch.3, adding co-authorship trailers, and adding dedicated student reflection sections. | Ratified |

## Agents-style working protocol

- One task per iteration; verify with a real command; log a ledger row; stop.
- Cut scope at the **next** gate, never at submission.
- Never claim more than works; the recorded video is the backup for everything.
| DEC-015 | 2026-10-24 | **Post-freeze docs-only release pass (`submission/final-docs`)** | Code freeze (Oct 22 23:59) locked `src/`, `frontend/src/`, `tests/`, `scripts/run_*`. Submission package (report PDFs, deck, README) still contained provably false/stale statements (35 tests, MIT, mixed Sharpe conventions, unverified claims). Decision: make docs-only corrections on branch `submission/final-docs` after freeze — no frozen path touched; user opens/merges the PR (H8). | Ratified |
| DEC-016 | 2026-10-24 | **One Sharpe convention: rf = 6%, annualised** | `sweep_summary.json`/`run_sweep.py` compute Sharpe at rf=0 while `MetricsEngine`, Table 5.1, the workbook UI and every report figure use rf=6%. Old §3.7.1 mixed an rf=6% observed SR with an rf=0 E[max] hurdle (DSR 0.260). Decision: report uses rf=6% everywhere; sweep statistics recomputed from `experiments/sweep_returns.csv` (script+output in `.agent/evidence/2026-10-24_PRM-VER-113_*`); `sweep_summary.json` NOT regenerated (generated artifact); rf=0 reproduction kept in ledger only; verdict restated plainly (best DSR 0.205 of 133, baseline 0.112). Approved by user via old-vs-new table. | Ratified |
