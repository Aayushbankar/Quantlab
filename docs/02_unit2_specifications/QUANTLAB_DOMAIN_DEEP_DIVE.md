# QuantLab — Domain-Segregated Deep Study Guide
## Hard Facts, Exact Knowledge Requirements, and Learning Priorities per Domain

**Project**: QuantLab: A Realistic Backtesting Engine & Overfitting Diagnostic Platform for Indian Equities  
**Course Code**: GTU DI05000341 (Minor Project — Semester 5)  
**Authors**: Aayush Avinash Bankar (Leader) & Meet Jayeshbhai Patel  
**Date**: August 18, 2026  
**Status**: Unit 1–2 Study Phase — Design Contracts Frozen Before Code

---

## 📊 DOMAIN MAP: QUANTLAB'S FIVE PILLARS

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        QUANTLAB KNOWLEDGE ARCHITECTURE                      │
├──────────────┬──────────────┬──────────────┬──────────────┬────────────────┤
│  MATHEMATICS │   FINANCE    │  PROGRAMMING │    QUANT     │ SOFTWARE ENGG  │
│  (Foundations)│  (Domain)    │  (Implementation)│ (Methodology)│  (Architecture)│
├──────────────┼──────────────┼──────────────┼──────────────┼────────────────┤
│ Statistics   │ Market       │ Python Core  │ Backtest     │ Event-Driven   │
│ Probability  │ Microstructure│ Data Stack  │ Biases       │ Architecture   │
│ Linear Algebra│ Cost Models  │ Testing      │ Overfitting  │ Design Patterns│
│ Optimization │ Risk Metrics │ Version Ctrl │ Validation   │ Modularity     │
│ Numerical    │ Regulations  │ CI/CD        │ DSR/PSR      │ Documentation  │
│ Methods      │              │              │              │                │
└──────────────┴──────────────┴──────────────┴──────────────┴────────────────┘
```

---

## 1️⃣ MATHEMATICS — The Non-Negotiable Foundations

### 1.1 Statistics & Probability (Core)

| Concept | QuantLab Application | Required Mastery Level | Source |
|---------|---------------------|------------------------|--------|
| **Descriptive Statistics** | Mean, std, skew, kurtosis of daily returns | Compute by hand + code | Mathematical Specs §3 |
| **Sampling Distributions** | Sharpe ratio distribution under H₀ | Derive asymptotic variance | López de Prado 2014 Eq. 8 |
| **Hypothesis Testing** | DSR p-value, PSR | Implement from first principles | Bailey & López de Prado 2014 |
| **Multiple Testing Correction** | DSR = correction for N trials | Understand Euler-Mascheroni γ | DSR Skill §1 |
| **Non-Normality Adjustment** | Sharpe variance with skew/kurt | Implement Eq. 30 in DSR skill | Mathematical Specs §4.2 |
| **Order Statistics** | E[max SRₙ] under null | Quantile function Φ⁻¹ usage | DSR Skill Eq. 21 |

**Hard Fact**: You **cannot** implement DSR correctly without:
- `scipy.stats.norm.ppf` (inverse CDF / quantile function)
- `scipy.stats.norm.cdf` (CDF for p-value)
- Sample skew/kurtosis via `scipy.stats.skew/kurtosis` or manual formulas

### 1.2 Linear Algebra (Minimal but Required)

| Concept | Application | Level |
|---------|-------------|-------|
| **Matrix Operations** | Covariance matrix for portfolio variance (if multi-asset) | NumPy `@` operator |
| **Eigenvalues** | Not needed for 3 single-asset strategies | Awareness only |
| **Vectorized Operations** | Pandas/NumPy broadcasting for signal generation | Daily practice |

### 1.3 Numerical Methods (Critical for Engine)

| Method | QuantLab Use | Implementation |
|--------|--------------|----------------|
| **Floating-Point Arithmetic** | Paisa-level accuracy in cost model | `decimal.Decimal` for money, NOT `float` |
| **Rounding Modes** | Banker's rounding (ROUND_HALF_EVEN) for GST | `quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)` |
| **Time Series Alignment** | Day t signal → Day t+1 Open fill | Index shifting, not interpolation |
| **Missing Data Handling** | Drop vs forward-fill decision | Drop (prevents look-ahead) |

### 1.4 Optimization (For Unit 4)

| Technique | Application | Priority |
|-----------|-------------|----------|
| **Grid Search** | 2D parameter heatmaps (SMA short×long, RSI period×threshold) | Required |
| **Walk-Forward** | Not in scope (IS/OOS is diploma equivalent) | Explicitly excluded |
| **Bayesian Optimization** | Overkill — skip | Skip |

### MATHEMATICS LEARNING CHECKLIST
```
[ ] Derive Sharpe ratio asymptotic variance with skew/kurtosis (López de Prado Eq. 8)
[ ] Implement Φ⁻¹ (ppf) and Φ (cdf) correctly for DSR
[ ] Use Python's decimal.Decimal for all monetary calculations
[ ] Understand why forward-fill creates look-ahead bias
[ ] Compute sample skew/kurtosis without scipy (for viva defensibility)
[ ] Golden master test: hand-calculate ₹10,000 round-trip → ₹9,615.19 net
```

---

## 2️⃣ FINANCE — Indian Market Microstructure & Theory

### 2.1 Indian Equity Delivery Cost Structure (EXACT — Memorize)

| Component | Buy Rate | Sell Rate | Legal Basis | QuantLab Implementation |
|-----------|----------|-----------|-------------|------------------------|
| **Brokerage** | 0.03% (cap ₹20) | 0.03% (cap ₹20) | Broker-specific, discount broker standard | `min(20, value × 0.0003)` |
| **STT** | 0.10% | 0.10% | Finance Act 2004, Sec 98 | `value × 0.0010` |
| **NSE Turnover** | 0.00345% | 0.00345% | NSE Circular 2024 | `value × 0.0000345` |
| **SEBI Turnover** | ₹10/Crore | ₹10/Crore | SEBI Act | `value × 0.000001` |
| **GST** | 18% on (Brok+Turnover) | 18% on (Brok+Turnover) | CGST Act 2017 | `(brok+turnover) × 0.18` |
| **Stamp Duty** | 0.015% | 0% (buy only) | Indian Stamp Act 2019 Rules | `value × 0.00015` (buy) |
| **Slippage (Model)** | +0.05% | -0.05% | Kissell & Glantz 2003 | `price × (1 ± 0.0005)` |

**Round-Trip Total Friction (₹1,000 × 100 shares):**
- **Buy**: ₹1,00,192.28 (cost: ₹142.28 = 0.142%)
- **Sell**: ₹1,09,807.47 (cost: ₹137.53 = 0.125%)
- **Total Drag**: ₹384.81 on ₹10,000 gross = **3.85% friction**

### 2.2 Market Microstructure Knowledge

| Concept | QuantLab Relevance | Source |
|---------|-------------------|--------|
| **Bid-Ask Spread** | Slippage model (0.05%) | Kissell & Glantz Ch. 4 |
| **Market Impact** | Proven negligible (<0.0025% participation) | `stock_universe.md` §2.1 |
| **Participation Rate** | Trade size / ADV < 0.01% | Mathematical justification |
| **Liquidity Tiers** | 10 mega-caps only (ADV > 1M shares) | Universe selection criteria |
| **Corporate Actions** | Split/dividend adjusted close | yfinance `auto_adjust=True` |
| **Trading Calendar** | 252 days/year (NSE) | CAGR annualization factor |

### 2.3 Financial Theory (Academic Grounding)

| Theory | Strategies It Informs | Key Papers |
|--------|----------------------|------------|
| **Weak-Form EMH** | Null hypothesis: no technical strategy beats buy-hold after costs | Fama 1970 |
| **Momentum Anomaly** | Strategy 3 (Jegadeesh & Titman 1993) | J&T 1993 J Finance |
| **Mean Reversion** | Strategy 2 (RSI) | Poterba & Summers 1988 |
| **Trend Following** | Strategy 1 (SMA) | Brock, Lakonishok, LeBaron 1992 |
| **Overfitting in Finance** | DSR, data snooping | Bailey & López de Prado 2014 |
| **Deflated Sharpe Ratio** | Unit 4 core novelty | López de Prado 2014 JPM |

### 2.4 SEBI Empirical Reality (Your Problem Statement Anchor)

| Statistic | Value | Source |
|-----------|-------|--------|
| **Loss-Making Traders** | 93.0% | SEBI Sep 2024 |
| **Aggregate Loss** | ₹1,81,000 Crore (FY22–24) | SEBI Sep 2024 |
| **Avg Loss/Trader/Year** | ~₹2,00,000 | SEBI Sep 2024 |
| **Profitable >₹1L** | 1.0% | SEBI Sep 2024 |
| **Intraday Cash Losses** | 71% | SEBI Jul 2024 |
| **Cost Share of Losses** | 28% | SEBI Sep 2024 |

### FINANCE LEARNING CHECKLIST
```
[ ] Recite all 7 Indian cost components with rates from memory
[ ] Hand-calculate round-trip for any (price, qty) pair
[ ] Explain why participation rate < 0.01% → zero market impact
[ ] Map each strategy to its academic anomaly paper
[ ] State null hypothesis H₀: CAGR_strat ≤ CAGR_Nifty50 after costs
[ ] Cite SEBI 2024 statistics verbatim for problem statement
[ ] Explain STT asymmetry (buy+sell) vs Stamp Duty (buy only)
```

---

## 3️⃣ PROGRAMMING — Python Implementation Mastery

### 3.1 Python Core (Non-Negotiable)

| Feature | QuantLab Usage | Mastery Required |
|---------|----------------|------------------|
| **Type Hints** | All public functions | Full annotation |
| **Dataclasses** | Order, Position, Portfolio, Signal | `@dataclass(frozen=True)` |
| **Decimal** | ALL monetary math | `from decimal import Decimal, ROUND_HALF_EVEN` |
| **Pathlib** | File paths | `Path(__file__).parent / "data"` |
| **Logging** | Engine traceability | Structured JSON logs |
| **Enum** | Signal: BUY/SELL/HOLD | `Signal(Enum)` |
| **Protocol/ABC** | Strategy interface | `class Strategy(Protocol)` |

### 3.2 Data Stack (Pandas/NumPy)

| Operation | Correct Pattern | Anti-Pattern |
|-----------|-----------------|--------------|
| **OHLCV Fetch** | `yfinance.download(tickers, start, end, auto_adjust=True)` | Manual CSV parsing |
| **Date Index** | `DatetimeIndex` with `freq='B'` (business day) | String dates |
| **Shift for Signals** | `signal.shift(1)` — Day t signal acts on Day t+1 | `signal` (look-ahead!) |
| **Rolling Windows** | `.rolling(window).mean()` — min_periods=window | Expanding windows |
| **Vectorized Math** | `df['close'].pct_change()` | Loop over rows |
| **Missing Data** | `.dropna()` — NOT `.ffill()` | Forward-fill = look-ahead |

### 3.3 Testing (Pytest — 100% Coverage Required)

| Test Type | Target | Example |
|-----------|--------|---------|
| **Unit** | CostModel golden master | `test_cost_model.py` — ₹10,000 → ₹9,615.19 |
| **Unit** | Metrics formulas | Sharpe, Sortino, MDD vs hand-calc |
| **Unit** | Strategy signals | SMA crossover on synthetic data |
| **Integration** | Engine loop | 10-day synthetic → known equity curve |
| **Property** | Determinism | Same seed → identical results |

### 3.4 Version Control & CI/CD

| Practice | QuantLab Standard |
|----------|-------------------|
| **Branching** | `main` (protected), `dev`, feature branches |
| **Commits** | Conventional: `feat:`, `fix:`, `test:`, `docs:` |
| **Pre-commit** | `ruff`, `mypy`, `pytest` |
| **CI** | GitHub Actions: lint → test → build docs |
| **Releases** | Semantic versioning `v0.1.0`, `v0.2.0` |

### PROGRAMMING LEARNING CHECKLIST
```
[ ] Write Strategy Protocol with generate_signals(price_data, params) -> pd.Series
[ ] Implement CostModel with Decimal-only arithmetic
[ ] Build event-driven loop: for day in dates: signal = strat(day); fill at next_open
[ ] Write pytest fixture for golden master cost test
[ ] Use dataclasses for Order, Position, Portfolio (frozen=True)
[ ] Set up pre-commit: ruff + mypy + pytest
[ ] NO look-ahead: signal at index i uses data ≤ i, fills at i+1
```

---

## 4️⃣ QUANT METHODOLOGY — The Research Discipline

### 4.1 Backtest Biases (The "Three Killers")

| Bias | Definition | QuantLab Structural Fix |
|------|------------|------------------------|
| **Look-Ahead** | Using future data in past decision | Event-driven: only data ≤ Day t available |
| **Overfitting** | Tuning on same data used for evaluation | Mandatory IS (2019–2022) / OOS (2023–2024) split |
| **Survivorship** | Testing only on current survivors | Acknowledged limitation; universe fixed |
| **Data Snooping** | Multiple testing without correction | DSR (Deflated Sharpe Ratio) |
| **Cost Blindness** | Zero-fee simulation | Exact Indian statutory cost model + toggle |

### 4.2 Overfitting Diagnostics (Unit 4 Core)

| Diagnostic | Formula | Implementation | Visualization |
|------------|---------|----------------|---------------|
| **In-Sample vs OOS Degradation** | `SR_OOS / SR_IS` | Compare metrics across split | Bar chart per strategy |
| **Deflated Sharpe Ratio (DSR)** | `Φ((SR_obs - E[max SR]) / σ_SR)` | `deflated_sharpe.py` | p-value heatmap |
| **Parameter Stability** | 2D grid: Sharpe(params) | `validation.py` grid search | **Heatmap (plateau vs spike)** |
| **Probabilistic Sharpe (PSR)** | `Φ((SR_obs - SR_bench) / σ_SR)` | Optional bonus | Comparison |

**DSR Implementation Requirements:**
```python
# Must implement from López de Prado 2014 exactly:
def deflated_sharpe(observed_sr: float, n_trials: int, 
                    returns: pd.Series, benchmark_sr: float = 0.0) -> float:
    # 1. Compute sample skew, kurtosis
    # 2. Asymptotic variance: (1 - skew*SR + (kurt-1)/4 * SR^2) / T
    # 3. E[max SR] = SR* + σ_SR * ((1-γ)*Φ⁻¹(1-1/N) + γ*Φ⁻¹(1-1/(N*e)))
    # 4. Z_DSR = (observed_sr - E[max]) / σ_SR
    # 5. Return Φ(Z_DSR)  ← this is the p-value
