# QuantLab — Monetization & Business Strategy

**Source of truth:** `src/` engine, `README.md`, `QuantLab_Project_Documentation.md`, `LICENSE` (Apache 2.0).  
**Audience:** Product / GTU project reimagination team.  
**Tone:** Brutally realistic. Retail Indian traders will not pay; TradingView is free.

---

## 1. Bottom Line Up Front

Do **not** build a B2C retail subscription. Retail traders in India are price-sensitive, TradingView/zerodha Streak already offer free backtesting, and QuantLab's data source (`yfinance`) is explicitly **not licensed for commercial redistribution** (`README.md:19`).

**Recommended model:** Freemium B2B SaaS + self-hosted enterprise, targeting **SEBI-registered Investment Advisors (RIAs), Research Analysts (RAs), small prop desks, and wealth managers** — not retail traders. India first; global only after adding non-Indian cost models and asset classes.

**What people will actually pay for:** the *Indian statutory cost model* (STT/GST/Stamp Duty/slippage) + **overfitting diagnostics** (Deflated Sharpe Ratio, CPCV/PBO, parameter stability). These are the two things TradingView does not provide for Indian equities, and compliance-minded advisors/prop desks need them before deploying capital.

---

## 2. Product Reality Check (from actual code)

| Capability | Status | Commercial implication |
|---|---|---|
| 3 strategies (SMA, RSI, Momentum) | `src/strategies/` | Too thin for a paid strategy marketplace; fine as a diagnostic sandbox |
| Daily bars only | `QuantLab_Project_Documentation.md:20` | Excludes intraday algo traders and options/futures users — a large paying segment in India |
| Equities only, NSE market | `README.md:20-21` | No FnO, no commodities, no crypto. Addressable market is cash-equity segment only |
| No live execution / no broker | `README.md:18` | No execution/revenue-share monetization path (no broker referral fees) |
| `yfinance` free data | `README.md:19`, `requirements.txt:7` | **Not licensed for commercial redistribution.** Must replace with NSE bhavcopy or paid vendor before any commercial launch |
| Indian statutory cost model | `src/engine/cost_model.py` (STT, GST, Stamp Duty, NSE turnover, Almgren-Chriss slippage) | **Core moat.** Nothing else in the Indian retail stack models this at backtest time |
| DSR + CPCV/PBO | `src/analytics/deflated_sharpe.py`, `cpcv.py` | **Core moat.** Statistical overfitting diagnostics absent from retail tools |
| Streamlit MVP dashboard | `src/dashboard/app.py` | Demo-grade UI, not production SaaS-grade |
| Apache 2.0 license | `LICENSE` | Permissive — compatible with proprietary commercialization (Section 8) |

**Verdict:** The product is a *diagnostic compliance tool*, not a trading platform. Price it like a B2B analytic, not a consumer app.

---

## 3. Business Model Evaluation

| Model | Fit for QuantLab | Verdict |
|---|---|---|
| **Free / OSS only** | Already Apache 2.0 | Viable but $0 revenue. Good for adoption, bad for sustainability |
| **Freemium SaaS** | Strong fit | Free tier hooks students/retail; paid tier sells diagnostics to RIAs/prop desks |
| **Subscription (SaaS)** | Strong fit | Recurring revenue; matches the "run backtests periodically" usage pattern |
| **One-time purchase** | Weak fit | No ongoing value delivery; SaaS expectations are subscription now |
| **Open-core** | Partial fit | Apache 2.0 means you *can* open-core, but there's no natural "core vs. enterprise" split in a 3-strategy engine |
| **Self-hosted enterprise** | Strong fit | Prop desks/RIAs often require on-prem for data privacy; command higher ACV |
| **Paid desktop** | Weak fit | Streamlit/web-native; desktop distribution adds friction for little gain |

**Recommended:** Freemium SaaS (cloud) + self-hosted enterprise (on-prem), subscription pricing. Apache 2.0 stays as the open base; value-add services, commercial data, and hosted diagnostics are monetized.

