# QuantLab — Academic Progress Ledger

**Project**: QuantLab — Realistic Backtesting Engine & Overfitting Diagnostic Platform  
**Team**: Aayush Avinash Bankar (Leader) & Meet Jayeshbhai Patel  
**Timeline**: Aug 16 – Sep 11, 2026 (27 Days)  
**GTU Syllabus**: DI05000341 (Minor Project)  

---

## 📌 Task Status Legend
- ❌ Not Started
- 🔄 In Progress
- ✅ Completed
- 🐛 Blocked / Debugging

---

## Phase 1 — Unit 1 & Unit 2: Literature Study, Market Data, Alternatives & Design (Aug 16 – Aug 20)
*Target: Seminar 1 Milestone (10 Marks) — 100% Research & Academic Specifications (NO CODE)*

### Day 1 — Sun, Aug 16 (TODAY) — Foundational Research & Specifications Task Pool
*Shared Task Pool for Aayush & Meet to review, split, and complete by EOD:*

| Task ID | Task Title & Detailed Scope | Target Deliverable | Status | Assigned To |
|---|---|---|---|---|
| **D1-1** | **Literature Survey on Backtest Biases & Friction**<br>• Research & synthesize: (1) Look-Ahead Bias (Bailey et al. 2014), (2) Data Snooping / Overfitting (White 2000), (3) Survivorship Bias (Brown et al. 1992), and (4) Transaction Friction Drag (Kissell & Glantz 2003).<br>• Include formal citations, mathematical definitions of each bias, and explicit mitigation strategies for QuantLab. | `docs/01_unit1_literature/literature_review.md` | ✅ | Completed |
| **D1-2** | **SEBI 2024 Retail Trader Data Analysis & Problem Formulation**<br>• Analyze official SEBI 2023–2024 study on Indian retail traders (93% active traders losing money, ₹1.81L Cr lost).<br>• Formulate core Problem Statement, background, and formal Research Questions (RQ1: Cost Drag, RQ2: In-Sample vs Out-of-Sample Decay, RQ3: False Discovery via Multi-Testing).<br>• Define Null ($H_0$) and Alternative ($H_1$) hypotheses. | `docs/01_unit1_literature/problem_statement.md` | ✅ | Completed |
| **D1-3** | **Indian Statutory Equity Delivery Cost & Microstructure Formulation**<br>• Extract exact NSE/SEBI statutory circulars for Indian equity delivery: Brokerage (₹20 / 0.03%), STT (0.10% buy & sell), NSE Turnover (0.00345%), GST (18% on brokerage+turnover), Stamp Duty (0.015% buy), and Slippage (0.05%).<br>• Formulate complete LaTeX equations for round-trip cash flows and effective fill prices.<br>• Provide a step-by-step hand-calculated numerical example (₹1,00,000 trade) to verify paisa-level accuracy for Unit 3 testing. | `docs/02_unit2_specifications/mathematical_specifications.md` | ✅ | Completed |
| **D1-4** | **Stock Universe Selection & Benchmark Justification**<br>• Select and justify 10 liquid Indian equities across major sectors (Energy: RELIANCE, IT: TCS/INFY, Banking: HDFCBANK/ICICIBANK/SBIN, FMCG: ITC/HINDUNILVR, Infra: LT, Telecom: BHARTIARTL).<br>• Document Average Daily Volume (ADV > 1M shares) to justify zero market impact assumption.<br>• Justify `^NSEI` (Nifty 50 Index) as the benchmark for market Beta and risk-adjusted Alpha.<br>• Define In-Sample (2019–2022) vs Out-of-Sample (2023–2024) date window rationale. | `docs/02_unit2_specifications/stock_universe.md` | ✅ | Completed |

---

### Day 2 — Mon, Aug 17: Technical Strategies & Literature Review Assembly
| Task ID | Task Description | Deliverable | Status | Owner |
|---|---|---|---|---|
| D2-1 | Literature Survey: SMA Crossover (Brock 1992), RSI (Wilder 1978), Momentum (Jegadeesh 1993) | Strategy theory notes | ✅ | Completed |
| D2-2 | Comprehensive Literature Review Assembly | `docs/01_unit1_literature/literature_review.md` complete | ✅ | Completed |
| D2-3 | Problem Statement & Objectives Document Finalization | `docs/01_unit1_literature/problem_statement.md` complete | ✅ | Completed |

---

### Day 3 — Tue, Aug 18: Unit 2 Alternatives & Feasibility Study
| Task ID | Task Description | Deliverable | Status | Owner |
|---|---|---|---|---|
| D3-1 | Alternative Architecture Matrix (Event-Driven vs Vectorized) | Architecture tradeoff table | ✅ | Completed |
| D3-2 | Alternative Tool Tradeoff Matrix (Custom vs Backtrader/Lean/Vectorbt) | Tool comparison matrix | ✅ | Completed |
| D3-3 | Zero-Budget Hardware & Compute Feasibility Analysis | `docs/02_unit2_specifications/alternative_solutions_and_feasibility.md` | ✅ | Completed |

---

