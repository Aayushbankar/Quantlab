# QuantLab — Complete Day-by-Day Execution Plan

**Timeline**: August 14 → September 11, 2026 (29 days)
**Team**: Aayush (A) — Data & Strategies | Meet (M) — Engine & Dashboard
**Daily commitment**: ~3–4 focused hours per person

---

## Calendar Overview

```
     AUGUST 2026                          SEPTEMBER 2026
Mo Tu We Th Fr Sa Su                   Mo Tu We Th Fr Sa Su
             14 15 16 17                  1  2  3  4  5  6  7
18 19 20 21 22 23 24                    8  9 10 11 ← DEADLINE
25 26 27 28 29 30 31

Phase 1 ████░░░░░░░░░░░░░░░░░░░░░░░░░  Aug 14–20  (Foundation)
Phase 2 ░░░░████████████░░░░░░░░░░░░░░  Aug 21–31  (Core Build)
Phase 3 ░░░░░░░░░░░░░░░░████████░░░░░░  Sep 1–7    (Experiments + Dashboard)
Phase 4 ░░░░░░░░░░░░░░░░░░░░░░░░██████  Sep 8–11   (Report + Defense)
```

---

## Phase 1 — Foundation (Aug 14–20)

> **Goal**: Repo is set up, data pipeline works, engine architecture is designed on paper, both agree on the data schema contract.

---

### Day 1 — Thu, Aug 14

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Literature study: read about look-ahead bias, overfitting, survivorship bias | Set up GitHub repo with full directory structure (Section 7 of docs) |
| **Deliverable** | 1-page notes summarizing the 3 biases in your own words | Repo live with `src/`, `tests/`, `data/`, `experiments/` folders, `requirements.txt`, `.gitignore`, `README.md` |
| **Time** | 2–3 hrs | 2 hrs |

```
quantlab/
├── README.md
├── requirements.txt          ← pandas, numpy, yfinance, matplotlib, plotly, streamlit, pytest
├── .gitignore                ← data/raw/, __pycache__, .env
├── data/raw/
├── data/processed/
├── src/data/
├── src/strategies/
├── src/engine/
├── src/analytics/
├── src/dashboard/
├── tests/
├── experiments/
└── docs/
```

---

### Day 2 — Fri, Aug 15 (Independence Day — lighter day)

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Study the 3 strategies in depth: SMA crossover, RSI mean-reversion, momentum. Write down exact formulas and signal rules | Design engine classes on paper. Define the interface for Order, Position, Portfolio, CostModel, BacktestEngine |
| **Deliverable** | Strategy spec doc: formulas, parameters, buy/sell/hold conditions for each | Class diagram or markdown with all class attributes + methods |
| **Time** | 2 hrs | 2 hrs |

---

### Day 3 — Sat, Aug 16

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Write `src/data/fetch.py` — fetch OHLCV data using yfinance. Test with 3 stocks (e.g., RELIANCE.NS, TCS.NS, INFY.NS) | Write `src/engine/order.py` and `src/engine/position.py` — implement the two simplest classes |
| **Deliverable** | Script that downloads and saves OHLCV CSVs to `data/raw/` | `Order` dataclass + `Position` class with `update()` and `unrealized_pnl()` |
| **Time** | 3 hrs | 3 hrs |

---

### Day 4 — Sun, Aug 17

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Finalize stock universe: pick 10–15 Indian stocks across sectors. Test data availability for 5-year range (2019–2024). Document any gaps | Study event-driven backtesting loop design. Read how the loop should process: get bar → compute signal → generate order → fill → update portfolio |
| **Deliverable** | `docs/stock_universe.md` with ticker list, sectors, date range, any data gaps noted | Pseudocode for the main `BacktestEngine.run()` loop |
| **Time** | 2 hrs | 2 hrs |

---

### Day 5 — Mon, Aug 18

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Write `src/data/clean.py` — drop missing OHLC rows, use adjusted close, validate data integrity | Write `src/engine/portfolio.py` — cash management, position dict, `apply_order()`, `total_value()` |
| **Deliverable** | Cleaning function that takes raw CSV → returns clean DataFrame in schema format (date, symbol, O, H, L, C, volume) | `Portfolio` class with all methods. Manual test: create portfolio with ₹100,000, apply a buy order, check cash and positions |
| **Time** | 3 hrs | 3–4 hrs |

