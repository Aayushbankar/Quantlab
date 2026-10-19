# QuantLab: The Master 6-Level WWWH Engineering & Financial Bible
**GTU Diploma Engineering — Semester 5 Minor Project (DI05000341)**  
**Team**: Aayush Avinash Bankar (Technical Engine & Quantitative Architect) & Meet Jayeshbhai Patel (Frontend Architect & Empirical Quantitative Analyst)

---

# 👥 TEAM DIVISION & OWNERSHIP CONTRACT

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   QUANTLAB TEAM ROLES                                       │
├─────────────────────────────────────────────┬───────────────────────────────────────────────┤
│ AAYUSH BANKAR (Leader & Engine Architect)   │ MEET PATEL (Frontend & Empirical Analyst)     │
├─────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ 1. Discrete-Event Simulation Loop Core      │ 1. Streamlit Interactive Master Dashboard UI  │
│ 2. Zero-Lookahead Queue Invariant Logic     │ 2. Plotly Visual Components & Waterfall Charts│
│ 3. Portfolio State Machine & Cash Invariant │ 3. Data Ingestion & Timezone Cleaning Pipeline│
│ 4. Total-Equity Dynamic Position Sizing     │ 4. 10-Stock Liquid Mega-Cap Universe Selection│
│ 5. Indian Statutory Cost Model & Math       │ 5. Technical Strategy Implementations (SMA/RSI)│
│ 6. Almgren-Chriss Market Impact Slippage    │ 6. Automated Experiment Matrix Logger         │
│ 7. Deflated Sharpe Ratio (DSR) Mathematics  │ 7. SEBI 2024 Empirical Literature Synthesis   │
│ 8. CPCV Algorithm & Embargo Leakage Logic   │ 8. Faculty Presentation Deck & Viva Support   │
│ 9. Automated Pytest Testing Suite (7 Tests) │ 9. Golden Master Fixture Paisa Verification   │
└─────────────────────────────────────────────┴───────────────────────────────────────────────┘
```

---

# 📖 6-LEVEL WWWH SYSTEM BREAKDOWN

```
WWWH Matrix:
  Level 1: WHO   -> Actors, stakeholders, evaluators, developers, regulators.
  Level 2: WHAT  -> The concept, mathematical formulas, data structures, code classes.
  Level 3: WHY   -> The root cause, failure mode prevented, academic/market justification.
  Level 4: WHEN  -> Temporal causality, chronological execution, regime periods, syllabus phases.
  Level 5: WHERE -> File paths, class methods, memory states, test assertions.
  Level 6: HOW   -> Step-by-step algorithms, cash flows, state mutations, data transformations.
