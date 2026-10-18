# QuantLab — Product Reimagination Report

**Prepared:** 2026-10-16 · **Repo:** `/mnt/work/projects/Quantlab` @ `feat/v2-architecture`
**Context:** GTU DI05000341 Sem-5 Minor Project (submission 26/10/2026) → launchable real product
**Method:** Full source inspection of all `src/` modules + web market research (9 subagent roles). Facts are cited to file paths. Research-sourced claims cite URLs. Anything unverifiable is marked UNKNOWN.

---

## 1. Executive Summary

QuantLab is a genuine, working, event-driven backtesting engine for Indian equities (~1,008 LOC `src/`, 9/9 tests passing). Its core value is **"honesty"**: zero-lookahead T+1 execution (`backtest_engine.py`), the full Indian statutory cost stack (`cost_model.py`), and institutional-grade overfitting diagnostics — Deflated Sharpe Ratio (`deflated_sharpe.py`) and Combinatorial Purged Cross-Validation with embargo (`cpcv.py`).

**But it is not a product.** The market for backtesting SaaS is a red ocean dominated by TradingView (free, 100M users), MetaTrader (free + brokers), AmiBroker ($299 once), and Indian players AlgoTest (25 free backtests/week) and Zerodha Streak (₹500–1,400/mo). Retail willingness-to-pay in India is ₹0–500/mo. A paid retail backtester currently fails on data rights (`yfinance` is not licensed for commercial redistribution), breadth (3 strategies, daily bars, equities-only), and UI (64-line Streamlit MVP).

**The defensible wedge is narrow but real.** Research found a concrete market gap: (1) no global tool models Indian statutory costs; (2) DSR+CPCV overfitting diagnostics are almost absent from retail/commercial tools; (3) users' #1 complaint is "backtests lie" (lookahead, unrealistic fills, hidden costs). QuantLab already solves all three in code.

**Recommendation:** Keep the Apache 2.0 engine as an open-source "honest backtest engine for India" — this maximizes academic marks and adoption. Monetize a thin freemium B2B/SaaS layer targeting SEBI-registered Investment Advisors (RIAs) and small prop desks who need cost-inclusive, overfitting-validated backtesting for compliance. Realistic year-1 revenue: ₹3.6–12 lakh/yr — a niche B2B business, not a unicorn. Ship desktop-first (PyInstaller wrapping the existing Python/Streamlit app) + optional PWA. **No backend, no live execution, no native mobile rewrite in v1.**

For the academic deliverable, follow `.agent/quantlab_eval_strategy.md` (Plan B): fix 4 critical gaps by Oct 26 without breaking the v2 architecture → predicted CA 34/50 → 44–47/50.

---

## 2. What the Repository Currently Is

| Dimension | Finding (evidence-based) |
|---|---|
| **What** | Event-driven backtesting engine + overfitting diagnostic platform, NSE cash equities, daily bars, long-only |
| **Architecture** | 4-layer: Dashboard (Streamlit) → Analytics → Engine → Data/Strategies (`QuantLab_Project_Documentation.md:120-148`) |
| **Core strength** | Zero-lookahead T+1 (signal t Close → fill t+1 Open) enforced by construction and tested (`backtest_engine.py:31-63`; `test_engine.py` asserts fill at Open 105.0) |
| **Cost model** | Full Indian stack: STT 0.1% both sides, stamp 0.015% buy-only, GST 18%, NSE 0.00297% + SEBI 0.0001%, brokerage min(20,0.03%), Almgren-Chriss √ impact capped 5% (`cost_model.py`) |
| **Diagnostics** | DSR (`deflated_sharpe.py`, skew/kurtosis-adjusted), CPCV + embargo with AR(1) leakage proof (PBO 28.89%→37.78%, `cpcv.py`, `test_cpcv.py`), 2D parameter stability (`validation.py`) |
| **Strategies** | SMA crossover, Wilder RSI mean-reversion, ROC momentum — all with position guards |
| **Data** | yfinance fetch, drop-NaOH (no forward-fill), 10-symbol universe + Nifty 50 benchmark |
| **UI** | Streamlit `app.py` (64 lines) + `components.py` (3 Plotly charts). `plot_2d_heatmap` exists but is **never called**; DSR/waterfall/IS-OOS unwired |
| **Tests** | 9/9 pytest PASS. No tests for SMA/RSI/data layer |
| **Quality** | Code quality 8/10, clean layering, meaningful asserts. No lint, no type hints, no CI |
| **Team** | 2-person on paper; **29/0 git commit split** (single author) |
| **Stage** | ~70% weighted completion; `experiments/` empty, `data/raw/` absent, no real-data run on disk |

