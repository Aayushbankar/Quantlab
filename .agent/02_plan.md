---
title: "Implementation Plan & Gates — Pramaan"
date: 2026-10-16
project:
  - pramaan
tier:
  - meta
  - engine
  - api
  - frontend
  - academic
tags:
  - plan
  - gates
  - roadmap
  - pramaan
status: active
---

# Implementation Plan & Gates — Pramaan

**Started:** 2026-10-16 · **Hard deadline:** 2026-10-26 10:30 IST (GTU DI05000341 submission)
**Code freeze:** 2026-10-22 23:59 IST
**Team:** Aayush Bankar (Leader) · Meet Patel
**Branch:** `feat/v2-architecture`
**Every task carries a `PRM-EXP-`/`PRM-GATE-` ID whose result is recorded in [[01_verification_ledger|the ledger]]** — a task is not done until its ID has a row with evidence.

---

## 0. Objective

Deliver **both** by Oct 26:
- **Track A (mandatory):** GTU minor-project submission — real-data evidence, department-format report, PPTX, live demo, team evidence. Predicted CA today 34/50 → target **44–47/50**.
- **Track B (differentiator):** a **deployed product** — desktop GUI + landing page + public OSS repo with releases — built on the existing engine, so the submission reads as *"research engine, productized and shipped"* rather than *"college CRUD app"*.

**Non-negotiable rule:** Track B exists to strengthen Track A. If Track B threatens Track A at the freeze gate, Track B gets cut back to the Streamlit fallback. **No exceptions.**

---

## 1. Scope

### In scope (both tracks)
- Engine unchanged (zero-lookahead T+1, Indian cost model, DSR, CPCV) — **this is the contribution**
- Real NIFTY-50 2019–2024 data run + committed artifacts
- FastAPI wrapper → Next.js UI → Tauri desktop → Vercel/Fly.io deploy → GitHub releases
- BYOK (bring-your-own-key) OSS distribution
- Department-format report + PPTX

### Out of scope (state explicitly in report and viva)
- Live trading / broker integration
- Native mobile app (Android/iOS) — desktop-first
- Intraday / tick / options / futures / multi-asset
- Supabase-dependent flows in the demo (SQLite local-first; Supabase optional)
- AI/LLM assistant
- Multi-user collaboration

---

## 2. Architecture (single source of truth)

```
LANDING (Vercel,  / route)
   │
Tauri v2 shell ──► Next.js 15 (React + TS + Tailwind + shadcn/ui + Recharts)
                         │  HTTPS/REST
                   FastAPI (Python, uvicorn)
                         │
        ┌────────────────┼─────────────────────┐
   src/engine       src/analytics        src/data
   (unchanged)      DSR/CPCV/metrics    fetch→cache
                         │
              SQLite (local) ──► Supabase (optional: auth, sync, history)
```

| Layer | Technology | Runs where |
|---|---|---|
| UI | Next.js 15 + TS + Tailwind + shadcn/ui + Recharts | Browser (web + Tauri shell) |
| API | FastAPI (Python) | Fly.io (hosted) or local sidecar |
| Engine | `src/engine` + `src/analytics` — **untouched** | Same process as API |
| Store (demo) | SQLite + Parquet cache + `.env`/OS keyring | Local |
| Store (product) | Supabase Postgres + Auth + Storage + RLS | Cloud |
| Data | yfinance runtime fetch → cached; **replay mode from commit for demo** | Local |
| Distribute | GitHub Releases (binaries) + Vercel (web) | — |

---

## 3. Phase Plan

### Phase 0 — Foundation & Real Data · Oct 16–17 · (~14 h) · **BLOCKER**

| # | Task | Files | Owner |
|---|---|---|---|
| 0.1 | Run real-data matrix: NIFTY-50 daily 2019–2024 | `scripts/run_experiments.py`, `run_pbo_experiment.py` → `experiments/experiment_log.csv`, IS/OOS decay table, `docs/charts/*.png` with params recorded | Aayush |
| 0.2 | Fix `scipy` missing from `requirements.txt` | `requirements.txt` | Aayush |
| 0.3 | Fix RSI all-gains edge (`rs=0` → RSI 100, not 0) + regression test | `src/strategies/rsi_mean_reversion.py:23,39` | Aayush |
| 0.4 | Reconcile NSE turnover to **0.00297%** (one cited circular); `risk_free_rate=0.06` | `src/engine/cost_model.py`, `src/analytics/metrics.py`, docs | Aayush |
| 0.5 | Add `tests/test_sma.py`, `test_rsi.py`, `test_data.py` | `tests/` | Aayush |
| 0.6 | **DECIDED: name = Pramaan** (Hindi: "proof/evidence"). Tagline: *"Prove your edge before you deploy a rupee."* Domain check + handle lock (pramaan.app / pramaan.dev) | `README.md`, `AGENTS.md` | Both |
| 0.7 | Repo hygiene: `.gitignore` (no data bulk), `SECURITY.md`, `privacy-policy.md`, `terms-of-service.md`, `LICENSE` (Apache 2.0 kept) | repo root | Meet |
| 0.8 | Backfill `docs/03_unit3_testing/` (test plan, golden fixtures, log) + `docs/04_unit4_redesign/` (OOS decay, stability) | `docs/` | Meet |

