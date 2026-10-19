# QuantLab — QA & Release Engineering Document

**Product:** QuantLab — event-driven backtesting engine & overfitting diagnostic platform for Indian equities  
**Repo state:** `feat/v2-architecture`, ~1,008 LOC `src/`, 9 pytest tests passing (6 test files), no CI, no lint, no typing, no versioning beyond git tags  
**Owner:** QA / Release Engineering subagent  
**Status:** Pre-launch (alpha) — not launch-ready

---

## 1. Testing Strategy

### Current state (verified)
- 6 test files: `test_engine.py`, `test_cost_model.py`, `test_metrics.py`, `test_portfolio.py`, `test_cpcv.py`, `test_momentum.py`
- Coverage: engine look-ahead, position sizing, Indian cost model (STT/GST/stamp duty/turnover), metrics (CAGR/Sharpe/Sortino/MDD), CPCV embargo + PBO, momentum strategy
- **Missing:** no tests for SMA, RSI strategies; no `test_data.py` (fetch/clean/universe); no integration tests; no property-based tests; no financial-correctness oracle tests

### 1.1 Unit tests (pytest)
Target ≥90% line coverage on `src/engine`, `src/analytics`, `src/data`, `src/strategies`.
| Module | What to test |
|---|---|
| `engine/backtest_engine.py` | T+1 execution boundary (signal T Close → fill T+1 Open), pending-order lifecycle, data alignment with missing dates/symbols, empty universe, single-bar universe |
| `engine/cost_model.py` | Brokerage min(20, 0.03%), STT rounding (nearest integer, buy+sell), stamp duty buy-only, NSE+SEBI turnover, GST 18% on brokerage+turnover, Almgren-Chriss impact cap 5%, `apply_costs=False` bypass |
| `engine/portfolio.py` | Cash ≥ 0 invariant enforcement, equity history MTM, partial fills, sell-without-position guard, cash-goes-negative warning path |
| `engine/position.py` | Average entry price recalculation on add/trim, realized PnL on sell, quantity sign |
| `analytics/metrics.py` | Sharpe/Sortino/Calmar with zero-volatility (return 0.0 not crash), empty history `{}`, single-row history, known-value CAGR/MDD oracle |
| `analytics/cpcv.py` | Embargo drops indices at block boundaries, PBO in [0,1], empty strategies → NaN, n_test_splits > n_splits error |
| `analytics/deflated_sharpe.py` | DSR p-value in [0,1], skew/kurtosis adjustment direction |
| `analytics/validation.py` | Schema validation of OHLCV, monotonic date check, duplicate-date rejection |
| `data/fetch.py` | yfinance failure → None (mocked), empty df → None, column standardization |
| `data/clean.py` | Outlier/winsorization bounds, missing-date interpolation, duplicate removal |
| `data/universe.py` | Symbol list validation, NSE `.NS` suffix enforcement |
| `strategies/sma_crossover.py` | Cross-above/cross-below signal emission, no look-ahead (uses ≤ current_date), insufficient-data skip |
| `strategies/rsi_mean_reversion.py` | RSI oversold/overbought crossing, Wilder's smoothing stability, `down==0` division guard |
| `strategies/momentum.py` | Lookback window, look-ahead absence |

### 1.2 Integration tests (new: `tests/integration/`)
- **End-to-end backtest:** fetch → clean → run engine on 10 NSE symbols × 5 years → assert metrics finite, cash ≥ 0 at all steps, equity_history length == timeline length
- **Dashboard smoke test:** `streamlit run src/dashboard/app.py` with seeded `data/raw/` → app loads without exception, "No data found" path renders
- **CLI smoke:** `python -m src` / experiment scripts run end-to-end
- **Cost-model integration:** engine run with `apply_costs=True/False` → equity difference matches summed `total_cost`