**Verdict:** A technically strong diploma prototype, ~40% of the way to a launchable product.

---

## 3. What It Could Become

Three credible directions, ranked by fit:

| # | Direction | Thesis | Assessment |
|---|---|---|---|
| 1 | **Open-source honest-backtest engine for India** (recommended) | Permissive engine; T+1, full NSE cost+impact ledger, DSR/CPCV out-of-box. Compete with dormant Backtrader (GPL) and AGPL backtesting.py — not TradingView | **Best fit.** Max academic marks, real adoption path, Apache 2.0 keeps commercial door open |
| 2 | **Pre-live audit layer for existing algo-tool users** | Upload TradingView/Streak/AmiBroker strategy params → audit against Indian costs + overfitting before going live | Strong secondary; no execution risk, no data wars |
| 3 | **Quant-education companion** | "Why backtests lie" curriculum: lookahead lab, cost lab, DSR lab | Adoption funnel + academic; not standalone revenue |

**Not viable today:** head-on commercial SaaS, live execution, retail app. See §28 Final Verdict.

---

## 4. Market Research (summary — full table in research)

- **Global backtesting is captured.** TradingView (free tier → $155–2,399/yr), MetaTrader (free + brokers), AmiBroker ($299–499 one-time), TrendSpider ($648–2,568/yr, no free tier), QuantConnect/LEAN (free tier, $ for compute).
- **India is captured too.** AlgoTest (₹1/backtest, 25 free/week, 60+ brokers), Zerodha Streak (₹500–1,400/mo, broker-locked), Sensibull (free/₹392–1,300, options-only, no backtest), Tradetron/AlgoBulls (₹300–1,180/mo).
- **Open-source tier is stagnant/encumbered.** Backtrader (22k★, dormant since 2024), Zipline (20k★, abandoned), backtesting.py (AGPL — blocks closed SaaS), VectorBT (Commons Clause). A permissive, maintained, India-aware engine is a welcome gap.
- **Algo-trading market** $20–26B (2026) but that is institutional+infra revenue; retail monetizes via brokerage, not backtest fees. Retail algos grow fastest (8.3% CAGR) yet won't pay for backtests when alternatives are free.
- **Sources:** tradingview.com/pricing; trendspider.com/pricing; amibroker.com/order.html; quantconnect.com/pricing; github.com/mementum/backtrader (22,423★, last push 2024-08-19); zerodha.com; docs.algotest.in; reddit.com/r/algotrading.

---

## 5. Competitor Analysis

| Competitor | Platform | Pricing | Their weak spot (our wedge) |
|---|---|---|---|
| TradingView + Pine | Web/desktop/mobile | Free → $155–2,399/yr | No Indian cost model, no DSR/CPCV, lookahead-prone pine |
| TrendSpider | Web/mobile | No free tier, $648+/yr | US-centric, no NSE costs, 2.5× TV cost |
| MetaTrader 5 | Desktop/web/mobile | Free via brokers | FX/CFD-centric; tester complaints (skipped trades, holiday shifts); no Indian costs |
| AmiBroker | Windows only | $299–499 once | No Indian costs/DSR; Windows-only |
| QuantConnect/LEAN | Cloud + OSS | Free → custom $$ | Opaque pricing; overkill for daily NSE; no India presets |
| AlgoTest | Web/mobile | ₹1/backtest, 25 free/wk | Options-centric, no overfitting rigor, credit UX confusing |
| Zerodha Streak | Web/mobile | ₹500–1,400/mo | Broker-locked, no-code, no DSR/CPCV |
| Backtrader / Zipline / backtesting.py | Python libs | Free OSS (dormant/GPL/AGPL) | Frozen code, no India costs, licensing friction |

