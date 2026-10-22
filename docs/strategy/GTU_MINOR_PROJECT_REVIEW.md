# GTU Minor Project Audit — QuantLab (DI05000341)

**Auditor role:** Senior GTU Project Evaluation Committee Auditor & Technical Mentor
**Date of audit (UTC):** 2026-10-15
**Scope:** Current working directory `/mnt/work/projects/Quantlab` — read-only audit; only this report file was created/modified.
**Standard:** GTU Diploma Minor Project DI05000341, 5th semester, w.e.f. 2026-27 (`DI05000341.pdf`, 12 pages, verified on disk).
**Submission:** Government Polytechnic-Gandhinagar Sem-5 timetable — **Minor Project (DI05000341) submission: 26/10/2026, 10:30 AM onwards, Respective Group Faculty** (user-confirmed 2026-10-15; no seminar marks received to date).
**Countdown at update:** **11 days** (Oct 15 → Oct 26). All forecasts below are pure predictions; the Action Plan (§12) is re-phased to this 11-day window. *Report updated 2026-10-15 on user input.*
**Note on sub-point count:** The audit brief states "all 31 sub-points". The official syllabus on disk actually contains **34 sub-points** (Unit 1: 1.1–1.4 = 4; Unit 2: 2.1–2.11 = 11; Unit 3: 3.1–3.7 = 7; Unit 4: 4.1–4.5 = 5; Unit 5: 5.1–5.7 = 7). This report covers **all 34**.

---

## 1. Executive Summary

**Verdict in 3 sentences:** QuantLab is a genuine, working, from-scratch event-driven backtesting engine for Indian equities with unusually strong Unit 1–2 documentation and a verified 9/9 green pytest suite — technically the strongest diploma software prototype this auditor has seen on disk this semester. However, it is **not defense-ready today**: there is zero evidence of real-market data runs (`data/raw/` and `experiments/experiment_log.csv` are absent), the git history shows only **one** contributor for a **two-person** team, and the mandatory Unit 5 formalities (PPTX, department-format report with certificate/declaration/acknowledgements/reflections, safety note, SSIP/patent record, title-originality check) are missing or thin. Predicted CA today is **34/50** with **High** near-term risk; closing the 6 critical gaps below can realistically lift the project to 44+/50 and an A grade.

---

## 2. Project Profile

| Field | Finding | Evidence |
|---|---|---|
| **Title** | QuantLab: A Realistic Backtesting Engine & Overfitting Diagnostic Platform for Indian Equities | `README.md:1`, `docs/01_unit1_literature/problem_statement.md:3` |
| **Branch** | Computer Engineering (software) | Python/Streamlit stack; LaTeX report; no hardware scope |
| **Course** | GTU DI05000341, Semester 5 Minor Project | `README.md:3`, `QuantLab_Project_Documentation.md:4` |
| **Project type** | (vii) Development of process/software/application to solve a complex problem + (v) application of emerging technology (syllabus scope §p7–8) | Working simulation + DSR/CPCV methodology |
| **Hardware vs software** | Pure software; no firmware/microcontroller | `src/` is 100% Python; no Arduino/ESP/AVR code found |
| **Tech stack** | Python 3.11, pandas 2.2.2, numpy 1.26.4, matplotlib 3.8.4, plotly 5.20.0, streamlit 1.33.0, pytest 8.1.1, yfinance 0.2.37 (+ scipy imported but **missing** from requirements — see CONS) | `requirements.txt`, `src/analytics/deflated_sharpe.py:3` |
| **Architecture** | 4-layer decoupled: Dashboard → Analytics → Engine → Data/Strategies | `docs/02_unit2_specifications/system_architecture.md`, `QuantLab_Project_Documentation.md:120-148` |
| **Team (on paper)** | 2 students: Aayush Avinash Bankar (246230316006, Leader) + Meet Jayeshbhai Patel (246230316133) | `QuantLab_Project_Documentation.md:6-9` |
| **Team (on disk)** | **1 git contributor only**: `aayushbankar <aayushbankar42@gmail.com>` × 29 commits | `git shortlog -sne HEAD` → 29 / 0 split |
| **Apparent stage** | Late **Testing / Redesign**, entering **Documentation** — NOT defense-ready | Code + tests done; `experiments/` empty; report drafts thin; no PPTX |
| **Code size** | ~1,008 LOC `src/` (excl. pycache) across 18 modules; ~2,011 LOC incl. tests + scripts | `wc -l` audit, 2026-10-15 |
| **Tests** | 9 pytest tests, **9/9 PASS** (verified by re-run during audit) | `tests/`, `.pytest_cache` |
| **Docs volume** | 23 markdown docs; 3 compiled LaTeX PDFs (Thesis ~1.1 MB, Master Report ~662 KB, Completion Report ~113 KB); 7 PNG charts | `docs/` tree |
| **Work history** | 29 commits, 2026-08-14 → 2026-08-31 (17 days, day-wise Day 6–19 plan); **no commits after Aug 31** — ~6.5-week silence to audit date | `git log --oneline --stat` |
| **Branches** | `main`, `feat/v2-architecture` (active, audited), `feat/antigravity-implementation`, `origin/meet` (empty/unmerged — never inspected by auditor) | `git branch -a` |
| **License** | Apache 2.0 | `LICENSE` |

---

## 3. Current State Assessment

