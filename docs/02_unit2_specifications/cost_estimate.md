---
title: "Project Cost Estimate"
date: 2026-10-19
project: [pramaan]
tier: [academic]
tags: [cost, feasibility, unit2, unit3]
status: active
---

# Project Cost Estimate

**Satisfies GTU DI05000341 syllabus sub-point 3.2.**

---

## 1. Software and data

| Item | Specification | Cost (₹) | Note |
|---|---|---|---|
| Programming language runtime | Python 3.11 | 0 | Open source |
| Numerical stack | NumPy, pandas, SciPy | 0 | Open source |
| Charting | Matplotlib, Plotly | 0 | Open source |
| Web framework | Streamlit, FastAPI | 0 | Open source |
| Testing | pytest | 0 | Open source |
| Historical market data | NSE daily OHLCV, 2019–2024 | 0 | Free public source; academic use |
| Licensed data feed | — | 0 | Not used in this submission; BYOK in deployment |
| IDE / editor | VS Code | 0 | Open source |
| Version control | Git, GitHub | 0 | Free for public repositories |
| **Software subtotal** | | **0** | |

## 2. Hardware

| Item | Specification | Cost (₹) | Note |
|---|---|---|---|
| Development laptop | Existing student hardware | 0 | Already owned |
| Test/verification machine | Existing student hardware | 0 | Already owned |
| Additional storage | < 100 MB for the NIFTY dataset | 0 | Negligible |
| **Hardware subtotal** | | **0** | |

## 3. Services and infrastructure

| Item | Cost (₹) | Note |
|---|---|---|
| Cloud compute | 0 | Not required; runs locally |
| Web hosting | 0 | Not used in the academic submission |
| Domain registration | project-specific | Optional; deferred |
| CI minutes | 0 | Free tier |
| **Services subtotal** | **0** | |

## 4. Academic submission costs

| Item | Cost (₹) | Note |
|---|---|---|
| Printing and binding — report (2 copies) | project-specific | Submitted for department estimate |
| Printing and binding — charts/appendices | included | Single-source document |
| Presentation media | 0 | Pen drive, existing |
| **Submission subtotal** | **project-specific** | |

---

## 5. Total

| Category | Cost (₹) |
|---|---|
| Software | 0 |
| Hardware | 0 |
| Services and infrastructure | 0 |
| Academic submission (printing) | project-specific |
| **Engineering total** | **₹0** |

---

## 6. Feasibility assessment

| Dimension | Assessment |
|---|---|
| **Technical** | High. All required libraries are mature; the engine is ~1,050 lines of straightforward Python requiring no exotic capability. |
| **Operational** | High. Runs on existing student hardware with no configuration beyond a `pip install`. |
| **Economic** | High. Zero capital outlay; no recurring cost. |
| **Time** | Moderate. The deterministic execution model and validation statistics demanded most of the effort, not the infrastructure. |
| **Legal** | Bounded. The data path is academic/personal use; a licensed provider is required for commercial deployment, and this is stated as a limitation. |

A deliberate design consequence of the ₹0 constraint is that nothing in this project depends on a service that could be withdrawn mid-semester. Every result in the report can be regenerated from the repository by anyone with a laptop and a network connection.