```

### 4.3 Experimental Design (Reproducibility)

| Element | QuantLab Standard |
|---------|-------------------|
| **Experiment Log** | CSV: run_id, strategy, params, universe, dates, IS/OOS, costs, metrics |
| **Matrix** | 3 strategies × 2 cost settings × 2 samples = 12 runs × 10 stocks = 120 rows |
| **Determinism** | Fixed random seeds, no hidden state, same input → same output |
| **Documentation** | Every metric formula in `mathematical_specifications.md` |

### QUANT METHODOLOGY LEARNING CHECKLIST
```
[ ] Explain look-ahead bias with code example (wrong vs right shift)
[ ] Implement DSR from scratch (no library) — viva defensibility
[ ] Generate 2D parameter heatmap for SMA (short=5-50, long=10-200)
[ ] Identify "spike" (overfit) vs "plateau" (robust) in heatmap
[ ] Run full 120-row experiment matrix automatically
[ ] Articulate why IS/OOS split dates (2019-2022 / 2023-2024) capture regime change
```

---

## 5️⃣ SOFTWARE ENGINEERING — Architecture & Delivery

### 5.1 Architecture (Four-Layer, Decoupled)

```
┌─────────────────────────────────────────────────────────────┐
│  DASHBOARD LAYER (Streamlit)                                │
│  • Cost toggle, IS/OOS selector, equity curves, heatmaps   │
└──────────────────────────┬──────────────────────────────────┘
                           │ Interface: ExperimentRunner.run()
