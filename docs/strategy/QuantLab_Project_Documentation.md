# QuantLab
### A Realistic Backtesting Engine for Algorithmic Trading Strategies

**GTU Diploma Engineering — Semester 5 Minor Project (DI05000341)**

**Team:**
- Aayush Avinash Bankar — 246230316006 (Group Leader)
- Meet Jayeshbhai Patel — 246230316133

---

## Table of Contents

1. Project Overview
2. Software Requirements Specification (SRS)
3. System Design Document
4. Data Design
5. Testing Plan
6. Roadmap (Phase-Based, Parallel Tracks)
7. Repository Structure
8. Scope & Limitations
9. Risk Register
10. Syllabus Mapping (GTU DI05000341)
11. Viva Preparation
12. References

---

## 1. Project Overview

### 1.1 Problem Statement

Trading strategies frequently appear profitable when evaluated naively on historical price data. This apparent profitability is often an artifact of three factors: (1) ignoring transaction costs and slippage, (2) testing a strategy on the same data used to tune it (overfitting), and (3) look-ahead bias in the simulation logic itself. There is a need for a backtesting tool that exposes these effects explicitly rather than hiding them.

### 1.2 Objective

Build a software platform that:
- Simulates multiple algorithmic trading strategies against historical equity data
- Models realistic execution conditions (transaction costs, slippage)
- Separates in-sample (tuning) and out-of-sample (validation) performance
- Quantifies how much of a strategy's apparent edge survives realistic conditions
- Presents results through a comparative dashboard

### 1.3 One-Line Description

A software platform that tests and compares trading strategies on real historical stock data — including trading costs — to find out which strategies genuinely perform well, so users don't rely on strategies that only look good on paper.

### 1.4 Intended Users

Diploma-level evaluators (as a demonstrable prototype), and secondarily, any student/retail user wanting to sanity-check a trading idea before risking capital. The platform is explicitly **not** intended for production trading use.

---

## 2. Software Requirements Specification (SRS)

### 2.1 Functional Requirements

| ID | Requirement |
|---|---|
| FR-1 | System shall fetch and store historical OHLCV (Open/High/Low/Close/Volume) data for a defined set of equities |
| FR-2 | System shall clean data (handle missing values, stock splits/adjustments) before use |
| FR-3 | System shall implement at least 3 distinct trading strategies (e.g., SMA crossover, RSI mean-reversion, momentum) |
| FR-4 | System shall generate buy/sell/hold signals per strategy per day |
| FR-5 | System shall simulate order execution against signals, including position sizing |
| FR-6 | System shall apply configurable transaction costs and slippage to simulated trades |
| FR-7 | System shall support splitting a dataset into in-sample and out-of-sample periods |
| FR-8 | System shall compute performance metrics: total return, Sharpe ratio, max drawdown, win rate, CAGR |
| FR-9 | System shall allow toggling costs on/off to compare their impact |
| FR-10 | System shall display equity curves, drawdown charts, and a strategy comparison table via a dashboard |
| FR-11 | System shall allow parameter changes for each strategy (e.g., moving average window) and re-run experiments |
| FR-12 | System shall log every experiment run (strategy, parameters, period, cost settings, results) for reproducibility |

### 2.2 Non-Functional Requirements

| ID | Requirement |
|---|---|
| NFR-1 | Reliability — engine output must be deterministic given identical inputs (no hidden randomness in simulation) |
| NFR-2 | Performance — a single strategy backtest over ~5 years of daily data for 10–15 stocks should complete in under 30 seconds on a standard laptop |
| NFR-3 | Usability — dashboard must let a non-technical evaluator compare strategies without reading code |
| NFR-4 | Maintainability — engine core, strategy logic, and data layer must be decoupled modules, not a single script |
| NFR-5 | Portability — must run on standard student hardware (no GPU, no paid cloud dependency, no paid data feeds) |
| NFR-6 | Transparency — every metric shown on the dashboard must be traceable to a documented formula, no black-box numbers |

### 2.3 Constraints

- Free/open data sources only (yfinance, NSE historical archives)
- No paid APIs or brokers
- Daily-bar resolution only (no tick-level data)
- Single asset class: equities
- Single market: Indian equities (NSE) with statutory cost modeling

### 2.4 Assumptions

