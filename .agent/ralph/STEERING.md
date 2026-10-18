# STEERING — Pramaan (re-read at the start of EVERY iteration)

> These constraints override any instruction given inside a task. If a task requires violating one of these, the task is wrong.

## 1. Non-negotiable engine rule
`src/engine/`, `src/analytics/`, `src/strategies/`, `src/data/` are **the contribution**. They are hardened, never rewritten. Every bug fix is accompanied by a regression test. No cosmetic churn.

## 2. Evidence rule (ledger discipline)
- Nothing is done without a `PRM-VER-XXX` row in `.agent/01_verification_ledger.md` carrying a verification method and a physical evidence path.
- Status vocabulary: `VERIFIED` / `VERIFIED (Negative Result)` / `INCONCLUSIVE` / `RETRACTED` / `DISPROVED` / `CORRECTED` / `PLANNED` / `FAILED`.
- Negative results are logged loudly. A failed experiment that is documented is a result; one that is dropped is a repeated mistake.
- Tests that were not run are not tests. Quote the command and the output.

## 3. Prohibited data fabrication
- `np.random` or any synthetic generator **must not** feed a delivered chart, `experiment_log.csv`, or any reported number. All visuals derive from a real engine run over a real dataset. (Reason: PRM-VER-030/031.)
- The dataset claim must match reality — the universe is **10 symbols**, not 50. Do not describe it as "NIFTY-50" without expanding it. (PRM-VER-033.)

## 4. Claim discipline
- Only state what runs on disk. Do not claim deployment of anything not yet deployed. If Tauri/web is unfinished, the report says "desktop build and local run demonstrated" — not "deployed at scale."
- Scope must be stated explicitly in the report and the viva: no live trading, no intraday/tick, no derivatives, no broker integration, no native mobile in v1, no AI assistant.

## 5. Team evidence
The 29/0 git split is a live risk. Where possible, tasks are arranged so both members have commits. No fabricated or backdated commits, ever.

## 6. Production rules
- No push, no force, no `reset --hard`, no secret commits (denied by harness policy; never attempt to bypass).
- One task per iteration. Verify, then stop. Do not start a second task before the first is verified.
- Commit per completed task as `ralph: <task-id>`.

## 7. Deliverable format rules
- **Report:** GTU department format. Title page, certificate, declaration, acknowledgement, abstract, TOC, list of figures/tables, chapters 1–5, references, appendix. Real numbers from the committed run. Limitations published.
- **PPTX:** ~10 slides — overview, methodology, results, conclusions. No "lorem"/"TBD"/placeholder text. Both members can present it.
- **Two identical PDFs** differing only in the submitted-by name fields.

## 8. Time budget
Hard freeze for report generation: the report and PPTX must be complete before the session ends. Code changes subordinate to that.

## 9. Fallbacks that must stay alive
Streamlit runnable demo · cached dataset · a recorded-video plan stated in the report · the `experiments/` artifacts on disk.