┌──────────────────────────▼──────────────────────────────────┐
│  ANALYTICS LAYER (metrics.py, deflated_sharpe.py, validation.py)│
│  • Pure functions: compute_metrics(equity_curve) → dict     │
│  • No I/O, no state                                         │
└──────────────────────────┬──────────────────────────────────┘
                           │ Interface: BacktestEngine.run()
┌──────────────────────────▼──────────────────────────────────┐
│  ENGINE LAYER (backtest_engine.py, portfolio.py, cost_model.py)│
│  • Event loop: for day in dates: signal → order → fill → portfolio│
│  • CostModel: stateless, Decimal-only                       │
└──────────────────────────┬──────────────────────────────────┘
                           │ Interface: Strategy.generate_signals()
┌──────────────────────────▼──────────────────────────────────┐
│  STRATEGY & DATA LAYER (strategies/, data/)                 │
│  • fetch.py, clean.py, universe.py                          │
│  • SMA, RSI, Momentum — all implement Strategy Protocol     │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Design Patterns Used

| Pattern | Where | Why |
|---------|-------|-----|
| **Protocol (Interface)** | `Strategy` protocol | Swap strategies without engine changes |
| **Dataclass (DTO)** | `Order`, `Position`, `Trade` | Immutable, typed, serializable |
| **Strategy Pattern** | CostModel (could swap for US costs) | Extensible |
| **Factory** | `create_strategy(name, params)` | Dashboard dynamic loading |
| **Repository** | `DataRepository.fetch(symbol, start, end)` | Swap yfinance ↔ NSE CSV |