---

## 6. Market Gap

Evidence-backed, specific gaps:

1. **Cost honesty for NSE cash equities** — no global or Indian tool models STT+GST+Stamp+Turnover+SEBI+market-impact at backtest time. Confidence: high.
2. **Overfitting diagnostics in retail/advisor tools** — DSR + CPCV/PBO almost absent from TradingView/Streak/AlgoTest. Confidence: high.
3. **Zero-lookahead by construction** — most tools assume close-fills; off-by-one is "killers #1" in user forums. Confidence: high.
4. **Overfit/regime blindness everywhere** — 6-month intraday windows = single regime; no walk-forward exposed. Confidence: medium.
5. **Licensing clean-room** — GPL/AGPL/Commons-Clause encumbers honest engines. A permissive one is differentiated. Confidence: high (license text verified).

---

## 7. Product Positioning

**Positioning statement:**
> QuantLab is the open-source honest backtesting engine for Indian equities that proves whether a strategy survives real statutory costs, slippage, and overfitting before a rupee is deployed — for advisors, prop desks, and quant students who refuse to let backtests lie.

**Name:** QuantLab (retained — zero rename cost, already in LICENSE/GTU records). **Codenames:** *Satyam* (truth).

**What it is NOT:** not a live trading platform; not a broker app; not a general charting platform; not a strategy marketplace; not a consumer subscription; not Indian-equity-proprietary even after monetization.

---

## 8. Target Users

| Segment | Role | Why |
|---|---|---|
| **Primary (pays)** | SEBI RIAs, Research Analysts, small prop desks trading NSE cash equities | Compliance needs honest, cost-inclusive, overfitting-validated backtests. Willingness ₹799–2,999/mo |
| **Secondary (free tier)** | Quant students, finance faculty, serious retail traders | Adoption funnel, academic pipeline, brand |
| **Explicitly excluded** | HFT, options/futures traders, crypto, global-equities users, price-sensitive retail | Out of scope for v1 |

---

## 9. Product Vision

**Philosophy:**
1. Backtests must not lie.
2. Indian equities first — that's the moat.
3. Simulation, not execution.
4. Open engine, paid diagnostics/service/data.
5. Decisive scope — daily bars, cash equities, NSE only, long-only.

**USP:** the only zero-lookahead T+1 + full Indian statutory cost + Almgren-Chriss impact + DSR/CPCV overfitting diagnostics, open source, for NSE cash equities.

---

## 10. Feature Architecture

- **Engine:** BacktestEngine (T+1), Portfolio (cash≥0, double-entry), Position (long-only + realized/unrealized split), IndianCostModel (broker→STT→stamp→turnover→GST→impact).
- **Strategies:** SMA, RSI, Momentum (long-only, guards against duplicate signals).
- **Analytics:** Metrics (Sharpe/Sortino/Calmar/MDD/CAGR), DSR, CPCV+embargo, 2D stability grid.
- **UI:** Streamlit single-page today; target = Dashboard + Advanced (grid, CPCV, IS/OOS) + Settings.
- **New (product):** demo/deterministic fixtures, Parquet cache, SQLite run history, cost-breakdown waterfall chart, run reproducibility (`run_id`, cost-model version), CLI wrapper.

---

## 11. P0 / P1 / P2 / CUT Prioritization

**P0 (launch-blockers):** real-data run pipeline cache + fix missing `scipy`; empty/error/loading states replacing `st.stop()`; DSR badge; wire existing `plot_2d_heatmap`; cost-breakdown waterfall + Profit Mirage ON/OFF overlay; run metadata (run_id/params/cost-version) persisted; deterministic fixtured test data; lint/typecheck/CI.

**P1 (next):** IS/OOS comparison tab; dashboard CPCV/PBO panel; run-history browser (SQLite); cost-model metadata + SEBI rule versioning; RSI `down==0` bug fix; parameter validation (`fast<slow`); packaging via `pyproject.toml`.

**P2 (later / commercial):** multi-user workspaces; PDF/report export; commercial data source replacing yfinance; saved templates; desktop + web client; RIA/quotation workflows; pointers to alternative data sources.

