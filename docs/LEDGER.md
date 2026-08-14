# QuantLab — Progress Ledger

**Project**: QuantLab — Realistic Backtesting Engine
**Team**: Aayush (A) | Meet (M)
**Timeline**: Aug 14 – Sep 11, 2026

> Update this file daily. Commit after each update.

---

## Legend

- ✅ Done
- 🔄 In Progress
- ❌ Not Started
- ⏭️ Skipped
- 🐛 Blocked

---

## Phase 1 — Foundation (Aug 14–20)

### Day 1 — Thu, Aug 14

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Literature study: look-ahead bias, overfitting, survivorship bias | ❌ | |
| M | Set up repo structure, requirements.txt, .gitignore, pytest skeleton | ❌ | |

### Day 2 — Fri, Aug 15

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Study 3 strategies in depth, document formulas & signal rules | ❌ | |
| M | Design engine classes on paper: Order, Position, Portfolio, CostModel, BacktestEngine | ❌ | |

### Day 3 — Sat, Aug 16

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Write `src/data/fetch.py` — yfinance OHLCV download, test with 3 stocks | ❌ | |
| M | Implement `Order` dataclass + `Position` class | ❌ | |

### Day 4 — Sun, Aug 17

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Finalize stock universe (10–15 tickers), test data availability | ❌ | |
| M | Study event-driven loop design, write pseudocode for `BacktestEngine.run()` | ❌ | |

### Day 5 — Mon, Aug 18

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Write `src/data/clean.py` — drop missing, adjusted close, validate | ❌ | |
| M | Implement `Portfolio` class — cash, positions, apply_order, total_value | ❌ | |

### Day 6 — Tue, Aug 19

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Write `tests/test_data.py` — unit tests for data cleaning | ❌ | |
| M | Implement `CostModel` class — transaction_cost_pct, slippage_pct, apply() | ❌ | |

### Day 7 — Wed, Aug 20

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Write `src/strategies/base.py` — Strategy abstract base class | ❌ | |
| M | Write `tests/test_engine.py` + `tests/test_cost_model.py` | ❌ | |

### 🔄 Checkpoint 1 — Wed, Aug 20

| Check | Status |
|---|---|
| Data schema agreed (date, symbol, O, H, L, C, volume) | ❌ |
| Cleaned data output matches engine input format | ❌ |
| All tests pass (`pytest`) | ❌ |
| Git repo has clean commits from both | ❌ |

---

## Phase 2 — Core Build (Aug 21–31)

### Day 8 — Thu, Aug 21

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Implement `SMACrossoverStrategy` — signal generation | ❌ | |
| M | Implement `BacktestEngine.run()` — core event-driven loop | ❌ | |

### Day 9 — Fri, Aug 22

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Visually validate SMA signals — plot price + buy/sell markers | ❌ | |
| M | Connect engine to Portfolio + CostModel, test with dummy signals | ❌ | |

### Day 10 — Sat, Aug 23

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Implement `RSIMeanReversionStrategy` | ❌ | |
| M | Integrate SMA strategy with engine → first real equity curve | ❌ | |

### Day 11 — Sun, Aug 24 (Buffer)

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Debug Days 8–10 issues, review Meet's engine code | ❌ | |
| M | Debug Days 8–10 issues, review Aayush's strategy code | ❌ | |

### Day 12 — Mon, Aug 25

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Implement `MomentumStrategy`, validate RSI signals visually | ❌ | |
| M | Add `equity_curve` to Portfolio, run RSI through engine | ❌ | |

### Day 13 — Tue, Aug 26

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Validate Momentum signals, write `tests/test_strategies.py` | ❌ | |
| M | Run Momentum through engine, fix integration bugs | ❌ | |

### Day 14 — Wed, Aug 27

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Fix any strategy bugs from checkpoint | ❌ | |
| M | Fix any engine bugs from checkpoint | ❌ | |

### 🔄 Checkpoint 2 — Wed, Aug 27

| Check | Status |
|---|---|
| SMA runs end-to-end → plausible equity curve | ❌ |
| RSI runs end-to-end → plausible equity curve | ❌ |
| Momentum runs end-to-end → plausible equity curve | ❌ |
| All unit tests pass | ❌ |
| 2–3 trades manually verified against price charts | ❌ |

