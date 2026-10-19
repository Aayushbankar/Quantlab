# QuantLab - Final Report Draft

## Executive Summary
QuantLab successfully built a 4-layer Python architecture to simulate realistic trading environments for Indian Equities. We demonstrated that without modeling transaction costs and slippage, strategies look artificially profitable (Profit Mirage). 

## Methodology
- **Zero Look-Ahead**: Strict Event Loop.
- **Costs**: Modeled STT, GST, Brokerage, and Slippage.
- **Metrics**: DSR used to penalize multiple testing.

## Results
- SMA crossover without costs showed high CAGR.
- SMA crossover WITH costs showed significant degradation.
- Heatmaps reveal parameters are unstable out-of-sample.

## Conclusion
Evaluating strategies naively leads to overfitting. A robust event-driven simulator is required to find true edges.

## Audit and Architecture Fixes
Following an architectural audit, several critical invariants were reinforced:
1. MTM (Mark-to-Market) was centralized to run exactly once per day.
2. Hard cash-overdraft bounds were added to prevent phantom leverage.
3. The dataset passed to strategies is strictly sliced up to $T$ to formally eliminate Look-Ahead Bias.
4. Sell-sizing was corrected to target existing position quantities, decoupling it from the cash fraction used for entries.