**Unit position:** Unit 1 complete. Unit 2 substantially complete (minus safety + real-data evidence). Unit 3 implementation + unit testing complete (minus real-data end-to-end proof). Unit 4 redesign substantially complete in code (DSR, CPCV+embargo, Almgren-Chriss, O(1) slicing) but **undocumented in `docs/03_unit3_testing/` and `docs/04_unit4_redesign/` — both directories are EMPTY**. Unit 5 ~40%: thesis PDFs exist but chapters are stubs, no PPTX, no certificate/acknowledgement/reflections.

**Overall completion: ~70%** (weighted — see Metrics Dashboard).

Key evidence anchors:

- Strongest artifacts: `docs/01_unit1_literature/problem_statement.md` (SEBI-grounded RQs + H₀/H₁), `docs/01_unit1_literature/literature_review.md` (14 refs), `docs/02_unit2_specifications/mathematical_specifications.md` (golden-master paisa example), `src/engine/backtest_engine.py`, `src/analytics/cpcv.py`, `src/analytics/deflated_sharpe.py`.
- Weakest points: `experiments/` (empty — FR-12 reproducibility log never generated), `data/raw/` (absent — pipeline never run on disk), `docs/03_unit3_testing/` + `docs/04_unit4_redesign/` (empty), `docs/final_report_draft.md` (24 lines), `docs/chapters/chapter1-6.tex` (5–27 lines each, stubs), no `.pptx`, single-author git.

---

## 4. Full Unit-wise Checklist (all 34 syllabus sub-points)

Status key: **Done** = evidence on disk · **Partial** = exists but incomplete/inconsistent · **Pending** = planned, not started · **Missing** = no evidence and not planned · **Cannot-verify** = inherently off-disk (meetings, viva performance).

### Unit 1 — Review literature / identify problems (12 h, 14%)

| # | Syllabus sub-point | Status | Evidence / remark |
|---|---|---|---|
| 1.1 | Survey research papers, books, websites; industry visit if necessary | **Done** | `docs/01_unit1_literature/literature_review.md` (14 refs: Bailey, White, Brock, Kissell…), `comprehensive_study.md`, `QUANTLAB_DOMAIN_DEEP_DIVE.md`. No industry-visit record [ASSUMED not done — no penalty for software] |
| 1.2 | Identify problem related to specific branch | **Done** | "Three Silent Killers" (cost blindness, overfitting, look-ahead) framed for Computer/quant-software branch — `problem_statement.md:51-94` |
| 1.3 | Identify and gather information on selected problem | **Done** | SEBI Sep 2024 (93%, ₹1.81L Cr) + SEBI Jul 2024 cash study (71%); NSE rate card; universe ADV data — `problem_statement.md:28-48`, `stock_universe.md` |
| 1.4 | Make appropriate problem statement and abstract (with guide) | **Done** | Formal problem statement + executive summary + RQ1–RQ4 + H₀/H₁ — `problem_statement.md:96-125`. Standalone "Abstract" page exists only inside thesis PDFs — accepted as Done |

### Unit 2 — Select solution: budget + methodology (18 h, 20%)

| # | Syllabus sub-point | Status | Evidence / remark |
|---|---|---|---|
| 2.1 | Collect relevant data from various sources | **Partial** | Universe + fetch pipeline defined (`src/data/universe.py`, `src/data/fetch.py`, IS/OOS partition). BUT: no data on disk — `data/` dir absent, `experiments/` empty. Collection is specified, not evidenced |
| 2.2 | Analyze collected data to understand problem, identify solutions | **Partial** | SEBI-data analysis is excellent. Own-market-data analysis: **no notebook/CSV/analysis artifact on disk** |
| 2.3 | Use charts, graphs, simulations to evaluate methods | **Partial** | 7 PNGs in `docs/charts/` + `scripts/generate_*_charts.py`. Filenames say "simulated" (`simulated_equity_curve.png`); real-data provenance unverified |
| 2.4 | Compare different methods for solving problem | **Done** | Event-driven vs vectorized matrix + 6-tool comparison (Backtrader/Lean/Zipline/Vectorbt/TradingView) — `alternative_solutions_and_feasibility.md:42-79` |
| 2.5 | Consider alternative approach if chosen solution ineffective | **Partial** | V2 redesign IS an alternative-approach pivot (documented in Completion Report). No guide-feedback-driven pivot recorded [ASSUMED none needed] |
| 2.6 | Assess financial implications and feasibility | **Done** | 4-dimensional feasibility matrix; ₹0.00 budget — `alternative_solutions_and_feasibility.md:84-112` |
| 2.7 | Evaluate/compare methods considering financial viability | **Partial** | Viability argument is "everything is free" — true but trivial; no comparative costing table (e.g., cloud/data-feed options costed and rejected) |
| 2.8 | Select appropriate machines/equipment/instruments/software | **Done** | Student laptop target, full stack pinned in `requirements.txt` |
| 2.9 | Ensure safety considerations prioritized in planning | **Missing** | Zero occurrences of "safety" in project docs (only in the word "Safety" of the syllabus PDF itself). Software-safety equivalent (no-advice disclaimer, data-risk note) exists informally in `README.md:18-20` but no explicit Safety section — **Critical gap for rubric** |
| 2.10 | Seek continuous guidance from guide/mentors/experts | **Cannot-verify** | No meeting log on disk. `LEDGER.md` tracks tasks, not guide interactions |
| 2.11 | Prepare structured work plan | **Done** | `docs/00_management/execution_plan.md` (27-day gated plan) + `LEDGER.md` |