### Day 15 — Thu, Aug 28

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Run all 3 strategies on full stock universe, log results | ❌ | |
| M | Implement `total_return()` and `cagr()` in metrics.py | ❌ | |

### Day 16 — Fri, Aug 29

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Design IS/OOS split dates, document rationale | ❌ | |
| M | Implement `sharpe_ratio()`, `max_drawdown()`, `win_rate()` + tests | ❌ | |

### Day 17 — Sat, Aug 30

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Implement `split_data()` for IS/OOS | ❌ | |
| M | Start Streamlit dashboard — basic layout + sidebar controls | ❌ | |

### Day 18 — Sun, Aug 31

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Test IS/OOS split with SMA, first comparison | ❌ | |
| M | Dashboard: connect to engine, strategy → run → equity curve | ❌ | |

---

## Phase 3 — Experiments + Dashboard (Sep 1–7)

### Day 19 — Mon, Sep 1

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Parameter sensitivity for SMA (5 param combos), log results | ❌ | |
| M | Dashboard: add cost toggle, connect to CostModel | ❌ | |

### Day 20 — Tue, Sep 2

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Parameter sensitivity for RSI + Momentum, log results | ❌ | |
| M | Dashboard: add metrics table below equity curve | ❌ | |

### Day 21 — Wed, Sep 3

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Implement experiment logging to `experiments/experiment_log.csv` | ❌ | |
| M | Dashboard: add drawdown chart + strategy comparison table | ❌ | |

### Day 22 — Thu, Sep 4

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Run COMPLETE 12-cell experiment matrix, fix data issues | ❌ | |
| M | Dashboard bug fixes, ensure all chart combos render | ❌ | |

### 🔄 Checkpoint 3 — Thu, Sep 4

| Check | Status |
|---|---|
| 12-cell experiment matrix (3 strats × 2 costs × 2 periods) complete | ❌ |
| All 12 runs display on dashboard | ❌ |
| experiment_log.csv has all entries | ❌ |
| Cost toggle visually shows impact | ❌ |
| IS vs OOS comparison visible | ❌ |

### Day 23 — Fri, Sep 5

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Analyze results: write observations for RQ1–RQ4 | ❌ | |
| M | Dashboard polish: colors, labels, responsive layout, IS/OOS view | ❌ | |

### Day 24 — Sat, Sep 6

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Run final experiments, capture all screenshots for report | ❌ | |
| M | Add metric formula tooltips to dashboard, final testing | ❌ | |

### Day 25 — Sun, Sep 7 (Buffer)

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Catch up on any incomplete Phase 3 tasks | ❌ | |
| M | Catch up on any incomplete Phase 3 tasks | ❌ | |

---

## Phase 4 — Report + Viva (Sep 8–11)

### Day 26 — Mon, Sep 8

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Write report: Problem Statement, Literature Review, Data, Strategies, Results | ❌ | |
| M | Write report: Architecture, Engine, Cost Model, Metrics, Dashboard, Testing | ❌ | |

### Day 27 — Tue, Sep 9

| Owner | Task | Status | Notes |
|---|---|---|---|
| A | Write: Conclusion, Limitations, Future Work. Insert charts | ❌ | |
| M | Write: Introduction, ToC, References. Cross-review Aayush's sections | ❌ | |

### Day 28 — Wed, Sep 10

| Owner | Task | Status | Notes |
|---|---|---|---|
| Both | Finalize report — merge, proofread, format | ❌ | |
| Both | Viva rehearsal — each explains the other's subsystem | ❌ | |

### Day 29 — Thu, Sep 11 🎯

| Owner | Task | Status | Notes |
|---|---|---|---|
| Both | Final review, run dashboard one last time | ❌ | |
| Both | **SUBMIT** | ❌ | |

### 🔄 Checkpoint 4 (Final) — Sep 11

| Check | Status |
|---|---|
| Code complete and working | ❌ |
| Dashboard runs without errors | ❌ |
| Report complete and proofread | ❌ |
| Both can explain each other's subsystem | ❌ |
| Submitted | ❌ |

---

## Change Log

| Date | What Changed | Who |
|---|---|---|
| Aug 14 | Ledger created | — |
