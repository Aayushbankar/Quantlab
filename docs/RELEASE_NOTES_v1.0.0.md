# Pramaan v1.0.0-alpha.1 — Release Notes

**Release Date:** 2026-10-26 (GTU DI05000341 Submission)
**Git Tag:** `submission-final` (to be created on docs-only commit after PR merge)

---

## Overview

Pramaan (प्रमाण — "proof") is an event-driven backtesting engine and overfitting diagnostic platform for Indian equities. This release delivers the academic submission artifact: a reproducible engine, validation statistics, and a deployed analytical workstation.

**Tagline:** *Prove your edge before you deploy a rupee.*

---

## What's Included

### Engine (The Academic Contribution)
- **Zero look-ahead execution** — Signal at bar *t* Close → fill at bar *t+1* Open, enforced by construction
- **Full Indian statutory cost stack** — STT (both sides), stamp duty (buy only), NSE turnover, SEBI fee, GST (on brokerage + turnover + DP), CDSL DP charge (₹13.50 + GST on sell)
- **Almgren–Chriss market impact** — Square-root law, calibrated to trailing volatility & ADV, capped at 5%
- **Deflated Sharpe Ratio** — Cross-trial variance, skew/kurtosis adjustment, Bailey & López de Prado (2014) worked example verified
- **Combinatorial Purged Cross-Validation** — Configurable *k*, *g*, embargo; leakage validated on AR(1) ground truth
- **Determinism** — Same request → byte-identical equity curve (SHA-256 verified)

### Validation Artifacts (Committed, Reproducible)
- `experiments/experiment_log.csv` — 30 runs × 10 symbols × 1,480 bars (2019–2024)
- `experiments/oos_decay.csv` — IS/OOS Sharpe decay for all strategies
- `experiments/sweep_summary.json` — 133 configs, PBO = 60.0% [44.4%, 73.3%], 45 CPCV paths
- `experiments/sweep_returns.csv` — Full return matrix for DSR recomputation
- `experiments/PROVENANCE.json` — Data source, fetch window, library versions
- `data/manifest.json` — SHA-256 hashes for all 13 committed CSV files

### API & Workstation
- **FastAPI** — `/health`, `/strategies`, `/universe`, `/replay`, `/run`, `/jobs`, `/report`, `/trials`, `/sweep`
- **Next.js 15 Workstation** — Tri-theme (Abyss/Vellum/Graphite), Profit Mirage, Statutory Tollgate, Overfitting Diagnostics, T+1 Ledger, Run History
- **Streamlit fallback** — Headless demo mode
- **Tauri v2 desktop shell** — `frontend/src-tauri/` builds with `cargo build` (WebKit2GTK)

### Test Suite
- **72 automated tests** across 16 modules (up from 9 at baseline)
- 100% offline executable via seeded fixtures (`tests/fixtures/`)
- Categories: Invariants, Golden values, Edge/failure, Properties, No look-ahead, Data integrity

---

## Key Results (Honest, Unembellished)

| Metric | Value | Context |
|--------|-------|---------|
| Best active strategy (SMA 10,30) | Sharpe 0.685 | Costs on, full period |
| Buy-and-hold benchmark | Sharpe 0.746 | **No active strategy beat it** |
| Momentum cost drag (Sharpe) | 48.2% removed | 0.359 → 0.186 |
| Momentum cost drag (equity) | ₹12,995 destroyed | On ₹1,00,000 capital |
| PBO (133-config sweep) | 60.0% [44.4%, 73.3%] | 45 CPCV paths, 1% embargo |
| Best sweep DSR (rf=6%) | 0.200 (sma_15_200) | **No config reaches DSR ≥ 0.95** |
| Baseline SMA(20,50) DSR | 0.112 | Statistically indistinguishable from luck |

**Central finding:** Under realistic Indian transaction costs over 2019–2024 on ten large-cap NSE equities, the tested classic technical strategies did not demonstrate positive risk-adjusted alpha relative to passive ownership.

---

## Known Limitations (Stated Up Front)

1. **Survivorship bias** — Universe is currently listed symbols; no delisting adjustment
2. **Daily bars only** — Impact model is coarse; no intraday/tick data
3. **Long-only, cash equities only** — No derivatives, short selling, or leverage
4. **Legacy replay artifacts** — Use cost profile `1.0-indian-delivery-2024` (no DP charge); workstation uses `standard_discount_2024`
5. **DSR trial-ledger dependence** — Workstation DSR differs from committed sweep figures
6. **No live trading, broker integration, or order routing** — Simulation only
7. **No data redistribution** — Market data fetched at runtime under user's own key
8. **No live URL, Docker image, GitHub Release, or packaged binary in this submission** — Source-only release; binary builds locally via `cargo build`

---

## Reproduction

```bash
# Fresh clone
git clone https://github.com/Aayushbankar/Quantlab
cd Quantlab

# Install & test
pip install -e ".[dev,api]"
pytest tests/ -q          # 72 passed

# Regenerate all artifacts
python scripts/run_experiments.py      # writes experiments/
python scripts/run_sweep.py            # 133 configs, PBO
python scripts/generate_real_charts.py # writes docs/charts/

# Build reports
python scripts/build_reports.py        # 3 PDFs (master + 2 member copies)

# Build presentation
python scripts/build_presentation.py   # Pramaan_Presentation.pptx

# Frontend (requires Node.js 18+)
cd frontend && npm install && npm run build && npm run dev

# Desktop (requires Rust + WebKit2GTK dev libraries)
cd frontend/src-tauri && cargo build --release
```

---

## Commands to Create Tag & Release (Run After PR Merge)

```bash
# 1. Ensure on main with the docs-only commit
git checkout main
git pull origin main

# 2. Create annotated tag
git tag -a submission-final -m "GTU DI05000341 submission-final: docs-only commit after code freeze

Engine: 5a1f09f (submission-freeze)
Docs: submission/final-docs branch merged
Report: 46 pages, 0 LaTeX errors, 0 undefined refs
Tests: 72/72 passing
PPTX: 10 slides, data-driven
Artifacts: experiments/, docs/charts/, data/manifest.json
"

# 3. Push tag
git push origin submission-final

# 4. Create GitHub Release (via web UI or gh CLI)
gh release create submission-final \
  --title "Pramaan v1.0.0-alpha.1 — GTU Submission" \
  --notes-file docs/RELEASE_NOTES_v1.0.0.md \
  --target submission-final
```

**Do NOT create the tag or release yourself** — these commands are for the human to run after PR approval.

---

## License

Apache-2.0 (engine, unchanged). See `LICENSE`.

---

## Academic Metadata

- **Project:** Pramaan (GTU DI05000341 Minor Project, Semester 5)
- **Institution:** Government Polytechnic Gandhinagar
- **Team:** Aayush Avinash Bankar (246230316006, Leader) · Meet Jayeshbhai Patel (246230316133)
- **Submission:** 2026-10-26 10:30 IST
- **Code Freeze:** 2026-10-22 23:59 IST (tag `submission-freeze` = 5a1f09f)

---

*This release is the academic submission artifact. Post-submission code fixes will be developed on `post-submission/code-fixes` branch and merged after Oct 26 10:30 IST.*