**CUT (do not add):** live trading/broker integration; native mobile app v1; cloud backend v1; custom auth (local-only); strategy marketplace; options/futures; intraday/tick data; AI assistant; headline gimmicks.

---

## 12. UX Architecture

Target user journey (full detail in `UX_ARCHITECTURE.md`): **First Launch** (empty state + data load or use bundled demo) → **Onboarding** (3-step, skip-able: what QuantLab does, "Profit Mirage", run first backtest) → **Live demo** ("Profit Mirage" ON/OFF toggle with T+1 invariant proof) → **Advanced workflow** (2D stability heatmap, CPCV/PBO) → **Settings** (data source, cost-model version, universe, initial capital) → **Errors** (every error has a recovery action; no stack traces) → **Empty/loading/offline** states designed; **Recovery** (corrupt cache → reset).

**Priority P0:** replace `st.stop()` with designed empty state + CTAs; DSR badge; wire the dead heatmap; Profit Mirage overlay; dark theme. Full journey + copy in `UX_ARCHITECTURE.md`.

---

## 13. Platform Strategy (most important draft decision)

**Core stays local + Python.** Recommended stack:
- **Desktop** (Windows/Linux/macOS) = PyInstaller/Briefcase wrapping existing Streamlit UI — **only new dependency is packaging**; zero engine rewrite. Native mobile requires engine rewrite → rejected v1.
- **Web** (Streamlit Cloud demo + PWA) = reach extension.
- **CLI** = thin CLI + Streamlit GUI sharing one codebase.

**Where computation runs:** 100% local. Public yfinance data → Parquet cache; no backend needed (no broker, no multi-user, no proprietary data). Full justification in `PLATFORM_STRATEGY.md` / `ARCHITECTURE.md`.

---

## 14. Technical Architecture (summary — full in ARCHITECTURE.md)

**Decision:** no backend, no cloud DB, no remote auth. Client: desktop Streamlit/PyInstaller. Store: local **SQLite** (run metadata + config) + **Parquet** (market data). API: local CLI + GUI. Computation: 100% client. CI: GitHub Actions (ruff + mypy + pytest + pip-audit). Backup: file copy of cache + export/import. Versioning: SemVer; cost-model version stored per-run. Feature flags: JSON config.

**Computation-location rationale:** public data, no broker, daily bars, small universe, data residency. Moving to server would add cost/latency with zero benefit.

---

## 15. AI Architecture — NOT applicable for v1

There is no compelling AI feature. QuantLab's value is deterministic math and honesty. **CUT:** AI assistant. Possible future (P3+): NLP on strategy parameters, or LLM explanation of metrics — only if a real user problem appears. Do not add an LLM chatbot.

---

## 16. Security & Privacy (summary — full in SECURITY.md)

- **P0 blockers:** yfinance is an unofficial scraper, **not licensed for commercial redistribution** → must use licensed data source or restrict Free to academic/personal use; **`scipy` is missing from `requirements.txt`** (broken install) → add pinned dep.
- **Threats:** local plaintext data files (`data/raw/*.csv`), MITM on yfinance fetch, dependency/typosquat risk, Streamlit parameter input (no validation), unscienced strategy code execution.
- **No auth for v1** (single-user local). If adding multi-user: OS keyring, JWT+RBAC, TLS, MFA.
- **Privacy:** PDP Act / GDPR — QuantLab processes no personal data; publish privacy policy, data-retention, account-deletion documentation before any user-facing release.

---

## 17. Data Architecture

OHLCV schema as specified in documentation. Store Parquet + SQLite. Existing `data/fetch.py` and `data/clean.py` work, but need incremental fetch + fallback when offline + schema validation. Clean task should document adjusted vs adjusted-close policy (no forward-fill).

---

## 18. Monetization (summary — full in MONETIZATION_STRATEGY.md)

