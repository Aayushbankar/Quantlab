# QuantLab — System Architecture & Design Document (SDD)

**Project Title**: QuantLab: A Realistic Backtesting Engine & Overfitting Diagnostic Platform for Indian Equities  
**Course Code**: GTU DI05000341 (Minor Project — Semester 5)  
**Academic Unit**: Unit 2 — System Architecture, Component Design & Execution Invariants  
**Authors**: Aayush Avinash Bankar (Leader) & Meet Jayeshbhai Patel  
**Date**: August 19, 2026  

---

## 1. Architectural Philosophy & Layered Decomposition

QuantLab is built on a **strictly decoupled 4-layer architecture**. Each layer has a single responsibility and depends only on the layer immediately below it, with zero circular imports.

```mermaid
graph TD
    subgraph L1["Layer 1: User Interface & Presentation (`src/dashboard/`)"]
        UI1["Streamlit Master Dashboard (`app.py`)"]
        UI2["Interactive Controls & Heatmap Visualizers (`components.py`)"]
    end

    subgraph L2["Layer 2: Statistical Analytics & Overfitting Lab (`src/analytics/`)"]
        A1["Performance Metrics Engine (`metrics.py`)<br/>CAGR, Sharpe, Sortino, Calmar, MDD"]
        A2["Marcos López de Prado DSR Engine (`deflated_sharpe.py`)"]
        A3["2D Parameter Stability Grid Search (`validation.py`)"]
    end

    subgraph L3["Layer 3: Discrete-Event Simulation Engine (`src/engine/`)"]
        E1["Event Dispatcher & Loop (`backtest_engine.py`)"]
        E2["Portfolio Ledger & Cash Invariants (`portfolio.py`)"]
        E3["Indian Statutory Cost Model (`cost_model.py`)"]
        E4["Order & Position State (`order.py`, `position.py`)"]
        E5["Event Definitions (`events.py`)"]
    end

    subgraph L4["Layer 4: Data Ingestion & Strategy Layer (`src/data/`, `src/strategies/`)"]
        D1["Yahoo Finance Fetcher (`fetch.py`)"]
        D2["Data Cleaner & Validator (`clean.py`)"]
        D3["Universe & Sector Definitions (`universe.py`)"]
        S1["SMA Crossover (`sma_crossover.py`)"]
        S2["RSI Mean Reversion (`rsi_mean_reversion.py`)"]
        S3["Relative Momentum (`momentum.py`)"]
    end

    L1 --> L2
    L2 --> L3
    L3 --> L4
```

---

## 2. The Core Execution Invariant: Zero Look-Ahead Event Loop

The defining architectural feature of QuantLab is **temporal causality protection**. In naive backtests, signals calculated at Day $t$'s `Close` are filled at that same Day $t$'s `Close`—a physical impossibility.

QuantLab enforces a strict two-phase daily bar execution loop:

```mermaid
sequenceDiagram
    autonumber
    participant M as Market Data Stream
    participant S as Strategy Engine
    participant Q as Order Queue
    participant E as BacktestEngine
    participant C as Indian CostModel
    participant P as Portfolio Ledger

    Note over M,P: DAY t (15:30 IST — Market Close)
    M->>S: Deliver Day t OHLCV Bar (Close Price Established)
    S->>S: Compute Technical Indicators on Day t Close
    S->>Q: Emit SignalEvent (+1 BUY / -1 SELL)
    Q->>E: Convert Signal to Pending Order (Target: Day t+1 Open)

    Note over M,P: DAY t+1 (09:15 IST — Market Open)
    M->>E: Deliver Day t+1 Bar (Open Price Established)
    E->>C: Calculate Slippage-Adjusted Fill Price (Open * (1 ± Slippage))
    C->>C: Calculate STT, GST, Stamp Duty, Brokerage Cap
    C->>E: Return Exact Cash Frictions
    E->>P: Deduct Cash & Reconcile Position Ledger (Cash >= 0 Invariant)
    P->>E: Confirm FillEvent & Update Portfolio Equity
```

---

## 3. Detailed Component & Class Design

### 3.1 `src/engine/events.py`
Defines the immutable data structures passed through the simulation queue:
- `MarketEvent(timestamp, symbol, open, high, low, close, volume)`
- `SignalEvent(timestamp, symbol, signal_type, strength)`
- `OrderEvent(timestamp, symbol, order_type, side, quantity)`
- `FillEvent(timestamp, symbol, side, quantity, raw_price, fill_price, commission, stt, stamp_duty, gst, turnover_fee, total_cost)`