---

## 4. Pricing Tiers

### Pricing philosophy
- **India-first:** Price in INR, sensitive to advisor/prop-desk budgets, not retail trader pockets.
- **Global:** USD, ~3.5× INR (FX + higher willingness to pay), only after cost models for US/other markets exist.

| Tier | Price (India) | Price (Global) | Who | What's included |
|---|---|---|---|---|
| **Free** | ₹0 | $0 | Students, retail traders, hobbyists | 3 strategies, daily bars, basic metrics (CAGR/Sharpe/MDD), cost on/off toggle, single-stock backtests, `yfinance` data, personal/academic use only, Streamlit dashboard, no export |
| **Pro** | ₹299/mo or ₹2,999/yr | $9/mo or $99/yr | Serious retail traders, independent advisors | Full Indian statutory cost model (STT/GST/Stamp/slippage), DSR + CPCV/PBO overfitting diagnostics, parameter-stability heatmaps, up to 20-stock universe, PDF report export, commercial-grade data source (replaces `yfinance`) |
| **Team** | ₹799/mo per seat | $29/mo per seat | RIAs, RAs, small prop desks, wealth managers | Everything in Pro + multi-user workspaces, client-ready branded reports, run history/audit log, shareable backtest links, priority support |
| **Enterprise** | ₹15,000–₹25,000/yr | $400–$700/yr | Prop desks, broker research teams, institutions | Self-hosted (on-prem) deployment, SLA, custom cost models/additional markets, API access, SSO, indemnification, data-residency compliance |

**Free → Pro conversion trigger:** The moment a user wants to know "after all Indian taxes and slippage, is this strategy still profitable?" — that's the paid moment. Free shows the equity curve; Pro tells them whether it survives reality.

---

## 5. P0 Paid vs Free Feature Matrix

| Feature | Free | Paid (Pro/Team/Ent) | Rationale |
|---|---|---|---|
| 3 strategies (SMA/RSI/Momentum) | ✅ | ✅ | Hook / demo value |
| Daily-bar backtest | ✅ | ✅ | Core engine, commoditized |
| Basic metrics (CAGR, Sharpe, MDD, win rate) | ✅ | ✅ | Table stakes |
| Cost on/off toggle | ✅ | ❌ | Teaser only; real cost model is paid |
| Full Indian statutory cost model (STT/GST/Stamp/Turnover/Slippage) | ❌ | ✅ **P0 Paid** | Differentiator; costs money to maintain accuracy with SEBI rule changes |
| Deflated Sharpe Ratio (DSR) | ❌ | ✅ **P0 Paid** | Differentiator; academic IP, overfitting protection |
| CPCV / PBO overfitting diagnostic | ❌ | ✅ **P0 Paid** | Differentiator; prevents backtest overfitting claims |
| Parameter-stability heatmaps | ❌ | ✅ **P0 Paid** | Advisor-facing "does this strategy actually hold up?" |
| Multi-stock universe (>1) | ❌ (single) | ✅ | Portfolio-level diagnostics are the paid use case |
| PDF / branded report export | ❌ | ✅ | RIAs need client deliverables |
| Commercial data source (not yfinance) | ❌ | ✅ | `yfinance` cannot be used commercially (`README.md:19`) |
| API access | ❌ | Enterprise only | Integration with advisor workflows |
| Self-hosted / on-prem | ❌ | Enterprise only | Data privacy for prop desks |

**P0 paid = anything that touches compliance, accuracy, or defensibility.** Free = anything that touches curiosity/demo.

---

## 6. Apache 2.0 — Commercial Compatibility

**Apache 2.0 is fully compatible with commercial plans.** Key terms:

- ✅ Commercial use permitted
- ✅ Proprietary derivative works permitted (you do **not** have to open-source your SaaS or desktop app built on QuantLab)
- ✅ Patent grant included
- ⚠️ Must preserve copyright + license notices and include the NOTICE file in distributions
- ⚠️ Cannot use trademarks of contributors without permission

**Implication:** You can keep the QuantLab engine Apache 2.0 (good for adoption/academic credibility) and monetize the hosted service, commercial data pipe, report export, and enterprise features as proprietary. No license change required.

**Caveat:** Apache 2.0 governs the *code*, not the *data*. `yfinance`/Yahoo Finance data is not licensed for commercial redistribution (`README.md:19`). Before charging anyone, replace `yfinance` with NSE bhavcopy archives or a paid Indian market-data vendor, and restrict the Free tier's data rights to personal/academic use.

---

## 7. Target Segments — Who Actually Pays

### Segment 1: SEBI-Registered Investment Advisors (RIAs) & Research Analysts (RAs) — PRIMARY
- **Why they pay:** SEBI compliance requires honest, cost-inclusive backtesting before recommending strategies to clients. They need client-ready reports with DSR/CPCV to defend against "backtest overfitting" challenges. QuantLab's Indian statutory cost model is unique here.
- **Willingness to pay:** ₹799–₹2,999/month. Budget exists; compliance is non-negotiable.
- **Tier:** Team / Pro

### Segment 2: Small Prop Desks & Algo Shops (India) — PRIMARY
- **Why they pay:** Before deploying capital, they need to know true PnL after STT/GST/slippage and whether Sharpe is inflated by multiple testing (DSR). A bad backtest costs more than the subscription.
- **Willingness to pay:** ₹2,999/month or enterprise on-prem ₹15,000–₹25,000/yr.
- **Tier:** Team / Enterprise (self-hosted for data privacy)

### Segment 3: Wealth Managers / Family Offices (India) — SECONDARY
- **Why they pay:** Portfolio-level stress-testing of equity strategies for HNIs; need audit trails and branded reports.
- **Willingness to pay:** ₹1,499–₹7,999/month.
- **Tier:** Team

### Segment 4: Retail Traders & Students — DO NOT TARGET FOR PAYMENT
- **Why they won't pay:** Price-sensitive; TradingView offers free backtracking; Zerodha Streak is free/cheap; `yfinance` is free; they won't pay ₹299 for a 3-strategy daily-bar tool.
- **Role:** Free-tier adoption, brand awareness, academic pipeline. Convert only the rare serious subset to Pro.

### Segment 5: Global (US/other markets) — LATER
- **Why wait:** Cost model is India-specific (STT/GST/Stamp/NSE turnover). Global users need US/UK cost models and intraday/FnO data first. India is the moat; global is expansion.

---

## 8. India vs Global — Initial Target

**India, first and only, for 12–18 months.**

Reasons:
1. **The moat is India-specific.** STT/GST/Stamp Duty/NSE-turnover cost modeling + NSE equity universe is not offered by TradingView or backtrader. That's the only defensible wedge.
2. **Data.** `yfinance` works for NSE (free, no API key) — perfect for an Indian MVP. Global data would require paid feeds.
3. **Regulatory tailwind.** SEBI's retail-loss data (`SEBI 2024 ₹1.81L Cr retail loss`, cited in `docs/01_unit1_literature/problem_statement.md`) creates demand for honest backtesting among advisors.
4. **Price sensitivity.** India supports lower ARPU but lower CAC via content/SEO around "honest backtesting India."

**Global expansion** only after: adding US cost models, intraday bars, FnO/options support, and paid market data. Re-price in USD at ~3.5× INR.

---

## 9. Revenue Potential (TAM / SAM / SOM) — High Level

### TAM (Total Addressable Market)
Indian SEBI-registered RIAs + RAs ≈ 1,500–2,000 entities; small prop desks/algo shops ≈ 300–500; wealth-management equity desks ≈ 200–400. At even ₹10,000/yr average, TAM ≈ ₹20–₹30 crore (~$2.5–$4M). Realistically smaller given niche.

