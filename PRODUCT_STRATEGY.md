# QuantLab Product Strategy

**Status:** Recommended (pre-implementation)  
**Audience:** Product, engineering, GTU project team  
**Source of truth:** `src/` engine (~1,008 LOC), `README.md`, `MONETIZATION_STRATEGY.md`, `PLATFORM_STRATEGY.md`, companion market research

---

## 1. Product name / working codename

**Product name:** QuantLab (retained — already in code, README, LICENSE, and GTU project records; no rename cost).  
**Working codename:** *Satyam* (Sanskrit for "truth") — the product's mission is that a backtest must not lie. Every codename reference in design docs, issue labels, and release branches uses Satyam.

---

## 2. One-sentence product definition

QuantLab is an open-source, event-driven backtesting engine and overfitting diagnostic platform for Indian equities that proves whether a strategy survives real statutory costs, slippage, and lookahead-free execution before a rupee is deployed.

---

## 3. Core user problem

**Backtests lie.** Retail and advisor backtests hide three frictions that turn profitable paper strategies into losing live strategies:

1. **Hidden costs:** STT (0.1% both sides), stamp duty (0.015% buy-only), GST (18%), NSE turnover (0.00297%), SEBI fee, brokerage, and slippage are omitted, so gross returns are presented as net.
2. **Hidden slippage:** Order size vs. average daily volume moves the execution price (Almgren-Chriss square-root impact); most retail tools fill at the close price as if impact is zero.
3. **Hidden lookahead / overfitting:** Signals are generated on data that includes the future, and Sharpe is inflated by testing many parameter combinations without correction (no Deflated Sharpe Ratio, no Combinatorial Purged Cross-Validation).

**Code evidence (not opinion):**
- `src/engine/backtest_engine.py:9-11` — "Signal on day T Close -> Executed on day T+1 Open"; zero-lookahead is enforced in the event loop (`backtest_engine.py:31-63`).
- `src/engine/cost_model.py:41-55` — full Indian statutory cost model (STT 0.1% both sides, stamp duty 0.015% buy-only, GST 18%, NSE turnover 0.00297% + SEBI 0.0001%, brokerage min(20, 0.03%)), plus Almgren-Chriss slippage capped at 5% (`cost_model.py:23-28`).
- `src/analytics/deflated_sharpe.py` — DSR p-value adjusts observed Sharpe for multiple-testing selection bias.
- `src/analytics/cpcv.py` — CPCV with embargo purges train/test leakage at block boundaries; `calculate_pbo` returns Probability of Backtest Overfitting.
- `README.md:6` — a documented bug sized positions on *cash* instead of *total equity*, silently shrinking trades and masking compounding reality.

**Market research evidence:** Users' #1 complaint is "backtests lie" (lookahead, unrealistic fills, no cost honesty). DSR + CPCV overfitting diagnostics are almost absent in retail tools — a genuine gap. No global tool models Indian statutory costs.

---

## 4. Target customer / user (specific segment)

**Primary (pays):** SEBI-registered Investment Advisors (RIAs) and Research Analysts (RAs) in India, and small proprietary desks / algo shops trading NSE cash equities.

- Why: SEBI compliance demands honest, cost-inclusive backtesting before recommending or deploying capital. They need client-ready reports and overfitting diagnostics (DSR, CPCV/PBO) to defend performance claims. They have budgets; compliance is non-negotiable. Willingness to pay: ₹799–₹2,999/mo (per `MONETIZATION_STRATEGY.md:112-118`).

**Secondary (free tier, brand/adoption):** Quant students, finance faculty, and serious retail traders using the tool to learn honest backtesting. Not targeted for payment; used as the top of funnel and academic pipeline.

**Explicitly NOT targeted:** High-frequency traders, options/futures traders, crypto traders, global equities users, and retail traders expecting a free consumable app. (See scope boundaries in Section 11.)

---

## 5. Primary use case

Run a cost-inclusive, lookahead-free daily-bar backtest of a long-only equity strategy (SMA / RSI / Momentum) over NSE cash equities, then read DSR and CPCV/PBO diagnostics to decide whether the Sharpe is real or an artifact of multiple testing — before allocating client or firm capital.

