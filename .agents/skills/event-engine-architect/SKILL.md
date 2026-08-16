---
name: event-engine-architect
description: >-
  Principal Systems Architect for Event-Driven Simulation Engines.
  Enforces zero look-ahead execution timing invariants (signal at Bar t Close -> fill at Bar t+1 Open),
  portfolio state invariants (cash >= 0, position ledger reconciliation),
  and clean decoupled 4-layer Python architecture ready for modular V2 Rust extensions.
---

# Event-Driven Simulation Engine Architect

This skill provides architectural patterns, state machine designs, and execution timing rules for building deterministic, zero look-ahead backtesting engines.

## 1. Zero Look-Ahead Execution Timing Contract

The most critical architectural invariant in quantitative simulation:

```
Timeline:
Day t:
  09:15 - 15:30: Trading session for Bar t
  15:30: Market Closes. Bar t data (O, H, L, C, V) becomes finalized.
  15:30+: Strategy evaluates Bar t Close -> Emits SignalEvent(t) -> Queues OrderEvent(t+1)
Day t+1:
  09:15: Market Opens for Bar t+1.
  09:15: BacktestEngine executes queued OrderEvent at Bar t+1 OPEN price adjusted by CostModel.
  09:15+: Portfolio state (Cash, Positions, Realized PnL) is updated.
```

> [!CAUTION]
> **Rule**: An order generated from Day $t$ Close MUST NEVER execute at Day $t$ Close. Executing at Day $t$ Close is a fatal look-ahead bug.

---

## 2. Decoupled 4-Layer Architecture

```
Layer 1: Dashboard UI (Streamlit)
         │  (calls analytics & visualizes)
Layer 2: Analytics & Validation (Metrics, DSR, Stability Heatmaps)
         │  (consumes equity curves & trade logs)
Layer 3: Event Engine Core (BacktestEngine, Portfolio, Order, CostModel)
         │  (processes chronological event queue)
Layer 4: Data & Strategy Layer (Clean OHLCV, Signal Generators)
```

### Decoupling Invariants
1. **Strategies** only take clean DataFrames and emit `pd.Series` or `SignalEvent`. They know nothing about cash, positions, or brokers.
2. **CostModel** takes an `OrderEvent` and execution price and emits a `FillEvent`. It knows nothing about strategies.
3. **Portfolio** maintains cash balances, position ledger, and equity time series. Cash invariant: $\text{Cash}_t \ge 0$.
4. **BacktestEngine** drives the discrete-event chronological loop.

---

## 3. V2 Modular Rust Extension Ready

By keeping the interface between Layer 3 (Engine) and Layer 4 (Data) strictly based on typed data structures / numpy arrays:
- In V2, `src/engine/backtest_engine.py` can be replaced with a compiled Rust extension (`quantlab_engine_rs` via PyO3) without touching any strategy code or the Streamlit dashboard!
