# QuantLab — Stock Universe Selection & Benchmark Justification

**Project Title**: QuantLab: A Realistic Backtesting Engine & Overfitting Diagnostic Platform for Indian Equities  
**Course Code**: GTU DI05000341 (Minor Project — Semester 5)  
**Academic Unit**: Unit 1 & Unit 2 — Data Design & Universe Architecture  
**Authors**: Aayush Avinash Bankar (Leader) & Meet Jayeshbhai Patel  
**Date**: August 16, 2026  

---

## 1. Executive Summary

A pervasive vulnerability in quantitative backtesting is the arbitrary selection of test assets without explicit liquidity, survivorship, and market microstructure disclosures. 

This document formalizes the **QuantLab Indian Equity Universe**: a curated portfolio of **10 mega-cap Indian equities listed on the National Stock Exchange (NSE)** and the **Nifty 50 Benchmark Index (`^NSEI`)**. We provide the mathematical and economic justification for each asset, analyze liquidity profiles using official NSE volume data to validate the zero market-impact assumption, and define the **In-Sample (2019–2022) vs Out-of-Sample (2023–2024)** market regime partitioning.

---

## 2. Selection Methodology & Microstructure Criteria

The universe was constructed using four strict quantitative filtering criteria [NSE India, 2026]:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    UNIVERSE SELECTION FILTERING FUNNEL                      │
├───────────────────────────────┬─────────────────────────────────────────────┤
│ 1. Market Capitalization      │ Mega-Cap (>₹4,50,000 Crore / >$50B USD)     │
├───────────────────────────────┼─────────────────────────────────────────────┤
│ 2. Microstructure Liquidity   │ Average Daily Volume (ADV) > 1,000,000 shs  │
│                               │ Average Daily Turnover > ₹200 Crore         │
├───────────────────────────────┼─────────────────────────────────────────────┤
│ 3. Economic Sector Diversity  │ 7 Distinct Sectors (Energy, IT, Banking,    │
│                               │ FMCG, Telecom, Infrastructure, Industrials) │
├───────────────────────────────┼─────────────────────────────────────────────┤
│ 4. Historical Continuity      │ 100% Trading Day Presence (2019–2024)       │
│                               │ Zero corporate delisting or trading halts   │
└───────────────────────────────┴─────────────────────────────────────────────┘
```

### 2.1 Mathematical Justification for the Zero Market-Impact Assumption
In financial simulation, assuming that orders execute without non-linear price impact is mathematically valid **only if the simulated order size represents an infinitesimal fraction of the Average Daily Volume (ADV)** [Kissell & Glantz, 2003]:

$$\text{Participation Rate} = \frac{\text{Simulated Trade Size}}{\text{Average Daily Volume (ADV)}} < 0.01\%$$

For a simulated retail trading portfolio with ₹10,00,000 capital executing trades of ₹1,00,000 to ₹5,00,000 in stocks with daily turnover exceeding ₹200 Crore (~$24M USD per day), the participation rate is **$< 0.0025\%$**. Therefore, non-linear market impact is negligible, and execution friction is fully captured by the bid-ask spread slippage model ($0.05\%$).

---

## 3. The 10 Selected Indian Equities (Verified Profiles)

| # | Company Name | Yahoo Finance Ticker | Sector | Market Capitalization (₹ Cr) | Average Daily Volume (Shares) | Macroeconomic & Sector Rationale |
|---|---|---|---|---|---|---|
| **1** | **Reliance Industries Ltd.** | `RELIANCE.NS` | Energy / Oil / Conglomerate | **₹17,72,763 Cr** | **10,497,000+** | Heavyweight in Nifty 50; represents Indian oil, refining, telecom (Jio), and organized retail. |
| **2** | **Bharti Airtel Limited** | `BHARTIARTL.NS` | Telecommunications | **₹12,13,898 Cr** | **12,282,000+** | Dominant telecom and digital infrastructure provider with secular growth and ARPU expansion. |
| **3** | **HDFC Bank Limited** | `HDFCBANK.NS` | Private Banking & Financials | **₹11,20,263 Cr** | **20,364,000+** | Core anchor of the Indian financial sector; highest institutional foreign portfolio (FII) liquidity. |
| **4** | **ICICI Bank Limited** | `ICICIBANK.NS` | Private Banking | **₹10,16,879 Cr** | **6,097,000+** | Fast-growing private bank with strong corporate credit and retail loan momentum. |
| **5** | **State Bank of India** | `SBIN.NS` | Public Sector Banking (PSU) | **₹9,85,553 Cr** | **6,273,000+** | India's largest state-owned lender; bellwether for sovereign credit, deposit growth, and treasury yield. |
| **6** | **Tata Consultancy Services** | `TCS.NS` | Information Technology | **₹8,54,230 Cr** | **2,232,000+** | India's largest IT exporter; driven by global enterprise spending, cloud transformation, and USD/INR. |
| **7** | **Larsen & Toubro Ltd.** | `LT.NS` | Infrastructure & Capital Goods | **₹5,70,784 Cr** | **934,000+** | Core driver of Indian capital expenditure, defense, and public infrastructure modernization. |
| **8** | **ITC Limited** | `ITC.NS` | FMCG / Conglomerate | **₹5,20,000 Cr** | **8,500,000+** | High-dividend defensive asset; historically displays strong statistical mean-reversion. |
| **9** | **Hindustan Unilever Ltd.** | `HINDUNILVR.NS` | FMCG / Consumer Staples | **₹4,88,010 Cr** | **1,148,000+** | Consumer staple bellwether reflecting rural and urban disposable income and inflation trends. |
| **10** | **Infosys Limited** | `INFY.NS` | Information Technology | **₹4,74,468 Cr** | **5,844,000+** | Highly liquid large-cap tech titan; primary vehicle for momentum and earnings volatility strategies. |

*(Market Cap and Volume data verified via NSE Official Bulletin as of August 2026)*

---

## 4. Benchmark Index Justification

| Parameter | Specification |
|---|---|
| **Benchmark Asset** | **NIFTY 50 Index** |
| **Yahoo Finance Ticker** | `^NSEI` |
| **Asset Class** | Free-Float Market-Weighted Equities Index (Top 50 Companies on NSE) |
| **Role in QuantLab** | Baseline for Beta ($\beta$), Alpha ($\alpha$), and Active Excess Return |

### Academic Justification for Nifty 50:
1. **The Economic Hurdle**: Any systematic strategy that fails to beat a passive Buy-and-Hold allocation in the Nifty 50 Index after fees and taxes is economically unviable for an investor.
2. **Cap-Weighted Market Proxy**: Nifty 50 represents approximately **~60% of the total free-float market capitalization** of all listed stocks on the NSE.
3. **Beta Decomposition**: Enables isolating whether strategy returns are genuine skill ($\alpha$) or merely leveraged exposure to the broader market index ($\beta \times R_{\text{m}}$).

---

## 5. Timeline & Market Regime Partitioning

To rigorously test for overfitting and parameter decay, the 6-year dataset (January 1, 2019 to December 31, 2024) is partitioned into two distinct non-overlapping market regimes:

```
2019                  2020                  2021                  2022                  2023                  2024
├─────────────────────┼─────────────────────┼─────────────────────┼─────────────────────┼─────────────────────┤
│ ◄───────────────────────── IN-SAMPLE (IS) ────────────────────────► │ ◄──────────── OUT-OF-SAMPLE (OOS) ──────────► │
│ Pre-COVID + Crash + Liquidity Bull Run + Rate Hike Consolidation    │ Macroeconomic Expansion + All-Time Highs    │
│ (4 Years: Jan 2019 – Dec 2022 | ~990 Trading Days)                 │ (2 Years: Jan 2023 – Dec 2024 | ~490 Days)  │
```

---

### 5.1 In-Sample Period (Tuning & Training): 2019-01-01 to 2022-12-31
- **Duration**: 4 Calendar Years (~990 Trading Days).
- **Macroeconomic & Market Regimes Included**:
  1. *2019*: Pre-pandemic range-bound market and corporate tax cuts.
  2. *March 2020*: COVID-19 Black Swan liquidity shock (-38% crash in 30 days, India VIX spiking to 86).
  3. *2020–2021*: Unprecedented monetary easing and massive continuous trending bull run.
  4. *2022*: Global inflation shock, Russia-Ukraine geopolitical crisis, aggressive global central bank rate hikes, and sideways consolidation.
- **Academic Role**: Used exclusively for parameter optimization, strategy hypothesis formulation, and indicator threshold calibration.

---

### 5.2 Out-of-Sample Period (Validation & Overfitting Detection): 2023-01-01 to 2024-12-31
- **Duration**: 2 Calendar Years (~490 Trading Days).
- **Macroeconomic & Market Regimes Included**:
  1. *2023*: Post-Hindenburg recovery, infrastructure-led industrial rally, and small/mid-cap breakout.
  2. *2024*: General elections volatility, foreign institutional outflows countered by record domestic SIP inflows, and Nifty reaching milestone highs (>26,000).
- **Academic Role**: **Strictly quarantined out-of-sample test set**. Parameters optimized in the IS period are applied to the OOS period without re-tuning. 
- **Diagnostic Objective**: Quantify the exact percentage degradation in Sharpe ratio and return from In-Sample to Out-of-Sample.

---

## 6. Data Integrity & Survivorship Bias Disclosure

In accordance with academic research standards [Brown et al., 1992]:

1. **Survivorship Bias Acknowledgment**: The stock universe comprises current large-cap leaders. While this introduces mild survivorship bias compared to the entire historical exchange listing, all 10 companies were continuously listed and actively traded throughout the entire 2019–2024 window without bankruptcy or delisting events.
2. **Corporate Action Adjustments**: Daily historical prices are fetched using `yfinance` with split and dividend adjustments applied to the `Close` and `Open` prices to preserve continuous return calculations.
3. **Missing Bar Policy**: In the event of market holidays or missing quotes, QuantLab drops missing rows rather than forward-filling across weekends/holidays to prevent artificial zero-volatility bars.

---

## 7. Configuration Schema for Code Implementation (`src/data/universe.py`)

```python
# Standard Universe Definition Contract for src/data/universe.py
INDIAN_EQUITY_UNIVERSE = {
    "RELIANCE": {"symbol": "RELIANCE.NS", "name": "Reliance Industries Ltd", "sector": "Energy"},
    "BHARTIARTL": {"symbol": "BHARTIARTL.NS", "name": "Bharti Airtel Limited", "sector": "Telecommunications"},
    "HDFCBANK": {"symbol": "HDFCBANK.NS", "name": "HDFC Bank Limited", "sector": "Financials"},
    "ICICIBANK": {"symbol": "ICICIBANK.NS", "name": "ICICI Bank Limited", "sector": "Financials"},
    "SBIN": {"symbol": "SBIN.NS", "name": "State Bank of India", "sector": "Financials"},
    "TCS": {"symbol": "TCS.NS", "name": "Tata Consultancy Services", "sector": "Technology"},
    "LT": {"symbol": "LT.NS", "name": "Larsen & Toubro Ltd", "sector": "Industrials"},
    "ITC": {"symbol": "ITC.NS", "name": "ITC Limited", "sector": "Consumer Goods"},
    "HINDUNILVR": {"symbol": "HINDUNILVR.NS", "name": "Hindustan Unilever Ltd", "sector": "Consumer Goods"},
    "INFY": {"symbol": "INFY.NS", "name": "Infosys Limited", "sector": "Technology"},
}

BENCHMARK_TICKER = "^NSEI"  # Nifty 50 Index

DATE_CONFIG = {
    "IN_SAMPLE_START": "2019-01-01",
    "IN_SAMPLE_END": "2022-12-31",
    "OUT_OF_SAMPLE_START": "2023-01-01",
    "OUT_OF_SAMPLE_END": "2024-12-31",
}
```

---

## 8. Academic & Industry References

1. **Brown, S. J., Goetzmann, W., Ibbotson, R. G., & Ross, S. A.** (1992). *Survivorship Bias in Performance Studies*. The Review of Financial Studies, 5(4), 553–580.
2. **Kissell, R., & Glantz, M.** (2003). *Optimal Trading Strategies: Quantitative Approaches for Managing Market Impact and Trading Risk*. AMACOM / American Management Association.
3. **National Stock Exchange of India (NSE).** (2026). *Nifty 50 Index Factsheet, Market Capitalization and Trading Volume Statistics*. NSE India Indices. Available: https://www.nseindia.com
4. **Reserve Bank of India (RBI).** (2024). *Macroeconomic Indicators & Financial Markets Data*. Available: https://www.rbi.org.in