**Bottom line:** do not build a B2C retail subscription. Compete in B2B diagnostics.
- **Free:** full OSS engine + UI; 3 strategies; single-stock daily backtest; no commercial data; personal/academic use.
- **Pro (~₹299/mo, $9/mo):** full Indian cost model, DSR + CPCV/PBO, parameter-stability heatmaps, 20-symbol universe, PDF export, commercial-grade data source.
- **Team (~₹799/mo, $29/mo per seat):** shared workspaces, branded reports, run history, audit log, priority support — for RIAs/RAs/prop desks.
- **Enterprise (₹15k–25k/yr, $400–700/yr):** self-hosted on-prem, SLA, SSO, API, indemnification.

**Apache 2.0 stays** (commercial-compatible). **Realistic Year-1:** 15–40 paying accounts → ₹3.6–12 lakh/yr. Break-even ~8–12 Pro subs. Replace `yfinance` before charging.

---

## 19. Production Infrastructure

GitHub Releases + PyPI (library) + desktop installers + Streamlit Cloud demo. CI via GitHub Actions. Observability: structured logging; Sentry (opt-in). Update: GitHub Release check + signed artifacts. Backup: local copy. Policy: privacy-v1.md, terms-of-service, no-advice disclaimer.

---

## 20. Testing & QA (summary — full in QA_RELEASE_ENGINEERING.md)

- **Missing tests:** SMA, RSI, data layer, integration, property-based, determinism. **Add these.**
- **CI gate:** ruff + mypy + pytest (>80% cov) + pip-audit.
- **Release channels:** Alpha/Beta/Stable; SemVer; checklist includes scipy fix, chart provenance, disclaimer.
- **Play Store:** not viable v1 (Python/Streamlit desktop); requires full rewrite. See §21.
- **Desktop packaging:** Briefcase or PyInstaller + platform installers. See §22.
- **Blockers:** scipy missing, no CI, no SMA/RSI/data tests, `st.stop()` UX bug.

---

## 21. Play Store Strategy — NOT v1

There is no realistic Play Store path without a native rewrite or a backend. **Recommendation:** no native Android in v1. If later, options = TWA wrapper (Android-only) or thin client + FastAPI backend (contradicts "no backend"). Revisit after product-market fit.

---

## 22. Desktop Distribution

Packaged desktop app is the primary commercial artifact. Recommended tools/types:
- Windows: MSI/EXE (Inno Setup/NSIS)
- Linux: AppImage + DEB
- macOS: DMG (notarized)
- Toolchain: Briefcase (BeeWare) or PyInstaller + platform installers
- Updates: GitHub Releases + optional banner check; signed artifacts

Caveat: Streamlit-in-installer is awkward. If a polished GUI matters, migrate to a desktop framework (e.g., PySide6) — but that's P2. v1 = wrap existing Streamlit.

---

## 23. Minor Project / Academic Strategy (summary — full in .agent/quantlab_eval_strategy.md)

**Predicted CA today: 34/50 (B, High risk). Target 44–47/50 (A) without compromising the engine.**

Three critical gaps to close by Oct 26:
1. **Real-data run evidence** — run `scripts/run_experiments.py` + `run_pbo_experiment.py` on NIFTY-50 2019–2024; commit `experiments/experiment_log.csv`, IS-vs-OOS decay table, parameterized charts; backfill empty `docs/03_unit3_testing/` + `docs/04_unit4_redesign/`.
2. **Team evidence** — fix 29/0 split: Member 2 commits dashboard wiring or chapters via PR; OR signed task log. Both rehearse cross-defense.
3. **Unit 5 formalities** — full chapters, certificate/declaration/acknowledgement/reflections, PPTX, safety note, ₹0 cost sheet, originality clearance.

**Demo spine:** Profit Mirage (costs ON/OFF), golden-master paisa calc, embargo PBO 28.89→37.78%, zero-lookahead walkthrough. Both members present; each demos the other's module.

**Risks to neutralize:** one NSE rate card (0.00297 not 0.00345), risk_free=0.06, RSI all-gains (RSI=100), add `scipy`.

---

## 24. Implementation Roadmap (prioritized)