---

### Day 6 — Tue, Aug 19

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Write `tests/test_data.py` — unit tests for data cleaning. Validate output format, no NaN values, correct date range | Write `src/engine/cost_model.py` — `CostModel` class with `transaction_cost_pct`, `slippage_pct`, `apply()` method |
| **Deliverable** | 3–5 passing pytest tests | `CostModel` that adjusts execution price. Example: buy at ₹100, with 0.1% cost + 0.05% slippage → fill at ₹100.15 |
| **Time** | 2 hrs | 2–3 hrs |

---

### Day 7 — Wed, Aug 20

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Write `src/strategies/base.py` — Strategy abstract base class with `generate_signals()` interface | Write `tests/test_engine.py` and `tests/test_cost_model.py` — unit tests for Portfolio and CostModel |
| **Deliverable** | Base class that all strategies will inherit from | 5–8 passing pytest tests covering: order application, cash updates, cost adjustments, edge cases |
| **Time** | 1–2 hrs | 3 hrs |

### 🔄 SYNC CHECKPOINT 1 — Wed evening, Aug 20

> **Both sit together (call/meet) and verify:**
> - [ ] Aayush's cleaned data output is a DataFrame with columns: `date`, `symbol`, `open`, `high`, `low`, `close`, `volume`
> - [ ] Meet's engine classes expect exactly that format
> - [ ] Both can run `pytest` and see all tests pass
> - [ ] Git repo has clean commits from both

---

## Phase 2 — Core Build (Aug 21–31)

> **Goal**: All 3 strategies implemented, engine runs end-to-end, unit tests pass, all strategies produce plausible equity curves.

---

### Day 8 — Thu, Aug 21

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Implement `src/strategies/sma_crossover.py` — SMA crossover signal generation | Implement `src/engine/backtest_engine.py` — the core event-driven loop |
| **Deliverable** | `SMACrossoverStrategy` class: takes price data + params (short_window, long_window) → returns signal series (1=buy, -1=sell, 0=hold) | `BacktestEngine.run(price_data, signals)` → iterates day-by-day, creates orders from signals, calls `portfolio.apply_order()` with cost model |
| **Time** | 3 hrs | 4 hrs |

---

### Day 9 — Fri, Aug 22

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Visually validate SMA signals: plot price chart with SMA lines + buy/sell markers for 1 stock | Connect engine to Portfolio + CostModel. Test with hardcoded dummy signals (buy on day 5, sell on day 20) |
| **Deliverable** | Saved chart image showing signals make intuitive sense (buys at golden crosses, sells at death crosses) | Engine produces a portfolio history (list of daily portfolio values) from dummy signals. No crashes. |
| **Time** | 2 hrs | 3 hrs |

---

### Day 10 — Sat, Aug 23

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Implement `src/strategies/rsi_mean_reversion.py` | Integrate real SMA strategy with engine. Feed Aayush's SMA signals into the engine |
| **Deliverable** | `RSIMeanReversionStrategy` class with params: rsi_period, oversold_threshold, overbought_threshold | **First real equity curve** — SMA strategy on RELIANCE.NS, 2019–2024, costs OFF. Save the chart. |
| **Time** | 3 hrs | 3 hrs |

---

### Day 11 — Sun, Aug 24 (Buffer Day)

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Debug any issues from Days 8–10. Review Meet's engine code | Debug any issues from Days 8–10. Review Aayush's strategy code |
| **Deliverable** | Both understand each other's code well enough to explain it | Clean, working integration of SMA → Engine |
| **Time** | 1–2 hrs | 1–2 hrs |

> [!WARNING]
> **Do NOT skip this buffer day.** Integration bugs always appear. Use this day to fix them before moving forward.

---

### Day 12 — Mon, Aug 25

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Implement `src/strategies/momentum.py`. Test RSI signals visually (same as Day 9 for RSI) | Add `equity_curve` property to Portfolio (time series of daily total values). Run RSI strategy through engine |
| **Deliverable** | `MomentumStrategy` class + RSI signal validation chart | RSI equity curve generated. Portfolio tracks daily values correctly |
| **Time** | 3–4 hrs | 3 hrs |

---