### 1.3 Property-based tests (hypothesis)
Add `hypothesis` to dev deps. Properties:
- Cost model: `total_cost >= 0` for all valid orders; stamp duty == 0 on SELL; brokerage capped at 20
- Portfolio: `cash + sum(positions MTM) == total_equity` at every time index (invariant)
- Engine: no signal references a date > current_date (zero look-ahead invariant across random price walks)
- Metrics: MDD ≤ 0, Sharpe finite for non-degenerate returns, CAGR == total return annualized for flat curve
- Strategies: signal_type ∈ {-1, 0, 1}; no SELL signal without open position

### 1.4 Financial correctness (golden/oracle)
- Hard-coded expected values for a fixed synthetic 3-day dataset (as in `test_engine.py`) — commit dataset + expected equity curve as regression goldens
- Cost model: hand-computed STT/GST/stamp duty for known trade values (already partially in `test_cost_model.py`) — extend to round-trip BUY+SELL
- DSR/PBO: synthetic AR(1) returns with known overfitting → PBO > threshold; i.i.d. returns → PBO ≈ 0
- Benchmark regression: same seed + same data must produce bit-identical equity curve (determinism test)

### 1.5 Test hygiene
- `pytest` with `--cov`, `pytest-cov`, `pytest-randomly`, `hypothesis`
- `tests/conftest.py` with shared fixtures (sample OHLCV, engine, cost model)
- CI gate: coverage ≥ 80%, no test may access network (mock yfinance)

---

## 2. CI/CD Pipeline (GitHub Actions recommended)

No CI currently exists. Propose `.github/workflows/`:

| Workflow | Trigger | Jobs |
|---|---|---|
| `ci.yml` | push to any branch, PR | lint (ruff), typecheck (mypy), unit tests (pytest, py3.10/3.11/3.12), property-based tests |
| `nightly.yml` | schedule 02:00 UTC | integration tests (real yfinance fetch, network allowed), full 10-symbol × 5yr backtest performance, benchmark regression |
| `release.yml` | push tag `v*` | build wheels + sdist, desktop installers (MSI/AppImage/DMG), GitHub Release, smoke-test installers |
| `security.yml` | weekly + PR | pip-audit / safety, dependency vulnerability scan |

**Quality gates (must pass before merge):**
- ruff check + format --check
- mypy --strict on `src/`
- pytest all green, coverage ≥ 80%
- no network in unit tests (block `yfinance` via `responses`/`requests-mock` or pytest-socket)

**Concurrent run:** lint, typecheck, unit tests in parallel jobs (~3–5 min total).

---

## 3. Crash Reporting

No crash reporting exists. Options:

| Option | Fit | Notes |
|---|---|---|
| **Sentry (Python SDK)** | Recommended | Captures unhandled exceptions in CLI/dashboard, breadcrumbs, release tracking, user feedback. Free tier sufficient for alpha/beta. |
| Custom (local JSONL + optional remote endpoint) | Fallback | Zero third-party dependency; write crashes to `~/.quantlab/crashes/`. Good for air-gapped/academic use. |

**Recommendation:** Sentry SDK initialized in `src/__init__.py` and dashboard `app.py` (wrapped in try/except around `st.button` callbacks), with `before_send` scrubbing PII (symbols are fine; paths/usernames scrubbed). Opt-in telemetry flag gates crash reporting (see §4). Provide `--no-sentry` CLI flag and env var `QUANTLAB_SENTRY_DSN=off`.

---

## 4. Telemetry / Analytics

No telemetry exists. Privacy-first design (India PDP Act + GDPR):

### 4.1 What to track (opt-in only, anonymized)
- Backtest run completed (boolean), symbol count, date range, strategy name
- Aggregated metric buckets (CAGR/MDD ranges, not raw values)
- Python/OS versions, QuantLab version
- Error/crash events (stack traces without file paths or user identifiers)

### 4.2 What NOT to track
- Raw price/OHLCV data, portfolio values, cash balances, order quantities
- User email/name/device ID, IP addresses, MAC addresses
- Any data enabling re-identification of a specific trading account