```

---

## 🏛️ CHAPTER 1: THE FOUNDATION & PROBLEM STATEMENT (GROUND ZERO)

### 1. WHO
* **Target Users**: Retail systematic traders, quant researchers, student evaluators, and SEBI-registered Research Analysts (RAs) who need honest backtest validation.
* **Regulator**: Securities and Exchange Board of India (SEBI).
* **Developers**: Aayush Bankar (Engine Lead) & Meet Patel (UI/Data Lead).
* **Evaluators**: GTU Internal Mentors (Seminars 1–4) and External GTU ESE Examiner (50-Mark Viva).

### 2. WHAT
* **The Concept**: QuantLab is an event-driven backtesting and overfitting diagnostic platform designed to uncover the **"Profit Mirage"**—the phenomenon where trading algorithms show high paper profitability on past data but immediately lose money when deployed live.
* **Key Phenomena Modeled**:
  1. *Look-Ahead Bias*: Accidental usage of future data in current trading decisions.
  2. *Statutory Cost Drag*: Systematic erosion of returns by mandatory Indian taxes (STT, GST, Stamp Duty, Turnover).
  3. *Overfitting (Data Snooping)*: Inflated Sharpe ratios resulting from testing multiple parameter combinations on noise.

### 3. WHY
* **SEBI 2024 Retail Study Reality**:
  - In September 2024, SEBI released a study analyzing over 1 Crore individual Indian retail traders across FY22–FY24.
  - **93.0%** of active retail traders lost money, suffering cumulative wealth destruction of **₹1,81,000 Crore (~$21.8 Billion USD)**.
  - Transaction costs accounted for **~28%** of total gross losses.
  - **The Root Cause**: Retail traders use naive tools (like simple charting backtesters) that ignore transaction taxes, assume same-bar fills, and encourage over-optimizing indicators.

### 4. WHEN
* **Historical Date Window**:
  - **In-Sample (IS)**: Jan 1, 2019 – Dec 31, 2022 (4 Years | ~990 Days): Covers Pre-COVID, COVID Crash, Bull Run, and Rate Hike Consolidation.
  - **Out-of-Sample (OOS)**: Jan 1, 2023 – Dec 31, 2024 (2 Years | ~490 Days): Strictly quarantined unseen data to evaluate regime decay.
* **Academic Schedule**: GTU DI05000341 Minor Project 27-day execution cycle.

### 5. WHERE
* **Documentation**: `docs/01_unit1_literature/problem_statement.md` and `docs/01_unit1_literature/literature_review.md`.
* **Repository Anchor**: `README.md` and `docs/00_management/LEDGER.md`.

### 6. HOW
* **Failure Workflow**:
  $$\text{Naive Backtest (+45\% CAGR)} \xrightarrow{\text{Deploy}} \text{Cost Drag (-18\%)} + \text{Lookahead Collapse (-15\%)} + \text{Overfitting Decay (-20\%)} = \text{Realized Loss (-8\% CAGR)}$$
* **QuantLab Solution**: Forces deterministic event queues, deducts every statutory paisa, and calculates the probability of overfitting before any strategy is trusted.

---

## 📊 CHAPTER 2: THE DATA LAYER & STOCK UNIVERSE

### 1. WHO
* **Owner**: Meet Patel (Data Pipeline & Universe Selection) with Aayush Bankar (Data Contract Review).
* **Data Provider**: Yahoo Finance API via `yfinance` Python library (Free/Open for academic research).

### 2. WHAT
* **Data Schema (Standardized OHLCV Interface)**:
  - `date`: `pd.Timestamp` (Timezone-naive, daily trading day).
  - `open`, `high`, `low`, `close`: `float64` (Adjusted for splits and dividends).
  - `volume`: `int64` (Total shares traded).
  - `symbol`: `str` (Ticker symbol, e.g., `"RELIANCE.NS"`).
* **Stock Universe**: 10 liquid Indian mega-caps across 7 sectors:
  - *Energy*: `RELIANCE.NS`
  - *IT*: `TCS.NS`, `INFY.NS`
  - *Banking*: `HDFCBANK.NS`, `ICICIBANK.NS`, `SBIN.NS`
  - *FMCG*: `ITC.NS`, `HINDUNILVR.NS`
  - *Infra*: `LT.NS`
  - *Telecom*: `BHARTIARTL.NS`
  - *Benchmark Proxy*: `^NSEI` (Nifty 50 Index)

### 3. WHY
* **Why Mega-Caps?**: Each selected stock has an Average Daily Volume (ADV) $> ₹200\text{ Crore}$. A retail trade of ₹1–5 Lakhs represents $< 0.0025\%$ of daily turnover. This mathematically proves that our linear slippage model is valid and large orders do not distort market prices.
* **Why Drop Missing Dates Instead of Forward-Filling?**: Forward-filling missing values creates flat synthetic bars that artificially suppress historical return volatility, falsely inflating the Sharpe ratio.

### 4. WHEN
* Daily resolution (09:15 to 15:30 IST). Data is fetched at market close or pre-downloaded as CSV batches in `data/raw/`.

### 5. WHERE
* **Code**: `src/data/fetch.py`, `src/data/clean.py`, `src/data/universe.py`.
* **Tests**: Verified through end-to-end integration runs in `tests/test_engine.py`.

### 6. HOW
1. `fetch_stock_data(symbol, start, end)` calls `yf.Ticker(symbol).history()`.
2. `clean_data(df)` strips timezone offsets, forces lowercase column naming, filters incomplete rows, and validates monotonicity of dates.
3. `download_universe()` loops through the 10 tickers and saves them locally as clean CSVs.

---

## ⚙️ CHAPTER 3: THE EVENT-DRIVEN ENGINE & TEMPORAL INVARIANT

### 1. WHO
* **Owner**: Aayush Bankar (Principal Engine Architect).
* **Consumer**: All strategy modules and analytics engines.

### 2. WHAT
* **Core Engine Classes**:
  - `BacktestEngine`: Drives the chronological event loop.
  - `SignalEvent`: Emitted by strategies (`symbol`, `timestamp`, `signal_type: +1 BUY / -1 SELL`).
  - `OrderEvent`: Generated by engine (`symbol`, `timestamp`, `order_type: MKT`, `side: BUY/SELL`, `quantity`).
  - `FillEvent`: Generated by CostModel (`symbol`, `timestamp`, `side`, `quantity`, `execution_price`, `commission_total`).

### 3. WHY
* **Why Discrete-Event instead of Vectorized Pandas (`df['signal'].shift(1) * df['returns']`)?**:
  - Vectorized operations process whole columns at once. A single accidental omission of `.shift(1)` allows tomorrow's price to calculate today's signal without throwing any syntax errors.
  - Vectorized operations cannot handle stateful cash constraints (e.g., rejecting an order when cash is ₹0) or dynamic compounding portfolio allocations.
  - An event loop processes time sequentially bar-by-bar, guaranteeing zero look-ahead bias and stateful cash verification.

### 4. WHEN (The Golden Execution Invariant)
```
Day t:
  15:30 IST -> Market Closes. Data up to Bar t is finalized.
  15:30 IST -> Strategy receives sliced_data[0:t] -> Emits SignalEvent(t)
  15:30 IST -> Engine sizes position -> Queues OrderEvent(t) in pending_orders