Workflow: select strategy + parameters → toggle costs on/off → run event-driven T+1 simulation → review CAGR/Sharpe/MDD + full Indian cost breakdown → review DSR p-value and CPCV/PBO → export report (paid tier) → go/no-go on live deployment.

---

## 6. Secondary use cases

- **Quant education:** Teaching DSR, CPCV, embargo, and Indian statutory costs in classrooms (GTU minor-project context; `DI05000341.pdf`).
- **Pre-live audit layer:** An existing algo-tool user (TradingView / Streak / AmiBroker) exports their strategy parameters to QuantLab to audit whether the backtest survives Indian costs and overfitting checks before going live.
- **Parameter-stability stress-test:** Run the same strategy across CPCV paths to see if performance decays out of sample (embargo-aware).
- **Academic research:** Replicating López de Prado's DSR / CPCV / PBO on Indian equity data.

---

## 7. Why users would choose it over existing alternatives

| Alternative | Why users leave it for QuantLab |
|---|---|
| TradingView (free, network effects) | No Indian statutory cost model (STT/GST/Stamp/turnover); no DSR/CPCV; lookahead-prone pine scripts. |
| MT5 (free + brokers) | Built for FX/CFD, not Indian equity delivery costs; no overfitting diagnostics. |
| AmiBroker ($299 once) | No Indian cost model, no DSR/CPCV, desktop-only, not Indian-market-native. |
| AlgoTest (25 free backtests/week) | Indian but cost/slippage honesty and overfitting diagnostics are not the core differentiator; usage-capped free tier. |
| Zerodha Streak | Broker-tied, no-code, no DSR/CPCV, not an independent audit layer. |

**Decision:** Do not try to beat TradingView on charting, community, or breadth. Compete on the two things they don't do for Indian equities: **honest Indian cost modeling** and **overfitting diagnostics (DSR + CPCV/PBO)**.

---

## 8. Unique selling proposition

*The only backtesting engine that enforces zero-lookahead T+1 execution, applies the full Indian statutory cost stack (STT, GST, stamp duty, NSE turnover, SEBI fee, Almgren-Chriss slippage), and reports Deflated Sharpe Ratio and CPCV/PBO overfitting diagnostics — for Indian cash equities — open source.*

---

## 9. Core differentiator

**Cost honesty + overfitting honesty, Indian-market-native.**

- `src/engine/cost_model.py` models every Indian delivery levy, not just brokerage.
- `src/analytics/deflated_sharpe.py` + `src/analytics/cpcv.py` bring institutional-grade overfitting protection (DSR, CPCV, embargo, PBO) to a segment where they are almost absent.
- Zero-lookahead T+1 is architected into the event loop, not a checkbox (`backtest_engine.py:31-63`).

Everything else (3 strategies, daily bars, Streamlit) is table-stakes packaging around this core.

---

## 10. Product philosophy

1. **Backtests must not lie.** If a cost, slippage, or leakage makes a strategy look better than live reality, it is a bug, not a feature.
2. **Indian equities first.** The moat is India-specific (STT/GST/Stamp/NSE-turnover cost model + NSE universe). Do not dilute it with half-baked global markets.
3. **Simulation, not execution.** QuantLab tells you whether a strategy *could* have worked; it never sends an order to a broker.
4. **Open engine, paid diagnostics.** The engine stays Apache 2.0 (adoption + academic credibility); the hosted service, commercial data, reports, and enterprise features are monetized (`LICENSE`, `MONETIZATION_STRATEGY.md:92-102`).
5. **Decisive scope.** Daily bars, equities only, NSE only, long-only. Depth over breadth.

---

## 11. What the product should NOT try to do (explicit scope boundaries)

- **No live trading / no broker integration.** Not a trading bot, not an execution platform, no order routing, no broker API. (`README.md:18`, `backtest_engine.py` is simulation-only.)  
  *Decision: NO live trading.* Commercially right because (a) execution adds regulatory burden (SEBI broker/RA licensing), liability, and ops complexity a 1,008 LOC academic project cannot carry; (b) there is no execution/revenue-share monetization path without a broker partner; (c) the market gap is *diagnostic honesty*, not execution. Execution can be reconsidered only after a paid user base exists and a broker partnership is signed.