### 4.3 Implementation
- `src/telemetry.py`: opt-in flag `QUANTLAB_TELEMETRY=1`, hashed random UUID v4 (per-install, rotated quarterly), batch HTTPS POST to own endpoint or Sentry, respect `Do Not Track`
- First run: consent dialog in dashboard + CLI prompt; store consent in `~/.quantlab/config.json`
- Data retention: 90 days raw, 12 months aggregated

---

## 5. Release Channels

No release channels exist (only git tags). Propose:

| Channel | Source | Cadence | Audience |
|---|---|---|---|
| **Alpha** | `main` (or `feat/*`) nightly | Every merge to main | Internal / contributors |
| **Beta** | release branch `release/v*` | Weekly / feature-complete | Opt-in testers |
| **Stable** | git tag `vX.Y.Z` | Per release | General public |

**Versioning:** SemVer (Semantic Versioning 2.0.0), starting `v0.1.0` (alpha). Pre-release tags `v0.1.0-alpha.1`, `v0.1.0-beta.1`. Git tags + GitHub Releases + PyPI distribution (`twine upload`).

**Promotion rules:** Alpha → Beta requires feature freeze + all CI green + manual QA (§14). Beta → Stable requires 2 clean beta builds, no P1/P2 open bugs, security scan clean, docs complete.

---

## 6. Play Store Requirements (Android)

QuantLab is a **Python desktop/Streamlit app**, not an Android native app. **There is no Play Store path without a major rewrite.**

Requirements if pursued:
- Rewrite as native Android (Kotlin/Java) or Flutter with Python backend bundled (briefcase/Chaquopy) — substantial effort, outside current scope
- Google Play developer account ($25 one-time)
- Target API level 33+, privacy declaration, data safety section (no personal data collected → simplest)
- App signing by Google Play, bundle (.aab)
- Content rating questionnaire

**Recommendation:** Do not target Play Store for v1. Launch as desktop (Windows/macOS/Linux) + web (Streamlit Cloud) first. Re-evaluate mobile after product-market fit.

---

## 7. Desktop Packaging

No packaging exists. Streamlit app is not desktop-native. Options:

| Platform | Format | Tool | Notes |
|---|---|---|---|
| Windows | MSI + EXE installer | Inno Setup / NSIS / cx_Freeze | Bundle Python + streamlit; heavy (~150–300 MB) |
| Linux | AppImage + DEB | python-appimage / fpm / cx_Freeze | AppImage most portable; DEB for Debian/Ubuntu |
| macOS | DMG + .app | py2app / Briefcase | Apple notarization required for Gatekeeper; Apple Silicon + Intel universal |

**Recommended tooling:** **Briefcase** (BeeWare project) — single `briefcase` config generates MSI/AppImage/DMG from one Python codebase. Alternative: `PyInstaller` + platform installers.

**Packaging caveat:** Streamlit inside a frozen desktop app is awkward (needs a bundled browser/electron or local port). Consider packaging the CLI backtest engine as the desktop product, and keep Streamlit as web-only. If desktop GUI required, migrate from Streamlit to a desktop framework (PySide6/Tkinter) — do not force Streamlit into an installer.

---

## 8. Update Mechanism

None exists. Propose:

| Mechanism | Scope |
|---|---|
| PyPI `pip install --upgrade quantlab` | CLI/library users |
| GitHub Releases + auto-download installer | Desktop users (Briefcase supports app updates via GitHub) |
| Streamlit Cloud auto-deploy | Web users (git push → redeploy) |

**In-app update check:** On startup (opt-in), GET `https://api.github.com/repos/<org>/QuantLab/releases/latest`, compare `tag_name` vs `__version__`, show non-blocking banner. Never auto-install; user initiates.

---

## 9. Documentation Requirements

Current docs are academic/thesis-oriented (`docs/`, LaTeX, PDFs). For launch, add user-facing docs:

| Doc | Owner | Status |
|---|---|---|
| README quickstart (install, run backtest, interpret metrics) | Required | Partial (README exists, thin) |
| API reference (docstrings → mkdocs/sphinx) | Required | Missing |
| Cost model methodology (Indian statutory fees, sources) | Required | Partial (README + code comments) |
| CPCV/DSR methodology + limitations | Required | Partial (thesis docs) |
| Data requirements (OHLCV schema, `data/raw/`) | Required | Missing |
| Contributing guide (testing, linting, PR template) | Required | Missing |
| Changelog (`CHANGELOG.md`, Keep a Changelog) | Required | Missing |
| Security policy (`SECURITY.md`, vulnerability disclosure) | Required | Missing |

**Docs site:** MkDocs + Material theme, hosted on GitHub Pages, auto-deployed on tag push.

---

## 10. Privacy Policy Requirements

### India PDP Act (Digital Personal Data Protection Act, 2023)
- QuantLab processes **no personal data** by design (market data only). If telemetry/opt-in is added, collect only device-level pseudonymous ID; obtain **consent** before collection; provide **right to withdraw/delete**; data fiduciary obligations (notice in plain language, breach notification to DP Board).
- If any user email/account is ever collected: appoint Data Protection Officer (India contact), purpose limitation, storage limitation, erasure on request.

### GDPR (if global/EU users)
- Same minimization/consent principles; record of processing activities; right to access/erasure/portability; DPA supervisor authority if high-risk (not expected).
- Privacy Policy must state: what is collected, why, legal basis (consent/legitimate interest), retention, third parties (Sentry → note as processor, execute DPA), user rights, contact.

### Deliverables
- `privacy-policy.md` (plain language, linked from README/dashboard footer)
- `terms-of-service.md` (no financial advice disclaimer — critical for a backtesting tool)
- Cookie/banner-free (no cookies if no tracking); if telemetry, consent banner

**Disclaimer (mandatory):** "QuantLab is a simulation/educational tool, not financial advice. Past performance does not guarantee future results. Indian statutory cost figures are model approximations; verify against current broker/SEBI rates."

---

## 11. Licensing (Apache 2.0)