Day t+1:
  09:15 IST -> Market Opens. Engine loads Bar t+1 OPEN price.
  09:15 IST -> CostModel calculates slippage and statutory taxes on Open price.
  09:15 IST -> Order executes -> Portfolio balance and position ledger update.
```

### 5. WHERE
* **Code**: `src/engine/backtest_engine.py`, `src/engine/events.py`.
* **Tests**: `tests/test_engine.py::test_engine_zero_look_ahead`.

### 6. HOW
1. `BacktestEngine.run()` extracts all unique trading dates sorted in chronological order.
2. For each date $t$:
   a. **Fill Pending Orders**: Iterates through `pending_orders` from Day $t-1$ and fills them using Day $t$ `open` prices.
   b. **Update Portfolio Mark-to-Market**: Evaluates total portfolio equity using Day $t$ `close` prices.
   c. **Generate New Signals**: Passes data sliced up to Day $t$ to `strategy.generate_signals()`.
   d. **Create New Orders**: Sizes new buy/sell orders and stores them in `pending_orders` for execution on Day $t+1$.

---

## 💼 CHAPTER 4: PORTFOLIO STATE MACHINE & DYNAMIC EQUITY SIZING

### 1. WHO
* **Owner**: Aayush Bankar.

### 2. WHAT
* **Classes**:
  - `Position`: Stores `symbol`, `quantity`, `average_entry_price`. Methods: `update(order, fill_price)`, `unrealized_pnl(current_price)`.
  - `Portfolio`: Tracks `cash: float`, `positions: Dict[str, Position]`, `equity_history: List[dict]`.
* **Dynamic Sizing Formula**:
  $$\text{Target Capital per Trade} = \text{Total Equity}_t \times 0.10$$
  $$\text{Order Quantity} = \left\lfloor \frac{\text{Total Equity}_t \times 0.10}{\text{Estimated Price}} \right\rfloor$$
  $$\text{where } \text{Total Equity}_t = \text{Cash}_t + \sum_{i} (\text{Quantity}_i \times \text{Close Price}_{i, t})$$

### 3. WHY (The Unit 4 Redesign Story)
* **The Cash-vs-Equity Sizing Bug**:
  - *Original Flawed Implementation*: `target_value = self.portfolio.cash * 0.10`.
  - *Failure Mode*: As the engine bought stocks, available cash dropped from ₹1,00,000 to ₹20,000. Subsequent trades were sized at only ₹2,000 instead of ₹10,000, causing trade sizes to collapse artificially as the portfolio grew.
  - *The Fix*: Sizing was redesigned to calculate 10% of **Total Mark-to-Market Equity** (Cash + Value of all Open Positions).

### 4. WHEN
* Evaluated at Day $t$ Close for order sizing; executed at Day $t+1$ Open upon fill.

### 5. WHERE
* **Code**: `src/engine/portfolio.py`, `src/engine/position.py`, `src/engine/backtest_engine.py` (lines 109–115).
* **Tests**: `tests/test_engine.py::test_engine_position_sizing_uses_total_equity`, `tests/test_portfolio.py`.

### 6. HOW
* When a BUY order fills:
  $$\text{Cash}_{\text{new}} = \text{Cash}_{\text{old}} - (\text{Quantity} \times \text{Fill Price}) - \text{Total Taxes}$$
  $$\text{Average Entry Price}_{\text{new}} = \frac{(Q_{\text{old}} \times P_{\text{avg}}) + (Q_{\text{new}} \times P_{\text{fill}})}{Q_{\text{old}} + Q_{\text{new}}}$$
* When a SELL order fills:
  $$\text{Cash}_{\text{new}} = \text{Cash}_{\text{old}} + (\text{Quantity} \times \text{Fill Price}) - \text{Total Taxes}$$
  $$\text{Realized PnL} = Q_{\text{sold}} \times (P_{\text{fill}} - P_{\text{avg}}) - \text{Total Taxes}$$

---

## ⚖️ CHAPTER 5: INDIAN STATUTORY COST MODEL & SLIPPAGE

### 1. WHO
* **Owner**: Aayush Bankar (Formulation & Code) & Meet Patel (Golden Master Fixture Verification).

### 2. WHAT
* **The Exact Indian Delivery Rate Card (NSE Circular Rules)**:
  1. **Brokerage**: $\min(₹20.00, \text{Trade Value} \times 0.0003)$ (0.03% capped at ₹20).
  2. **STT (Securities Transaction Tax)**: $0.10\%$ on Buy Value AND $0.10\%$ on Sell Value (Section 98 of Finance Act).
  3. **Exchange Turnover Charge (NSE)**: $0.00297\%$ of trade value.
  4. **SEBI Turnover Fee**: $0.0001\%$ of trade value (₹10 per Crore).
  5. **GST (Goods and Services Tax)**: $18.0\%$ charged strictly on $(\text{Brokerage} + \text{Exchange Fee} + \text{SEBI Fee})$. *(Note: GST is NOT levied on STT or Stamp Duty).*
  6. **Stamp Duty (State Government)**: $0.015\%$ on Buy Value only (Indian Stamp Act 2020).
  7. **Slippage Model**: Almgren-Chriss Square-Root Market Impact:
     $$\text{Execution Price}_{\text{BUY}} = P_{\text{open}} \times (1 + \text{slippage\_pct})$$
     $$\text{Execution Price}_{\text{SELL}} = P_{\text{open}} \times (1 - \text{slippage\_pct})$$

### 3. WHY
* **Why Paisa-Level Precision?**: On high-turnover retail strategies, statutory taxes accumulate exponentially. On a ₹1,00,000 round-trip trade earning 10% gross profit, Indian taxes destroy **₹384.81 (3.85% of profit)**. Over 50 trades a year, friction completely wipes out trading capital.

### 4. WHEN
* Applied instantly on every order fill event inside `CostModel.calculate_cost()`.

### 5. WHERE
* **Code**: `src/engine/cost_model.py`.
* **Tests**: `tests/test_cost_model.py::test_indian_cost_model_buy` (asserts exact paisa calculations against hand-derived golden masters).

### 6. HOW
1. `CostModel.calculate_cost(order, execution_price)` computes `trade_value = qty * execution_price`.
2. Computes each tax component independently according to order side (BUY vs SELL).
3. Sums total fees and adjusts the net cash balance accordingly.

---

## 📈 CHAPTER 6: STRATEGY IMPLEMENTATIONS & SIGNAL LOGIC

### 1. WHO
* **Owner**: Meet Patel (Strategy Code & Tuning) with Aayush Bankar (Signal Interface Contracts).

### 2. WHAT
* **Three Canonical Strategies**:
  1. **SMA Crossover (`SMACrossoverStrategy`)**:
     - Fast Window: 20 days, Slow Window: 50 days.
     - Buy when SMA(20) crosses above SMA(50); Sell when SMA(20) crosses below SMA(50).
  2. **RSI Mean Reversion (`RSIMeanReversionStrategy`)**:
     - 14-period Wilder's RSI.
     - Buy when $\text{RSI} < 30$ (Oversold); Sell when $\text{RSI} > 70$ (Overbought).
  3. **Momentum (`MomentumStrategy`)**:
     - 20-day Rate of Change: $\text{ROC} = (P_t - P_{t-20}) / P_{t-20}$.
     - Buy when $\text{ROC} > 5\%$; Sell when $\text{ROC} < 0\%$.

### 3. WHY
* **Duplicate Buy Signal Prevention**:
  - *The Bug*: In naive momentum strategies, when price stays above threshold for 10 consecutive days, the strategy emits 10 BUY signals in a row, exhausting cash on day 2.
  - *The Fix*: Added an open-position guard: `if symbol not in positions or positions[symbol].quantity == 0: emit BUY`.

### 4. WHEN
* Signals generated at 15:30 IST Close of Day $t$.

### 5. WHERE
* **Code**: `src/strategies/sma_crossover.py`, `rsi_mean_reversion.py`, `momentum.py`.
* **Tests**: `tests/test_momentum.py::test_momentum_no_duplicate_signals`.

### 6. HOW
* Each strategy inherits from `Strategy` abstract base class and implements `generate_signals(current_date, data, positions) -> List[SignalEvent]`.

---

## 🔬 CHAPTER 7: OVERFITTING DIAGNOSTICS (DSR, CPCV & EMBARGO)

### 1. WHO
* **Owner**: Aayush Bankar (Mathematical Formulation & Implementation).
* **Reference**: Prof. Marcos López de Prado (*Advances in Financial Machine Learning*, 2018 & *Journal of Portfolio Management*, 2014).

### 2. WHAT
* **A. Deflated Sharpe Ratio (DSR)**:
  - Adjusts observed Sharpe Ratio for non-normality (skewness $\gamma_3$, kurtosis $\gamma_4$) and selection bias over $N$ trials:
  $$E[\max \text{SR}_N] = \sqrt{2 \ln N} + \frac{\gamma_{\text{Euler}}}{\sqrt{2 \ln N}}$$
  $$\text{DSR} = \Phi\left( \frac{\text{SR}_{\text{observed}} - E[\max \text{SR}_N]}{\sqrt{\text{Var}(\text{SR})}} \right)$$
* **B. Combinatorial Purged Cross-Validation (CPCV) & PBO**:
  - Timeline split into $N$ blocks ($N=10$, $k=2$ test blocks $\implies 45$ paths).
  - Calculates the **Probability of Backtest Overfitting (PBO)**: the percentage of paths where the best In-Sample strategy ranks below the median Out-of-Sample.

### 3. WHY (The Embargo Leakage Breakthrough)
* **The Time-Series Leakage Problem**: Financial returns are autocorrelated (serially dependent). Standard $K$-Fold cross-validation leaks information across fold boundaries.
* **The Embargo Solution**: An embargo window ($5\%$ of timeline) is dropped before and after each test block.
* **Empirical AR(1) Test Evidence**:
  - *Without Embargo (Leakage)*: $\text{PBO} = \mathbf{28.89\%}$ (False confidence).
  - *With 5% Embargo (Leakage Prevented)*: $\text{PBO} = \mathbf{37.78\%}$ (True risk exposed).

### 4. WHEN
* Executed post-simulation in Layer 2 Analytics before any strategy parameters are deployed.

### 5. WHERE
* **Code**: `src/analytics/cpcv.py`, `src/analytics/deflated_sharpe.py`, `src/analytics/metrics.py`.
* **Tests**: `tests/test_cpcv.py` (`test_calculate_pbo_random_returns`, `test_calculate_pbo_real_signal`, `test_cpcv_embargo_ar1`).
* **Experiment Script**: `scripts/run_pbo_experiment.py`.

### 6. HOW
1. `CPCV.generate_paths()` computes train and test splits, explicitly removing `embargo_size` samples from train indices around test boundaries.
2. Computes IS and OOS Sharpe ratios for each strategy variant across all paths.
3. Quantifies overfit paths where $\text{Sharpe}_{\text{OOS}}(S^*) < \text{Median}(\text{Sharpe}_{\text{OOS}})$.

---

## 🖥️ CHAPTER 8: STREAMLIT DASHBOARD & TESTING SUITE

### 1. WHO
* **Owner**: Meet Patel (Streamlit UI & Plotly Components) & Aayush Bankar (Backend Integration).

### 2. WHAT
* **Dashboard Capabilities (`src/dashboard/app.py`)**:
  - Interactive strategy selection dropdown (SMA, RSI, Momentum).
  - Parameter sliders for real-time recalibration.
  - "Apply Transaction Costs" toggle to instantly reveal the "Profit Mirage".
  - Plotly interactive equity curves and underwater drawdown visualizations.
  - Core metrics display: CAGR, Sharpe Ratio, Maximum Drawdown, Calmar Ratio.
* **Open Source License**: Apache License 2.0.

### 3. WHY
* **Why Streamlit?**: Allows university evaluators and non-technical stakeholders to interact with backtest simulations dynamically without modifying Python code.
* **Why Apache 2.0?**: Protects against patent trolling via explicit patent grants, safeguarding any future commercial spinoffs.

### 4. WHEN
* Launched locally during faculty presentations and viva demonstrations.

### 5. WHERE
* **Code**: `src/dashboard/app.py`, `src/dashboard/components.py`, `LICENSE`, `README.md`.

### 6. HOW
1. User starts app via `streamlit run src/dashboard/app.py`.
2. App loads cleaned OHLCV data from `data/raw/`.
3. User selects strategy and clicks "Run Backtest".
4. Engine processes simulation and passes equity history to Plotly chart components for immediate rendering.

---

# 🎯 SUMMARY VIVA DEFENSE CHEAT SHEET

| Question | Winning Response |
|---|---|
| **"Why not use Pandas vectorized backtesting?"** | *"Vectorized code processes entire arrays at once, making it dangerously easy to leak future data across bars. An event-driven loop enforces chronological time-stepping, stateful cash management, and $t+1$ Open execution."* |
| **"Why is the Deflated Sharpe Ratio superior to standard Sharpe?"** | *"Standard Sharpe assumes a single trial. When testing 50 parameter variations, the best observed Sharpe is an extreme value of noise. DSR mathematically penalizes multi-testing and adjusts for non-normal return distributions."* |
| **"What did your AR(1) test prove about CPCV embargoes?"** | *"Autocorrelated returns leak across cross-validation splits. Without an embargo, PBO was artificially low at 28.9%. Dropping a 5% embargo window eliminated boundary leakage, revealing the true overfitting probability of 37.8%."* |
| **"How does the engine ensure cash integrity?"** | *"The portfolio verifies `cash >= total_cost` before every fill. Furthermore, position sizing calculates 10% of total portfolio equity (cash + open positions MTM), preventing position sizes from collapsing as capital is deployed."* |