- Historical data availability is sufficient and stable for the chosen stock universe
- Strategies are rule-based (with an optional simple ML-based strategy if the team chooses to extend scope)
- Users interacting with the dashboard have basic familiarity with financial terms (return, drawdown)

### 2.5 Use Cases

**UC-1: Run a single strategy backtest**
Actor: Student evaluator
Flow: Select strategy → select stock universe → select date range → select cost settings → run → view results

**UC-2: Compare multiple strategies**
Actor: Student evaluator
Flow: Select 2+ strategies → same universe/date range → run all → view side-by-side comparison table and overlaid equity curves

**UC-3: Test cost sensitivity**
Actor: Student evaluator
Flow: Select one strategy → toggle transaction costs on/off → run both → view performance delta

**UC-4: Test overfitting via out-of-sample validation**
Actor: Student evaluator
Flow: Select strategy → define in-sample period to tune parameters → apply best parameters to out-of-sample period → compare in-sample vs out-of-sample metrics

---

## 3. System Design Document

### 3.1 Architecture Overview

Four-layer architecture, deliberately decoupled so each layer can be tested independently:

```
┌─────────────────────────────────────────┐
│              Dashboard Layer             │  (Streamlit / Flask+HTML)
│   equity curves, comparison tables,      │
│   parameter controls, cost toggles       │
└───────────────────┬───────────────────────┘
                     │
┌────────────────────▼──────────────────────┐
│              Analytics Layer               │
│  Sharpe, drawdown, CAGR, win rate,         │
│  in/out-of-sample comparison               │
└────────────────────┬──────────────────────┘
                     │
┌────────────────────▼──────────────────────┐
│               Engine Layer                 │
│  Order, Position, Portfolio, BacktestEngine│
│  (event-driven simulation loop)            │
└────────────────────┬──────────────────────┘
                     │
┌────────────────────▼──────────────────────┐
│           Strategy & Data Layer            │
│  signal generation (3 strategies),         │
│  OHLCV fetch + cleaning                    │
└─────────────────────────────────────────────┘
```

### 3.2 Core Classes (Engine Layer)

```
Order
  - symbol, side (buy/sell), quantity, price, timestamp

Position
  - symbol, quantity, average_entry_price
  - method: update(order)
  - method: unrealized_pnl(current_price)

Portfolio
  - cash, positions: dict[symbol -> Position]
  - method: apply_order(order, cost_model)
  - method: total_value(current_prices)
  - method: equity_curve  # time series of total_value

BacktestEngine
  - portfolio: Portfolio
  - cost_model: CostModel
  - method: run(price_data, signals) -> Portfolio history
  # event-driven loop: for each day, check signals,
  # generate orders, apply cost model, update portfolio

CostModel
  - transaction_cost_pct, slippage_pct
  - method: apply(order) -> adjusted execution price
```

### 3.3 Strategy Interface (Strategy Layer)

All strategies implement a common interface so the engine treats them uniformly:

```
Strategy (interface)
  - method: generate_signals(price_data, params) -> signal series (buy/sell/hold per day)

Implementations:
  - SMACrossoverStrategy(short_window, long_window)
  - RSIMeanReversionStrategy(rsi_period, oversold_threshold, overbought_threshold)
  - MomentumStrategy(lookback_period)
```

### 3.4 Data Flow (Single Backtest Run)

1. User selects strategy + parameters + universe + date range + cost settings via dashboard
2. Data layer fetches/loads cleaned OHLCV data for the selected universe and range
3. Strategy layer generates a signal series from the price data
4. Engine layer runs the event-driven loop: for each day, evaluates signals, creates orders, applies cost model, updates portfolio state
5. Analytics layer computes metrics from the resulting equity curve
6. Dashboard renders equity curve, drawdown chart, and metrics table
7. Run parameters + results are logged for reproducibility (FR-12)

### 3.5 Module/Owner Mapping (2-Person Team)

| Module | Owner |
|---|---|
| Data fetch & cleaning | Person A (Aayush) |
| Strategy signal generation (3 strategies) | Person A |
| Parameter sensitivity experiments | Person A |
| Backtest engine core (Order/Position/Portfolio/Engine) | Person B (Meet) |
| Cost model (transaction costs + slippage) | Person B |
| Performance metrics computation | Person B |
| Dashboard & visualization | Person B |
| Experiment logging / reproducibility | Shared |
| Report writing & viva prep | Shared |

---

## 4. Data Design

