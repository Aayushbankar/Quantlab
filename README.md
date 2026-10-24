# Pramaan (प्रमाण) — The Honest Backtesting Engine

[![CI](https://github.com/Aayushbankar/Quantlab/actions/workflows/ci.yml/badge.svg)](https://github.com/Aayushbankar/Quantlab/actions/workflows/ci.yml)
[![Tests](https://img.shields.io/badge/tests-72%20passed%20offline-2ea44f.svg)](tests/)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.13-blue.svg)](pyproject.toml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

> **"Prove your edge before you deploy a rupee."**

Pramaan is an honest, production-ready backtesting and validation engine for Indian (NSE) equities. It enforces **zero look-ahead T+1 execution** by mathematical construction, deducts the **complete Indian statutory delivery cost stack** (STT, DP charges, stamp duty, GST, exchange turnover, SEBI fee, IPFT, Almgren–Chriss square-root impact) down to exact paise, and subjects strategies to **Marcos López de Prado overfitting diagnostics** (Deflated Sharpe Ratio, CPCV/PBO with non-zero embargo).

- **Academic Origin:** GTU DI05000341 Minor Project, DIET (Sem-5).
- **Authors:** Aayush Avinash Bankar (Engine, API, Math, Costs) & Meet Jayeshbhai Patel (Frontend, UI, Desktop Packaging).
- **Core Principle:** Nothing is claimed without verifiable evidence recorded in [`.agent/01_verification_ledger.md`](.agent/01_verification_ledger.md). Honesty is the brand.

---

## The Two Moats

### 1. The Statutory Friction Tollgate (The Profit Mirage)
Most backtesters apply flat or nominal international broker commissions (e.g., 0.05%), which dramatically misrepresents Indian equity trading. Pramaan computes the **exact legal statutory tariff** based on SEBI and NSE circulars (including the Oct 2024 True-to-Label rate card) with date-resolved profiles:
- **STT (Securities Transaction Tax):** 0.10% delivery on both buy and sell legs. STT heavily dominates friction drag at small/retail account sizing.
- **Depository Participant (DP) Charges:** Flat ₹13.50 + 18% GST per debit transaction on sell executions (CDSL/NSDL).
- **Stamp Duty:** 0.015% buy-side statutory tax (Indian Stamp Act).
- **Exchange Turnover & SEBI Tariff:** 0.00297% NSE exchange charge + ₹10 per crore SEBI regulatory fee + Investor Protection Fund (IPFT).
- **GST:** 18% tax on brokerage, turnover charges, and DP fees.
- **Market Impact:** Almgren–Chriss square-root execution model based on trailing volatility and Average Daily Volume (ADV), plus user-configurable slippage floor (bps).

**Empirical Result:** On 10 NSE large caps (2019–2024, 14,800 bars), statutory friction destroys **48.2% of momentum alpha** (Sharpe 0.359 → 0.186), evaporating ₹12,995 of terminal equity on ₹1,00,000 capital.

### 2. Overfitting Diagnostics (Truth Over Backfit)
- **Deflated Sharpe Ratio (DSR):** Corrected for true cross-trial variance ($V[\{SR_k\}]$) and selection bias across $N$ evaluated trials, validated against Bailey & López de Prado (2014) published worked examples.
- **Combinatorial Purged Cross-Validation (CPCV):** 45 overlapping test paths with a non-zero embargo period to eliminate serial correlation leakage.
- **Empirical Probability of Backtest Overfitting (PBO):** In our 133-configuration parameter sweep, empirical PBO was **60.0% with 95% bootstrap CI [44.4%, 73.3%]**—demonstrating that 6 out of 10 in-sample "winners" underperform out-of-sample.

---

## Shipped Artifacts

- **Headless Core Engine (`src/engine/`):** Discrete event simulation queue, zero look-ahead execution ($Signal_t \to Fill_{t+1}$ Open), cash $\ge 0$ portfolio accounting, rejected trade tracking, and versioned cost profiles (`cost_profiles/`).
- **Statistical Analytics (`src/analytics/`):** Performance metrics, exposure tracking, benchmark confound controls (alpha, beta, exposure-matched returns), DSR, CPCV, and embargo.
- **FastAPI REST Backend (`src/api/`):** Full async job worker (`POST /jobs`, `GET /jobs/{id}`), SQLite WAL trial ledger (`GET /trials`), parameter sweep summary (`GET /sweep`), and printable HTML audit report export (`GET /report/{run_id}`).
- **Next.js 15 Institutional Workstation (`frontend/`):** Expansive 100vw/100vh canvas, tri-theme engine (Abyss / Vellum / Graphite), interactive SVG Profit Mirage dissector, Statutory Tollgate breakdown, live trial history drawer, and interactive product landing page (`/landing`).
- **Desktop Shell (`frontend/src-tauri/`):** Tauri v2 + WebKit2GTK configuration for wrapping the web workstation as a native Linux desktop app. The packaged binary is **not** distributed with this repository; it builds from source with `cargo build` on a machine with the WebKit2GTK development libraries (verified locally: dev-profile build completes, 201 MB ELF).
- **Legacy Fallback Surface (`src/dashboard/`):** Standalone Streamlit demonstration dashboard (`app.py`).
- **Academic Deliverables (`docs/`):** 43-page GTU report PDF (`docs/Pramaan_Report.pdf`) with dual per-member submission copies, presentation (`Pramaan_Presentation.pptx`), and committed reproducibility logs (`experiments/`).

---

## Explicit Scope & Boundaries

- **No live broker routing or execution:** Simulation, research, and validation only.
- **No intraday, tick data, or F&O derivatives:** Daily bars, NSE cash equities, long-only.
- **No commercial market data redistribution:** Comes with an offline synthetic fixture dataset with SHA-256 manifest verification (`data/manifest.json`). Live fetching uses free public Yahoo Finance APIs.
- **Not investment advice:** Designed to prevent capital destruction, not promise riches.

---

## Known Limitations

Stated plainly so nobody has to discover them after the fact:

1. **Survivorship bias:** the 10-symbol universe is today's large caps — the companies that survived. No delisting adjustment is applied.
2. **Daily bars only:** no intraday or tick data; market impact is modelled from daily volume (Almgren–Chriss square-root law), a coarse approximation of intraday participation.
3. **Long-only, no leverage:** shorting and derivatives are out of scope by design.
4. **Exposure / cash-yield confound vs buy-and-hold:** active strategies are on average far less invested than the benchmark; idle cash earns 0% while Sharpe subtracts a 6% risk-free rate. "No active strategy beat buy-and-hold" is therefore partly an exposure effect. The engine exposes `average_exposure`, `alpha`, `beta`, and `exposure_matched_return` (MetricsEngine) to quantify it; committed artifacts do not yet contain exposure-matched headline numbers.
5. **Replay artifacts use the legacy cost model:** committed replay/CSV results carry `cost_model_version = 1.0-indian-delivery-2024` (no DP charge). The live default profile is `standard_discount_2024` (DP ₹13.50 + GST on sells), so replay and live numbers differ slightly — every run stamps its profile.
6. **DSR depends on the local trial ledger:** expected-max-SR inputs (N, cross-trial variance) come from the local SQLite trial ledger when no committed sweep is loaded, so first-run DSR values are not meaningful. Headline DSR figures in the report are computed from the committed `experiments/sweep_summary.json` instead.
7. **Market data is not redistributed:** `data/raw/` and `experiments/equity_curves/` are gitignored; results are regenerated by running the Appendix C scripts against freshly fetched Yahoo Finance data. Run provenance and a SHA-256 manifest of the committed demo data are in-repo.
8. **No live URL, Docker image, desktop binary, or published GitHub release is included in this repository** unless stated otherwise in the release notes.

---

## Quickstart

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/Aayushbankar/Quantlab.git
cd Quantlab

# Install editable package with development and API dependencies
pip install -e ".[dev,api]"
```

### 2. Verify Offline Test Suite (72 Tests)

Pramaan includes a deterministic seeded synthetic dataset (`tests/fixtures/`) that guarantees clean-clone offline test execution:

```bash
pytest tests/ -q
# Output: 72 passed in ~7s
```

### 3. Launch Backend API

```bash
python -m src.api.main
# Engine API starts on http://127.0.0.1:8000
# OpenAPI Swagger documentation: http://127.0.0.1:8000/docs
```

### 4. Launch Next.js Web UI

```bash
cd frontend
npm install
npm run dev
# Workstation UI opens on http://localhost:3000
# Product Landing Page available at http://localhost:3000/landing
```

### 5. Run Native Desktop Binary

```bash
# Build desktop binary using Cargo / Tauri
cd frontend/src-tauri
cargo build

# Run native Linux desktop workstation
./target/debug/pramaan-desktop
```

---

## Reproducibility Guarantee

Every backtest run generates a byte-identical equity curve identified by a deterministic hash:
$$\text{run\_id} = H(\text{strategy}, \text{params}, \text{universe}, \text{dates}, \text{cost\_profile}, \text{lib\_versions})$$

To regenerate the 30-run baseline matrix and the 133-config parameter sweep:

```bash
# 1. Run the baseline 30-run matrix
python scripts/run_experiments.py

# 2. Run the 133-configuration parallel sweep (8 CPU cores)
python scripts/run_sweep.py

# 3. Generate parameter-stamped research charts
python scripts/generate_real_charts.py

# 4. Compile the GTU academic report PDFs
python scripts/build_reports.py
```

### Baseline Performance Matrix (2019-01-01 to 2024-12-30)

| Strategy | Gross Sharpe | Net Sharpe | CAGR | Max DD | Net Total Return |
|---|---|---|---|---|---|
| SMA(20, 50) | 0.612 | 0.527 | 11.37% | −14.76% | +89.65% |
| SMA(10, 30) | 0.798 | 0.685 | 13.25% | −14.64% | +110.15% |
| RSI(14, 30, 70) | 0.354 | 0.307 | 9.80% | −32.77% | +74.20% |
| Momentum(20) | 0.359 | 0.186 | 7.43% | −10.28% | +53.64% |
| **Buy & Hold Benchmark** | **0.746** | **0.746** | **19.07%** | −32.93% | **+188.21%** |

*Central Finding:* Active long-only daily equity strategies incurred massive opportunity cost and statutory drag compared to passive index ownership over the 2019–2024 Indian market bull cycle.

---

## Tested Hardware & Runtime Environment

- **Operating System:** Linux (Arch Linux x86_64, kernel 6.x / Ubuntu 22.04+ compatible)
- **Python:** 3.11.16 tested (compatible with 3.10 through 3.13)
- **Node.js:** v20+ / Next.js 15.1.0
- **Rust / Tauri:** rustc 1.97.1, Tauri 2.12, WebKit2GTK 2.52
- **Determinism:** Verified byte-identical across repeated runs (`tests/test_determinism.py`)

---

## Project Structure

```
├── .agent/              # CypherMatrix verification ledger, daily logs, decisions
├── cost_profiles/       # Versioned JSON rate cards (Zerodha 2024, Pre-Oct 2024, Discount)
├── data/                # Data manifest with SHA-256 checksums (data/manifest.json)
├── docs/                # Academic report (Pramaan_Report.pdf), LaTeX source, syllabus units
├── experiments/         # Real run artifacts: experiment_log.csv, sweep_summary.json, pbo.json
├── frontend/            # Next.js 15 + TypeScript + Tailwind + Tauri desktop shell
│   ├── src/app/         # Terminal view (/) and Landing overview (/landing)
│   ├── src/components/  # Header, ProfitMirage, StatutoryTollgate, HistoryDrawer, Matrix
│   └── src-tauri/       # Tauri v2 Rust desktop application configuration & Cargo.toml
├── pyproject.toml       # Modern packaging standard (pramaan package)
├── scripts/             # Experiment execution, sweep, presentation, and report builders
├── src/
│   ├── analytics/       # DSR (cross-trial variance), CPCV/PBO, exposure & metrics
│   ├── api/             # FastAPI REST endpoints, JobManager, SQLite WAL db, HTML report
│   ├── data/            # DataProvider ABC, cleaners, universe metadata
│   ├── engine/          # Event loop, portfolio ledger, position sizing, cost model
│   └── strategies/      # SMA, RSI, Momentum, Bollinger Breakout, Buy & Hold
└── tests/               # 72 automated tests (offline-capable seeded synthetic fixtures)
```

---

## Academic Defense & License

This project was built for the **Gujarat Technological University (GTU) DI05000341 Minor Project** course. 

- Report PDF: [`docs/Pramaan_Report.pdf`](docs/Pramaan_Report.pdf)
- Presentation Slides: [`Pramaan_Presentation.pptx`](Pramaan_Presentation.pptx)
- Code License: **Apache License 2.0** — See [`LICENSE`](LICENSE).
