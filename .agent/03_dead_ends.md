---
title: "Dead Ends Register — Pramaan"
date: 2026-10-16
project:
  - pramaan
tier:
  - meta
tags:
  - dead-ends
  - methodology
  - pramaan
status: active
---

# Dead Ends Register — Pramaan

> Purpose: record what was **attempted and abandoned**, with the reason. A documented dead end is knowledge; a silently dropped one is a repeated mistake. Protocol: `00_overview.md` §4.

| Dead-End ID | Date | Attempted | Why it was abandoned | Lesson |
|---|---|---|---|---|
| DE-001 | 2026-10-16 | Presenting `docs/charts/*.png` as evidence of real backtest results | The generators synthesise data (`np.random`); charts are labelled *illustrative* — see PRM-VER-030/031 | Never cite a chart as evidence until its generator consumes a real run artifact |
| DE-002 | 2026-10-16 | Describing the dataset as "NIFTY-50, 2019–2024" | Universe is 10 symbols (`universe.py`); entry scripts fetch only 2022–2024 — PRM-VER-032/033 | Claim the dataset you actually have, or make the dataset you claim |
| DE-003 | 2026-10-16 | Claiming the engine achieves "near-compiled speeds" end-to-end | Strategies still rescan with `df[df['date'] <= current_date]` per symbol per day — PRM-VER-027 | O(1) applies to the engine loop, not the strategy layer |
| DE-004 | 2026-10-16 | Using `src/engine/order.py` as the order type | Duplicate of `events.OrderEvent` and unused by the engine — PRM-VER-016 | Consolidate; delete `order.py` in Phase 1 |

## Candidate approaches under evaluation (not yet dead-ends)

| Candidate | Status | Kill criterion |
|---|---|---|
| Native mobile app (Kotlin/Flutter) | REJECTED for v1 | Requires engine rewrite or backend; contradicts "no backend" — recorded in `05_decisions.md` DEC-005 |
| Supabase in the demo path | DEFERRED | Demo must not depend on network/cloud — `05_decisions.md` DEC-002 |
| Live trading / broker integration | REJECTED | Out of scope by rule 5; regulatory + liability — DEC-003 |
| Backend/cloud compute for v1 | REJECTED | Local compute suffices; no multi-user — DEC-001 |
