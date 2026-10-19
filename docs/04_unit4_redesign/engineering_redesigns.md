# Unit 4: Engineering Modifications & Iterative Redesigns

**Subject:** GTU DI05000341 Minor Project (Unit 4 — Modify / Redesign from Test Results)  
**System:** Pramaan (QuantLab) Event-Driven Backtesting Engine  
**Rationale:** Engineering iteration must be demonstrated through documented failure analysis, parameter modification, and architectural redesign.

---

## 1. Summary of 4 Iterative Redesigns

| Redesign # | Subsystem | Defect / Failure in Initial Design | Engineering Modification Implemented | Empirical Impact / Verification |
|---|---|---|---|---|
| **1** | Position Sizing (`backtest_engine.py`) | Orders sized as 10% of *available cash*, shrinking later orders as capital deployed and understating market impact | Fixed to size against **total portfolio equity** (cash + mark-to-market positions) | Compounding cost drag and impact accurately reflected; verified in `test_engine_position_sizing_uses_total_equity` |
| **2** | Data Slicing (`backtest_engine.py`) | Boolean dataframe masking `df[df['date'] <= t]` on every bar ($O(N)$ repeated allocations) | Pre-sorted chronological indexing with integer `.iloc` pointers | Eliminates repeated memory allocations on the hot simulation loop |
| **3** | Slippage Model (`cost_model.py`) | Flat static 0.05% slippage haircut insensitive to trade volume | **Almgren–Chriss square-root impact model** ($\gamma \cdot \sigma \cdot \sqrt{Q/\text{ADV}}$) calibrated to 20-day trailing volatility | Penalizes aggressive positioning in illiquid or high-volatility regimes |
| **4** | Cross-Validation (`cpcv.py`) | Contaminated train/test splits leaking serial correlation at block boundaries | Added **1% timeline embargo** before and after test splits | AR(1) autocorrelation leakage detected; PBO without embargo (28.89%) vs with embargo (37.78%) verified in `test_cpcv_embargo_ar1` |

---

## 2. Statistical Failure Analysis: The Profit Mirage & PBO

When the 2019–2024 NIFTY-10 dataset was evaluated across classic trading strategies:
- **Momentum Strategy:** Gross Sharpe of 0.359 degraded to **0.186 Net** (48.16% Sharpe reduction). ₹12,994.83 of capital was consumed by statutory fees on a ₹1,00,000 base.
- **RSI Mean Reversion:** Severely underperformed benchmark (CAGR 9.80% vs 19.07% Buy & Hold), suffering a 32.77% maximum drawdown.
- **Combinatorial Purged Cross-Validation (CPCV):** Across 28 paths ($N=8, k=2$), Probability of Backtest Overfitting (PBO) was measured at **64.29%**, proving that in-sample backtest rank does not generalize out-of-sample.