### 5.3 Code Quality Standards

| Standard | Tool | Configuration |
|----------|------|---------------|
| **Linting** | Ruff | `ruff check . --fix` |
| **Type Checking** | MyPy | `mypy --strict src/` |
| **Formatting** | Ruff format | `ruff format .` |
| **Testing** | Pytest | `pytest -v --cov=src --cov-fail-under=90` |
| **Pre-commit** | All above | `.pre-commit-config.yaml` |

### 5.4 Documentation (Viva-Ready)

| Document | Purpose | Audience |
|----------|---------|----------|
| **SRS** | 12 FRs, 6 NFRs, frozen before code | Evaluator |
| **Mathematical Specs** | Every formula with LaTeX | You (viva) |
| **Architecture Decision Records** | Why event-driven? Why Decimal? Why not Backtrader? | You (viva) |
| **Experiment Log** | 120-row reproducibility proof | Evaluator |
| **Code Docstrings** | Every public function | You (viva) |

### SOFTWARE ENGINEERING LEARNING CHECKLIST
```
[ ] Draw the 4-layer architecture from memory with interfaces
[ ] Write Strategy Protocol with generate_signals() method
[ ] Implement frozen dataclasses for Order, Position, Portfolio
[ ] Set up Ruff + MyPy + Pytest in pre-commit
[ ] Write ADR: "Why event-driven not vectorized?"
[ ] Write ADR: "Why Decimal not float for money?"
[ ] Write ADR: "Why from-scratch not Backtrader?"
[ ] Ensure every public function has type hints + docstring
```