| Phase | Focus | Key work | Exit criteria |
|---|---|---|---|
| **0** | Repo cleanup / real-data proof | Run matrix, commit `experiments/` + charts + decay table; backfill `docs/03/04/`; fix scipy, RSI, rate-card, rf-rate | C1/C2/C3 action items done; CA ≥ 40/50 |
| **1** | Production foundation | Parquet cache; Parquet/CSV tested; CLI; `pyproject.toml`; lint/typing/CI; data schema validation | CI green; scipy pinned; deterministic fixture demo |
| **2** | Core MVP polish | Empty/error/loading states; DSR badge; wire heatmap; cost waterfall + Profit Mirage; run metadata | serious-product credibility achieved |
| **3** | Desktop packaging | Briefcase/PyInstaller build; CLI packaging; installers for Win/Lin/Mac | one build + install smoke test |
| **4** | Cloud/commercial layer (if pursuing) | Replace yfinance with licensed data; auth (JWT+RBAC); multi-user workspaces; PDF reports; Stripe billing | legal data + policy; first paid pilot |
| **5** | Web/PWA demo | Streamlit Cloud + PWA manifest | accessible demo link |
| **6** | Testing/security | property tests, integration, pip-audit, privacy-policy/ToS, ethics review | release checklist P1 pass |

**Sequencing rule:** Oct 16–22 = Phase 0 (code freeze Oct 22). Oct 23–25 = report/PPTX/rehearsal. After Oct 26, continue Phases 1+ in parallel with academic maintenance.

---

## 25. Risk Register (top 10)

