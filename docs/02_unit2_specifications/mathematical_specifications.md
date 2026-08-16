# QuantLab — Mathematical Specifications & Indian Cost Formulation

**Project Title**: QuantLab: A Realistic Backtesting Engine & Overfitting Diagnostic Platform for Indian Equities  
**Course Code**: GTU DI05000341 (Minor Project — Semester 5)  
**Academic Unit**: Unit 1 & Unit 2 — Mathematical Foundations & Financial Specifications  
**Authors**: Aayush Avinash Bankar (Leader) & Meet Jayeshbhai Patel  
**Date**: August 16, 2026  

---

## 1. Executive Overview

This document provides the formal mathematical specifications for all financial modeling, statutory Indian market transaction charges, performance metrics, risk analytics, and statistical overfitting corrections implemented in **QuantLab**.

Every equation defined herein serves as an unambiguous specification contract for the Python simulation engine (`src/engine/` and `src/analytics/`) and the automated test suite (`tests/`).

---

## 2. Indian Equity Delivery Statutory Cost Formulation (NSE)

In Indian equity markets, delivery transactions executed on the National Stock Exchange (NSE) are governed by statutory rates mandated by the **Ministry of Finance (Government of India)**, **SEBI**, and the **Indian Stamp Act** [Ministry of Finance, 2020; NSE Circulars, 2024].

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                    INDIAN EQUITY DELIVERY STATUTORY RATE CARD                     │
├────────────────────────────────┬────────────────────────┬────────────────────────┤
│ Charge Component               │ Buy Side Rate          │ Sell Side Rate         │
├────────────────────────────────┼────────────────────────┼────────────────────────┤
│ 1. Brokerage                   │ 0.03% (capped at ₹20)  │ 0.03% (capped at ₹20)  │
│ 2. Securities Transaction Tax  │ 0.10% of Trade Value   │ 0.10% of Trade Value   │
│ 3. Exchange Transaction Charge │ 0.00297% (NSE)         │ 0.00297% (NSE)         │
│ 4. SEBI Turnover Fee           │ 0.0001% (₹10 / Crore)  │ 0.0001% (₹10 / Crore)  │
│ 5. GST                         │ 18% on (Brok+Exch+SEBI)│ 18% on (Brok+Exch+SEBI)│
│ 6. Stamp Duty (State Govt)     │ 0.015% of Trade Value  │ 0.000% (Buy only)      │
│ 7. Execution Slippage (Model)  │ +0.05% price penalty   │ -0.05% price penalty   │
└────────────────────────────────┴────────────────────────┴────────────────────────┘
```

---

### 2.1 Formal Cost Equations

Let:
- $P_{\text{raw}}$ = Raw market Open price at Day $t+1$.
- $Q$ = Order quantity (number of shares).
- $\delta_{\text{slip}}$ = Execution slippage fraction (default: $0.0005$ or $0.05\%$).
- $r_{\text{brok}}$ = Brokerage rate ($0.0003$ or $0.03\%$, subject to max cap $C_{\text{brok}} = ₹20.00$).
- $r_{\text{stt}}$ = Securities Transaction Tax rate ($0.0010$ or $0.10\%$).
- $r_{\text{exch}}$ = NSE Exchange Transaction rate ($0.0000297$ or $0.00297\%$).
- $r_{\text{sebi}}$ = SEBI Turnover rate ($0.000001$ or $0.0001\%$).
- $r_{\text{gst}}$ = Goods and Services Tax rate ($0.18$ or $18.0\%$).
- $r_{\text{stamp}}$ = Stamp Duty rate ($0.00015$ or $0.015\%$).

#### A. Buy Order Execution
1. **Slippage-Adjusted Execution Price**:
   $$P_{\text{fill, buy}} = P_{\text{raw}} \times (1 + \delta_{\text{slip}})$$
2. **Gross Trade Value**:
   $$V_{\text{buy}} = P_{\text{fill, buy}} \times Q$$
3. **Friction Breakdown**:
   $$\text{Brokerage}_{\text{buy}} = \min\left(C_{\text{brok}}, V_{\text{buy}} \times r_{\text{brok}}\right)$$
   $$\text{ExchangeFee}_{\text{buy}} = V_{\text{buy}} \times r_{\text{exch}}$$
   $$\text{SEBIFee}_{\text{buy}} = V_{\text{buy}} \times r_{\text{sebi}}$$
   $$\text{GST}_{\text{buy}} = \left(\text{Brokerage}_{\text{buy}} + \text{ExchangeFee}_{\text{buy}} + \text{SEBIFee}_{\text{buy}}\right) \times r_{\text{gst}}$$
   $$\text{STT}_{\text{buy}} = V_{\text{buy}} \times r_{\text{stt}}$$
   $$\text{StampDuty}_{\text{buy}} = V_{\text{buy}} \times r_{\text{stamp}}$$
4. **Total Buy Cash Outflow**:
   $$\text{CashOutflow}_{\text{buy}} = V_{\text{buy}} + \text{Brokerage}_{\text{buy}} + \text{ExchangeFee}_{\text{buy}} + \text{SEBIFee}_{\text{buy}} + \text{GST}_{\text{buy}} + \text{STT}_{\text{buy}} + \text{StampDuty}_{\text{buy}}$$

---

#### B. Sell Order Execution
1. **Slippage-Adjusted Execution Price**:
   $$P_{\text{fill, sell}} = P_{\text{raw}} \times (1 - \delta_{\text{slip}})$$
2. **Gross Trade Value**:
   $$V_{\text{sell}} = P_{\text{fill, sell}} \times Q$$
3. **Friction Breakdown**:
   $$\text{Brokerage}_{\text{sell}} = \min\left(C_{\text{brok}}, V_{\text{sell}} \times r_{\text{brok}}\right)$$
   $$\text{ExchangeFee}_{\text{sell}} = V_{\text{sell}} \times r_{\text{exch}}$$
   $$\text{SEBIFee}_{\text{sell}} = V_{\text{sell}} \times r_{\text{sebi}}$$
   $$\text{GST}_{\text{sell}} = \left(\text{Brokerage}_{\text{sell}} + \text{ExchangeFee}_{\text{sell}} + \text{SEBIFee}_{\text{sell}}\right) \times r_{\text{gst}}$$
   $$\text{STT}_{\text{sell}} = V_{\text{sell}} \times r_{\text{stt}}$$
   $$\text{StampDuty}_{\text{sell}} = 0.0 \quad \text{(Stamp duty is zero on sell orders)}$$
4. **Total Net Sell Cash Inflow**:
   $$\text{CashInflow}_{\text{sell}} = V_{\text{sell}} - \left(\text{Brokerage}_{\text{sell}} + \text{ExchangeFee}_{\text{sell}} + \text{SEBIFee}_{\text{sell}} + \text{GST}_{\text{sell}} + \text{STT}_{\text{sell}}\right)$$

---

### 2.2 Golden Master Worked Example (Deterministic Test Fixture)

To serve as a deterministic test fixture for `tests/test_cost_model.py`:

**Scenario**:
- Buy $Q = 100$ shares of `RELIANCE.NS` at raw price $P_{\text{raw}} = ₹1,000.00$.
- Sell $Q = 100$ shares of `RELIANCE.NS` later at raw price $P_{\text{raw}} = ₹1,100.00$.
- Slippage $\delta_{\text{slip}} = 0.05\%$.

#### Step 1: Buy Order Calculations
- Fill Price: $1000.00 \times (1 + 0.0005) = ₹1,000.50$
- Gross Buy Value: $1000.50 \times 100 = ₹1,00,050.00$
- Brokerage: $\min(20.00, 100050.00 \times 0.0003) = \min(20.00, 30.015) = ₹20.00$ (capped)
- NSE Exchange Fee: $100050.00 \times 0.0000297 = ₹2.9715$
- SEBI Turnover Fee: $100050.00 \times 0.000001 = ₹0.1001$
- GST (18%): $(20.00 + 2.9715 + 0.1001) \times 0.18 = 23.0716 \times 0.18 = ₹4.1529$
- STT (0.10%): $100050.00 \times 0.0010 = ₹100.05$
- Stamp Duty (0.015%): $100050.00 \times 0.00015 = ₹15.0075$
- **Total Buy Frictions**: $20.00 + 2.9715 + 0.1001 + 4.1529 + 100.05 + 15.0075 = \mathbf{₹142.2820}$
- **Total Cash Deducted**: $100050.00 + 142.2820 = \mathbf{₹1,00,192.28}$

#### Step 2: Sell Order Calculations
- Fill Price: $1100.00 \times (1 - 0.0005) = ₹1,099.45$
- Gross Sell Value: $1099.45 \times 100 = ₹1,09,945.00$
- Brokerage: $\min(20.00, 109945.00 \times 0.0003) = \min(20.00, 32.9835) = ₹20.00$ (capped)
- NSE Exchange Fee: $109945.00 \times 0.0000297 = ₹3.2654$
- SEBI Turnover Fee: $109945.00 \times 0.000001 = ₹0.1099$
- GST (18%): $(20.00 + 3.2654 + 0.1099) \times 0.18 = 23.3753 \times 0.18 = ₹4.2076$
- STT (0.10%): $109945.00 \times 0.0010 = ₹109.945$
- Stamp Duty: ₹0.00
- **Total Sell Frictions**: $20.00 + 3.2654 + 0.1099 + 4.2076 + 109.945 = \mathbf{₹137.5279}$
- **Net Cash Credited**: $109945.00 - 137.5279 = \mathbf{₹1,09,807.47}$

#### Step 3: Round-Trip PnL Synthesis
- **Gross Paper Profit (without fees/slippage)**: $(1100.00 - 1000.00) \times 100 = \mathbf{+₹10,000.00}$
- **Net Realized Profit (after statutory costs & slippage)**: $109807.47 - 100192.28 = \mathbf{+₹9,615.19}$
- **Total Round-Trip Friction Drag**: $₹10,000.00 - ₹9,615.19 = \mathbf{₹384.81}$ (or **3.85%** of gross profit eroded on a single delivery trade).

---

## 3. Core Financial & Risk Performance Metrics

Let $\{V_t\}_{t=0}^T$ denote the daily portfolio equity series over $T$ trading days, and let daily returns be:
$$R_t = \frac{V_t - V_{t-1}}{V_{t-1}} \quad \text{for } t = 1, 2, \dots, T$$

### 3.1 Total Return ($R_{\text{total}}$)
$$R_{\text{total}} = \frac{V_T - V_0}{V_0}$$

### 3.2 Compounded Annual Growth Rate (CAGR)
$$\text{CAGR} = \left(\frac{V_T}{V_0}\right)^{\frac{252}{T}} - 1$$
*(where 252 represents the standard annual trading days on NSE)*

### 3.3 Annualized Sharpe Ratio ($\text{SR}$)
Let $R_f$ denote the annual risk-free rate ($6.0\%$ default, representing 10-year Indian Government G-Sec yield) [RBI, 2024].  
Daily risk-free rate: $R_{f, \text{daily}} = \frac{R_f}{252}$.

$$\text{Excess Return}: D_t = R_t - R_{f, \text{daily}}$$
$$\text{Mean Excess Return}: \bar{D} = \frac{1}{T} \sum_{t=1}^T D_t$$
$$\text{Sample Standard Deviation}: \sigma_R = \sqrt{\frac{1}{T-1} \sum_{t=1}^T (R_t - \bar{R})^2}$$
$$\text{Annualized Sharpe Ratio}: \text{SR} = \sqrt{252} \times \frac{\bar{D}}{\sigma_R}$$

---

### 3.4 Downside Deviation & Sortino Ratio
The **Sortino Ratio** penalizes only downside semi-variance below the risk-free rate:

$$\sigma_{\text{downside}} = \sqrt{\frac{1}{T} \sum_{t=1}^T \min\left(0, R_t - R_{f, \text{daily}}\right)^2}$$
$$\text{Sortino Ratio} = \sqrt{252} \times \frac{\bar{D}}{\sigma_{\text{downside}}}$$

---

### 3.5 Maximum Drawdown (MDD) & High-Water Mark
The High-Water Mark ($\text{HWM}_t$) tracks the highest portfolio valuation up to time $t$:
$$\text{HWM}_t = \max_{0 \le s \le t} V_s$$

The Drawdown at day $t$ is:
$$\text{DD}_t = \frac{\text{HWM}_t - V_t}{\text{HWM}_t} \quad \text{where } \text{DD}_t \in [0, 1]$$

$$\text{Maximum Drawdown}: \text{MDD} = \max_{0 \le t \le T} \text{DD}_t$$

### 3.6 Calmar Ratio
$$\text{Calmar Ratio} = \frac{\text{CAGR}}{\text{MDD}}$$

---

## 4. Institutional Overfitting Diagnostics: Marcos López de Prado's DSR

In quantitative finance, evaluating $N$ parameter combinations and reporting the best observed Sharpe ratio ($\widehat{\text{SR}}$) induces severe **selection bias under multiple testing** [Bailey & López de Prado, 2014].

### 4.1 Return Distribution Higher Moments
Let $\widehat{\mu}$, $\widehat{\sigma}$, $\widehat{\gamma}_3$ (skewness), and $\widehat{\gamma}_4$ (kurtosis) represent the sample moments of daily returns $\{R_t\}$:
$$\widehat{\gamma}_3 = \frac{\frac{1}{T}\sum_{t=1}^T (R_t - \widehat{\mu})^3}{\widehat{\sigma}^3}, \quad \widehat{\gamma}_4 = \frac{\frac{1}{T}\sum_{t=1}^T (R_t - \widehat{\mu})^4}{\widehat{\sigma}^4}$$

### 4.2 Asymptotic Variance of the Sharpe Ratio
Under non-normal returns, the asymptotic variance of the estimated annualized Sharpe ratio $\widehat{\text{SR}}$ is:
$$\text{Var}(\widehat{\text{SR}}) = \frac{1}{T} \left( 1 - \widehat{\gamma}_3 \widehat{\text{SR}} + \frac{\widehat{\gamma}_4 - 1}{4} \widehat{\text{SR}}^2 \right)$$

### 4.3 Expected Maximum Sharpe Ratio Under the Null Hypothesis
Under the Null Hypothesis $H_0$ (all $N$ strategy trials have zero true alpha and are drawn from independent or correlated noise with variance $\sigma_{\text{SR}}^2$):

$$\text{E}\left[\max_{1 \le n \le N} \widehat{\text{SR}}_n\right] = \text{SR}^* + \sigma_{\text{SR}} \left( (1 - \gamma_{\text{EM}}) \Phi^{-1}\left(1 - \frac{1}{N}\right) + \gamma_{\text{EM}} \Phi^{-1}\left(1 - \frac{1}{N \cdot e}\right) \right)$$

where:
- $\gamma_{\text{EM}} \approx 0.5772156649$ is the Euler-Mascheroni constant.
- $e \approx 2.7182818284$ is Euler's number.
- $\Phi^{-1}(\cdot)$ is the standard normal quantile function.
- $\text{SR}^*$ is the benchmark Sharpe ratio (default: 0.0).

### 4.4 Deflated Sharpe Ratio (DSR) P-Value
$$\text{Z}_{\text{DSR}} = \frac{\widehat{\text{SR}} - \text{E}\left[\max_{n} \widehat{\text{SR}}_n\right]}{\sqrt{\text{Var}(\widehat{\text{SR}})}}$$

$$\text{DSR} = \Phi(\text{Z}_{\text{DSR}})$$

where $\Phi(\cdot)$ is the standard normal cumulative distribution function (CDF).

> **Decision Threshold**:
> - If $\text{DSR} \ge 0.95$ ($p \le 0.05$): The strategy is **statistically significant** (not a lucky artifact of data snooping).
> - If $\text{DSR} < 0.95$ ($p > 0.05$): The strategy is **overfitted** (fails the multi-testing hurdle).

---

## 5. Canonical Technical Strategy Signal Equations

### 5.1 Strategy 1: Simple Moving Average (SMA) Crossover
$$\text{SMA}_{\text{short}, t} = \frac{1}{S} \sum_{i=0}^{S-1} P_{t-i}, \quad \text{SMA}_{\text{long}, t} = \frac{1}{L} \sum_{i=0}^{L-1} P_{t-i} \quad (S < L)$$

$$\text{Signal}_t = \begin{cases} +1 \ (\text{BUY}) & \text{if } \text{SMA}_{\text{short}, t} > \text{SMA}_{\text{long}, t} \text{ and } \text{SMA}_{\text{short}, t-1} \le \text{SMA}_{\text{long}, t-1} \\ -1 \ (\text{SELL}) & \text{if } \text{SMA}_{\text{short}, t} < \text{SMA}_{\text{long}, t} \text{ and } \text{SMA}_{\text{short}, t-1} \ge \text{SMA}_{\text{long}, t-1} \\ 0 \ (\text{HOLD}) & \text{otherwise} \end{cases}$$

### 5.2 Strategy 2: Relative Strength Index (RSI) Mean-Reversion
Using Wilder's Exponential Smoothing with period $M=14$ [Wilder, 1978]:
$$\text{Gain}_t = \max(0, P_t - P_{t-1}), \quad \text{Loss}_t = \max(0, P_{t-1} - P_t)$$
$$\text{AvgGain}_t = \frac{\text{AvgGain}_{t-1} \times 13 + \text{Gain}_t}{14}, \quad \text{AvgLoss}_t = \frac{\text{AvgLoss}_{t-1} \times 13 + \text{Loss}_t}{14}$$
$$\text{RS}_t = \frac{\text{AvgGain}_t}{\text{AvgLoss}_t}, \quad \text{RSI}_t = 100 - \frac{100}{1 + \text{RS}_t}$$

$$\text{Signal}_t = \begin{cases} +1 \ (\text{BUY}) & \text{if } \text{RSI}_t < 30 \ (\text{oversold}) \\ -1 \ (\text{SELL}) & \text{if } \text{RSI}_t > 70 \ (\text{overbought}) \\ 0 \ (\text{HOLD}) & \text{otherwise} \end{cases}$$

### 5.3 Strategy 3: Lookback Relative Momentum
Let $L$ denote the lookback window in days (default: $L=60$) [Jegadeesh & Titman, 1993]:
$$\text{Mom}_t = \frac{P_t - P_{t-L}}{P_{t-L}}$$

$$\text{Signal}_t = \begin{cases} +1 \ (\text{BUY}) & \text{if } \text{Mom}_t > 0 \text{ and } \text{Mom}_{t-1} \le 0 \\ -1 \ (\text{SELL}) & \text{if } \text{Mom}_t < 0 \text{ and } \text{Mom}_{t-1} \ge 0 \\ 0 \ (\text{HOLD}) & \text{otherwise} \end{cases}$$

---

## 6. Academic & Statutory Citations

1. **Bailey, D. H., & López de Prado, M.** (2014). *The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality*. Journal of Portfolio Management, 40(5), 94–107.
2. **Brock, W., Lakonishok, J., & LeBaron, B.** (1992). *Simple Technical Trading Rules and the Stochastic Properties of Stock Returns*. The Journal of Finance, 47(5), 1731-1764.
3. **Jegadeesh, N., & Titman, S.** (1993). *Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency*. The Journal of Finance, 48(1), 65-91.
4. **Ministry of Finance, Government of India.** (2020). *Indian Stamp (Collection of Stamp-Duty through Stock Exchanges, Clearing Corporations and Depositories) Rules, 2019*. Gazette of India, Notification w.e.f. 1st July 2020.
5. **National Stock Exchange of India (NSE).** (2024). *Comprehensive Master Circular on Transaction Charges and Levies in Capital Market Segment*. Circular Ref: NSE/CM/2024. Available: https://www.nseindia.com
6. **Reserve Bank of India (RBI).** (2024). *Handbook of Statistics on the Indian Economy: Benchmark Yields and Repo Rates*. Available: https://www.rbi.org.in
7. **Wilder, J. W.** (1978). *New Concepts in Technical Trading Systems*. Trend Research, Greensboro, NC.