### 3.2 `src/engine/cost_model.py` (Indian Statutory Tax Model)
- **Class**: `IndianCostModel`
- **Responsibilities**:
  1. Computes slippage-adjusted execution prices ($P_{\text{open}} \times (1 \pm \delta_{\text{slip}})$).
  2. Evaluates exact statutory levies based on official Indian regulations:
     - Brokerage: $\min(20.00, \text{TradeValue} \times 0.0003)$ (or ₹0.00 in discount preset).
     - STT: $\text{TradeValue} \times 0.0010$ (on both Buy and Sell).
     - Stamp Duty: $\text{TradeValue} \times 0.00015$ (on Buy only).
     - NSE Turnover Fee: $\text{TradeValue} \times 0.0000297$.
     - SEBI Turnover Fee: $\text{TradeValue} \times 0.000001$.
     - GST: $(\text{Brokerage} + \text{Turnover} + \text{SEBI}) \times 0.18$.

### 3.3 `src/engine/portfolio.py`
- **Class**: `Portfolio`
- **Invariants Enforced**:
  1. **Non-Negative Cash**: $\text{Cash}_t \ge 0.0$ (Orders requiring more cash than available are rejected or rightsized).
  2. **Double-Entry Ledger Integrity**: $\text{Total Equity}_t = \text{Cash}_t + \sum_i (\text{Shares}_i \times P_{i, \text{close}, t})$.
  3. **No Unmodeled Leverage**: Strict 1x equity delivery allocation.

### 3.4 `src/analytics/deflated_sharpe.py`
- **Functions**:
  - `calculate_higher_moments(returns)`: Computes sample skewness ($\widehat{\gamma}_3$) and kurtosis ($\widehat{\gamma}_4$).
  - `expected_max_sharpe(N_trials, variance_sr, benchmark_sr=0.0)`: Evaluates Euler-Mascheroni extreme value asymptotic limit.
  - `deflated_sharpe_ratio(observed_sr, N_trials, returns)`: Evaluates CDF p-value under the False Strategy Theorem.

---

## 4. V2 Modular Rust Extension Architecture

To prepare for future high-performance requirements (e.g., million-bar intraday ticks or large Monte Carlo simulations), QuantLab decouples the engine interface:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    V2 RUST / PyO3 EXTENSION BOUNDARY                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ Python Frontend Layer: Streamlit UI + Data Ingestion + Matplotlib Plotting │
├─────────────────────────────────────────────────────────────────────────────┤
│ [PyO3 C-FFI Bridge]: Exposes zero-copy NumPy buffers to compiled engine    │
├─────────────────────────────────────────────────────────────────────────────┤
│ Rust Engine Core (`crates/quantlab-core/`):                                 │
│   • Multi-threaded Rayon event loop                                         │
│   • 0.005s execution time across 100,000 bars                              │
│   • Memory-safe zero-allocation cash ledger                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. File System & Implementation Map

```
Quantlab/
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   ├── fetch.py              # FR-1: yfinance downloader
│   │   ├── clean.py              # FR-2: Missing bars, splits, NaN cleaner
│   │   └── universe.py           # FR-3: 10 NSE stocks + Nifty 50 dicts
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── events.py             # Event dataclasses
│   │   ├── order.py              # Order dataclass & states
│   │   ├── position.py           # Position state & PnL tracking
│   │   ├── cost_model.py         # FR-9: Exact Indian statutory taxes
│   │   ├── portfolio.py          # Portfolio state & cash invariants
│   │   └── backtest_engine.py    # FR-8: Zero look-ahead event loop
│   ├── strategies/
│   │   ├── __init__.py
│   │   ├── base.py               # Base Strategy abstract class
│   │   ├── sma_crossover.py      # FR-5: Fast/Slow SMA crossover
│   │   ├── rsi_mean_reversion.py # FR-6: 14-day Wilder RSI
│   │   └── momentum.py           # FR-7: Lookback rate of change
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── metrics.py            # FR-10: CAGR, Sharpe, Sortino, MDD
│   │   ├── deflated_sharpe.py    # FR-11: Marcos López de Prado DSR
│   │   └── validation.py         # FR-12: 2D Parameter Grid Search
│   └── dashboard/
│       ├── __init__.py
│       ├── app.py                # Streamlit master application
│       └── components.py         # Waterfall & 2D heatmap widgets
└── tests/
    ├── test_data.py
    ├── test_strategies.py
    ├── test_cost_model.py
    ├── test_engine.py
    └── test_metrics.py
```