| Risk | Impact | Mitigation |
|---|---|---|
| yfinance legal/data cost | Critical | Licensed data or academic-free only; legal review |
| Red-ocean positioning | High | Win niche via honesty/education/B2B diagnostics; do not fight TradingView |
| Scope creep (live/FnO/intraday) | High | Hard scope; one feature per phase |
| Team evidence (29/0) | High (CA) | PR + task log + cross-defense |
| No real-data artifacts on disk | High (CA) | Run matrix + commit artifacts (Action #6) |
| Architecture mismatch (Streamlit as product) | Medium | Accept for academic/demo; migrate GUI later |
| Missing scipy / unpinned deps | Medium | Fix now; pip-audit in CI |
| RSI bug / rate-card inconsistency | Medium | Fix + regression tests |
| monetization delay until legal data | Medium | Monetize service/reports/education first |
| Single-person bandwidth | Medium | ruthless prioritization; one owner per phase |

---

## 26. Estimated Development Complexity

- **Keep as-is:** engine (well-built, event-driven, tested)
- **Fix in hours:** scipy, RSI, rate-card, rf
- **Small effort (days):** tests SMA/RSI/data, CLI, Parquet cache, CI, UX states, cost waterfall, Profit Mirage overlay
- **Medium (2–4 weeks):** parameter-stability UX, run-history SQLite, dtype/lint/typecheck, desktop packaging
- **Large (1–3 months):** multi-user auth, licensed data, PDF/report export, workspaces
- **Massive (months, avoid v1):** live execution/broker integration, intraday engine, full cross-platform GUI rewrite

---

## 27. "What I Would Build If This Were My Product"

**Would build:** a high-integrity, desktop-first, local+OSS diagnosis engine:
- Locked invariants (cash≥0, T+1, no look-ahead; continuous assertions).
- Reproducible backtests: `run_id` = hash(sorted inputs + library versions + universe filter), cached results, deterministic.
- Config as code (YAML); universe/data filters; parameter sweeps + walk-forward validation.
- A composite **credibility score** using DSR + CPCV/PBO + parameter stability + cost drag; the "Profit Mirage" moment as product identity.
- Reports: HTML/PDF with per-trade cost breakdown; audit-friendly.

**Would NOT build:** live trading; strategy marketplace; native mobile; cloud backend for v1; AI assistant.

---

## 28. Final Verdict

QuantLab is a rare, honest diploma prototype with a real wedge. **Keep the engine. Fix the gaps. Monetize B2B diagnostics. Don't try to be TradingView.** Market research says the space is captured by free/low-cost incumbents — but not for Indian equity honesty and overfitting validation. The only defensible product v1 is: **an open-source engine, packaged for desktop, with a thin B2B/education layer that sells compliance-grade, overfitting-validated diagnostics.** For GTU marks: this path is *both* the best academic and product path.

---

## THE PRODUCT I WOULD ACTUALLY BUILD

**Working title:** QuantLab — *honest backtesting engine for Indian equities* (Apache 2.0, codename Satyam).

**Definition:** A local-first, zero-lookahead backtesting engine and overfitting diagnostic platform that answers one question honestly: "After real Indian taxes, slippage, and validation against multiple-testing bias, does this strategy survive?" — target users: SEBI RIAs/prop desks (paid), quant students (free).

**Architecture (single codebase, three surfaces):**
```
┌──────────────────────── CORE (unchanged, ~1,008 LOC) ────────────────────────┐
│ Engine (T+1, cost model, Almgren-Chriss)   · Analytics (DSR, CPCV, metrics)   │
│ Strategies (SMA/RSI/Momentum)            · Data (fetch→cache, universe)      │
└───────┬──────────────────────┬───────────────────────────┬────────────────────┘
        │                      │                           │
   CLI (quantlab            Streamlit GUI               Engine as library
   fetch/run/report/validate)  (arrow in v1)               (pip install quantlab)
        │                      │                           │
   Scripts / automation     Desktop via PyInstaller      Jupyter / education
                           (Windows/Linux/macOS)        (free, adoption)
        └──────────────────────┴───────────────────────────┘
                 Local Parquet cache + SQLite run-history
```

**Rules:**
1. **Invariants enforced, not asserted.** Portfolio.cash ≥ 0; no signal from data > t; strategy params validated in constructors; cost model unit-tested per component; deterministic (seeded, same inputs→same equity).
2. **Reproducible by construction.** Every run stores `run_id` = hash(strategy+params+dates+universe_filter+library_versions). Re-runs against same data = bit-identical.
3. **Honesty by default.** Costs ON; DSR + CPCV always computed; Profit Mirage overlay is the UI's identity.
4. **India-specific moat.** NSE equity cost stack (STT/GST/Stamp/Turnover/SEBI + AC impact) and overfitting diagnostics are the product. Do not chase breadth (no FnO, no intraday, no live execution in v1).
5. **Local-first, no backend.** Public yfinance→Parquet cache; compute on user's machine; sync = none. Remote backends only if multi-user demand appears.
6. **Keep Apache 2.0.** Open engine maximizes academic marks and adoption; monetize diagnostics, reports, data, and enterprise features.
7. **UX must not look like a college CRUD app.** Empty/error/loading states; replay-able runs; dark theme; Profit Mirage hero.

**Roadmap to launch (post-academic deadline):**
- **Phase 1 (2 weeks):** production foundation — `pyproject.toml`, CI, lint/typecheck, `scipy` fix, `tests` for SMA/RSI/data, Parquet cache, CLI.
- **Phase 2 (2 weeks):** desktop MVP — Briefcase/PyInstaller build; UX states; DSR badge; heatmap wired; cost waterfall; Profit Mirage.
- **Phase 3 (4 weeks):** commercial v1 — licensed data or academic-only; RIA B2B workshop-driven; PDF reports; paid tier.
- **Phase 4 (later):** web demo/PWA; workspaces; Stripe integration if B2B demand proven.

**Academic alignment:** every phase maps to GTU units (Unit 1 problem, Unit 2 architecture, Unit 3 implementation/testing, Unit 4 redesign based on evidence, Unit 5 defense). The demo spine remains Profit Mirage + golden-master paisa + embargo PBO + zero-lookahead — technically honest and impressive without gimmicks.

**One-sentence recommendation:** Keep the engine, ship it open-source and desktop-first, polish the "honesty" UX, and earn ₹299–2,999/mo from Indian advisors and prop desks — not from retail, not from app stores, and not from an AI wrapper.

---
*Companion docs (on disk): `ARCHITECTURE.md`, `SECURITY.md`, `UX_ARCHITECTURE.md`, `PLATFORM_STRATEGY.md`, `MONETIZATION_STRATEGY.md`, `QA_RELEASE_ENGINEERING.md`, `.agent/quantlab_eval_strategy.md`, `GTU_MINOR_PROJECT_REVIEW.md`, `DI05000341.pdf`.*
