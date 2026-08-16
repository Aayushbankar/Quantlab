# QuantLab — Academic Master Execution Plan

**Project**: QuantLab: Realistic Backtesting & Overfitting Diagnostic Platform for Indian Equities  
**Timeline**: August 16 → September 11, 2026 (27 days)  
**GTU Syllabus Code**: DI05000341 (Minor Project - 5th Semester)  
**Team**: Aayush Avinash Bankar (Group Leader) & Meet Jayeshbhai Patel  
**Standard**: 100/100 Distinction in GTU Seminars 1–4 & ESE External Viva  

---

## 1. The Core Academic Principle: Study Before Code

In accordance with GTU Syllabus DI05000341 and academic engineering standards, **no implementation code is written until Unit 1 (Literature Survey & Problem Identification) and Unit 2 (Alternative Solutions, Feasibility & System Design) are completed and documented**.

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                      GTU DI05000341 SYLLABUS GATING                            │
├────────────────────────────────┬───────────────────────────────────────────────┤
│ Unit 1: Literature Review      │ Survey existing papers, identify biases,      │
│ & Problem Identification       │ analyze SEBI 2024 data, define problem.       │
│ (Seminar 1 — 10 Marks)         │ 🚫 NO CODE WRITTEN (Aug 16–18)                │
├────────────────────────────────┼───────────────────────────────────────────────┤
│ Unit 2: Alternative Solutions  │ Compare Vectorized vs Event-driven, custom vs │
│ & System Design                │ Backtrader, formalize SRS & Indian tax math.  │
│ (Seminar 2 — 10 Marks)         │ 🚫 NO CODE WRITTEN (Aug 18–20)                │
├────────────────────────────────┼───────────────────────────────────────────────┤
│ Unit 3: Implementation,        │ Build from-scratch Python engine, 3 strats,   │
│ Simulation & Testing           │ Indian CostModel, Pytest 100% test suite.     │
│ (Seminar 3 — 10 Marks)         │ 💻 CODE & UNIT TESTING (Aug 21–28)            │
├────────────────────────────────┼───────────────────────────────────────────────┤
│ Unit 4: Modification &         │ Diagnose out-of-sample decay, redesign with   │
│ Redesign Based on Results      │ Deflated Sharpe Ratio (DSR) & Heatmaps.       │
│ (Seminar 3/4 Rubric)           │ 🔬 EMPIRICAL REDESIGN (Aug 29–Sep 04)         │
├────────────────────────────────┼───────────────────────────────────────────────┤
│ Unit 5: Defense, Final Report  │ Streamlit UI Demo, GTU Comprehensive Final    │
│ & ESE Viva Voce                │ Project Report, Viva Cross-Defense.           │
│ (Seminar 4 + ESE — 70 Marks)   │ 🎓 ACADEMIC DEFENSE (Sep 05–11)               │
└────────────────────────────────┴───────────────────────────────────────────────┘
```

---

## 2. Day-by-Day Academic Phase Breakdown

### Phase 1 — Unit 1 & Unit 2: Literature Study, Market Data, Alternatives & Design (Aug 16 – Aug 20)
*Target: Seminar 1 Milestone (10 Marks) — 100% Research & Academic Specifications (NO CODE)*

- **Day 1 (Sun, Aug 16 - TODAY)**:
  - **Task D1-1**: Academic Literature Survey on Backtest Biases (Look-Ahead, Overfitting, Survivorship, Cost Friction). Deliverable: `docs/literature_review.md`.
  - **Task D1-2**: Empirical Market Grounding & Problem Statement (SEBI 2024 ₹1.81L Cr Retail Loss Data Analysis). Deliverable: `docs/problem_statement.md`.
  - **Task D1-3**: Indian Statutory Equity Delivery Cost & Microstructure Formulation (STT, GST, Stamp Duty, Slippage Math). Deliverable: `docs/mathematical_specifications.md`.
  - **Task D1-4**: Stock Universe Selection & Benchmark Justification (10 Diverse NSE Equities + Nifty 50 Benchmark). Deliverable: `docs/stock_universe.md`.
- **Day 2 (Mon, Aug 17)**:
  - Technical Strategies Literature Survey: SMA Crossover (Brock 1992), RSI (Wilder 1978), Momentum (Jegadeesh 1993).
  - Assemble Complete Unit 1 Literature Review Document in `docs/literature_review.md`.
  - Finalize Formal Research Hypotheses ($H_0$ and $H_1$) in `docs/problem_statement.md`.
- **Day 3 (Tue, Aug 18)**:
  - Unit 2 Alternative Solutions Matrix: Event-Driven vs Vectorized; Custom From-Scratch vs Backtrader/Lean/Vectorbt (tradeoff analysis).
  - Feasibility & Hardware Constraints: Zero-cost budget, student laptop compute, free public data sources.
  - Draft `docs/alternative_solutions_and_feasibility.md`.
- **Day 4 (Wed, Aug 19)**:
  - Unit 2 Formal SRS: 12 Functional Requirements (FR-1 to FR-12) & 6 Non-Functional Requirements (NFR-1 to NFR-6) in `docs/srs.md`.
  - LaTeX Metric Formulations: Sharpe, Sortino, Calmar, Max Drawdown, and López de Prado's Deflated Sharpe Ratio (DSR) in `docs/mathematical_specifications.md`.
  - In-Sample (2019–2022) vs Out-of-Sample (2023–2024) Date Partitioning Design.
- **Day 5 (Thu, Aug 20) — 🔄 SYNC CHECKPOINT 1 (Seminar 1 Milestone - 10 Marks)**:
  - Review all Unit 1 & Unit 2 academic documents.
  - Slide deck prepared for GTU Seminar 1 presentation.
  - **Academic Design Contracts Frozen** — Ready for Unit 3 implementation.

---

### Phase 2 — Unit 3: Implementation, Simulation & Unit Testing (Aug 21 – Aug 28)
*Target: Seminar 2 Milestone (10 Marks) — From-Scratch Python Engine & Strategies*

- **Day 6 (Fri, Aug 21)**: Scaffolding, `requirements.txt`, `.gitignore`, and Data Fetcher `src/data/fetch.py`.
- **Day 7 (Sat, Aug 22)**: Data Cleaner `src/data/clean.py` & Universe `src/data/universe.py`.
- **Day 8 (Sun, Aug 23)**: Core Events `src/engine/events.py`, `src/engine/order.py`, `src/engine/position.py`.
- **Day 9 (Mon, Aug 24)**: Indian Statutory Cost Model `src/engine/cost_model.py` & Portfolio `src/engine/portfolio.py`.
- **Day 10 (Tue, Aug 25)**: Core Event Simulation Loop `src/engine/backtest_engine.py` (Day $t$ Close signal $\rightarrow$ Day $t+1$ Open execution).
- **Day 11 (Wed, Aug 26)**: 3 Strategies (`src/strategies/sma_crossover.py`, `rsi_mean_reversion.py`, `momentum.py`).
- **Day 12 (Thu, Aug 27)**: Metrics Engine `src/analytics/metrics.py` (CAGR, Sharpe, Sortino, Drawdown, Win Rate).
- **Day 13 (Fri, Aug 28) — 🔄 SYNC CHECKPOINT 2 (Seminar 2 Milestone)**:
  - Full Pytest suite (`test_data.py`, `test_cost_model.py`, `test_engine.py`, `test_strategies.py`, `test_metrics.py`) passing 100%.
  - Seminar 2 presentation slides ready.

---

### Phase 3 — Unit 4: Modification & Redesign Based on Results (Aug 29 – Sep 04)
*Target: Seminar 3 Milestone (10 Marks) — Empirical Redesign with DSR & Stability Surfaces*

- **Day 14 (Sat, Aug 29)**: Run full In-Sample (2019–2022) vs Out-of-Sample (2023–2024) matrix; isolate parameter failure & cost drag.
- **Day 15 (Sun, Aug 30)**: **Unit 4 Redesign Module 1**: Implement Marcos López de Prado's Deflated Sharpe Ratio (`src/analytics/deflated_sharpe.py`).
- **Day 16 (Mon, Aug 31)**: **Unit 4 Redesign Module 2**: 2D Parameter Stability Grid Search (`src/analytics/validation.py`).
- **Day 17 (Tue, Sep 01)**: Streamlit Dashboard Core & Interactive Controls (`src/dashboard/app.py`).
- **Day 18 (Wed, Sep 02)**: "Profit Mirage" Waterfall Breakdown & Parameter Stability Heatmaps in Streamlit.
- **Day 19 (Thu, Sep 03)**: Automated Reproducibility Logger (`experiments/experiment_log.csv`) generating complete 12-cell matrix across 10 stocks.
- **Day 20 (Fri, Sep 04) — 🔄 SYNC CHECKPOINT 3 (Seminar 3 Milestone)**:
  - Unit 4 Redesign documented: how DSR and stability heatmaps solve false-positive parameter traps.
  - Complete 12-cell matrix rendered in dashboard and logged.

---

### Phase 4 — Unit 5: Final Report Assembly, Viva Preparation & ESE Defense (Sep 05 – Sep 11)
*Target: Seminar 4 (20 Marks) & GTU ESE Viva (50 Marks) — Total 70 Marks*

- **Day 21 (Sat, Sep 05)**: GTU Comprehensive Project Report Structure & Chapter Outlines (`docs/final_report_draft.md`).
- **Day 22 (Sun, Sep 06)**: Empirical Results, Tables, Charts & Discussion synthesis into Report.
- **Day 23 (Mon, Sep 07)**: Assemble Complete GTU Report (Chapters 1 to 7: Problem, SRS, Design, Implementation, Testing, Unit 4 Redesign, Conclusion).
- **Day 24 (Tue, Sep 08)**: Peer Cross-Review & Proofreading (Aayush reviews Engine/Math; Meet reviews Data/Strategies/Results).
- **Day 25 (Wed, Sep 09)**: Viva Voce Defense Rehearsal #1 (10 critical questions using `viva-defense-coach`).
- **Day 26 (Thu, Sep 10)**: Viva Voce Defense Rehearsal #2 (Cross-Subsystem Defense & Live Demo Dry-Run).
- **Day 27 (Fri, Sep 11) — 🎯 FINAL SUBMISSION & EXTERNAL ESE VIVA**:
  - Full project submission, live software demonstration, final viva defense.