### SAM (Serviceable Addressable Market)
RIAs/RAs and prop desks needing cost-inclusive + overfitting diagnostics, India only, equities-only. ≈ 500–800 addressable accounts. At ₹15,000–₹30,000/yr blended ARPU → SAM ≈ ₹7.5–₹24 crore (~$1–$3M).

### SOM (Serviceable Obtainable Market) — Year 1–2
Capture 2–5% of SAM via content-led acquisition (honest-backtesting SEO, GTU academic network, advisor workshops). ≈ 15–40 paying accounts.
- Conservative: 20 accounts × ₹18,000/yr ≈ **₹3.6 lakh/yr (~$4,300/yr)**
- Optimistic: 40 accounts × ₹30,000/yr ≈ **₹12 lakh/yr (~$14,400/yr)**

### Reality check
This is a **small, niche B2B SaaS**, not a venture-scale business. Expect low single-digit crore revenue at best. Do not project consumer-scale ARPU. The goal is to cover hosting + data costs and fund the GTU project's next phase, not to build a unicorn.

**Break-even:** Very low. A Streamlit app on a small VPS + market-data feed costs ~₹10,000–₹20,000/month. ~8–12 Pro subscribers covers it.

---

## 10. Go-to-Market & Roadmap

| Phase | Action | Monetization impact |
|---|---|---|
| **Now** | Keep Apache 2.0 OSS; free Streamlit demo; academic/GTU credibility | Adoption, brand, zero revenue |
| **Pre-launch** | Replace `yfinance` with NSE bhavcopy / paid vendor; add Terms of Service restricting commercial use of Free tier | Enables legal charging |
| **Launch** | Free + Pro tiers; ₹299/mo Pro; PDF export + DSR/CPCV behind paywall | First revenue |
| **Scale** | Team tier for RIAs; advisor workshops; SEBI compliance content marketing | B2B ACV growth |
| **Enterprise** | Self-hosted on-prem + API + SLA for prop desks | High-ACV deals |
| **Global (18+ mo)** | US cost models, intraday/FnO, paid data; USD pricing | Expansion |

**Content strategy (low CAC in India):** "Why your TradingView backtest is lying to you — STT, GST, slippage, and overfitting explained for NSE equities." Leverage the GTU academic angle and DSR/CPCV IP.

---

## 11. Key Risks

| Risk | Mitigation |
|---|---|
| `yfinance` not commercially licensed | Replace data source before charging; Free tier = personal/academic use only |
| Retail won't pay | Do not target retail; gate value props (cost model, DSR, CPCV) behind Pro |
| TradingView adds Indian cost model + DSR | Moat is narrow; differentiate via advisor workflow, client reports, SEBI compliance framing |
| Only 3 strategies, daily bars, equities | Position as diagnostic/compliance tool, not strategy marketplace; expand FnO/intraday only if revenue justifies |
| Apache 2.0 lets competitors fork | Allowed; compete on service, data, reports, support — not the engine code |

---

## 12. Recommendation Summary

1. **Model:** Freemium SaaS (Free/Pro/Team) + self-hosted Enterprise; subscription pricing.
2. **License:** Keep Apache 2.0 for the engine (commercial-friendly, adoption-friendly).
3. **Data:** Drop `yfinance` for commercial use; switch to NSE bhavcopy/paid vendor before launch.
4. **Target:** Indian SEBI RIAs/RAs and small prop desks — not retail traders.
5. **P0 paid features:** Full Indian statutory cost model, DSR, CPCV/PBO, parameter-stability heatmaps, multi-stock universe, PDF reports, commercial data.
6. **Market:** India first; global after adding non-Indian cost models and asset classes.
7. **Revenue:** Realistic SOM ≈ ₹3.6–₹12 lakh/yr in years 1–2; low CAC, low break-even, niche B2B — not consumer scale.
