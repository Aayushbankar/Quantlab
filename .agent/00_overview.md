---
title: "Pramaan — Agent Vault Overview & Ledger Protocol"
date: 2026-10-16
project:
  - pramaan
tier:
  - meta
tags:
  - verification-ledger
  - methodology
  - conventions
  - pramaan
status: active
---

# Pramaan — Agent Vault Overview & Ledger Protocol

> **Master ledger (SSOT):** `.agent/01_verification_ledger.md` · **Plan:** `.agent/02_plan.md` · **Gates:** `.agent/02_plan.md` §5 · **Entry point:** `AGENTS.md`


---


## 1. Why a ledger, not a progress doc

`progress.md` records *effort*. A ledger records *claims that survived verification*. Pramaan's thesis is that assertions must be reconciled against evidence — the project uses its own medicine. This is also what a GTU examiner rewards: every number traceable to an artifact.

**Rule: nothing is "done" until it has a `PRAM-VER-XXX` row with a physical evidence path.**

## 2. Directory structure

```
.agent/
├── 00_overview.md               # THIS FILE — protocol + conventions
├── 01_verification_ledger.md    # MASTER LEDGER — the SSOT, every claim
├── 02_plan.md                   # phases, gates, tasks (each with a VER ID)
├── 03_dead_ends.md              # dead-ends register — what we tried and abandoned
├── 04_open_contradictions.md    # contradictions + kill criteria
├── 05_decisions.md              # decision records (dated, justified)
├── 06_daily/                    # daily logs, one file per date
├── _templates/                  # task / verification / daily templates
└── (legacy) quantlab_eval_strategy.md
```

## 3. File conventions

- **Front matter on every file** — no exceptions:
  ```yaml
  ---
  title: "Human Readable Title"
  date: 2026-10-16
  project: [pramaan]
  tier: [meta, engine, api, frontend, desktop, academic]
  tags: [lowercase-hyphen-tags]
  status: active
  ---
  ```
- **Filenames:** lowercase, numeric prefixes for order (`01_verification_ledger.md`), hyphens not camelCase.
- **One concept per file** — atomic and independently linkable.
- **Wikilinks** for internal cross-references.
- **Zero dead links** — run the link check before committing ledger/plan changes.
- **Conventional commits:** `feat:` `fix:` `docs:` `refactor:` `chore:`

## 4. Status vocabulary (use exactly these)

| Status | Meaning |
|---|---|
| `VERIFIED` | Claim executed and evidence exists on disk |
| `VERIFIED (Negative Result)` | Claim **falsified** — a win, not a failure |
| `INCONCLUSIVE` | Attempted, evidence incomplete; must be re-attempted |
| `RETRACTED` | Claim withdrawn — **must** appear in the Retraction Log with reason |
| `DISPROVED` | Claim shown false |
| `CORRECTED` | Earlier wrong claim superseded |
| `PLANNED` | Not yet attempted |
| `FAILED` | Attempted, did not achieve target |

**A negative result is logged proudly.** A dead end that is documented is knowledge; a dead end that is silently dropped is a repeated mistake. See `03_dead_ends.md`.

## 5. Verification method vocabulary

| Method | Means |
|---|---|
| `STATIC (source audit)` | Claim read directly from source files |
| `RUNTIME (pytest)` | Test command executed, output quoted |
| `RUNTIME (curl)` | Endpoint called, response recorded |
| `RUNTIME (build)` | Binary produced, install verified |
| `RUNTIME (browser)` | Page/flow exercised manually |
| `STATIC-HIGH-CONFIDENCE` | Inferred from a documented external fact (e.g. a statutory circular) |

## 6. The iteration loop (every session)

```
1. READ   .agent/01_verification_ledger.md   → what is already VERIFIED
2. READ   .agent/02_plan.md                  → find next task whose VER ID is PLANNED
3. READ   .agent/04_open_contradictions.md   → check nothing there blocks it
4. DO     exactly ONE task
5. VERIFY it — run the real command, quote the output
6. RECORD a row in .agent/01_verification_ledger.md with:
         PRAM-VER-XXX | UTC timestamp | claim | file:line (or endpoint)
         | method | evidence path | status
7. LOG    .agent/06_daily/<YYYY-MM-DD>.md → task ID, files touched, evidence, next task
8. STOP   — do not start a second task before the first is VERIFIED
```

## 7. Retraction rule

If a previously logged claim turns out false, **do not overwrite it**. Strike the claim text (`~~...~~`), set status to `RETRACTED`, and add a row to the **Retraction Log** section of the ledger with the reason. Honesty is the asset.

## 8. Gate records

Gates are verified as ledger rows, not as intentions. A gate passes only when its acceptance criteria have evidence rows pointing at real artifacts.

## 9. Cross-references

- [[01_verification_ledger|Master Verification Ledger]]
- [[02_plan|Implementation Plan & Gates]]
- [[03_dead_ends|Dead Ends Register]]
- [[04_open_contradictions|Open Contradictions & Kill Criteria]]
- [[05_decisions|Decision Records]]
- [[AGENTS|Root AGENTS.md]]
