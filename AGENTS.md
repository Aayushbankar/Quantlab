# AGENTS.md — Pramaan (QuantLab)

**Project:** Pramaan (प्रमाण — "proof") — the honest backtesting engine for Indian equities.
**Tagline:** *"Prove your edge before you deploy a rupee."*
**Origin:** GTU DI05000341 Sem-5 Minor Project. **Deadline:** 2026-10-26 10:30 IST. **Code freeze:** 2026-10-22 23:59 IST.

---

## 1. What this project is

An event-driven backtesting engine for Indian (NSE) equities that enforces zero-lookahead T+1 execution, applies the full statutory cost stack (STT, stamp duty, GST, exchange turnover, SEBI fee, Almgren-Chriss market impact), and reports overfitting diagnostics (Deflated Sharpe Ratio, Combinatorial Purged Cross-Validation with embargo).

Being productized into a shipped, deployable, open-source **Pramaan**: desktop GUI + web + landing page + GitHub releases. **The engine is the contribution; the product is the delivery vehicle.**

## 2. Read this first (source of truth)

1. `.agent/01_verification_ledger.md` — **the ledger. Every claim, its evidence, its status. Start here.**
2. `.agent/02_plan.md` — phases, gates, tasks. Each carries a `PRM-EXP-`/`PRM-GATE-` ID.
3. `.agent/00_overview.md` — ledger protocol, conventions, status vocabulary.
4. `.agent/04_open_contradictions.md` — open contradictions + kill criteria. Check before starting a task.
5. `.agent/05_decisions.md` — dated decision records.
6. `README.md` — public-facing identity.

## 3. The ledger rule (non-negotiable)

**Nothing is "done" until it has a `PRM-VER-XXX` row in `.agent/01_verification_ledger.md` with a real evidence path.**

- No row = not done. A task-log entry without a verification row is an opinion.
- Negative results are logged loudly — `VERIFIED (Negative Result)` is a win, not a failure.
- A disproven claim is struck through (`~~...~~`) and moved to the **Retraction Log** with a reason. Never overwrite history.
- Method must be one of: `STATIC (source audit)` / `RUNTIME (pytest)` / `RUNTIME (curl)` / `RUNTIME (build)` / `RUNTIME (browser)` / `STATIC-HIGH-CONFIDENCE`.

## 3b. Non-negotiable rules

1. **Do not rewrite the engine.** `src/engine/`, `src/analytics/`, `src/strategies/`, `src/data/` are the contribution. Harden them; never replace them. Fix bugs found via tests.
2. **Track A beats Track B.** The academic submission is mandatory. If the product threatens it, the product gets cut. Freeze discipline is absolute.
3. **Gates over intentions.** At each gate (§5), if the gate fails, cut scope at the *next* gate — never at submission.
4. **Never claim more than works.** Only demo what runs. Recorded video is the backup for everything.
5. **No live trading, no native mobile, no intraday/FnO, no AI assistant, no cloud-only flow.** These are out of scope — stated in the report and the viva.
6. **The engine is visible.** Keep the Python surface (FastAPI routes, CLI, tests) as the demonstrable artifact. The Next.js UI wraps it; it does not replace it.
7. **Determinism is a feature.** Same request → byte-identical equity curve. Every run stores `run_id = hash(strategy+params+universe+dates+cost_version+lib_versions)`.
8. **Real data, always.** Results shown come from the committed NIFTY-50 2019–2024 dataset. Never hand-edit or fake numbers. Charts must record the parameters that produced them.
9. **India-native.** NSE cash equities only. The Indian cost model + overfitting diagnostics are the moat — do not dilute with half-built global support.
10. **Honest framing.** Limitations are strengths in a viva. Publish them (README §Limitations, terms, disclaimer).

## 4. How to work — the iteration protocol

Each session must follow this loop. **One task per iteration; do not sprawl.**

```
1. READ   .agent/01_verification_ledger.md → what is already VERIFIED
2. READ   .agent/02_plan.md → find the next task whose ID is PLANNED
3. READ   .agent/04_open_contradictions.md → confirm nothing there blocks it
4. DO     that single task (and nothing else)
5. VERIFY it — run the actual command, quote the output
         (pytest, curl the endpoint, open the page, build the binary)
6. RECORD a PRM-VER row in .agent/01_verification_ledger.md
         with method + evidence path + status
7. LOG    .agent/06_daily/<YYYY-MM-DD>.md → task ID, files touched, evidence, next task
8. STOP   when the task is verified. Do not start the next one unprompted.
```