### Day 13 — Tue, Aug 26

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Test Momentum signals visually. Write `tests/test_strategies.py` — unit tests for all 3 strategies using synthetic price data with known correct signals | Run Momentum strategy through engine. Fix any remaining integration bugs |
| **Deliverable** | 6–9 passing strategy tests (2–3 per strategy). Example: feed a steadily rising price → SMA should signal BUY | All 3 strategies produce equity curves. No crashes on any stock |
| **Time** | 3–4 hrs | 3 hrs |

---

### Day 14 — Wed, Aug 27

### 🔄 SYNC CHECKPOINT 2 — Wed, Aug 27

> **Critical milestone. Both verify together:**
> - [ ] SMA Crossover runs end-to-end → plausible equity curve ✓
> - [ ] RSI Mean Reversion runs end-to-end → plausible equity curve ✓
> - [ ] Momentum runs end-to-end → plausible equity curve ✓
> - [ ] All unit tests pass (`pytest` green) ✓
> - [ ] Manually verify 2–3 individual trades against raw price charts (sanity check) ✓

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Fix any strategy bugs found during checkpoint. Manually verify trades | Fix any engine bugs found during checkpoint. Manually verify fill prices |
| **Deliverable** | All 3 strategies validated and bug-free | Engine produces correct fill prices (including cost adjustments) |
| **Time** | 2–3 hrs | 2–3 hrs |

---

### Day 15 — Thu, Aug 28

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Run all 3 strategies on the full stock universe (10–15 stocks). Log results | Implement `src/analytics/metrics.py` — start with `total_return()` and `cagr()` |
| **Deliverable** | 3 × 15 = 45 equity curves generated (can be batch-run). Note any issues | Two metric functions, tested against hand-calculated examples |
| **Time** | 3 hrs | 3 hrs |

---

### Day 16 — Fri, Aug 29

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Design the in-sample / out-of-sample split. Decide on dates (e.g., IS: 2019–2022, OOS: 2023–2024) | Implement `sharpe_ratio()`, `max_drawdown()`, `win_rate()` in metrics.py |
| **Deliverable** | Document: IS period, OOS period, rationale for split point | All 5 metrics implemented. `tests/test_metrics.py` with hand-calculated verification |
| **Time** | 2 hrs | 3–4 hrs |

---

### Day 17 — Sat, Aug 30

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Implement IS/OOS split in data layer — function that splits data by date range | Start `src/dashboard/app.py` — basic Streamlit layout: sidebar with strategy selector, stock selector, date range picker |
| **Deliverable** | `split_data(df, is_end_date)` → returns `(is_data, oos_data)` | Running Streamlit app with sidebar controls (no engine connection yet) |
| **Time** | 2 hrs | 3 hrs |

---

### Day 18 — Sun, Aug 31

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Test IS/OOS split: run SMA on IS period, then same params on OOS period. Compare manually | Dashboard: connect to engine. User picks strategy + stock → click "Run" → shows equity curve |
| **Deliverable** | First IS vs OOS comparison numbers for 1 strategy | Working dashboard prototype: select → run → see chart |
| **Time** | 2–3 hrs | 3–4 hrs |

---

## Phase 3 — Full Experiments + Dashboard (Sep 1–7)

> **Goal**: Complete experiment matrix, polished dashboard, all results documented.

---

### Day 19 — Mon, Sep 1

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Run parameter sensitivity for SMA: test (10,30), (15,40), (20,50), (25,60), (30,100). Log all results | Dashboard: add cost toggle (checkbox: "Include transaction costs"), connect to CostModel |
| **Deliverable** | Table: SMA params → return, Sharpe, drawdown for each | Toggle works: same strategy with/without costs shows different equity curves |
| **Time** | 3 hrs | 3 hrs |

---

### Day 20 — Tue, Sep 2

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Run parameter sensitivity for RSI (vary period, oversold, overbought) and Momentum (vary lookback). Log results | Dashboard: add metrics table below equity curve. Show all 5 metrics |
| **Deliverable** | Parameter sensitivity tables for RSI and Momentum | Metrics display correctly after each run |
| **Time** | 3 hrs | 3 hrs |

---