### Unit 3 — Procure / implement / test (20 h, 22%)

| # | Syllabus sub-point | Status | Evidence / remark |
|---|---|---|---|
| 3.1 | Select components/equipment as per specifications | **Done** | All FR-1–FR-12 modules implemented: `src/data/`, `src/engine/` (6 files), `src/strategies/` (3 + base), `src/analytics/` (4), `src/dashboard/` (2) |
| 3.2 | Prepare cost estimate | **Partial** | Statutory per-trade rate card is rigorous, but there is **no project cost-estimate sheet** (hardware/software/data/hosting/printing line items, even if ₹0) |
| 3.3 | Distribute tasks among members by skill | **Partial** | Owner matrix exists (`QuantLab_Project_Documentation.md:203-215`, Master Bible team contract). Git shows 100/0 contribution split — distribution is **claimed, not evidenced** |
| 3.4 | Work consistently to achieve targets | **Done** | 29 commits over 17 days following the Day 6–19 plan; `git log` matches `LEDGER.md` checkpoints 1–3 |
| 3.5 | Test system/model/process as applicable | **Done** | 9/9 pytest PASS (re-verified 2026-10-15): zero-look-ahead, sizing, cost model, metrics, momentum guard, portfolio, CPCV×3 |
| 3.6 | Verify and modify program/parameters if necessary | **Done** | Adversarial-audit patch commit `f2b7c3d` (DSR scaling, Sortino, PnL), MTM/cash-fixes `9a310eb`, CPCV embargo `bfadca7` |
| 3.7 | Complete remaining implementation activities | **Partial** | Engine + analytics complete; dashboard is MVP-only (no DSR/heatmap/waterfall wiring — see CONS); experiment matrix never executed on disk |

### Unit 4 — Modify / redesign from test results (20 h, 22%)

| # | Syllabus sub-point | Status | Evidence / remark |
|---|---|---|---|
| 4.1 | Design the final layout | **Partial** | 4-layer architecture frozen = software "layout", but no explicit final-layout freeze note |
| 4.2 | Arrange sections/parts logically | **Done** | Zero circular imports; headless engine runs without Streamlit (`NFR-3`); clean `src/` map |
| 4.3 | Fabricate/construct final model per industry standards if possible | **Partial** | No lint/type config (`ruff`/`mypy` referenced in docs but absent on disk); no CI. Code itself is clean and idiomatic |
| 4.4 | Modify components based on earlier observations | **Done** | Four genuine redesigns: (1) cash→total-equity sizing, (2) O(1) slicing, (3) flat slippage→Almgren-Chriss, (4) CPCV embargo (PBO 28.89%→37.78% on AR(1) test) |
| 4.5 | Modify program/parameters based on findings | **Done** | `deflated_sharpe.py` + `validation.py` (2D grid) + duplicate-BUY guards; all covered by tests |

### Unit 5 — Defend: deliverables + report + presentation (20 h, 22%)

| # | Syllabus sub-point | Status | Evidence / remark |
|---|---|---|---|
| 5.1 | Each student works independently on allocated tasks | **Cannot-verify** | Single-author git; `origin/meet` branch exists but is empty/unmerged. Viva cross-defense is the only remedy |
| 5.2 | Report per department format | **Partial** | 3 LaTeX PDFs compile (Thesis/Completion/Master). BUT: `chapters/*.tex` are stubs; `final_report_draft.md` is 24 lines; no certificate, declaration, acknowledgement, reflection pages found. Department-format compliance **Cannot-verify** — collect the format |
| 5.3 | PPT prepared and presented per schedule | **Partial** | `faculty_presentation_deck.md`: 12 slides + speaker notes + viva cheat sheet — good content, but **no `.pptx`** and first deck is dated for Unit 1–2 milestone only |
| 5.4 | Reflect on experiences in report/presentation | **Missing** | No reflections section found anywhere |
| 5.5 | Acknowledge expert contributions | **Missing** | No acknowledgements section found |
| 5.6 | Incorporate guide/evaluation-team suggestions | **Cannot-verify** | No seminar feedback log on disk |
| 5.7 | Respond confidently to questions in seminars | **Cannot-verify** | Strong viva-prep artifacts (adversarial doc, WWWH bible, defense boxes in thesis) predict readiness, but performance is off-disk |

**Tally:** Done 17 · Partial 11 · Missing 3 (2.9, 5.4, 5.5) · Cannot-verify 4 (2.10, 5.1, 5.6, 5.7) · Pending 0. (34 total; the "31" in the brief undercounts the syllabus.)

---

## 5. Course Outcome Mapping

| CO | Statement (syllabus) | Status | Evidence |
|---|---|---|---|
| CO1 (R,A) | Review literature/system to identify problems | **Achieved** | `literature_review.md` + `problem_statement.md` + SEBI grounding + 14 refs |
| CO2 (U,A) | Select most appropriate solution considering budget & methodology | **Achieved** (minor deduction: safety) | Tool/architecture matrices + ₹0 feasibility + SRS FR-1–12/NFR-1–6; safety note missing |
| CO3 (A) | Initiate development — procure, implement, test | **Partial** → near-Achieved | Engine + 3 strategies + 9/9 tests green; held back by no real-data run on disk |
| CO4 (A) | Modify/redesign based on testing results | **Achieved** | 4 documented redesigns with tests (sizing, O(1), Almgren-Chriss, embargo) |
| CO5 (R,A) | Defend final review with deliverables, report, presentation | **Not achieved (yet)** | Prototype runs; report/PPT/acknowledgement/reflection formalities incomplete |