- **Current:** Apache License 2.0 (`LICENSE` present). Permissive: allows commercial use, modification, distribution, patent grant, private use. Requires license + notice preservation, state changes.
- **Implications for commercial:**
  - You may sell QuantLab or embed it in a commercial product **without opening your source** (unlike GPL).
  - Must include Apache 2.0 license text and NOTICE in distributions; must mark modified files.
  - `yfinance` dependency: **check its license** (yfinance is under its own terms; README explicitly says "not licensed for commercial redistribution" of data — that's a data-license restriction, not code license). Commercial use of yfinance-fetched NSE data may violate Yahoo/NSE terms — for commercial launch, switch to a licensed data vendor (NSE data feed, Zerodha/Kite, Upstox, TrueData) or explicitly state "bring your own data."
- **Recommendation:** Keep Apache 2.0 for OSS version; if offering a commercial SaaS, Apache 2.0 permits it (SaaS loophole — no distribution → no source obligation), but consider AGPL or a commercial license if you want to prevent SaaS competitors. Consult counsel before commercializing.

---

## 12. Security Review Requirements

No security review exists. Pre-launch audit checklist:

### Code-level
- [ ] `pip-audit` / `safety` on dependencies (CI `security.yml`)
- [ ] No hardcoded secrets/keys (grep for `sk-`, `AKIA`, passwords, tokens)
- [ ] `yfinance` network calls wrapped with timeout + error handling (no SSRF, no arbitrary URL fetch)
- [ ] File path handling in `data/raw/` load — prevent path traversal (`../`) if user-supplied paths ever accepted
- [ ] `eval()`/`exec()`/`pickle` usage audit (none currently; enforce ban)

### Supply chain
- [ ] Pin exact dependency versions (already done in `requirements.txt`) — add `pip-compile` / `requirements.lock` with hashes
- [ ] Add `scipy` to `requirements.txt` (currently imported in `deflated_sharpe.py` but missing — **immediate bug**)
- [ ] Split `requirements.txt` into `base` / `dev` / `dashboard` extras

### Infrastructure
- [ ] GitHub repo: branch protection, require PR review, require status checks, admins included
- [ ] Dependabot alerts enabled
- [ ] Sentry DSN not committed to repo (env var only)

### Data
- [ ] No user financial data stored locally/remotely by default
- `data/raw/` gitignored (already in `.gitignore` — verify)

---

## 13. Performance Benchmarks

### Claim to validate
"Under 30 seconds for 10–15 stocks, 5 years" — **unverified; no benchmark exists.**

### Required benchmarks (add `tests/benchmarks/` or `benchmarks/`)
| Scenario | Target | Measurement |
|---|---|---|
| 10 symbols × 5 years (~1,260 bars), SMA | < 30 s | wall time `engine.run()` |
| 15 symbols × 5 years, costs on | < 60 s | wall time |
| CPCV PBO (n_splits=8, n_test=2) | < 120 s | wall time |
| Memory peak (15 sym × 5y) | < 512 MB | `tracemalloc`/`memory_profiler` |
| Determinism: same input → identical equity hash | bit-identical | SHA-256 of equity CSV |

### Method
- `pytest-benchmark` or `airspeed velocity (asv)`; run on CI nightly; alert on regression > 10%
- Synthetic deterministic data (seeded random walk) to avoid network variance

---

## 14. Manual QA Checklist (pre-release gate)

**P1 — must pass for any release:**

- [ ] `pytest -q` all tests green (9 current + new)
- [ ] `ruff check src/ tests/` clean
- [ ] `mypy --strict src/` clean
- [ ] `scipy` added to `requirements.txt` and import works
- [ ] Engine run on seeded data produces deterministic equity curve
- [ ] Cash never negative across test matrix (10 × symbols × cost on/off)
- [ ] Zero-lookahead: no signal reads future bar (instrumented run)
- [ ] Dashboard launches with empty `data/raw/` → shows warning, no crash
- [ ] Dashboard runs full backtest with seeded `data/raw/` → metrics render
- [ ] Cost model: round-trip BUY+SELL totals match hand calculation
- [ ] `pip install -e .` works in fresh venv (py3.10/3.11/3.12)
- [ ] `python -m src` / experiment scripts run without error
- [ ] Git tag `v0.1.0` created; GitHub Release draft with notes
- [ ] `CHANGELOG.md` entry for v0.1.0
- [ ] `SECURITY.md` + `privacy-policy.md` + `terms-of-service.md` published
- [ ] Disclaimer banner present in dashboard + CLI help

**P2 — before Stable:**
- [ ] Integration test with real yfinance (network) passes
- [ ] Performance benchmarks meet §13 targets
- [ ] One desktop installer (MSI or AppImage) builds and installs
- [ ] Sentry crash reporting integrated + opt-in working
- [ ] Coverage ≥ 80%

**Blockers for launch:** missing `scipy` in requirements, no CI, no tests for SMA/RSI/data, dashboard hard-fails without `data/raw/`, no versioning/release process.

---

## Immediate next steps (first 2 weeks)

1. Add `scipy` to `requirements.txt`; split base/dev extras; pin versions.
2. Add `tests/test_sma.py`, `tests/test_rsi.py`, `tests/test_data.py`.
3. Add `.github/workflows/ci.yml` (ruff + mypy + pytest).
4. Add `tests/conftest.py` + `pytest.ini`/`pyproject.toml` config.
5. Draft `CHANGELOG.md`, `SECURITY.md`, `privacy-policy.md`, `terms-of-service.md`.
6. Tag `v0.1.0-alpha.1`, draft GitHub Release.