---

## 🎯 INTEGRATED LEARNING PATH (MENTOR-APPROVED SEQUENCE)

### Week 1 (Aug 16–22): FOUNDATIONS — NO CODE

| Day | Mathematics | Finance | Quant Methodology |
|-----|-------------|---------|-------------------|
| 1 | Sharpe variance derivation (López de Prado) | Indian cost components (7 rates) | Three biases: look-ahead, overfitting, survivorship |
| 2 | DSR formula walkthrough (E[max SR], Φ⁻¹) | SEBI 2024 stats memorization | IS/OOS regime partitioning rationale |
| 3 | Decimal arithmetic for money | Round-trip hand calculation | Experimental matrix design (3×2×2) |
| 4 | Non-normal Sharpe variance (skew/kurt) | Market impact proof (participation rate) | Golden master test concept |
| 5 | Φ⁻¹ (ppf) and Φ (cdf) usage | Cost toggle pedagogical value | DSR as multi-testing correction |
| 6 | **SYNC: Literature Review complete** | **SYNC: Problem Statement frozen** | **SYNC: SRS drafted** |
| 7 | **SYNC: Alternative solutions matrix** | **SYNC: Architecture ADRs written** | **SYNC: Checkpoint 1 ready** |

### Week 2 (Aug 23–29): IMPLEMENTATION

