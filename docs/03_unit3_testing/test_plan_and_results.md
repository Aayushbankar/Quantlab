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
collected 35 items

tests/test_cost_model.py::test_indian_cost_model_buy PASSED              [  2%]
tests/test_cpcv.py::test_calculate_pbo_random_returns PASSED             [  5%]
tests/test_cpcv.py::test_calculate_pbo_real_signal PASSED                [  8%]
tests/test_cpcv.py::test_cpcv_embargo_ar1 PASSED                         [ 11%]
tests/test_data.py::test_clean_drops_missing_ohlc_rows_not_forward_filled PASSED [ 14%]
tests/test_data.py::test_clean_does_not_forward_fill PASSED              [ 17%]
tests/test_data.py::test_clean_sorts_chronologically PASSED              [ 20%]
tests/test_data.py::test_clean_rejects_duplicate_dates PASSED            [ 22%]
tests/test_data.py::test_clean_accepts_empty_frame_without_crashing PASSED [ 25%]
tests/test_data.py::test_clean_handles_datetime_string_column PASSED     [ 28%]
tests/test_deflated_sharpe.py::test_expected_max_sharpe_increases_with_trials PASSED [ 31%]
tests/test_deflated_sharpe.py::test_expected_max_sharpe_single_trial_returns_benchmark PASSED [ 34%]
tests/test_deflated_sharpe.py::test_dsr_returns_valid_pvalue_for_noise PASSED [ 37%]
tests/test_deflated_sharpe.py::test_dsr_punishes_single_trial_less_than_many PASSED [ 40%]
tests/test_deflated_sharpe.py::test_dsr_rejects_insufficient_data PASSED [ 42%]
tests/test_deflated_sharpe.py::test_dsr_rejects_single_trial PASSED      [ 45%]
tests/test_deflated_sharpe.py::test_dsr_high_true_sharpe_is_credible PASSED [ 48%]
tests/test_determinism.py::test_backtest_is_byte_identical_across_runs PASSED [ 51%]
tests/test_determinism.py::test_backtest_equity_hash_stable PASSED       [ 54%]
tests/test_determinism.py::test_costs_change_the_outcome PASSED          [ 57%]
tests/test_engine.py::test_engine_zero_look_ahead PASSED                 [ 60%]
tests/test_engine.py::test_engine_position_sizing_uses_total_equity PASSED [ 62%]
tests/test_metrics.py::test_metrics_engine PASSED                        [ 65%]
tests/test_momentum.py::test_momentum_no_duplicate_signals PASSED        [ 68%]
tests/test_portfolio.py::test_portfolio_cash_flow PASSED                 [ 71%]
tests/test_rsi.py::test_rsi_100_when_all_gains PASSED                    [ 74%]
tests/test_rsi.py::test_rsi_0_when_all_losses PASSED                     [ 77%]
tests/test_rsi.py::test_rsi_neutral_on_flat_series PASSED                [ 80%]
tests/test_rsi.py::test_rsi_bounded_zero_to_hundred_on_random_walk PASSED [ 82%]
tests/test_rsi.py::test_rsi_all_gains_does_not_emit_oversold_buy PASSED  [ 85%]
tests/test_sma.py::test_sma_golden_cross_emits_buy PASSED                [ 88%]
tests/test_sma.py::test_sma_death_cross_emits_sell_only_with_position PASSED [ 91%]
tests/test_sma.py::test_sma_insufficient_history_produces_no_signal PASSED [ 94%]
tests/test_sma.py::test_sma_respects_fast_must_be_less_than_slow PASSED  [ 97%]
tests/test_sma.py::test_sma_no_lookahead_uses_only_past_bars PASSED      [100%]
============================== 35 passed in 2.91s ===============================
```