**Gate G0 (Oct 17 EOD):** `pytest` green (≥12 tests) · `experiments/experiment_log.csv` on disk · charts regenerated · all blockers fixed.

---

### Phase 1 — API Contract & Backend · Oct 17–18 · (~10 h) · **CRITICAL PATH**

| # | Task | Files | Owner |
|---|---|---|---|
| 1.1 | Define API contract (JSON schemas) — `POST /run`, `GET /strategies`, `GET /universe`, `POST /validate`, `GET /health` | `docs/api-contract.md` | Aayush |
| 1.2 | FastAPI app wrapping engine; engine adapter dict→dataclass | `src/api/main.py`, `src/api/schemas.py`, `src/api/adapter.py` | Aayush |
| 1.3 | Response: equity curve, metrics, **cost breakdown per component**, trade ledger, DSR p-value, CPCV/PBO, `run_id` hash | `src/api/` | Aayush |
| 1.4 | Run persistence (SQLite) + result cache keyed by request hash | `src/api/db.py` | Aayush |
| 1.5 | Determinism test: same request → byte-identical equity curve | `tests/test_api.py` | Aayush |
| 1.6 | **Replay/demo mode**: `DEMO_DATA=1` forces cached dataset, no network | `src/api/` | Aayush |

**Request schema (freeze this Day 1):**
```json
POST /run
{ "strategy":"sma", "params":{"fast":20,"slow":50},
  "universe":["RELIANCE.NS"], "start":"2019-01-01","end":"2024-12-31",
  "initial_capital":100000, "apply_costs":true, "demo_mode":false }
```
**Gate G1 (Oct 18 EOD):** `uvicorn src.api.main:app` up; `curl POST /run` returns full JSON with real NSE data; determinism test passes; replay mode works offline.

---

### Phase 2 — Frontend Core · Oct 18–20 · (~20 h)

| # | Task | Files | Owner |
|---|---|---|---|
| 2.1 | Next.js 15 scaffold + Tailwind + shadcn/ui; dark-first finance theme; mono numerals | `frontend/` | Meet |
| 2.2 | Design tokens: green `#0ECC71` / red `#FF4D4F` / indigo `#5B6BC0` / slate surfaces | `frontend/app/globals.css` | Meet |
| 2.3 | Run form: strategy, params (dynamic), universe, dates, capital, costs toggle | `frontend/app/run/` | Meet |
| 2.4 | **Profit Mirage hero**: costs ON/OFF equity overlay + ₹/% cost-drag callout | `frontend/components/ProfitMirage.tsx` | Meet |
| 2.5 | Charts (Recharts): equity curve, underwater drawdown, **cost waterfall**, 2D param heatmap, IS/OOS overlay | `frontend/components/charts/` | Meet |
| 2.6 | DSR + CPCV/PBO verdict badge (traffic-light) | `frontend/components/VerdictBadge.tsx` | Meet |
| 2.7 | Trade ledger table + per-trade cost breakdown | `frontend/components/TradeLedger.tsx` | Meet |
| 2.8 | Run history (SQLite-backed) + save/results browser | `frontend/app/history/` | Meet |

**Gate G2 (Oct 20 EOD):** Full run flow works in browser against local API; Profit Mirage toggle renders real before/after; all 5 charts render; dark theme looks product-grade in screenshot.

---

### Phase 3 — Deploy & Landing · Oct 20–21 · (~10 h)

| # | Task | Owner |
|---|---|---|
| 3.1 | Deploy FastAPI → Fly.io; Next.js → Vercel; **live URL** | Aayush |
| 3.2 | Landing page `/`: hero, one-liner, 4 features, screenshots, GitHub link, install CTA | Meet |
| 3.3 | Loading skeletons, empty states, error states (human copy + recovery action) | Meet |
| 3.4 | Online/offline + "replay demo" banner | Meet |
| 3.5 | `.env` / OS keyring BYOK data-key plumbing | Aayush |
| 3.6 | `README.md` product-grade: what it is, live demo link, install, BYOK, license, disclaimer | Meet |