- **Verify before claiming.** Tests that were not run are not tests. Say "unverified" otherwise.
- **Small reversable steps.** Prefer three small verified commits over one large unverified change.
- **If blocked**, write the blocker in `progress.md` with what you tried, then stop and ask.
- **If a rule must be broken**, write a dated decision note in `.agent/decisions.md` explaining why. Never silently break a rule.

## 5. Gate discipline

| Gate | Deadline | Question | If NO |
|---|---|---|---|
| G0 | Oct 17 | tests green ≥12, `experiment_log.csv` on disk, blockers fixed | finish blockers before anything else |
| G1 | Oct 18 | API returns a full backtest with real data | fix adapter only — **do not start frontend** |
| G2 | Oct 20 | UI flow works end-to-end locally | drop run history + half the charts |
| G3 | Oct 21 | live URL works | Vercel only; API stays local |
| G4 | Oct 22 | desktop binary runs on the demo laptop | **fallback to Streamlit demo**; keep URL + GitHub as proof |
| G5 | Oct 26 | everything reproducible | cached data + video only |

**Fallbacks must stay alive all week:** working Streamlit app, cached dataset, recorded demo video.

## 6. Ownership split (fixes the 29/0 git history)

- **Aayush (Leader):** engine, `src/api/`, data pipeline, math, cost model, tests, CI, GitHub/releases, report Ch.2–4 + deployment diagrams.
- **Meet:** `frontend/` (Next.js), Tauri packaging, landing page, PPTX, README/docs site, report Ch.1 + Ch.5 + reflections.
- **Cross-defense is mandatory:** each must be able to explain and demo the other's subsystem before submission.
- Every task gets committed by the person who did it. No shared machine commits without attribution.

## 7. Architecture map (do not deviate without a decision note)

```
frontend/            Next.js 15 + TS + Tailwind + shadcn/ui + Recharts  (web + Tauri shell)
src/api/             FastAPI — wraps engine, contract in docs/api-contract.md
src/engine/          UNTOUCHED core — backtest loop, portfolio, position, cost model
src/analytics/       UNTOUCHED — metrics, DSR, CPCV, validation
src/data/            fetch → cache (Parquet/SQLite), universe
src/dashboard/       Streamlit fallback (keep working)
experiments/         real-data run artifacts — FR-12 reproducibility log
docs/                GTU unit-mapped documentation
data/                gitignored bulk; committed manifest + demo cache only
```

**Demo rule:** all displayed results come from replay/cache mode. Runtime fetch is shown secondarily.

## 8. Definition of done (per task)

- code written in the existing style (type hints, no dead code, no comments unless non-obvious)
- lint/typecheck/tests pass where applicable
- verified with an actual command, output quoted in `.agent/progress.md`
- no unrelated files touched; no uncommitted secrets; no fabricated results
- plan/progress updated

## 9. Definition of done (project, Oct 26 10:30)

Live URL runs a real backtest · desktop binary on the demo laptop · GitHub repo with a published release · landing page live · `experiments/experiment_log.csv` + IS/OOS decay + parameter-stamped charts committed · pytest green · report in department format with certificate/declaration/acknowledgement/reflections · PPTX 15–18 slides · both members present and cross-defending · 90-second video backup on laptop and cloud · disclaimer + terms published · scope boundaries stated.

## 10. Language & framing

Public copy uses **Pramaan**. "QuantLab" may survive only as the engine/repo name for academic continuity — never in the product UI, landing page, or README title.

---

## Handoff prompt for the next agent

```
Read AGENTS.md and .agent/plan.md in /mnt/work/projects/Quantlab, then
.agent/progress.md.

You are continuing the Pramaan project. Find the current phase and the next
unchecked task. Execute exactly that one task.

Then verify it by running the real command and quote the output. Update
.agent/progress.md with: task ID, files touched, verification evidence,
and the next task.

Rules you must not break: the engine (src/engine, src/analytics,
src/strategies, src/data) is never rewritten — bugs are fixed with tests.
Never claim unverified work. Never fake data. Never start a second task
before the first is verified. Stop and report when the single task is
done or blocked.
```
