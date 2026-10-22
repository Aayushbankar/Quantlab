# Unit 3: Verification & Test Execution Results

**Subject:** GTU DI05000341 Minor Project (Unit 3 — Procure / Implement / Test)  
**System:** Pramaan (QuantLab) Event-Driven Backtesting Engine  
**Module Tested:** `src/engine/`, `src/analytics/`, `src/strategies/`, `src/data/`  
**Test Suite:** `tests/` (12 test modules, 35 automated tests)  
**Execution Status:** **35 / 35 PASS (100% Pass Rate)**

---

## 1. Test Suite Architecture

The Pramaan verification suite is designed around silent statistical and execution failure modes in quantitative finance. Tests are partitioned into five functional classes:

```
tests/
├── test_cost_model.py         # Paisa-exact statutory Indian equity delivery cost verification
├── test_cpcv.py               # Combinatorial Purged Cross-Validation & embargo leakage verification
├── test_data.py               # Missing bar, duplicate timestamp, and non-forward-fill data hygiene
├── test_deflated_sharpe.py    # DSR non-normality adjustment and extreme-value expectation
├── test_determinism.py        # SHA-256 byte-identical reproducibility across independent runs
├── test_engine.py             # Zero look-ahead T+1 Open execution & total-equity position sizing
├── test_metrics.py            # Financial performance ratios (Sharpe, CAGR, Sortino, MaxDD, Calmar)
├── test_momentum.py           # Momentum ROC signal emission and duplicate BUY guards
├── test_portfolio.py          # Cash flow, mark-to-market valuation, and position accounting
├── test_rsi.py                # Wilder RSI boundary handling (including all-gains saturation)
└── test_sma.py                # Dual SMA golden cross, death cross, and history bounds
```

---

## 2. Golden-Master Numerical Contract (Statutory Indian Delivery)

To satisfy Unit 3 paisa-level precision, a ₹1,00,000 round-trip transaction is asserted down to the exact paisa per SEBI circulars:

| Component | Buy ₹1,00,000 | Sell ₹1,10,000 | Formula / Circular Reference |
|---|---|---|---|
| **Brokerage** | ₹20.00 | ₹20.00 | $\min(₹20, 0.03\% \times \text{turnover})$ |
| **STT** | ₹100.00 | ₹110.00 | $0.10\%$ of turnover (delivery, both legs) |
| **Stamp Duty** | ₹15.00 | ₹0.00 | $0.015\%$ buy-side only (Indian Stamp Act) |
| **NSE Turnover** | ₹2.97 | ₹3.27 | $0.00297\%$ exchange levy (NSE Oct 2024 circular) |
| **SEBI Turnover** | ₹0.10 | ₹0.11 | $0.00010\%$ SEBI regulatory fee |
| **GST** | ₹4.15 | ₹4.21 | $18\%$ on $(\text{Brokerage} + \text{Turnover Fees})$ |
| **Total Statutory Cost** | **₹142.22** | **₹137.59** | Verified in `test_cost_model.py` |

---

## 3. Execution Verification Record

```
============================= test session starts ==============================
platform linux -- Python 3.11.16, pytest-8.3.4
rootdir: /mnt/work/projects/Quantlab
collected 72 items

tests/test_api.py (12 passed)
tests/test_bollinger.py (1 passed)
tests/test_cost_model.py (6 passed)
tests/test_cpcv.py (4 passed)
tests/test_data.py (6 passed)
tests/test_data_provider.py (4 passed)
tests/test_deflated_sharpe.py (10 passed)
tests/test_determinism.py (3 passed)
tests/test_engine.py (2 passed)
tests/test_honesty.py (9 passed)
tests/test_metrics.py (1 passed)
tests/test_momentum.py (1 passed)
tests/test_perf.py (2 passed)
tests/test_portfolio.py (1 passed)
tests/test_rsi.py (5 passed)
tests/test_sma.py (5 passed)

============================== 72 passed in 7.22s ===============================
```
