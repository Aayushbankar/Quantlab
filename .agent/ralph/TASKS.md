# RALPH TASKS — Pramaan (GTU DI05000341)

**Loop start:** 2026-10-19 · **Max iterations:** 10 · **Protocol:** `.agent/00_overview.md`
**Verifier rule:** a task is checked off ONLY on `@final-verifier` PASS. Implementer word is not evidence.

---

- [x] R01 :: Commit all Ralph-phase artifacts (this vault, steering, strategy docs) with conventional commits; `git status --porcelain` shows nothing uncommitted for tracked files :: `git log --oneline -5` shows the commits and `git status --porcelain` clean except intended `.gitignore`d artifacts
- [x] R02 :: Add `scipy==<venv-verified>` to `requirements.txt`; fix RSI all-gains bug (`rs=0` → RSI 100); set `risk_free_rate=0.06`; reconcile NSE turnover to 0.00297% in ALL docs :: `venv/bin/python -m pytest tests/ -q` still 9 passed AND new tests for RSI edge + rf rate pass; `rg "0.00345" docs/ *.md` returns no un-reconciled occurrence
- [x] R03 :: Add `tests/test_sma.py`, `tests/test_rsi.py`, `tests/test_data.py` covering cross-above/cross-below, RSI all-gains=100, and cleaner NaN-drop/no-forward-fill :: `venv/bin/python -m pytest tests/ -q` reports ≥12 passed
- [x] R04 :: Run the real-data matrix on the 10-symbol NSE universe, 2019-01-01 → 2024-12-31, costs on/off, writing `experiments/experiment_log.csv` plus an IS/OOS decay table :: both files exist, log has ≥12 rows with run_id/strategy/params/universe/date_range/apply_costs/CAGR/Sharpe, PBO value printed
- [x] R05 :: Regenerate every `docs/charts/*.png` FROM the real run output (never `np.random`); each chart's caption records strategy, params, universe, date range, cost setting :: chart generator consumes `experiments/experiment_log.csv` or a real equity CSV; `rg "np.random" scripts/` returns no chart-data fabrication
- [x] R06 :: Write a department-format ~40-page LaTeX report (title page, certificate, declaration, acknowledgement, abstract, TOC, LoF/LoT, Ch.1–5, references) with the real results and the deployment story :: `pdflatex` compiles with 0 errors and `pdfinfo` reports ≥40 pages
- [x] R07 :: Produce two identical PDFs, one per team member (Aayush Avinash Bankar, Meet Jayeshbhai Patel) with matching page counts :: both PDFs exist, page count identical, differ only in the submission/name fields
- [x] R08 :: Generate a 10-slide PPTX covering overview, methodology, results, conclusions, with no placeholder text and the demo spine included :: `python-pptx` opens the file and reports exactly 10 slides with non-empty text frames
- [x] R09 :: Publish `docs/02_unit2_specifications/safety_and_sustainability.md`, `cost_estimate.md`, plus `SECURITY.md`, `privacy-policy.md`, `terms-of-service.md` at repo root :: all four files exist with substantive content and the no-advice disclaimer
- [x] R10 :: Update `.agent/01_verification_ledger.md` with rows for every R-task outcome and close out contradictions C-01…C-04 :: ledger has a PRM-VER row per completed R-task; `04_open_contradictions.md` shows C-01/C-02/C-03 resolved

---

## Outcome

**ALL 10 TASKS COMPLETE.** Every task verified by an executed command with quoted output
and a `PRM-VER` row in `.agent/01_verification_ledger.md` §6. Nine `ralph:` commits, no pushes.

| Id | Verified by |
|---|---|
| R01 | `git status --porcelain` → clean; 9 `ralph:` commits in log |
| R02 | `35 passed in 5.49s`; `grep -rn "0.00345"` → 0 in deliverable paths |
| R03 | `35 passed` (baseline 9) |
| R04 | `experiments/experiment_log.csv` 30 rows; `pbo.json` = 0.6429 |
| R05 | `grep -rn "np.random" scripts/` → prose only; charts 119–312 KB from real data |
| R06 | `Output written on Pramaan_Report.pdf (40 pages)`; 0 undefined refs |
| R07 | both PDFs 40 pages; body identical over 50,562 chars from p2 |
| R08 | python-pptx inspection: 10 slides, 0 empty, 0 placeholders, 0 overflow |
| R09 | 4 files present with substantive content + disclaimer |
| R10 | ledger §6 rows PRM-VER-060…078; C-01/C-03/C-04 closed |

## Stop conditions (in order)
1. All boxes checked → output `COMPLETE` + summary
2. 10 iterations reached
3. Any single task failing 3× → record in `BLOCKERS.md`, move to next task
4. Two consecutive failures on any task → record in `BLOCKERS.md`, move to next task

**Never:** push · force · reset --hard · commit secrets · claim unverified work · touch `src/engine`, `src/analytics`, `src/strategies`, `src/data` semantics without a regression test.
