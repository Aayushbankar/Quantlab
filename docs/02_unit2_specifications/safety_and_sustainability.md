---
title: "Safety and Sustainability Considerations"
date: 2026-10-19
project: [pramaan]
tier: [academic]
tags: [safety, sustainability, compliance, unit2]
status: active
---

# Safety and Sustainability Considerations

**Satisfies GTU DI05000341 syllabus sub-point 2.9.** For a software project, safety is a behavioural and informational property rather than a physical one. This document treats it as a first-class requirement.

---

## 1. Why safety is a requirement, not a formality

Pramaan is a tool whose output a user might act on with real capital. A tool that confidently reports an edge that does not exist causes real financial harm. Safety in this context therefore means: **the system must not present a misleading result with confidence.** That principle drives three design decisions visible in the code.

### 1.1 No-advice framing

- The engine has no execution path at all — no broker connection, no order routing, no API key capable of placing an order.
- Every output surface carries a simulation-only notice.
- The README, terms of service, and dashboard all state explicitly that Pramaan is not investment advice and that past performance does not guarantee future results.
- No output is phrased as a recommendation ("buy REIANCE") — only as a measurement ("this configuration produced Sharpe X over this window").

### 1.2 Determinism as a safety property

A non-reproducible engine can hide a defect. Pramaan makes determinism a tested invariant (NFR-1): the same request produces a byte-identical equity curve, verified by hashing the serialised equity of two independent runs. This means that any reported result can be re-derived, and a defect that produces a wrong number produces it consistently and therefore visibly.

### 1.3 Honest reporting of negative results

A system that only reports outcomes favourable to the user's hypothesis is not safe. Pramaan's central reported finding is negative — no active strategy beat a passive benchmark. Suppressing that result would have produced a more persuasive demonstration and a less honest project.

---

## 2. Data safety and legal custody

| Concern | Position |
|---|---|
| Market data redistribution | Pramaan does **not** redistribute market data. Data is fetched at runtime on the user's machine, optionally under the user's own provider key (BYOK). No data asset is shipped in the repository. |
| Provider terms | The free-tier data path is documented as academic/personal use. Commercial deployment requires a licensed provider behind the BYOK interface. This limitation is published, not hidden. |
| Local data | Cached market data is stored as plain local files owned by the user. No data is transmitted off-device unless the user enables an optional sync feature. |
| No telemetry by default | No usage statistics, crash reporting, or analytics are enabled by default. |

---

## 3. Resource and energy sustainability

| Aspect | Position |
|---|---|
| Compute | The engine is a single-process Python computation on daily bars for ~10 symbols. No GPU required. |
| Memory | Runs within the memory envelope of a standard student laptop (8 GB class hardware). |
| Cloud footprint | Zero. No server is required to run, reproduce, or demonstrate the system. |
| Hardware reuse | Designed to run on existing student hardware; no new hardware is procured for the project. |
| Energy | A full 30-run experiment matrix completes in roughly six minutes of single-core CPU time on commodity hardware. |

The design goal was explicitly to keep the computational footprint low enough that the system is reproducible by the reader on their own machine — which is also what makes its results auditable.

---

## 4. Failure-mode safety

| Failure | Mitigation |
|---|---|
| Missing or corrupt data | Cleaning drops incomplete bars rather than forward-filling; duplicate dates rejected; empty inputs return empty results rather than partially wrong ones. |
| Degenerate parameters | Parameter ranges validated; extreme values rejected rather than silently producing nonsense. |
| Division-by-zero in RSI | Explicit handling: all-gains saturates at 100, all-losses floors at 0, flat series returns neutral 50. |
| Negative cash | Detected and warned; the engine's pre-trade sizing check prevents the condition from arising in practice. |
| Absurd market impact | Impact capped at 5% of price to prevent degenerate pricing on thin symbols. |

---

## 5. Accessibility and inclusivity

- Dark theme is the default to reduce eye strain during extended analysis.
- All figures are annotated with the parameters that produced them, so a reader with colour-vision deficiency can interpret results without relying on colour alone.
- Numbers are presented with explicit units and a starting-capital baseline, so a figure cannot be misread due to scale.

---

## 6. Responsible release

| Item | Status |
|---|---|
| License | Apache License 2.0 — permits commercial use with notice preservation. |
| Disclaimer | Published in README, terms of service, and dashboard. |
| Limitations | Published in README §Limitations and report Chapter 1, stated before the demonstration rather than discovered during it. |
| Security policy | `SECURITY.md` at repository root documents the threat model and reporting path. |
| Privacy | `privacy-policy.md` documents the no-personal-data position and the PDP Act / GDPR implications of any future collection. |
