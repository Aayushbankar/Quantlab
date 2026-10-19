# QuantLab — Production Architecture Document

**Product:** QuantLab — event-driven backtesting & overfitting diagnostic engine for Indian equities  
**Scope:** GTU DI05000341 Minor Project reimagination → production-grade desktop application  
**Audience:** Software architecture, engineering, product  
**Status:** Proposed (pre-implementation)

---

## 1. Executive Summary

QuantLab is a **purely local, client-side Python application** that fetches public market data (yfinance), runs an event-driven backtest in-process, computes Indian statutory costs and overfitting diagnostics (DSR, CPCV/PBO), and renders results via a Streamlit UI.

**Headline architectural decision: NO backend.** QuantLab does not need a backend API, database server, cloud sync, or authentication. All computation runs on the user's device; data is public and fetched at runtime; there is no broker integration and no live execution. Introducing a backend would add operational cost, security surface, and latency with zero functional benefit for the current scope.

Recommended stack: **Python + Streamlit + PyInstaller** (desktop-first), with optional Streamlit Cloud deployment for browser access. Data stored locally in **Parquet** (analytics) + **SQLite** (metadata/cache). Zero authentication. Offline-first. No CI/CD today; add GitHub Actions later.

---

## 2. Component Classification

Every existing file classified as KEEP / IMPROVE / REWRITE / REMOVE / NEW, with justification.

| File | Classification | Justification |
|------|---------------|---------------|
| `src/engine/backtest_engine.py` | IMPROVE | Core zero-lookahead event loop is correct and valuable. Needs type hints, input validation, structured logging, error boundaries, and config-driven parameters (currently hardcoded 10% sizing). Keep the event-loop architecture; harden production-grade. |
| `src/engine/portfolio.py` | IMPROVE | Cash >= 0 invariant and double-entry ledger are sound. Needs exception-on-negative-cash (not just print warning), position reconciliation, and thread-safety if parallelized later. |
| `src/engine/cost_model.py` | IMPROVE | Indian statutory model (STT/GST/Stamp/Turnover/Almgren-Chriss) is the core commercial moat. Keep logic; add config-driven fee schedules (SEBI rules change), unit tests for each fee component, and audit-loggable cost breakdown. |
| `src/engine/events.py` | KEEP | Immutable dataclass event definitions (Market/Signal/Order/Fill). Well-designed; no change needed beyond optional frozen=True and type refinements. |
| `src/engine/position.py` | IMPROVE | Long-only position tracking is adequate. Add short-sale guard (explicit rejection), average-price precision (Decimal), and realized/unrealized PnL separation. |
| `src/engine/order.py` | REMOVE | Duplicate of `events.OrderEvent` (same fields, different class). Consolidate into `events.py`; delete `order.py`. |
| `src/analytics/metrics.py` | IMPROVE | Sharpe/Sortino/Calmar/MDD/CAGR are correct. Add annualization-config, rolling metrics, win rate, profit factor, and NaN-safe guards. Add type hints. |
| `src/analytics/deflated_sharpe.py` | IMPROVE | DSR implementation is mathematically sound but imports `scipy.stats` which is **missing from requirements.txt** (breaks installs). Add scipy to requirements or vendor the norm.cdf/skew/kurtosis. Add input validation. |
| `src/analytics/cpcv.py` | IMPROVE | Combinatorial Purged CV with embargo is correct per López de Prado. Add path caching, progress reporting, and O(N) block-index optimization for large timelines. |
| `src/analytics/validation.py` | IMPROVE | 2D grid search works but is limited to exactly 2 params. Generalize to N-dim, add IS/OOS split, result persistence to SQLite/Parquet, and early-stop on divergence. |
| `src/data/fetch.py` | IMPROVE | yfinance fetcher works but lacks retry/backoff, rate-limit handling, incremental updates, and checksum validation. Add cache layer (Parquet), concurrent fetch, and fallback to local files when offline. |
| `src/data/clean.py` | KEEP | Clean logic (drop NaN OHLC, sort chronologically) is correct for look-ahead prevention. Add schema validation (Great Expectations/pandera-lite) and split/dividend adjustment handling. |
| `src/data/universe.py` | KEEP | 10-symbol NSE universe + Nifty 50 benchmark. Simple constants file; keep, optionally externalize to JSON/YAML for config-driven universes. |
| `src/strategies/base.py` | KEEP | Abstract Strategy interface is clean. Keep; add registry pattern for strategy discovery. |
| `src/strategies/sma_crossover.py` | KEEP | Correct SMA crossover with cross detection. Keep; add parameter validation (fast < slow). |
| `src/strategies/rsi_mean_reversion.py` | KEEP | Wilder's RSI implementation is sound. Keep; add config for oversold/overbought. |
| `src/strategies/momentum.py` | KEEP | ROC momentum with position guard. Keep. |
| `src/dashboard/app.py` | IMPROVE | 64-line Streamlit MVP. Works but lacks state persistence, run history, error handling, config, and export. Refactor into page-based multi-app with session state. |
| `src/dashboard/components.py` | IMPROVE | 3 Plotly charts (equity, drawdown, heatmap). Keep; add return distribution, rolling Sharpe, cost breakdown chart, and interactive Plotly (zoom/hover). |
| `tests/test_engine.py` | KEEP | 2 tests, pass. Keep; expand coverage. |
| `tests/test_metrics.py` | KEEP | Keep; expand. |
| `tests/test_cost_model.py` | KEEP | Keep; expand. |
| `tests/test_cpcv.py` | KEEP | Keep; expand. |
| `tests/test_portfolio.py` | KEEP | Keep; expand. |
| `tests/test_momentum.py` | KEEP | Keep; expand. |
| `requirements.txt` | IMPROVE | Missing `scipy` (required by deflated_sharpe.py). Add typing (mypy), lint (ruff/black), test (pytest), build (pyinstaller), packaging deps. Pin versions. |
| `scripts/*.py` | REVIEW | Ad-hoc experiment/report scripts. Consolidate into a `cli/` entrypoint or remove if unused. |