### 4.1 Data Source
- Primary: `yfinance` Python library (Yahoo Finance)
- Fallback: NSE historical bhavcopy archives (CSV)

### 4.2 Data Schema (Interface Contract Between Data Layer and Engine)

| Field | Type | Notes |
|---|---|---|
| date | datetime | trading day |
| symbol | string | stock ticker |
| open, high, low, close | float | adjusted for splits/dividends |
| volume | integer | shares traded |

### 4.3 Data Cleaning Rules
- Drop days with missing OHLC values for a symbol rather than forward-filling (forward-filling can silently introduce look-ahead-adjacent bias)
- Use adjusted close for return calculations to correctly account for splits and dividends
- Explicitly document the date range and any excluded symbols/gaps in the final report

### 4.4 Experiment Log Schema

| Field | Notes |
|---|---|
| run_id | unique identifier |
| strategy_name, parameters | e.g., SMA(20,50) |
| universe, date_range | which stocks, which period |
| in_sample / out_of_sample flag | |
| cost_settings | costs on/off, cost %, slippage % |
| resulting_metrics | Sharpe, drawdown, return, win rate |

---

## 5. Testing Plan

| Test type | What it covers | Owner |
|---|---|---|
| Unit tests — Portfolio | Order application updates cash/position correctly | Person B |
| Unit tests — CostModel | Cost/slippage adjustments applied correctly to execution price | Person B |
| Unit tests — Metrics | Sharpe/drawdown/CAGR formulas verified against known hand-calculated examples | Person B |
| Unit tests — Strategy signals | Each strategy produces expected signals on a small synthetic price series with a known correct answer | Person A |
| Integration test | Full run of Strategy #1 through the engine produces a plausible, non-crashing equity curve | Both (Phase 2 sync checkpoint) |
| Experiment validation | Full 3-strategy × cost-toggle × in/out-of-sample matrix runs without error and produces sane, explainable numbers | Both (Phase 3 sync checkpoint) |
| Sanity checks | Manually verify a handful of individual trades against raw price charts to catch silent logic bugs | Both |

---

## 6. Roadmap (Phase-Based, Parallel Tracks)

*(No fixed week estimates — advance to the next phase only once the sync checkpoint is met.)*

### Phase 1 — Foundation
**Track A (Strategy & Data):** study look-ahead bias/overfitting/survivorship bias; finalize the 3 strategies; finalize the stock universe; verify data is fetchable and clean.
**Track B (Engine & Analytics):** design engine architecture on paper (classes above); choose event-driven loop design; set up repo, Git workflow, pytest skeleton.
**✅ Sync checkpoint:** Data schema (Section 4.2) agreed and data pipeline returns clean OHLCV in that format.

### Phase 2 — Core Build
**Track A:** implement signal generation for all 3 strategies; finalize dataset cleaning; visually sanity-check signals against price charts.
**Track B:** build the core backtest loop; add configurable transaction costs/slippage; write unit tests for fill logic and PnL.
**✅ Sync checkpoint:** Strategy #1 runs end-to-end through the engine and produces a plausible equity curve.

### Phase 3 — Full Experiments
**Track A:** get all 3 strategies running through the engine; design in-sample/out-of-sample split; run parameter sensitivity checks.
**Track B:** compute Sharpe/drawdown/win rate/CAGR; build the comparison dashboard; add a with/without-costs toggle.
**✅ Sync checkpoint:** Full experiment matrix (3 strategies × costs on/off × in/out-of-sample) runs and displays correctly on the dashboard.

### Phase 4 — Analysis, Modification, Defense Prep (done together)
Analyze where strategies degraded out-of-sample and why; tune/fix based on findings (satisfies syllabus Unit 4); document explicit limitations; write final report (Track A: strategy/results sections, Track B: engine/methodology sections, both: conclusion); rehearse viva answers to ALL questions, not just track-specific ones.
**✅ Sync checkpoint:** Each person can independently explain and defend the other's subsystem.

---

## 7. Repository Structure