---

## 6. Rubric-Based Mark Prediction (strict, committee-style, TODAY)

**Update 2026-10-15 (user input): no seminar marks received; submission is 26/10/2026 (11 days).** The predictions below therefore stand as pure forecasts with no anchoring data. Tactical consequence: with zero seminars conducted and 11 days left, the department will almost certainly assess Seminars I–III and the Final Evaluation in **compressed/bunched reviews at or just before submission** — the team must arrive on Oct 26 with the *entire* file complete (report + PPTX + demo + log), because there will be no later seminar to recover marks. There is no "Seminar-I is already banked" safety net — treat all 50 CA marks as live.

Bands: High Proficiency 8–10 · Proficiency 6–7 · Some Proficiency 3–5 · No/Limited 0–2. Final Evaluation /20 uses doubled bands (16–20 / 12–14 / 6–10 / 0–4).

| Seminar | Predicted | Band | One-line justification |
|---|---|---|---|
| Seminar-I /10 (Literature + Problem) | **8** | High Proficiency | SEBI-anchored problem statement, RQs/H₀H₁, 14-ref review, adversarial critique — among the best Unit 1 sets; −2 for no standalone abstract page and no industry-visit/record evidence |
| Seminar-II /10 (Approach + budget + plan) | **7** | Proficiency | Genuine tradeoff matrices, frozen SRS + math contracts, gated 27-day plan; −3 for missing safety section, no cost-estimate sheet, no collected-data evidence |
| Seminar-III /10 (Testing + modify) | **7** | Proficiency | 9/9 tests green (verified), 4 real redesigns with before/after rationale; −3 for empty `03/`+`04/` folders, never-run experiment matrix, MVP dashboard |
| Final Evaluation /20 (Defend + report + demo) | **12** | Proficiency (doubled) | Live demo would work and engine questions would be answered brilliantly; −8 for stub chapters, no PPTX, missing certificate/ack/reflections, single-author git exposure |
| **Predicted CA total** | **34 / 50** | — | 8 + 7 + 7 + 12. ESE /50 cannot be predicted from disk [ASSUMED: same proficiency → ~30/50 band] |

> Brutal-honesty note: these are *today* marks. Every point below is recoverable — see Action Plan for exact mark-gain mapping. Do not mistake a strong codebase for a strong file: committees mark the file.

---

## 7. PROS — strengths (each with file-path evidence)

1. **Problem statement is committee-grade.** SEBI 2024 statistics (93%, ₹1.81L Cr, 71% cash) → Three Silent Killers → RQ1–RQ4 → H₀/H₁ with Nifty-50 benchmark math. (`docs/01_unit1_literature/problem_statement.md`)
2. **Literature review is real, not decorative.** 14 cited works with equations (max-Sharpe inflation, DSR variance, friction model) and per-bias mitigation contracts pointing at source files. (`docs/01_unit1_literature/literature_review.md`)
3. **Build-vs-adopt decision is defended like engineers, not students.** 6-tool matrix + event-vs-vectorized tradeoff + "answering *the library did it* earns zero viva marks". (`docs/02_unit2_specifications/alternative_solutions_and_feasibility.md`)
4. **Math spec is a genuine test contract.** Paisa-level golden master (₹1,00,000 → buy ₹1,00,192.28 / sell ₹1,09,807.47 / net +₹9,615.19) with STT/stamp/GST equations. (`docs/02_unit2_specifications/mathematical_specifications.md:88-125`)
5. **Zero-look-ahead invariant is enforced by construction and tested.** Signal at Close → fill at next Open; `test_engine_zero_look_ahead` asserts fill at Open 105.0. (`src/engine/backtest_engine.py:31-63`, `tests/test_engine.py:15-38`)
6. **Unit 4 contains real redesigns, not cosmetic ones.** Cash→equity sizing fix, O(1) slicing, Almgren-Chriss impact, CPCV embargo with AR(1) proof (PBO 28.89%→37.78%). (`src/engine/backtest_engine.py:109-115`, `src/engine/cost_model.py:22-28`, `src/analytics/cpcv.py:21-44`, `tests/test_cpcv.py:35-59`)
7. **Test suite is green and meaningful.** 9/9 PASS re-verified during audit; tests assert exact paisa values, sizing math (110 shares), and embargo behavior — not tautological asserts. (`tests/`)
8. **Adversarial self-critique pre-empts the examiner.** Five theses (F&O-vs-delivery false equivalence, low-turnover paradox, ₹0 brokerage, DSR fragility, large-cap efficiency) each with hardened defenses. (`docs/01_unit1_literature/adversarial_critique_and_contradictions.md`)
9. **Report scaffolding compiles.** Three LaTeX PDFs build (Thesis, Completion Report with TikZ flowchart + case-study table, Master Report). (`docs/QuantLab_Thesis.pdf`, `docs/QuantLab_Completion_Report.pdf`, `docs/Master_Report.pdf`)
10. **Work history is consistent and gated.** 29 day-wise commits (Day 6–19) match `LEDGER.md` checkpoints 1–3; scope discipline (3 strategies, daily bars, no live trading) shows syllabus maturity. (`git log`, `docs/00_management/LEDGER.md`)