---

## 3. Client Architecture (runs on device)

### 3.1 Deployment model
**Desktop application (local-first).** Packaged with PyInstaller (one-dir) for Linux/Windows/macOS. The existing Streamlit `app.py` runs in-process inside a local browser window. No install step beyond downloading the executable/ZIP.

### 3.2 In-process layers (all on device)

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: Client UI (Streamlit, local browser window)        │
│   - Strategy selection, parameter sliders, run/stop         │
│   - Chart rendering (Plotly), report export (PDF/HTML)      │
│   - Run history browser (reads local SQLite)                │
├─────────────────────────────────────────────────────────────┤
│ Layer 2: Analytics (Metrics, DSR, CPCV, Validation)         │
│   - Pure pandas/numpy/scipy; in-process; no network         │
├─────────────────────────────────────────────────────────────┤
│ Layer 3: Event-Driven Engine (BacktestEngine)               │
│   - Zero-lookahead T+1 loop; Portfolio; Position; CostModel │
├─────────────────────────────────────────────────────────────┤
│ Layer 4: Data (fetch, clean, universe) + Strategies         │
│   - yfinance fetch → Parquet cache → clean → engine         │
└─────────────────────────────────────────────────────────────┘
```

### 3.3 Where computation runs: LOCAL (100% client-side)

| Task | Location | Why |
|------|----------|-----|
| Backtest engine | Local device | In-process Python; no latency; offline capable; data never leaves device |
| Data fetch (yfinance) | Local device → Yahoo Finance | Public data, no API key; academic/commercial redistribution restricted → keep on device |
| Metrics / DSR / CPCV | Local device | Pure pandas/numpy; cheap compute; no reason to move off-device |
| Chart rendering | Local device | Plotly in browser window; no server round-trip |
| Cost model | Local device | Indian statutory rules computed locally; regulatory audit trail stays on device |

**Why local, not remote:**
1. **Data is public** (yfinance/NSE) — no proprietary dataset to protect server-side.
2. **No broker integration** — no order routing, no execution, no credentials to manage.
3. **Daily bars, 10 symbols** — compute load is trivial; a laptop handles it in seconds.
4. **Regulatory/data-residency** — Indian equity data + cost calculations are sensitive; keeping them on-device avoids cross-border data transfer and simplifies compliance.
5. **No backend ops** — no servers, no uptime SLAs, no infrastructure cost.

---

## 4. Backend Architecture — KEY DECISION: No backend

**Decision: Do NOT build a backend.**

### Justification based on this repository

| Factor | Evidence in repo | Implication |
|--------|-----------------|-------------|
| No server code exists | `requirements.txt` has no FastAPI/Flask/Django; no `src/server/`, `src/api/`, `src/backend/` | Building a backend is net-new work, not an evolution |
| Local in-process computation | `BacktestEngine.run()` executes entirely in-process | Backend adds latency (serialization + network) for zero gain |
| Public data source | `yfinance` fetch, no API key, no auth | No need to proxy or cache data server-side |
| No broker integration | README: "No Live Execution", "No broker integration" | No order management, no execution reports, no webhooks |
| No user accounts | No auth, no user model, no multi-user concept | No reason for a central server to mediate access |
| Daily bars, small universe | 10 symbols, daily frequency | A single laptop is sufficient compute; no need for distributed/cluster execution |

**When a backend would be justified (future, out of scope):**
- Commercial SaaS with multi-user workspaces and shared run history (per MONETIZATION_STRATEGY.md)
- Paid commercial market data requiring server-side entitlement
- API access for RIAs to embed backtests in client portals
- Intraday tick-level or Monte Carlo at scale (the V2 Rust extension mentioned in system_architecture.md)

None of these apply to v1. **Skip the backend entirely.**

---

## 5. API Design

### 5.1 Local CLI (primary programmatic interface)
A thin CLI (`src/cli/`) wrapping the engine, analytics, and data layers:

```
quantlab fetch       # Download universe data to local Parquet cache
quantlab run         # Run a backtest (strategy, params, dates, costs on/off)
quantlab report      # Generate PDF/HTML backtest report
quantlab validate    # Run CPCV/DSR overfitting diagnostics
quantlab info        # Show universe, cost model version, data freshness
```

### 5.2 REST API (NOT built for v1)
No REST API. If enterprise customers later demand API access (per monetization strategy), add FastAPI as a separate, opt-in service — but it is not part of this architecture.

### 5.3 Streamlit UI (interactive interface)
The existing `app.py` becomes the desktop UI. It calls the same Python modules as the CLI — **one codebase, two entry points (CLI + GUI)** sharing the engine/analytics/data layers.

---

## 6. Database

### 6.1 Decision: No cloud database. Local SQLite + Parquet.

| Store | Technology | Purpose | Rationale |
|-------|-----------|---------|-----------|
| Market data (OHLCV) | **Parquet** (local `data/cache/`) | Time-series price/volume | Columnar, compressed, fast reads for backtest; append-only per symbol; ideal for pandas |
| Run metadata & history | **SQLite** (local `~/.quantlab/quantlab.db`) | Backtest runs, parameters, metrics, timestamps, cost-model version | Relational queries for run history; ACID; single file, zero-config; portable with the app |
| Strategy registry | JSON/YAML (local) | Available strategies + default params | Human-editable; no DB needed |
| User config | JSON/YAML (local) | UI preferences, cost toggles, universe | Single-user desktop app; no need for DB |

### 6.2 Why not cloud?
- Single-user desktop app; no multi-user collaboration in v1.
- Data is public (yfinance); no proprietary dataset to centralize.
- SQLite is zero-operations: no server, no credentials, no backups beyond file copy.

---

## 7. Local database / cache strategy

### 7.1 Data cache (Parquet)
- On first run, `fetch.py` downloads universe data from yfinance → writes to `data/cache/<SYMBOL>.parquet` partitioned by symbol.
- Subsequent runs read from local Parquet (offline-capable after first fetch).
- **Staleness policy:** Cache valid for N days (configurable, default 7). On app start, check cache freshness; if stale and online, incrementally update only missing dates; if offline, warn and use cached data.
- **Offline-first:** App works fully offline once data is cached. Backtests, metrics, DSR, CPCV all run without network.

### 7.2 Run history (SQLite)
- Each backtest run inserts a row: `run_id, timestamp, strategy, params, date_range, apply_costs, metrics_json, equity_curve_ref, cost_model_version, duration_seconds`.
- Equity curve and per-trade fills stored as Parquet files referenced by `run_id` (avoid bloating SQLite with large time-series).

### 7.3 Cache invalidation & versioning
- Cost model version stored in SQLite (SEBI fee rules change; audit which version produced which run).
- Data schema version in Parquet metadata to detect incompatible cache after clean.py changes.

---

## 8. Authentication

**Not needed. No auth for v1.**

### Justification
- Single-user desktop application; no multi-tenancy; no shared state.
- No backend to authenticate against.
- Data is public; no PII stored (only market data and backtest results).
- Adding auth (OAuth, JWT, session management) would add complexity, dependency surface, and friction with zero user benefit.

### Future (enterprise tier, out of scope)
If a self-hosted enterprise on-prem deployment is offered later (per MONETIZATION_STRATEGY.md), add SSO/SAML or API-key auth at that layer — but it is an enterprise feature, not part of the core architecture.

---

## 9. Background jobs

**None for v1.** All work is synchronous, user-triggered (click "Run Backtest").

### Future background jobs (if needed)
- Scheduled data refresh (daily, overnight) — could use `apscheduler` or a simple OS cron wrapper.
- Report generation for large parameter sweeps — could be offloaded to a `concurrent.futures` thread/process pool within the desktop app (no separate job server needed).

---

## 10. Storage format: Parquet vs CSV vs SQLite

| Format | Use case | Why |
|--------|----------|-----|
| **Parquet** | Market data (OHLCV time series), equity curves, fill logs | Columnar, compressed (~5-10× smaller than CSV), fast predicate pushdown, native pandas support, schema evolution |
| **SQLite** | Run metadata, configuration, run history | Zero-config relational store, ACID, single file, portable |
| **CSV** | NOT used for storage | Only as an interchange/export format for users who want to open in Excel |
| **JSON/YAML** | Strategy configs, user preferences | Human-editable, simple |

**Decision: Parquet for time-series, SQLite for metadata, JSON for config.** CSV retained only as export.

---

## 11. Observability, logging, error handling

### 11.1 Logging
- Python `logging` module, structured JSON logs to file (`~/.quantlab/quantlab.log`).
- Levels: DEBUG/INFO/WARN/ERROR.
- Log rotation (keep last 5 files, 10 MB each).
- Streamlit captures `st.exception()` and `st.error()` for UI-visible errors.

### 11.2 Error handling
- **Data fetch:** Retry with exponential backoff (3 attempts) on yfinance failure; graceful degradation to cached data; user-visible warning if offline and no cache.
- **Backtest:** Try/except around strategy signal generation so one bad symbol doesn't kill the whole run; log and skip.
- **Cost model:** Validate fee schedules; guard against division by zero (adv=0); cap market impact at 5% (already done).
- **Portfolio:** Raise `InsufficientCashError` instead of printing a warning; CLI exits non-zero, UI shows error toast.

### 11.3 Observability
- Run duration, symbol count, cache hit/miss, cost-model version logged per run.
- No telemetry/phone-home (desktop app, privacy-conscious user base). Optional anonymous usage stats only if user opts in.

---

## 12. CI/CD, deployment

### 12.1 CI (add — none exists today)
- **GitHub Actions** (free for public repos):
  - `pytest` on every push/PR (currently 9/9 passing; keep green).
  - `ruff` lint + `mypy` type check (add after introducing type hints).
  - Build PyInstaller artifact on tagged releases (Linux/Windows/macOS matrices).
  - Verify `scipy` import (currently missing from requirements — CI would catch this).

### 12.2 Deployment
- **Desktop:** GitHub Releases with signed installers/ZIPs per platform. Auto-update via a simple GitHub Release check (or `pyinstaller` + `pyuac`/`easy-update`).
- **Web (optional):** Streamlit Cloud free tier for browser-based demo (server-side compute; acceptable per PLATFORM_STRATEGY.md). Not required for desktop v1.

### 12.3 Release process
- Semantic versioning (v0.1.0 → v1.0.0).
- Changelog; cost-model version bumped when SEBI rules change (regulatory compliance).

---

## 13. Backup / recovery / versioning / feature flags

### 13.1 Backup & recovery
- Local SQLite + Parquet files are the source of truth.
- User backs up by copying `~/.quantlab/` directory (or `data/cache/` + `.quantlab/quantlab.db`).
- App includes "Export run history" and "Import run history" (SQLite dump/restore) buttons.
- No cloud backup (no cloud infrastructure).

### 13.2 Versioning
- **App version:** semver in `pyproject.toml`/`__init__.py`.
- **Data schema version:** stored in Parquet metadata; migrations handled in `clean.py` load path.
- **Cost model version:** stored per-run in SQLite; enables audit ("this run used cost model v2.1").

### 13.3 Feature flags
Simple JSON-based flags in `~/.quantlab/config.json`:
```json
{
  "enable_cpcv": true,
  "enable_dsR": true,
  "export_pdf": true,
  "cost_model_version": "2.1"
}
```
No remote flag service (no backend); flags are local config only.

---

## 14. Technology stack comparison & chosen stack

### Options evaluated

| Stack | Fit for this repo | Verdict |
|-------|-------------------|---------|
| **Python + Streamlit + PyInstaller** (desktop) | Reuses 100% of existing Python engine (~1,008 LOC); no new language; offline; single codebase; PyInstaller is the only new dependency | **CHOSEN** |
| Tauri (Rust + web) | Would need Python sidecar/PyO3 bridge; Rust learning curve; mobile immature; build complexity | Reject v1 (consider v2 if native chrome needed) |
| Electron (Node + Chromium) | Heavy binary (~100+ MB); Node/Python bridge; overkill for local backtest tool | Reject |
| Flutter / React Native | Would require engine rewrite (Dart/JS cannot run pandas); loses code investment | Reject |
| PWA (web-only) | Works on mobile browsers but server-side compute (Streamlit Cloud) or local Python-on-mobile; limited offline storage | Supplementary (mobile-browser reach), not primary |

### Chosen stack: Python + Streamlit + PyInstaller (desktop-first)

**Defense:**
1. **Reuses existing investment.** ~1,008 LOC of Python engine, analytics, and data code stays untouched. No rewrite in Kotlin/Dart/JS/Rust.
2. **Matches the architecture.** The engine is local, in-process, synchronous. Desktop Python packaging fits naturally; client-server would be a forced mismatch.
3. **Fits the team/timeline.** GTU academic project heritage; small team. PyInstaller + Streamlit is hours of work, not months.
4. **Cross-platform reach without native mobile.** Desktop (executable) + optional Streamlit Cloud/PWA (mobile browser) covers Windows/Linux/macOS/Android/iOS from one codebase.
5. **No new dependencies/languages.** `requirements.txt` already has pandas, numpy, streamlit, plotly, yfinance. PyInstaller is the only addition (plus scipy which is already imported but missing — fix that).

### Where computation runs: LOCAL (client device), 100%
**Why:** Public data, no broker, no live execution, daily bars on 10 symbols — a laptop is sufficient. Moving compute to a server adds latency, cost, and operational complexity for zero functional benefit.

### Data synchronization strategy: Offline-first, no cloud sync
- Data fetched from yfinance on demand, cached locally in Parquet.
- No cloud sync, no multi-device sync, no central database.
- If a user moves to a new machine, they re-fetch data (public, free) and re-run backtests (fast). Run history can be exported/imported via SQLite dump.

---

## 15. Summary of key decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Backend | **None** | No need; local compute, public data, no broker, no multi-user |
| API | **Local CLI + Streamlit GUI** | One codebase, two entry points; no REST |
| Database | **Local SQLite + Parquet** | Zero-config, portable, single-user |
| Cache | **Parquet (local), offline-first** | Columnar, compressed, works without network |
| Authentication | **None** | Single-user desktop; no PII; no backend |
| Background jobs | **None (sync, user-triggered)** | No job server needed |
| Storage | Parquet (time-series) + SQLite (metadata) + JSON (config) | Right tool per data type |
| Stack | **Python + Streamlit + PyInstaller** | Reuses existing code; no new language; offline desktop |
| Computation | **100% local client device** | Public data, trivial compute load, data residency |
| Sync | **Offline-first, no cloud sync** | Public data re-fetchable; run history import/export via file |

---

## 16. Implementation roadmap (high level)

**Phase 1 — Harden (no architecture change)**
- Add `scipy` to requirements.txt; add type hints, ruff, mypy, GitHub Actions CI.
- Consolidate `engine/order.py` into `engine/events.py` (REMOVE duplicate).
- Add structured logging, error boundaries, retry/backoff in data fetch.
- Parquet cache + SQLite run history.

**Phase 2 — Desktop packaging**
- PyInstaller one-dir build for Linux/Windows/macOS.
- CLI entrypoint (`quantlab run/fetch/report/validate`).
- Streamlit app refactor: session state, run history browser, error toasts.

**Phase 3 — Polish (optional)**
- PDF/HTML report export.
- PWA manifest + Streamlit Cloud for browser demo.
- Feature flags config file.

No backend, no auth, no cloud database, no CI/CD today — add CI in Phase 1, everything else only if commercial demand justifies it.