| Day | Programming | Software Engg | Deliverable |
|-----|-------------|---------------|-------------|
| 1 | Data layer: fetch.py, clean.py, universe.py | Repository pattern | Data pipeline tested |
| 2 | Engine core: Order, Position, Portfolio (dataclasses) | DTO pattern | State objects immutable |
| 3 | CostModel (Decimal, golden master test) | Stateless service | `test_cost_model.py` passes |
| 4 | BacktestEngine (event loop: t signal → t+1 fill) | Event-driven arch | Deterministic 10-day test |
| 5 | 3 Strategies (SMA, RSI, Momentum) | Strategy Protocol | Signal generation tested |
| 6 | Metrics (CAGR, Sharpe, Sortino, MDD, Calmar) | Pure functions | Hand-verified formulas |
| 7 | **SYNC: 100% pytest passes** | **SYNC: Checkpoint 2 ready** | Seminar 2 demo |

### Week 3 (Aug 30–Sep 5): UNIT 4 REDESIGN — THE NOVELTY

| Day | Quant Methodology | Programming | Dashboard |
|-----|-------------------|-------------|-----------|
| 1 | Run full 120-row experiment matrix | Automated runner | — |
| 2 | **Implement DSR from scratch** | `deflated_sharpe.py` | DSR p-value display |
| 3 | **2D Parameter Grid Search** | `validation.py` | Heatmap data |
| 4 | Plateau vs Spike detection | Visualization | **Heatmap in Streamlit** |
| 5 | Profit Mirage Waterfall | Components | **Waterfall chart** |
| 6 | Cost Toggle (ON/OFF) | State management | **Interactive toggle** |
| 7 | **SYNC: 12-cell matrix + DSR + Heatmaps** | **SYNC: Checkpoint 3 ready** | Seminar 3 demo |

### Week 4 (Sep 6–11): DEFENSE

| Day | Activity | Output |
|-----|----------|--------|
| 1 | GTU Report assembly (Units 1–5) | Formal document |
| 2 | Peer cross-review (Aayush↔Meet) | Polished report |
| 3 | Viva rehearsal #1 (10 critical Qs) | Confidence |
| 4 | Viva rehearsal #2 (Cross-defense + demo) | Fluency |
| 5 | **FINAL SUBMISSION + ESE VIVA** | **100/100** |

---

## 📚 MINIMAL READING LIST (HIGH SIGNAL ONLY)