---

## 8. CONS — weaknesses (tagged, with root cause)

### Critical (lose marks on the day / threaten the defense)

- **C1 — No real-data execution evidence.** `data/raw/` absent, `experiments/` empty, `experiment_log.csv` never generated. FR-12 and the entire IS-vs-OOS thesis are *claims without artifacts*. Root cause: pipeline needs network (`yfinance`) and was likely run elsewhere or never; nothing cached/committed. Kills Seminar-III "verify results" and Final Evaluation demo credibility.
- **C2 — Single-contributor git for a two-person team.** 29–0 commit split; `origin/meet` branch empty. An examiner running `git shortlog` asks one question ("who did what?") that currently has no good answer. Root cause: pair-work done on one machine/account without co-authorship or task-trail discipline.
- **C3 — No PPTX and no department-format-complete report.** Chapters are stubs (5–27 lines), `final_report_draft.md` is 24 lines, and there is no `.pptx`, certificate, declaration, acknowledgement, or reflections section. Root cause: Unit 5 never started (`LEDGER.md` Phase 4 all ❌) + 6.5-week commit silence since Aug 31.

### Major (each costs 1–3 marks if unfixed)

- **M1 — Safety & sustainability section missing (syllabus 2.9 + guide role).** Zero coverage; the rubric's Seminar-II explicitly rewards budget+plan completeness. Fix is 1 page (see Action Plan).
- **M2 — `scipy` imported but absent from `requirements.txt`.** `deflated_sharpe.py:3` needs `scipy.stats`; fresh-clone install breaks DSR/CPCV analytics. Root cause: scipy arrived transitively and was never pinned.
- **M3 — RSI division-by-zero semantics bug.** `rsi_mean_reversion.py:23,39`: when `down == 0` (pure up-moves), `rs = 0` → RSI computes **0 (max oversold)** instead of **100 (max overbought)**. Any all-gains window emits the exact wrong signal. Needs a regression test.
- **M4 — Statutory-rate inconsistency across docs.** NSE turnover fee is 0.00297% (`mathematical_specifications.md`, code) vs 0.00345% (`QUANTLAB_DOMAIN_DEEP_DIVE.md:95`, Completion Report). STT rounding: code rounds to ₹1 (`cost_model.py:42`) while the golden-master doc shows unrounded ₹100.05. Committee cross-checks numbers — reconcile to one NSE circular.
- **M5 — No direct tests for SMA/RSI; SRS test-contract breach.** SRS §6 promises `test_data.py` + `test_strategies.py`; neither exists. Only momentum has a strategy test. RSI bug (M3) survived precisely because of this.
- **M6 — Dashboard under-delivers the SRS.** `app.py` (64 lines) wires strategy select + cost toggle + equity/drawdown only. DSR p-value, 2D heatmap (`components.plot_2d_heatmap` exists but is never called), "Profit Mirage" waterfall, and IS/OOS comparison from the SRS/architecture docs are not wired. Demo shows ~40% of claimed UI.
- **M7 — Strategy-side filtering defeats the O(1) engine story.** Engine slices O(1) via `idx_trackers`, but every strategy re-filters with `df[df['date'] <= current_date]` (O(N) scan per symbol per day). Correctness is unaffected (still causal), but the "near-compiled speeds" viva claim is overstated until strategies accept the pre-sliced frame.

### Minor (polish; fix opportunistically)

- **m1 — Risk-free rate mismatch:** spec says 6.0% (`mathematical_specifications.md`), code defaults to 5% (`metrics.py:7`). One-line fix + cite RBI G-Sec source.
- **m2 — `docs/03_unit3_testing/` and `docs/04_unit4_redesign/` empty.** The work exists (tests + redesigns) but the syllabus-mapped folders are vacant — move/link test plan, golden fixtures, OOS-decay notes in.
- **m3 — `Order` (`order.py`) vs `OrderEvent` (`events.py`) duplication.** Two order representations; engine uses `OrderEvent`. Consolidate or document why both exist.
- **m4 — Position cost-basis excludes buy-side frictions** (`position.py:14`); sell-side subtracts `total_cost` once. Document the accounting choice explicitly so an examiner can't call it a bug.
- **m5 — Charts' provenance unclear.** `docs/charts/*.png` are "simulated" per filenames; regenerate from real runs with date-stamped scripts and record parameters.
- **m6 — Thesis defense-box contradiction:** ŧhesis Ch.5 says "strictly prohibit Adjusted Close" while `clean.py:23` relies on yfinance-adjusted closes. Reconcile the wording (adjusted closes are standard; the prohibition claim is over-broad).
- **m7 — Stale `origin/meet` branch + 6.5-week silence.** Either merge real work or delete the branch; resume weekly commits so the log shows "continuous guidance" rhythm.

---

## 9. Metrics Dashboard