- **No intraday / tick / minute bars.** Daily bars only. Intraday requires tick data, different cost structure, and a far more complex engine. (`backtest_engine.py` operates on daily `date`/`close`/`open`/`high`/`low`/`volume`.)  
  *Decision: daily bars is sufficient for v1.* It matches the compute load (local client is sufficient, `PLATFORM_STRATEGY.md:33`), the Indian cash-equity delivery cost model, and the target users (advisors/prop desks running end-of-day screens). Intraday/FnO is a post-revenue expansion, not a v1 requirement.

- **No derivatives, commodities, crypto, or global equities.** NSE cash equities only.  
  *Decision: Indian equities-only is differentiation, not limitation.* It is the only defensible wedge against TradingView/backtrader (`MONETIZATION_STRATEGY.md:139`). Global expansion requires non-Indian cost models and paid data — deferred until revenue justifies it.

- **No strategy marketplace / signal sales.** Three built-in strategies (SMA, RSI, Momentum) are a sandbox/demo, not a catalog. (`src/strategies/` has exactly 3 long-only strategies.)

- **No retail B2C subscription.** Retail willingness-to-pay in India is ₹0–₹500/mo (learning) and ₹500–₹2,500/mo (live); TradingView is free; retail will not pay for a 3-strategy daily-bar tool. (`MONETIZATION_STRATEGY.md:125-127`.) Retail is the free tier, not the revenue source.

- **No bundled licensed commercial data.** Uses `yfinance` (free, academic, not licensed for commercial redistribution). (`README.md:19`.) Before charging, replace `yfinance` with NSE bhavcopy or a paid Indian vendor; Free tier restricted to personal/academic use.

- **No native mobile app.** Streamlit desktop (PyInstaller/Briefcase) + web/PWA for mobile-browser reach. (`PLATFORM_STRATEGY.md`.) Native mobile requires an engine rewrite or backend — rejected for v1.

- **No new UI framework.** Streamlit stays; Plotly charts unchanged. (~96 LOC UI layer.)

---

## Critical decisions — justification summary

| Decision | Position | Evidence |
|---|---|---|
| Live trading? | **NO** | Simulation-only engine; no broker code; regulatory/liability cost unjustified; no execution revenue path (`README.md:18`, `backtest_engine.py`). |
| Indian equities-only? | **Differentiation** | Moat is India-specific cost model; no global tool does this (`MONETIZATION_STRATEGY.md:139`); market gap confirmed by research. |
| Daily bars sufficient? | **YES for v1** | Matches cost model, local compute, advisor end-of-day workflow; intraday deferred (`PLATFORM_STRATEGY.md:33`). |
| Streamlit the right UI? | **YES for v1** | Existing ~96 LOC responsive UI; no frontend build step; wrap via PyInstaller/Briefcase; PWA for mobile reach (`PLATFORM_STRATEGY.md:149-155`). |
| Free vs paid? | **Freemium B2B** | Engine Apache 2.0 (free OSS base); monetize hosted service, commercial data, DSR/CPCV diagnostics, PDF reports, enterprise on-prem (`MONETIZATION_STRATEGY.md:49, 59-64, 92-102`). Retail free tier; RIAs/prop desks pay. |

---

## Positioning statement (one sentence)

QuantLab is the open-source honest backtesting engine for Indian equities that proves whether a strategy survives real statutory costs, slippage, and overfitting before a rupee is deployed — for advisors, prop desks, and quant students who refuse to let backtests lie.

---

## Acceptance criteria for v1 (product view)

- Zero-lookahead T+1 execution verified by existing 9/9 tests (`tests/`).
- Full Indian statutory cost model produces a deterministic cost breakdown per fill (`cost_model.py`).
- DSR p-value and CPCV/PBO computable on any equity history (`deflated_sharpe.py`, `cpcv.py`).
- Streamlit dashboard runs end-to-end on daily NSE data via `yfinance` (`app.py`).
- Free tier: 3 strategies, daily bars, basic metrics, cost on/off toggle, single stock, no export.
- Paid tier (Pro/Team/Enterprise): full cost model, DSR/CPCV/PBO, multi-stock universe, PDF export, commercial data source.
