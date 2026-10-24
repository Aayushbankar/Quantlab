# Pramaan Demo Runbook

**Purpose:** Exact fresh-clone demo path with no internet, plus known hazards and mitigations.

---

## 1. Fresh-Clone Demo (Offline-Capable)

```bash
# 1. Clone and install
git clone https://github.com/Aayushbankar/Quantlab
cd Quantlab
pip install -e ".[dev,api]"

# 2. Run tests (verifies engine integrity)
pytest tests/ -q
# Expected: 72 passed in ~7-15s

# 3. Start API (uses cached data by default)
python -m src.api.main
# In another terminal:
curl http://127.0.0.1:8000/health
# {"status":"healthy", "demo_mode": false, ...}

# 4. Run a replay backtest (zero network, instant)
curl -X POST http://127.0.0.1:8000/replay \
  -H "Content-Type: application/json" \
  -d '{"strategy":"sma_crossover","params":{"fast_window":20,"slow_window":50},"run_id":"demo"}'
# Returns equity curve, metrics, cost breakdown from committed artifacts

# 5. Run a live fixture backtest (uses seeded synthetic data, zero network)
curl -X POST http://127.0.0.1:8000/run \
  -H "Content-Type: application/json" \
  -d '{"strategy":"sma_crossover","params":{"fast_window":20,"slow_window":50},"universe":["RELIANCE.NS"],"start":"2023-01-01","end":"2023-12-31","initial_capital":100000,"apply_costs":true,"demo_mode":true}'

# 6. Frontend (optional, requires npm)
cd frontend && npm install && npm run dev
# Open http://localhost:3000
```

---

## 2. Known Hazards & Mitigations

| # | Hazard | Impact | Mitigation |
|---|--------|--------|------------|
| H-1 | **Replay vs Live cost model mismatch** | Replay artifacts use legacy profile `1.0-indian-delivery-2024` (no DP charge). Live/workstation uses `standard_discount_2024` (DP ₹13.50 + GST on sells). SMA(20,50) Sharpe: 0.527 (replay) vs ~0.506 (live). | Always state which cost profile generated a result. The `cost_profile` field travels with every run response. |
| H-2 | **First-run DSR placeholder** | Adapter returns `dsr_p = 1.0 if obs_sr > 0 else 0.0` when trial ledger has < 2 trials. Do not present a first-run DSR as meaningful. | Only show DSR after ≥ 30 trials accumulated in SQLite ledger, or explicitly label as "insufficient trials". |
| H-3 | **DSR depends on local SQLite trial ledger** | DSR values in workstation differ from committed sweep artifacts because trial count and cross-trial variance differ. | Cite the committed sweep figures (DSR 0.200 best, 0.112 baseline) for the report; treat workstation DSR as runtime illustration. |
| H-4 | **`next/font/google` needs internet at build time** | `npm run build` fails offline. | Build frontend ahead of demo (`npm run build` in `frontend/`) or document the requirement. |
| H-5 | **API URL default** | Frontend expects `NEXT_PUBLIC_API_URL=http://127.0.0.1:8000`. | Set env var if API runs elsewhere. |
| H-6 | **No live URL / Docker / binary / release in submission** | Report and README explicitly state these are not included. | Backups: screen recording + PDF copy on USB. |

---

## 3. Demo Script (5 Minutes)

| Step | Action | Proof |
|------|--------|-------|
| 1 | Open desktop app (or browser) → run NIFTY-50 SMA(20,50) | Product works |
| 2 | Toggle **Profit Mirage** costs ON → OFF; show equity flip sign, ₹8,868 drag | Core differentiator |
| 3 | Open **Statutory Tollgate** → STT 44.7%, DP 21.9% breakdown | Indian realism |
| 4 | Open **Overfitting Diagnostics** → DSR 0.112, PBO 60.0% [44.4%, 73.3%] | Overfitting honesty |
| 5 | Show **T+1 Execution Ledger** → signal at t Close, fill at t+1 Open | Zero look-ahead |
| 6 | Show **Python engine source** (`src/engine/backtest_engine.py:31-63`) | Actual contribution |
| 7 | Show `experiments/experiment_log.csv` + `oos_decay.csv` | Reproducible results |
| 8 | If network fails → play recorded video, continue from cached data | Resilience |

---

## 4. Backup Artifacts (USB / Cloud)

- `demo_recording.mp4` — 90-second full demo
- `Pramaan_Report.pdf` — master copy
- `Pramaan_Presentation.pptx` — 10 slides
- Committed `experiments/` artifacts (log, decay, sweep, provenance)

---

## 5. Quick Reference: Key Numbers

| Metric | Value | Source |
|--------|-------|--------|
| Best active Sharpe (SMA 10,30) | 0.685 | `experiment_log.csv` |
| Buy-and-hold Sharpe | 0.746 | `experiment_log.csv` |
| Momentum cost drag (Sharpe) | 48.2% | `experiment_log.csv` |
| Momentum cost drag (equity) | ₹12,995 | `experiment_log.csv` |
| PBO (133-config sweep) | 60.0% [44.4%, 73.3%] | `sweep_summary.json` |
| Best sweep DSR | 0.200 (sma_15_200) | Recomputed from `sweep_returns.csv` |
| Baseline SMA(20,50) DSR | 0.112 | Recomputed from `experiment_log.csv` |
| Round-trip cost (standard_discount_2024) | ₹285.38 = 28.54 bps | `cost_model.py` golden master |

---

*Generated for GTU DI05000341 submission. All numbers traceable to committed artifacts.*