| Metric | Value | How computed |
|---|---|---|
| Overall completion (weighted) | **~70%** | Σ unit% × weight: 13.3 + 15.0 + 17.6 + 15.4 + 8.8 (see below) |
| Unit 1 (14%) | 95% → **13.3** | 4/4 done; −5% abstract/visit formality |
| Unit 2 (20%) | 75% → **15.0** | Safety + real-data + cost-sheet gaps |
| Unit 3 (22%) | 80% → **17.6** | Code+tests done; dashboard/matrix unfinished |
| Unit 4 (22%) | 70% → **15.4** | Code redesigns done; folders/docs + heatmap wiring pending |
| Unit 5 (22%) | 40% → **8.8** | PDFs compile; chapters/PPTX/formalities pending |
| Deliverable readiness | **7 / 12** | Done: problem stmt, literature, SRS, arch+flowchart, algorithm, simulation, work plan. Partial: block diagram, report, PPT, cost sheet. Missing: safety note |
| Predicted CA | **34 / 50** | 8 + 7 + 7 + 12 (§6) |
| Time remaining (updated 2026-10-15) | **11 days to submission (26/10/2026, 10:30 AM)** | Govt. Polytechnic-Gandhinagar Sem-5 timetable (user-confirmed); no seminar marks banked — all 50 CA marks effectively live |
| Risk level | **High** | No real-data artifacts + single-author git + missing Unit 5 formalities 6.5 weeks silent — any one of these dominates an ESE viva |
| Novelty | **7 / 10** | Diploma-outstanding (Indian tax matrix + DSR + CPCV + honest-framing pedagogy); not a research breakthrough — correctly scoped |
| Report completeness | **~55%** | Structure + PDFs exist; chapters stub; certificate/ack/reflections absent |
| Code quality | **8 / 10** | Clean layering, invariants, meaningful tests; −2 for M2/M3/M5/M7 |
| Documentation quality | **8 / 10** | Specs superb; −2 for inconsistencies (M4, m1, m6) + empty 03/04 folders |
| Tests | 9/9 PASS (re-run 2026-10-15) | `pytest tests/ -q` → 9 passed |
| Code volume | ~1,008 LOC src / ~2,011 incl. tests+scripts | `wc -l` |
| Team-evidence split | 29 / 0 commits | `git shortlog -sne` |
| Budget | ₹0 documented spend; no cost sheet | `srs.md:62` |

---

## 10. Gap Analysis vs GTU Requirements

Missing-or-thin items, ordered by mark impact:

1. Real-data run artifacts (OHLCV cache, `experiment_log.csv`, 12-cell matrix table) — C1
2. `.pptx` presentation + seminar delivery record — C3
3. Department-format report completion (certificate, declaration, acknowledgement, reflections, guide-suggestion log) — C3/5.4/5.5/5.6
4. Safety (+ sustainability) section — M1/2.9
5. Project cost-estimate sheet (even if all-₹0) — 3.2
6. Title-originality check (past-3-years list clearance) — mandatory GTU check, no evidence
7. SSIP/patent/techfest/paper trail (encouraged; currently none) — syllabus flowchart + §p2
8. `docs/03/` + `docs/04/` content (test plan, golden fixtures, OOS-decay + stability notes) — m2
9. Dashboard completion (DSR, heatmap, waterfall, IS/OOS views) — M6
10. Weekly guide-meeting record — 2.10/5.6
11. Task-split evidence for member 2 (commits or signed task log) — C2/5.1
12. Dependency + bug fixes (scipy pin, RSI edge case, rate reconciliation) — M2/M3/M4/m1

---

## 11. Compliance Check

| GTU mandatory / encouraged item | Status |
|---|---|
| Working model / prototype / process simulation (COMPULSORY) | **PASS** — event-driven simulator runs; 9/9 tests green (`src/engine/backtest_engine.py`, `tests/`) |
| Title not duplicating past 3 years | **NO EVIDENCE** — clearance record missing [ASSUMED unchecked] |
| Group of 2–5 | **ON PAPER** — 2 members (`QuantLab_Project_Documentation.md:6-9`); git shows 1 active contributor |
| Weekly guide meetings | **NO EVIDENCE** [ASSUMED unknown] |
| Block diagram | **PARTIAL** — ASCII/mermaid 4-layer diagrams in SRS/architecture docs; no standalone captioned block-diagram figure in report |
| Branch-specific drawing / process flow | **PASS (software equivalent)** — TikZ execution flowchart in Thesis Fig. (`QuantLab_Thesis.tex:197-225`) + Completion Report flowchart |
| Algorithm + flowchart (software projects) | **PASS** — O(1) slicing algorithm + signal equations + flowcharts documented |
| Simulation | **PASS** — see prototype above |
| Report in department format | **PARTIAL** — LaTeX report exists; format compliance + formal pages unverified |
| PPT | **PARTIAL** — 12-slide markdown deck with speaker notes; no `.pptx` |
| Safety + sustainability evident | **FAIL** — absent (M1) |
| SSIP grant / patent / techfest / hackathon / paper (encouraged) | **NONE** — no evidence; Apache 2.0 license keeps the patent path open (`LICENSE`) |

---

## 12. Prioritised Action Plan — 11-DAY SPRINT TO 26/10/2026

**Updated 2026-10-15.** With submission on **26/10/2026 at 10:30 AM** and no marks banked, the original open-ended phases collapse into a dated sprint. Rule: **nothing new is built after Oct 22** — Oct 23–25 is report + PPTX + rehearsal only. Each task states **Unit + CO + rubric improved** and **expected mark gain** (conservative, committee-style).

### Phase A — Oct 16–17 (48 hours, highest marks-per-hour)