### Day 4 — Wed, Aug 19: Unit 2 Formal SRS & Mathematical Contracts
| Task ID | Task Description | Deliverable | Status | Owner |
|---|---|---|---|---|
| D4-1 | Formal Software Requirements Specification (SRS) (12 FRs + 6 NFRs) | `docs/02_unit2_specifications/srs.md` | ✅ | Completed |
| D4-2 | LaTeX Formulations for Metrics (Sharpe, DSR, Sortino, Calmar, Drawdown) | `docs/02_unit2_specifications/mathematical_specifications.md` complete | ✅ | Completed |
| D4-3 | In-Sample / Out-of-Sample Partitioning Design Specification | Split date contract | ✅ | Completed |

---

### Day 5 — Thu, Aug 20 — 🔄 CHECKPOINT 1 (Seminar 1 Milestone - 10 Marks)
| Checkpoint Verification Item | Status | Verification Method |
|---|---|---|
| Literature Review & Problem Statement fully documented | ✅ | Review `docs/01_unit1_literature/literature_review.md` & `problem_statement.md` |
| Alternatives & Feasibility Study approved | ✅ | Review `docs/02_unit2_specifications/alternative_solutions_and_feasibility.md` |
| Formal SRS and Mathematical Specifications frozen | ✅ | Review `docs/02_unit2_specifications/srs.md` & `mathematical_specifications.md` |
| Seminar 1 presentation slide deck ready | ✅ | Review `docs/05_unit5_defense/faculty_presentation_deck.md` |

---

## Phase 2 — Unit 3: Implementation, Simulation & Testing (Aug 21 – Aug 28)
*Target: Seminar 2 Milestone (10 Marks)*

| Day | Task Summary | Deliverable | Status |
|---|---|---|---|
| Day 6 (Aug 21) | Scaffolding, deps, `fetch.py` | `src/data/fetch.py` | ✅ |
| Day 7 (Aug 22) | Data cleaner & universe module | `src/data/clean.py`, `src/data/universe.py` | ✅ |
| Day 8 (Aug 23) | Events, Order, Position classes | `src/engine/events.py`, `order.py`, `position.py` | ✅ |
| Day 9 (Aug 24) | Indian CostModel & Portfolio | `src/engine/cost_model.py`, `portfolio.py` | ✅ |
| Day 10 (Aug 25) | Zero Look-Ahead Event Loop (t+1 Open fills) | `src/engine/backtest_engine.py` | ✅ |
| Day 11 (Aug 26) | 3 Strategies (SMA, RSI, Momentum) | `src/strategies/` modules | ✅ |
| Day 12 (Aug 27) | Analytics & Metrics Engine | `src/analytics/metrics.py` | ✅ |
| Day 13 (Aug 28) | **🔄 CHECKPOINT 2 (Seminar 2 Milestone)** | 100% Pytest suite passing green | ✅ |

---

## Phase 3 — Unit 4: Modification & Redesign Based on Results (Aug 29 – Sep 04)
*Target: Seminar 3 Milestone (10 Marks) — Unit 4 Redesign*

| Day | Task Summary | Deliverable | Status |
|---|---|---|---|
| Day 14 (Aug 29) | Full IS vs OOS Backtest Matrix | Isolate parameter decay & cost friction | ❌ |
| Day 15 (Aug 30) | **Unit 4 Redesign**: Deflated Sharpe Ratio (DSR) | `src/analytics/deflated_sharpe.py` | ❌ |
| Day 16 (Aug 31) | **Unit 4 Redesign**: 2D Stability Surfaces | `src/analytics/validation.py` | ❌ |
| Day 17 (Sep 01) | Streamlit Master Dashboard App | `src/dashboard/app.py` | ❌ |
| Day 18 (Sep 02) | "Profit Mirage" Waterfall & 2D Heatmaps | `src/dashboard/components.py` | ❌ |
| Day 19 (Sep 03) | Automated Experiment Matrix Logger | `experiments/experiment_log.csv` | ✅ |
| Day 20 (Sep 04) | **🔄 CHECKPOINT 3 (Seminar 3 Milestone)** | 12-cell matrix complete, Unit 4 redesign demonstrated | ❌ |

---

## Phase 4 — Unit 5: Final Report Assembly, Viva Preparation & ESE Defense (Sep 05 – Sep 11)
*Target: Seminar 4 (20 Marks) & GTU ESE Viva (50 Marks) — Total 70 Marks*

| Day | Task Summary | Deliverable | Status |
|---|---|---|---|
| Day 21 (Sep 05) | Comprehensive Project Report Outline | `docs/final_report_draft.md` | ❌ |
| Day 22 (Sep 06) | Empirical Results, Tables & Discussion | Report results section | ❌ |
| Day 23 (Sep 07) | Assemble Complete GTU Report (Units 1–5) | Formal GTU project documentation | ❌ |
| Day 24 (Sep 08) | Peer Cross-Review & Proofreading | Final code & report polish | ❌ |
| Day 25 (Sep 09) | Viva Voce Defense Rehearsal #1 | 10 critical viva questions | ❌ |
| Day 26 (Sep 10) | Viva Voce Defense Rehearsal #2 | Cross-defense & live demo dry-run | ❌ |
| Day 27 (Sep 11) | **🎯 FINAL SUBMISSION & ESE VIVA** | 100/100 Distinction Defense | ❌ |

---

## Change Log
| Date | Change Summary | Author |
|---|---|---|
| Aug 16, 2026 | Refined Day 1 study tasks with deep, unambiguous scope and deliverables. Removed internal agent configuration tasks from student project ledger. | Aayush & Meet |
