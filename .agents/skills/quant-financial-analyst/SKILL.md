---
name: quant-financial-analyst
description: >-
  Quantitative Finance & Market Microstructure Specialist for Indian Equities.
  Provides exact mathematical formulations for trading metrics (Sharpe, Sortino, Calmar, Max Drawdown),
  statutory Indian equity delivery costs (STT, GST, Stamp Duty, Exchange Turnover, Slippage),
  and technical strategy specifications (SMA Crossover, RSI Mean Reversion, Momentum).
---

# Quantitative Finance & Market Microstructure Specialist

This skill provides quantitative finance domain knowledge, mathematical equations, and market microstructure modeling for Indian equities (NSE).

## 1. Indian Equity Delivery Statutory Friction Model

For Indian equity delivery transactions on NSE, calculate exact round-trip frictions:

### Mathematical Formulation
$$\text{Friction}_{\text{total}} = \text{Brokerage} + \text{STT} + \text{Turnover} + \text{GST} + \text{Stamp Duty} + \text{Slippage}$$

| Component | Buy Order Rate | Sell Order Rate | Base Formula |
|---|---|---|---|
| **Brokerage** | 0.03% (cap ₹20) | 0.03% (cap ₹20) | $\min(20, \text{Value} \times 0.0003)$ |
| **STT (Securities Transaction Tax)** | 0.10% | 0.10% | $\text{Value} \times 0.0010$ |
| **NSE Exchange Turnover Charge** | 0.00345% | 0.00345% | $\text{Value} \times 0.0000345$ |
| **GST** | 18% on (Brokerage + Turnover) | 18% on (Brokerage + Turnover) | $(\text{Brokerage} + \text{Turnover}) \times 0.18$ |
| **Stamp Duty** | 0.015% | 0.00% (Buy only) | $\text{Value} \times 0.00015$ (Buy only) |
| **Slippage** | 0.05% default | 0.05% default | $\text{Price} \times (1 \pm \text{Slippage})$ |

---

## 2. Performance & Risk Metrics Formulations

1. **CAGR (Compound Annual Growth Rate)**:
   $$\text{CAGR} = \left(\frac{V_{\text{final}}}{V_{\text{initial}}}\right)^{\frac{1}{\text{Years}}} - 1$$

2. **Sharpe Ratio (Annualized, Daily Bars)**:
   $$\text{SR} = \sqrt{252} \times \frac{\bar{R}_p - R_f}{\sigma_p}$$
   *(Default $R_f = 6.0\%$ for Indian 10-year G-Sec / RBI repo rate)*

3. **Sortino Ratio (Downside Risk Only)**:
   $$\text{Sortino} = \sqrt{252} \times \frac{\bar{R}_p - R_f}{\sigma_{\text{downside}}}$$
   $$\text{where } \sigma_{\text{downside}} = \sqrt{\frac{1}{N} \sum_{t=1}^N \min(0, R_{p,t} - R_f)^2}$$

4. **Maximum Drawdown (Peak-to-Trough)**:
   $$\text{MDD} = \max_{t} \left( \frac{\text{Peak}_t - V_t}{\text{Peak}_t} \right) \quad \text{where } \text{Peak}_t = \max_{s \le t} V_s$$

5. **Calmar Ratio**:
   $$\text{Calmar} = \frac{\text{CAGR}}{\text{MDD}}$$

---

## 3. Canonical Strategy Specifications

- **SMA Crossover**:
  $$\text{Signal}_t = \begin{cases} +1 (\text{BUY}) & \text{if } \text{SMA}_{\text{short}, t} > \text{SMA}_{\text{long}, t} \text{ and } \text{SMA}_{\text{short}, t-1} \le \text{SMA}_{\text{long}, t-1} \\ -1 (\text{SELL}) & \text{if } \text{SMA}_{\text{short}, t} < \text{SMA}_{\text{long}, t} \text{ and } \text{SMA}_{\text{short}, t-1} \ge \text{SMA}_{\text{long}, t-1} \\ 0 (\text{HOLD}) & \text{otherwise} \end{cases}$$
- **RSI Mean Reversion**:
  $$\text{RSI}_t = 100 - \frac{100}{1 + \frac{\text{EMA}(\text{Gains}, 14)}{\text{EMA}(\text{Losses}, 14)}}$$
  $$\text{BUY when } \text{RSI}_t < 30, \quad \text{SELL when } \text{RSI}_t > 70$$
- **Momentum**:
  $$\text{Return}_{\text{lookback}, t} = \frac{P_t - P_{t - L}}{P_{t - L}}$$
  $$\text{BUY when } \text{Return}_t > 0, \quad \text{SELL when } \text{Return}_t < 0$$