1. **Freeze one statutory rate card + fix `requirements.txt`.** Reconcile NSE fee (0.00297% vs 0.00345%) to a single cited circular; align STT-rounding wording between code and golden master; set `risk_free_rate=0.06`; add `scipy` to `requirements.txt`; re-run pytest. → Unit 2/3 · CO2/CO3 · Seminar-II/III · **+1–2 CA**
2. **Fix RSI all-gains edge + add SMA/RSI signal tests.** `rs=0 → RSI 100` guard; create `tests/test_strategies.py` (SMA cross up/down, RSI oversold/overbought, all-gain RSI=100); create `tests/test_data.py` (cleaner drops NaN, no ffill). Fulfills the SRS §6 test contract. → Unit 3 · CO3 · Seminar-III · **+1–2 CA**
3. **Write the 1-page Safety + Sustainability note** (data disclaimer: educational simulation, no live-trading advice; YFinance redistribution limit; reproducibility; e-waste/energy: runs on existing laptops, <25 MB RAM, no GPU/cloud). File as `docs/02_unit2_specifications/safety_and_sustainability.md` + 1 thesis page. → Unit 2 · CO2 · Seminar-II · **+1 CA**
4. **Produce the ₹0 cost-estimate sheet** (laptops already owned, software ₹0, data ₹0, printing/binding estimate, contingency) as `docs/02_unit2_specifications/cost_estimate.md`. → Unit 3 (3.2) · CO2/CO3 · Seminar-II/III · **+1 CA**
5. **Clear the title-originality check** with the coordinator (past-3-years list) and file the signed note in `docs/00_management/`. → Mandatory compliance · Final Evaluation · **prevents a catastrophic viva question**

### Phase B — Oct 18–22 (complete the engineering proof; CODE FREEZE Oct 22 night)

