---
title: "Open Contradictions & Kill Criteria — Pramaan"
date: 2026-10-16
project:
  - pramaan
tier:
  - meta
tags:
  - contradictions
  - kill-criteria
  - methodology
  - pramaan
status: active
---

# Open Contradictions & Kill Criteria — Pramaan

Two kinds of entry: **documentary contradictions** (repo says two different things) and **kill criteria** (if this becomes true, the direction is wrong).

---

## Documentary Contradictions (must be resolved before submission)

| ID | Contradiction | Side A | Side B | Resolution |
|---|---|---|---|---|
| ~~C-01~~ | NSE turnover fee value | `cost_model.py:48` = **0.00297%** | `QUANTLAB_DOMAIN_DEEP_DIVE.md:95` = 0.00345% | **RESOLVED 2026-10-19** — pinned to 0.00297% (code + NSE circular w.e.f. Oct 2024); Thesis.tex, build_report.py, DOMAIN_DEEP_DIVE.md and problem_statement.md all corrected. PRM-VER-077 |
| C-02 | Adjusted-close policy | `clean.py:23` relies on yfinance-adjusted closes | `QuantLab_Thesis.tex:419` claims adjusted close is "strictly prohibited" | **PARTIAL** — `Pramaan_Report.tex` (the new report) explicitly records "provider auto-adjusted close" as the adjustment policy with no prohibition wording, so the deliverable is consistent. The superseded `QuantLab_Thesis.tex` still carries the over-broad line; flagged for cleanup, not in the submission path. |
| ~~C-03~~ | Risk-free rate | `metrics.py:7` = 0.05 | `mathematical_specifications.md` = 0.06 | **RESOLVED 2026-10-19** — default set to 0.06; all 35 tests pass. PRM-VER-078 |
| ~~C-04~~ | Dataset claim | Report/demo: "NIFTY-50, 2019–2024" | `universe.py` = 10 symbols; scripts fetch 2022–2024 | **RESOLVED 2026-10-19** — the real 2019–2024 run now exists (PRM-VER-066) and all copy states "10 NSE large-cap symbols" rather than "NIFTY-50". The claim matches the artifact. |
| C-05 | Team evidence | 2-person team asserted | Single git author (`origin/meet` empty) | **OPEN — highest leverage remaining.** Meet must make substantive commits (frontend/Tauri/report chapters) or a signed task log must be filed. Both members must be able to demo each other's subsystem. |
| C-06 | Product name | `README`/report say "QuantLab" | Product decision = **Pramaan** | Kill "QuantLab" in public copy; retain only as legacy engine/repo name. DEC-006 |

---

## Kill Criteria (any true → change direction)

| ID | If this is true… | Then… |
|---|---|---|
| K-01 | The real-data matrix cannot run or produce no trades | The entire results narrative collapses. Fix data before anything else (Phase 0). |
| K-02 | The frontend is not demo-usable by Oct 22 | Drop to the Streamlit fallback for the live demo; keep URL/GitHub as product proof. |
| K-03 | `pytest` cannot reach ≥12 passing | Do not add features. Fix tests first — the engine must be defensible. |
| K-04 | A deployed claim cannot be demonstrated live | Downgrade the claim to "local build + published release" — never claim unverified deployment. |
| K-05 | Data cannot be shown without `yfinance` | Publish BYOK + academic-use disclaimer; do not ship unlicensed commercial data. |

---

## Self-Refuting Assumptions (challenge these in the viva)

| ID | Assumption | Counter |
|---|---|---|
| A-01 | "Daily bars are enough to prove cost realism" | Cost realism is directionally correct but ADV-based impact on daily bars is a coarse estimate — state it. |
| A-02 | "3 strategies prove the engine" | They prove the *engine*, not the strategy. Keep the framing on the engine. |
| A-03 | "DSR/CPCV make our results trustworthy" | They only quantify *risk* of overfitting with a small N-state universe. Never say "trustworthy" — say "diagnosed". |
| A-04 | "Pramaan is deployable commercially today" | Not until data licensing is solved. Academic use only. |
