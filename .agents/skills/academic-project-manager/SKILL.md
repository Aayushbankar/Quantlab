---
name: academic-project-manager
description: >-
  Academic and Engineering Project Manager for GTU DI05000341 Minor Project.
  Enforces strict phase gating: mandates exhaustive Unit 1 (Literature Review & Problem Identification)
  and Unit 2 (Alternative Solutions, Feasibility & System Design) research and documentation
  BEFORE any coding in Unit 3 (Implementation & Testing), Unit 4 (Modification/Redesign),
  and Unit 5 (Final Defense & Academic Paper).
---

# Academic & Engineering Project Manager (GTU DI05000341)

This skill governs the end-to-end execution of engineering projects following academic university standards (specifically GTU Minor Project syllabus DI05000341). It ensures that no team rushes prematurely into coding without completing formal academic study, literature reviews, mathematical specifications, and architectural design contracts.

## The 5-Unit Phase Gating Framework

```mermaid
graph TD
    U1["Unit 1: Literature Review & Problem Identification (Seminar 1)<br/>• Exhaustive literature study (López de Prado, White, Kissell, Brock)<br/>• Real-world data analysis (SEBI 2024 report)<br/>• Formal Problem Statement & Objectives<br/>🚫 NO CODE WRITTEN HERE"]
    U2["Unit 2: Alternative Solutions & System Design (Seminar 2)<br/>• Tradeoff matrix (Event-Driven vs Vectorized; Custom vs Backtrader)<br/>• Budget, feasibility & hardware constraints<br/>• Formal SRS, State Machine & Indian Tax Mathematical Specs<br/>🚫 NO CODE WRITTEN HERE"]
    U3["Unit 3: Implementation, Simulation & Testing (Seminar 3)<br/>• Python Event Engine, Indian CostModel, 3 Strategies<br/>• 100% Pytest test suite (Zero look-ahead, cash invariants)<br/>• In-Sample vs Out-of-Sample simulation execution"]
    U4["Unit 4: Modification & Redesign Based on Results (Seminar 3/4)<br/>• Document out-of-sample decay & cost drag failures<br/>• Redesign with Deflated Sharpe Ratio (DSR) & Parameter Heatmaps<br/>• Prove iterative engineering improvement"]
    U5["Unit 5: Final Defense, Academic Paper & ESE Viva (Seminar 4 & ESE)<br/>• Interactive Streamlit Demonstration<br/>• IEEE-Standard Research Paper Writeup<br/>• GTU Comprehensive Final Project Report & Viva Rehearsal"]

    U1 --> U2 --> U3 --> U4 --> U5
```

---

## Strict Rules of Engagement

1. **Gate 1 Approval**: Do not write single implementation code files until `docs/literature_review.md`, `docs/srs.md`, and `docs/mathematical_specifications.md` are completely drafted, reviewed, and cited.
2. **Deterministic Mathematical Formulas**: Every metric (Sharpe, DSR, Sortino, Drawdown) and every statutory fee (STT, GST, Stamp Duty, Exchange Turnover, Slippage) must have its exact LaTeX equation documented in the project specs before implementation.
3. **Traceability**: Every code function in Unit 3 must trace directly back to a functional requirement (FR) in the SRS from Unit 2.
4. **Unit 4 Redesign Rule**: The project MUST document what broke during testing and how the architecture was modified/redesigned to fix it (satisfying GTU Syllabus Unit 4 rubrics).
5. **Shared Task Pools**: Maintain transparent daily task pools for team members (Aayush & Meet) to ensure equal distribution of intellectual study, documentation, engineering, and viva preparation.