```
quantlab/
├── README.md                    # this document, or a summary + link to it
├── data/
│   ├── raw/                     # untouched downloaded data
│   └── processed/                # cleaned OHLCV, gitignored if large
├── src/
│   ├── data/
│   │   ├── fetch.py
│   │   └── clean.py
│   ├── strategies/
│   │   ├── base.py               # Strategy interface
│   │   ├── sma_crossover.py
│   │   ├── rsi_mean_reversion.py
│   │   └── momentum.py
│   ├── engine/
│   │   ├── order.py
│   │   ├── position.py
│   │   ├── portfolio.py
│   │   ├── cost_model.py
│   │   └── backtest_engine.py
│   ├── analytics/
│   │   └── metrics.py
│   └── dashboard/
│       └── app.py                # Streamlit entry point
├── tests/
│   ├── test_engine.py
│   ├── test_cost_model.py
│   ├── test_metrics.py
│   └── test_strategies.py
├── experiments/
│   └── experiment_log.csv        # FR-12 reproducibility log
├── docs/
│   ├── 00_management/           # LEDGER.md, execution_plan.md
│   ├── 01_unit1_literature/     # problem_statement.md, literature_review.md
│   ├── 02_unit2_specifications/ # mathematical_specifications.md, stock_universe.md, srs.md
│   ├── 03_unit3_testing/        # test_plan.md, golden_fixtures.md
│   ├── 04_unit4_redesign/       # out_of_sample_decay.md, parameter_stability.md
│   └── 05_unit5_defense/        # final_report.md, viva_master_guide.md
└── requirements.txt
```

---

## 8. Scope & Limitations

**In scope:**
- 3 rule-based strategies, 1 equity market, daily-bar backtesting
- Transaction cost and slippage modeling
- In-sample/out-of-sample validation

**Explicitly out of scope (state this in the report — it strengthens the viva, not weakens it):**
- No live/paper trading execution — backtesting only
- No tick-level or intraday data
- No partial order fills — orders assumed fully filled at (adjusted) price
- No multi-asset-class support (equities only)
- Not a production trading recommendation system

---

## 9. Risk Register

| Risk | Impact | Mitigation |
|---|---|---|
| Using an off-the-shelf library (`backtrader`) instead of building the engine | Cannot defend internals in viva | Commit to building the engine core in-house (Section 3.2) |
| Scope creep — adding a 4th/5th strategy | Depth suffers, integration risk rises late in semester | Hard cap at 3 strategies (Section 2.3) |
| Free data source has gaps/adjustment issues | Silent wrong results | Budget explicit time in Phase 1/2 for data cleaning validation |
| One track blocks on the other due to undefined interface | Wasted time, late integration bugs | Sync checkpoints per phase (Section 6), data schema fixed early |
| Overclaiming results ("this strategy works") | Weak/indefensible viva claims | Frame all findings as "under these assumptions, for this period" |

---

## 10. Syllabus Mapping (GTU DI05000341)

| Syllabus Unit | Project Activity |
|---|---|
| Unit 1 — Literature review, problem identification | Section 1.1, Phase 1 literature study |
| Unit 2 — Alternative solutions, budget/feasibility | Section 2 (SRS), 3 strategies compared, free/open-source stack |
| Unit 3 — Implementation, testing | Section 3 (Design), Section 5 (Testing Plan), Phase 2–3 |
| Unit 4 — Modification/redesign based on results | Phase 4 — tuning based on out-of-sample findings |
| Unit 5 — Final defense, report, presentation | Section 11 (Viva Prep), final report deliverable |

---

## 11. Viva Preparation

Both team members should be able to answer all of the following, not just questions tied to their own module:

- What is look-ahead bias, and how does this engine specifically avoid it?
- Why is a profitable backtest not proof of a profitable strategy?
- Why include slippage and transaction costs — what changed in your results when you added them?
- What is overfitting, and where did you observe evidence of it (or not) in your out-of-sample results?
- Why is out-of-sample testing done specifically the way you did it — what would happen without it?
- What does the Sharpe ratio measure, and what does it fail to capture?
- What does your engine NOT model, and why is that an acceptable limitation for a diploma-level prototype?
- Why did you build your own engine instead of using an existing library?

---

## 12. References

- Suggested reading: search "backtesting overfitting bias" and "algorithmic trading transaction cost slippage" on Google Scholar / SSRN for accessible papers to cite in the literature review
- Data: `yfinance` Python package documentation; NSE India historical data archives
- Libraries: pandas, NumPy, Matplotlib/Plotly, Streamlit, pytest

---

*This document consolidates the SRS, design, roadmap, and supporting material for the QuantLab minor project (DI05000341). Keep it in `docs/` and update it as the project evolves — it should reflect the actual system, not just the plan.*