### Day 21 — Wed, Sep 3

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Implement experiment logging: `experiments/experiment_log.csv` with columns from Section 4.4 | Dashboard: add drawdown chart + strategy comparison view (run multiple strategies, see side-by-side table) |
| **Deliverable** | Every experiment auto-logs to CSV: run_id, strategy, params, universe, period, costs, metrics | Comparison table showing all strategies' metrics next to each other |
| **Time** | 3 hrs | 4 hrs |

---

### Day 22 — Thu, Sep 4

### 🔄 SYNC CHECKPOINT 3 — Thu, Sep 4

> **Full experiment matrix must work. Both verify:**
> - [ ] 3 strategies × 2 cost settings × 2 periods (IS/OOS) = **12 runs** all complete ✓
> - [ ] All 12 runs display on dashboard ✓
> - [ ] Experiment log CSV has all 12 entries ✓
> - [ ] Cost toggle visually shows impact ✓
> - [ ] IS vs OOS comparison visible ✓

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Run the COMPLETE experiment matrix. Fix any data/strategy issues | Dashboard bug fixes. Ensure all charts render correctly |
| **Deliverable** | `experiment_log.csv` with all 12+ runs logged | Dashboard handles all combinations without crashes |
| **Time** | 3–4 hrs | 3–4 hrs |

---

### Day 23 — Fri, Sep 5

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Analyze results: write down observations. Where did strategies degrade OOS? Which strategy survived costs best? | Dashboard polish: better colors, clear labels, responsive layout, add IS/OOS comparison view |
| **Deliverable** | 1-page analysis notes with key findings for each research question (RQ1–RQ4) | Polished, presentation-ready dashboard |
| **Time** | 3 hrs | 3–4 hrs |

---

### Day 24 — Sat, Sep 6

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Run final experiments on best parameters. Take screenshots of all charts for report | Add "About" section to dashboard explaining each metric's formula. Final testing |
| **Deliverable** | Folder of screenshots: equity curves, drawdown charts, comparison tables, cost impact views | Dashboard is feature-complete and bug-free |
| **Time** | 2–3 hrs | 2–3 hrs |

---

### Day 25 — Sun, Sep 7 (Buffer Day)

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Catch up on any incomplete tasks. Run any missing experiments | Catch up on any incomplete tasks. Fix any remaining bugs |
| **Deliverable** | Everything from Phase 3 is done | Everything from Phase 3 is done |
| **Time** | 2–3 hrs | 2–3 hrs |

---

## Phase 4 — Report + Viva Prep (Sep 8–11)

> **Goal**: Report written, viva rehearsed, everything submitted.

---

### Day 26 — Mon, Sep 8

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Write report sections: Problem Statement, Literature Review, Data Design, Strategy Descriptions, Results & Analysis | Write report sections: System Architecture, Engine Design, Cost Model, Metrics, Dashboard, Testing |
| **Deliverable** | ~3–4 pages of report content (your sections) | ~3–4 pages of report content (your sections) |
| **Time** | 4 hrs | 4 hrs |

---

### Day 27 — Tue, Sep 9

| | Aayush (A) | Meet (M) |
|---|---|---|
| **Task** | Write: Conclusion, Limitations, Future Work. Insert charts/screenshots into report | Write: Introduction, Table of Contents, References. Review Aayush's sections |
| **Deliverable** | Report is ~80% complete | Report is ~80% complete. Cross-review done |
| **Time** | 3–4 hrs | 3–4 hrs |

---

### Day 28 — Wed, Sep 10

| | Both Together |
|---|---|
| **Task** | Finalize report. Merge sections. Proofread. Ensure charts, tables, references are correct |
| **Deliverable** | Complete `docs/final_report.md` or `.docx` |
| **Time** | 2–3 hrs |

| | Both Together |
|---|---|
| **Task** | **Viva rehearsal**. Practice answering ALL 8 viva questions (Section 11 of docs). Each person explains the OTHER person's subsystem |
| **Focus Areas** | Aayush must explain: engine loop, cost model, portfolio tracking. Meet must explain: strategy logic, data cleaning, parameter sensitivity |
| **Time** | 2 hrs |

---

### Day 29 — Thu, Sep 11 🎯 DEADLINE

| | Both Together |
|---|---|
| **Morning** | Final review of report. Run dashboard one last time. Ensure everything works |
| **Afternoon** | Submit. Clean up repo. Update README with final instructions |
| **Deliverable** | ✅ Code complete, ✅ Dashboard working, ✅ Report submitted, ✅ Both ready for viva |