**Gate G3 (Oct 21 EOD):** Live URL performs a full backtest from a phone browser; landing page presentable to an examiner.

---

### Phase 4 — Desktop, OSS & Freeze · Oct 21–22 · (~14 h) · **CODE FREEZE Oct 22 23:59**

| # | Task | Owner |
|---|---|---|
| 4.1 | Tauri v2 wrap (pointing at deployed API; local sidecar optional) | Meet |
| 4.2 | Build binaries: MSI (Win), AppImage + DEB (Linux); DMG if time | Meet |
| 4.3 | GitHub repo public; branch `main` = stable; squash + clean history | Aayush |
| 4.4 | CI: GitHub Actions — pytest + frontend build + Tauri build on tag | Aayush |
| 4.5 | Publish releases `v0.1.0-alpha.1` with binaries + checksums | Meet |
| 4.6 | **Record 90-second demo video** (local desktop, live URL, GitHub, landing) | Both |
| 4.7 | **Fallback decision gate** — see §6 | Both |

**Gate G4 (Oct 22 23:59):** `git tag v0.1.0-alpha.1` pushed; GitHub Releases page has binary; desktop binary runs on demo laptop; video saved locally + cloud.

---

### Phase 5 — Defense & Submission · Oct 23–25 · (~16 h) · NO NEW CODE

| # | Task | Owner |
|---|---|---|
| 5.1 | Report: department format — certificate, declaration, acknowledgement, **reflections**, abstract, TOC, LoF/LoT | Meet |
| 5.2 | Chapters: Ch.1 literature/problem · Ch.2 SRS+design+safety+cost · Ch.3 **implementation incl. product/deployment** · Ch.4 redesign (4 redesigns + OOS decay) · Ch.5 results+conclusion+future scope | Both |
| 5.3 | Architecture/figures: 4-layer stack, signal→fill timeline, cost waterfall, IS/OOS+embargo, deployment diagram (Next→API→engine→Supabase) | Aayush |
| 5.4 | PPTX 15–18 slides incl. deployment + live-URL slide | Meet |
| 5.5 | **Team evidence:** Meet commits (frontend/Tauri/report) via PR; signed task log in appendix | Both |
| 5.6 | Rehearse demo twice, each member demos the other's subsystem | Both |
| 5.7 | Submission day kit: printed report, PPTX on pen drive + cloud, laptop charged, APK/binary on laptop, video backup | Both |

**Gate G5 (Oct 26 10:30):** submitted with report + PPTX + live demo + video backup.

---

## 4. Effort Summary

| Phase | Est. hours | Deadline | Gate |
|---|---|---|---|
| 0 Foundation & real data | 14 | Oct 17 | G0 |
| 1 API + backend | 10 | Oct 18 | G1 |
| 2 Frontend core | 20 | Oct 20 | G2 |
| 3 Deploy + landing | 10 | Oct 21 | G3 |
| 4 Desktop + OSS + freeze | 14 | Oct 22 | G4 |
| 5 Defense & submission | 16 | Oct 25 | G5 |
| **Total** | **~84 h** | | |

That's ~42 h/person over 10 days, plus Track A's ~14 h already counted inside Phase 0/5. **Feasible only with strict gate discipline** — if a gate slips, cut scope at the *next* gate, never at submission.

---

## 5. Risks & Mitigations

| # | Risk | Impact | Mitigation |
|---|---|---|---|
| R1 | Frontend not demo-ready by Oct 22 | Fatal to Track B | Gate G4 fallback → Streamlit build (keep it working) |
| R2 | Network dies in projector room | Demo fails | Recorded video + replay/cache mode + live URL on phone |
| R3 | Tauri packaging fails on Windows | Desktop demo fails | Build on Linux (demo laptop); record video of desktop |
| R4 | Supabase adds latency/risk | Fatal | SQLite local-first; Supabase Phase 2+ only, never in demo path |
| R5 | yfinance blocked at runtime | No fresh data | Cache + replay mode; committed dataset |
| R6 | Examiner: "what did *you* build?" | Marks | Engine is the answer — show Python source; product = delivery vehicle |
| R7 | Examiner: "who did what?" (29/0 git) | Marks | Meet commits via PR + signed task log + cross-defense |
| R8 | Scope creep (mobile, live trading, AI) | Fatal | Hard out-of-scope list (§1); state it in report + viva |
| R9 | Vibecoded frontend, can't explain it | Marks | Meet must be able to explain every screen + flow in his own words |
| R10 | Claiming "deployed" while broken | Fatal | Only claim what works: live URL, run binary, real results |