| Domain | Must-Read | Pages | Why |
|--------|-----------|-------|-----|
| **Quant Finance** | Bailey & López de Prado (2014) "Deflated Sharpe Ratio" | 14 | DSR math |
| **Quant Finance** | López de Prado (2018) *Advances in FinML* Ch. 4, 5 | ~50 | Overfitting, purged CV |
| **Market Microstructure** | Kissell & Glantz (2003) *Optimal Trading Strategies* Ch. 2, 4 | ~60 | Slippage, impact |
| **Indian Regulation** | SEBI Sep 2024 Study "Analysis of P&L of Individual Traders" | 30 | Problem statement |
| **Technical Analysis** | Brock, Lakonishok, LeBaron (1992) "Simple Technical Trading Rules" | 30 | SMA academic basis |
| **Python Quant** | VanderPlas (2016) *Python Data Science Handbook* Ch. 3 (Pandas) | 40 | Data stack mastery |
| **Testing** | Brian Okken *Python Testing with Pytest* Ch. 1–4 | 60 | Pytest proficiency |

---

## ❌ EXPLICITLY EXCLUDED (DO NOT STUDY)

| Topic | Reason |
|-------|--------|
| Options pricing (Black-Scholes, Greeks) | Not in scope — equities only |
| Portfolio optimization (Markowitz, HRP) | Single-asset strategies |
| High-frequency microstructure (LOB, HFT) | Daily bars only |
| Machine Learning for Alpha | Rule-based only per SRS |
| Walk-forward optimization | IS/OOS is diploma equivalent |
| Monte Carlo simulation | Not required for RQ1–RQ4 |
| Crypto/Forex/Futures | Indian equities only |
| Backtrader/Zipline internals | You build from scratch |
| Database systems (PostgreSQL, etc.) | CSV/Parquet files sufficient |

---

## 🎯 MENTOR'S GUIDANCE DISTILLED: "STUDY DEEPLY, NICHELY SELECT"

**Your Niche = Pedagogical Transparency of the Backtest-Reality Gap**

| What You Master Excellently | What You Explicitly Skip |
|----------------------------|-------------------------|
| Exact Indian statutory cost model | Generic % cost models |
| DSR implementation from scratch | Library-based overfitting detection |
| Event-driven engine (no look-ahead) | Vectorized convenience |
| 2D parameter heatmaps (plateau vs spike) | Single-point optimization |
| Cost toggle + Profit Mirage waterfall | Static reports |
| IS/OOS as structural feature | Manual dataframe split |
| From-scratch defensibility | Black-box wrappers |

**This is your competitive advantage:** You're not building a better backtester — you're building a **teaching tool that exposes why backtests lie**, with mathematical rigor and Indian market specificity that no other student project has.

---

## 📋 DELIVERABLES STATUS (Unit 1–2)

| Document | Path | Status |
|----------|------|--------|
| Problem Statement | `docs/01_unit1_literature/problem_statement.md` | ✅ Complete |
| Comprehensive Study | `docs/01_unit1_literature/comprehensive_study.md` | ✅ Complete |
| Mathematical Specifications | `docs/02_unit2_specifications/mathematical_specifications.md` | ✅ Complete |
| Stock Universe | `docs/02_unit2_specifications/stock_universe.md` | ✅ Complete |
| Literature Review | `docs/01_unit1_literature/literature_review.md` | ❌ Pending |
| Alternative Solutions & Feasibility | `docs/02_unit2_specifications/alternative_solutions_and_feasibility.md` | ❌ Pending |
| Formal SRS | `docs/02_unit2_specifications/srs.md` | ❌ Pending |
| **This Document** | `docs/02_unit2_specifications/QUANTLAB_DOMAIN_DEEP_DIVE.md` | ✅ Complete |

---

## 🔗 CROSS-REFERENCES

- **Execution Plan**: `docs/00_management/execution_plan.md`
- **Progress Ledger**: `docs/00_management/LEDGER.md`
- **Quant Financial Analyst Skill**: `.agents/skills/quant-financial-analyst/SKILL.md`
- **Overfitting Diagnostic Skill**: `.agents/skills/overfitting-diagnostic-specialist/SKILL.md`
- **Viva Defense Coach Skill**: `.agents/skills/viva-defense-coach/SKILL.md`

---

*This document serves as the master study contract for QuantLab. All implementation decisions must trace back to the domain requirements specified herein. No code is written until Unit 1–2 documents are frozen (Checkpoint 1, Aug 20).*