---

## Progress Tracking Checklist

### Phase 1 — Foundation (Aug 14–20)
- [ ] Literature study notes complete (A)
- [ ] Repo set up with full structure (M)
- [ ] Strategy formulas documented (A)
- [ ] Engine class interfaces designed (M)
- [ ] `fetch.py` working — downloads OHLCV data (A)
- [ ] `Order` and `Position` classes implemented (M)
- [ ] Stock universe finalized — 10–15 tickers documented (A)
- [ ] `Portfolio` class implemented with `apply_order()` (M)
- [ ] `clean.py` working — handles missing data, adjusted close (A)
- [ ] `CostModel` class implemented (M)
- [ ] Data cleaning unit tests pass (A)
- [ ] Engine + CostModel unit tests pass (M)
- [ ] Strategy base interface created (A)
- [ ] **🔄 CHECKPOINT 1**: Data schema agreed, both sides compatible ✓

### Phase 2 — Core Build (Aug 21–31)
- [ ] `SMACrossoverStrategy` implemented and signals validated (A)
- [ ] `BacktestEngine.run()` loop implemented (M)
- [ ] `RSIMeanReversionStrategy` implemented and signals validated (A)
- [ ] First real equity curve generated (SMA on RELIANCE) (M)
- [ ] `MomentumStrategy` implemented and signals validated (A)
- [ ] All 3 strategies run through engine without crashes (M)
- [ ] Strategy unit tests pass — all 3 strategies (A)
- [ ] **🔄 CHECKPOINT 2**: All 3 strategies produce plausible equity curves ✓
- [ ] `total_return()`, `cagr()` implemented (M)
- [ ] `sharpe_ratio()`, `max_drawdown()`, `win_rate()` implemented (M)
- [ ] IS/OOS data split function implemented (A)
- [ ] Metrics unit tests pass (M)
- [ ] Basic Streamlit dashboard running (M)
- [ ] First IS vs OOS comparison done (A)

### Phase 3 — Experiments + Dashboard (Sep 1–7)
- [ ] Parameter sensitivity for SMA done (A)
- [ ] Parameter sensitivity for RSI done (A)
- [ ] Parameter sensitivity for Momentum done (A)
- [ ] Cost toggle working on dashboard (M)
- [ ] Metrics table on dashboard (M)
- [ ] Drawdown chart on dashboard (M)
- [ ] Strategy comparison table on dashboard (M)
- [ ] Experiment logging to CSV implemented (A)
- [ ] **🔄 CHECKPOINT 3**: Full 12-cell experiment matrix runs on dashboard ✓
- [ ] Results analysis written (A)
- [ ] Dashboard polished and presentation-ready (M)
- [ ] All screenshots captured (A)

### Phase 4 — Report + Defense (Sep 8–11)
- [ ] Report: Aayush's sections complete (strategy, data, results)
- [ ] Report: Meet's sections complete (engine, metrics, architecture)
- [ ] Report merged and proofread
- [ ] Viva rehearsal done — each explains the other's work
- [ ] **✅ SUBMITTED** — Sep 11

---

## Emergency Contingency Plan

> [!CAUTION]
> If you fall behind by 2+ days, cut scope in this priority order:

| Cut Priority | What to Cut | Impact |
|---|---|---|
| Cut last | IS/OOS validation | Don't cut this — it's the core research contribution |
| Cut last | Cost toggle | Don't cut this — it's the second key feature |
| Cut 3rd | Parameter sensitivity experiments | Reduce from 5 param combos to 2 per strategy |
| Cut 2nd | Dashboard polish | Use basic Streamlit defaults, skip styling |
| Cut 1st | Experiment logging (CSV) | Can manually document runs in the report instead |
| **Never cut** | The 3 strategies + engine + metrics | This is the minimum viable project |

---

## Daily Standup Template

Use this every morning (2 minutes each, via WhatsApp/call):

```
1. What did I finish yesterday?
2. What am I doing today?
3. Am I blocked on anything?
```

If either person is blocked, fix it THAT DAY. Don't let blockers accumulate.

---

*This plan gives you **29 days** with **4 buffer/catch-up days** built in (Aug 17, 24, Sep 7, and slack on weekends). Follow the checkpoints strictly — they're your early warning system.*