---

## 6. Fallback & Decision Gates

| Gate | Date | Question | If NO → |
|---|---|---|---|
| G1 | Oct 18 | Does the API return a full backtest with real data? | Fix engine adapter only; do NOT start frontend |
| G2 | Oct 20 | Does the UI flow work end-to-end locally? | Drop run history + half the charts; keep run + 3 charts |
| G3 | Oct 21 | Is the live URL working? | Deploy Vercel only; drop Fly.io (API stays local for demo) |
| G4 | Oct 22 | Does the desktop binary run on the demo laptop? | **Fallback to Streamlit** for the live demo; keep URL+GitHub as product proof |
| G5 | Oct 26 | Is everything reproducible? | Present from cached data + video only |

**Fallback artifacts to keep alive all week:** working Streamlit app (`src/dashboard/app.py`), cached dataset, recorded video.

---

## 7. Demo Run-Sheet (5 minutes, in order)

| # | Element | Proof of |
|---|---|---|
| 1 | Desktop app on laptop → run NIFTY-50 SMA → results render | Product works |
| 2 | **Profit Mirage** costs ON → OFF; equity flips sign; ₹ cost drag | Core differentiator |
| 3 | Cost waterfall (STT/GST/stamp/turnover/slippage per trade) | Indian realism, unique |
| 4 | DSR + CPCV/PBO verdict badge | Overfitting honesty, unique |
| 5 | Show **Python engine source** — T+1 invariant, cost math | *This is the actual contribution* |
| 6 | Live URL (phone browser) → same run | **Deployed** |
| 7 | GitHub repo → releases → binaries | **Open source + distributed** |
| 8 | Landing page | **Positioned product** |
| 9 | Show `experiments/experiment_log.csv` + IS/OOS decay | Real results, reproducible |

If network fails → play recorded video at step 1, then continue from cached data.

---

## 8. Definition of Done (Oct 26, 10:30)

- [ ] Live URL performs a real backtest (`quantlab.<domain>`)
- [ ] Desktop binary runs on the demo laptop
- [ ] GitHub repo public with `v0.1.0-alpha.1` release + binaries
- [ ] Landing page live with GitHub + install links
- [ ] `experiments/experiment_log.csv`, IS/OOS decay table, parameter-stamped charts committed
- [ ] `pytest` green ≥ 12 tests; `scipy` pinned; RSI + rate-card fixed
- [ ] Report in department format (certificate, declaration, acknowledgement, **reflections**)
- [ ] PPTX 15–18 slides, includes deployment + architecture diagrams
- [ ] Both members present; each demos and defends a different subsystem
- [ ] 90-second video backup on laptop + cloud
- [ ] Privacy policy + terms + no-advice disclaimer published
- [ ] Scope boundaries stated explicitly (no live trading, no mobile, no intraday)

---

## 9. Product Identity (FROZEN — do not change without a decision note)

| Field | Value |
|---|---|
| **Name** | **Pramaan** (प्रमाण — "proof / evidence") |
| **One-liner** | The honest backtesting engine for Indian equities — zero look-ahead, real statutory costs, overfitting-proof. |
| **Tagline** | *"Prove your edge before you deploy a rupee."* |
| **Viva story** | *"Pramaan means proof in Hindi. Before you deploy a single rupee of capital, our engine gives you the proof — or disproves the illusion."* |
| **Why this name** | Indian-native (examiner-friendly), states the thesis in one word, distinct from Western competitors, short and brandable |
| **Positioning** | Open-source engine + deployed product; B2B diagnostics for RIAs/prop desks; students free |
| **License** | Apache 2.0 (engine, unchanged) |

## 10. First 48 Hours (do these before anything else)

1. **Run the real-data matrix** — unblocks demo, report, cache, and charts. *(Phase 0.1)*
2. **Fix the 4 blockers** — scipy, RSI, rate card, rf-rate. 30 min of work. *(0.2–0.4)*
3. **Lock handles** — pramaan.app / pramaan.dev / GitHub org + README already renamed to Pramaan. *(0.6 — done)*
4. **Freeze the API contract** — write `docs/api-contract.md` before any UI code. *(1.1)*