6. **Run the real-data matrix and commit artifacts.** Execute `run_experiments.py` + `run_pbo_experiment.py` on 2019–2024 data; commit `data/` manifest (or cache + manifest if large), `experiments/experiment_log.csv`, IS-vs-OOS decay table, and regenerated charts with parameters recorded. Backfill `docs/03_unit3_testing/` (test plan + golden fixtures + test log) and `docs/04_unit4_redesign/` (OOS-decay analysis + stability note). → Unit 3/4 · CO3/CO4 · Seminar-III · **+2–3 CA**
7. **Wire the missing dashboard views.** DSR p-value panel, 2D heatmap tab (`plot_2d_heatmap` already exists — call it), Profit-Mirage waterfall (costs ON/OFF overlay), IS/OOS comparison. → Unit 3/4 · CO3/CO4 · Seminar-III + Final demo · **+1–2 CA**
8. **Repair team evidence.** Member 2 makes substantive commits on `origin/meet` (dashboard wiring or report chapters) and merges via PR; or maintain a signed task log with file-path deliverables per member. Both members rehearse cross-subsystem defense (each explains the other's module). → Unit 5 (5.1) · CO5 · Final Evaluation · **+2–4 /20 (highest leverage)**
9. **Collect department report format + SSIP/patent contact.** Get the format from the coordinator; open SSIP + prior-art/patent-eligibility threads and file the receipts (even "applied, pending" counts as encouraged-activity evidence). → Unit 5 · CO5 · Final Evaluation + ESE goodwill · **+1–2**

### Phase C — Oct 23–25 (defense polish; NO new code, report + PPTX + rehearsal only)

10. **Finish the report properly.** Expand `chapters/*.tex` to full chapters; add certificate, declaration, acknowledgement, reflections (5.4), guide-suggestion log (5.6), safety page, cost sheet, originality clearance, experiment tables, and heatmap figures. → Unit 5 · CO5 · Final Evaluation · **+2–4 /20**
11. **Build the `.pptx` (15–18 slides) from the markdown deck**, rehearse with the viva cheat sheet + 15 questions below, and dry-run the live demo twice (including the costs ON/OFF "Profit Mirage" moment). → Unit 5 (5.3/5.7) · CO5 · Final + ESE · **+2–3**
12. **Close minor inconsistencies** (m1–m7): Order/OrderEvent note, cost-basis accounting note, Adjusted-Close wording, chart provenance, branch cleanup, weekly commits. → Units 2–5 · CO2–CO5 · **+1 across seminars**

**Realistic trajectory if all done:** CA 34 → **44–47/50**; ESE posture transforms from "good code, thin file" to "complete distinction file".

**Submission-day checklist — Oct 26, 10:30 AM (Respective Group Faculty):** printed + bound report · PPTX on pen drive + laptop · live demo rehearsed twice (costs ON/OFF "Profit Mirage" moment) · `experiment_log.csv` + charts on disk · both members present, each able to demo the other's module · originality clearance + SSIP/patent receipts in file (even "applied, pending").

---

## 13. Defense Prep

### 15 likely viva questions

1. Signal at Day-t Close cannot fill at Day-t Close — walk me through your exact execution timeline. *(Ans: `backtest_engine.py:35-60` — pending queue → next-date Open fill; test asserts 105.0 Open.)*
2. Why build from scratch instead of Backtrader/Zipline? *(15k-line black box; no Indian tax matrix; no DSR; "the library did it" = 0 marks.)*
3. Your cost model line-by-line: STT both sides, stamp only buy, GST base — why? *(Finance Act §98; Indian Stamp Rules 2020; CGST on brokerage+turnover only — `cost_model.py`.)*
4. Your golden-master numbers: prove ₹1,00,000 → ₹1,00,192.28 buy. *(Whiteboard the 7-line calc from `mathematical_specifications.md:97-107`.)*
5. SMA trades ~3×/year — costs can't kill it. So what actually fails? *(Whipsaw vs friction vs falling-knife decomposition — adversarial doc Thesis 2.)*
6. Brokers charge ₹0 delivery. Does your thesis survive? *(Yes: STT 0.20% round-trip + slippage ≈ 0.32% remains — Thesis 3.)*
7. Standard Sharpe vs Deflated Sharpe — why should I care? *(N-trial extreme-value inflation; DSR p≥0.95 rule — `deflated_sharpe.py`.)*
8. Your SMA/RSI trials are correlated — doesn't that break DSR's N? *($N_{\text{eff}} = 1+(N-1)(1-\bar\rho)$ + 2D plateau requirement — adversarial doc Thesis 4.)*
9. What did the AR(1) embargo test prove numerically? *(PBO 28.89% → 37.78% with 5% embargo; leakage masked true overfitting — `test_cpcv_embargo_ar1`.)*
10. Cash vs total-equity sizing — what was the bug and its effect? *(Cash-based sizing shrank trades as capital deployed; fixed to 10% of total equity — `backtest_engine.py:109-115`, sizing test.)*
11. Why mega-caps if 1970s indicators can't beat them? *(Clean control: zero impact, lowest fees; failure there validates EMH and bounds small-cap claims — Thesis 5.)*
12. SEBI 93% is F&O data; you simulate delivery. False equivalence? *(No: SEBI Jul-2024 cash study, 71% loss; active trading converts positive-sum equity into negative-sum friction game — Thesis 1.)*
13. Where is your IS-vs-OOS decay evidence? *(Show `experiment_log.csv` + decay table — Action #6 makes this answerable.)*
14. What does your engine NOT model, and why is that acceptable? *(No intraday/live/derivatives/partial fills; diploma scope + assumption ledger in §8 Scope — limitations strengthen, not weaken.)*
15. Who did what? Prove both members can defend both subsystems. *(Task matrix + commits + cross-defense rehearsal — Action #8.)*

### Report structure checklist (department format + GTU 5.1–5.7)

- [ ] Title page, certificate, declaration, acknowledgement (5.5), abstract
- [ ] Table of contents, list of figures/tables
- [ ] Ch.1 literature + problem (CO1) · Ch.2 SRS/design/feasibility/safety/cost (CO2)
- [ ] Ch.3 implementation + testing with test log (CO3) · Ch.4 redesign with before/after + OOS evidence (CO4)
- [ ] Ch.5 results + conclusion + reflections (5.4) + future scope
- [ ] References, appendix (rate-card circular, originality clearance, SSIP receipts, guide-suggestion log 5.6)

### Presentation tips

- Open with the SEBI 93% number, then the costs ON/OFF live toggle — the "Profit Mirage" moment wins the room in 90 seconds.
- One architecture slide max; spend time on the golden-master calculation and the embargo PBO numbers — examiners remember numbers.
- Pre-empt with your own limitations slide (deliver Q14's answer before it's asked).
- Both members speak; each demos the other's module once (kills Q15).

---

## 14. Final Verdict

**Grade today: B** (strong technical core at ~70% weighted completion; predicted CA 34/50; High risk driven by missing defense formalities, not by engineering quality).

**Single most important next action:** run the real 2019–2024 experiment matrix and commit `experiments/experiment_log.csv` + IS-vs-OOS decay evidence (Action #6) — it simultaneously unblocks CO3, Seminar-III verification, the Unit 4 redesign narrative, and every results slide in the report and PPT.

---

## Appendix — Method note

- All code claims verified by reading source; tests re-executed (`pytest tests/ -q` → 9 passed, 2026-10-15).
- `.docx/.pptx/.pdf` handling: no docx/pptx exist; all 4 PDFs opened (syllabus text-extracted fully; thesis PDFs listed with sizes; content of thesis verified via `.tex` sources).
- Images: 7 PNGs listed by filename/size; pixel-verification not performed — recorded as PRESENT, provenance flagged (m5).
- `venv/`, `.git/objects`, `__pycache/` excluded from deep analysis per brief; `git log` (not objects) inspected.
- Every judgement above cites a file path or is flagged [ASSUMED]. No project files were modified.

---

## USER INPUT NEEDED

**Update 2026-10-15:** Q1 answered (no marks received — predictions stay unanchored forecasts), Q2 answered (submission **26/10/2026, 10:30 AM**, Gov. Polytechnic-Gandhinagar timetable; §§6, 9, 12 updated, plan re-phased to 11-day sprint). Still needed:

1. ~~Seminar marks~~ ✅ answered (none) / 2. ~~Submission date~~ ✅ answered (26/10/2026)
3. Actual money spent (if any) — hardware, printing, data, travel — for the cost sheet?
4. Guide meeting frequency + any recorded guide/evaluator suggestions to incorporate (§5.6)?
5. Past-3-years title-originality clearance: done / pending / with whom?
6. Group task split: who owns what going forward (to fix the 29–0 git split)?
7. Department report format received? (share template or rules: certificate/declaration/ack/reflection requirements)
8. SSIP / patent / techfest / hackathon / paper status: applied, planned, or not pursued?
9. Is `origin/meet` branch work real and unmerged, or should it be closed?
10. Demo laptop specs (for NFR-2 "under 30 s" claim) — confirm once the real-data matrix is run?
