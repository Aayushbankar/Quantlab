# Pramaan (प्रमाण)

> **"Prove your edge before you deploy a rupee."**

Pramaan is an honest backtesting engine for Indian equities. It runs event-driven simulations under **zero look-ahead T+1 execution**, deducts the **full statutory Indian cost stack** to the paisa, and reports **overfitting diagnostics** (Deflated Sharpe Ratio, Combinatorial Purged Cross-Validation) — so you never mistake a paper illusion for a real edge.

- **Status:** validated research engine + reproducible results artifact (GTU DI05000341 submission)
- **What ships today:** the engine, the FastAPI REST backend (`src/api/`), the Next.js 15 UI (`frontend/`), a 30-run real-data matrix, the 41-test suite, a 42-page report, and a 10-slide deck
- **Planned, not built:** Tauri desktop native packaging — see `.agent/02_plan.md`

---

## Backtests lie. Three specific lies.

A strategy that looks profitable in a backtest usually breaks live because of three silent killers:

| Lie | What it hides | How Pramaan kills it |
|---|---|---|
| **Hidden costs** | STT 0.1% both sides, stamp duty 0.015% buy-only, GST 18%, NSE turnover 0.00297%, SEBI fee, brokerage, market impact | `src/engine/cost_model.py` models every Indian delivery levy, not just brokerage |
| **Hidden slippage** | Order size vs. average daily volume moves your fill price | Almgren–Chriss square-root impact model, computed per order from trailing volatility and ADV |
| **Hidden look-ahead** | Signals generated on data that includes the future; Sharpe inflated by parameter fishing | Signal at day *t* Close → fill at day *t+1* Open, enforced by construction; DSR + CPCV/purging with embargo |

**The finding, from real data:** on 10 NSE large caps, 2019–2024, with costs enabled, **none of the four classic strategies beat passive ownership** — and the statutory stack alone removed 48.2% of momentum's Sharpe and ₹12,995 on ₹1,00,000. PBO: 64.29%.

## What it does NOT do (explicit scope)

- **No live trading or broker integration** — simulation and validation only
- **No intraday / tick / derivatives** — daily bars, NSE cash equities, long-only
- **No bundled commercial data** — data is fetched at runtime; the committed artifacts carry no market data
- **Not investment advice** — past performance does not guarantee future results

These boundaries are deliberate. Limitations are documented because they are defensible, not because they are missing.

---

## Quickstart

```bash
git clone https://github.com/<org>/pramaan && cd pramaan
pip install -r requirements.txt

# Run the full test suite
PYTHONPATH=. python -m pytest tests/ -q        # 41 passed

# Launch the FastAPI backend (port 8000)
uvicorn src.api.main:app --port 8000

# In a separate terminal: Launch the Next.js 15 frontend (port 3000)
cd frontend && npm run dev
```

The Streamlit dashboard (`src/dashboard/app.py`) remains available as a secondary legacy demonstration surface (`streamlit run src/dashboard/app.py`).

## Data

Data is fetched at runtime by your machine from a free public source (Yahoo Finance via `yfinance`), which is appropriate for academic and personal use. Pramaan redistributes no market data. **Commercial deployment requires a licensed provider** behind a bring-your-own-key interface — that path is specified but not built. Never commit keys: `.env*` and `*.pem` are gitignored, and no `.env.example` ships because no key is needed for the academic path.

## Repository layout

```
src/engine/      UNTOUCHED CORE — backtest loop, portfolio, position, cost model
src/analytics/   UNTOUCHED — metrics, DSR, CPCV + embargo, parameter search
src/strategies/  SMA · RSI · Momentum · BuyAndHold (benchmark control)
src/data/        fetch → clean → universe
src/dashboard/   Streamlit fallback UI (legacy demo surface)
scripts/         run_experiments.py · generate_real_charts.py · build_presentation.py
experiments/     experiment_log.csv · oos_decay.csv · pbo.json · PROVENANCE.json
tests/           35 automated tests
docs/            GTU report + charts + unit-mapped documentation
.agent/          verification ledger · plan · decisions · daily logs
```

## The numbers that matter

From `experiments/` (10 NSE symbols, 1480 bars each, 2019-01-01 → 2024-12-30, costs enabled, ₹1,00,000 start):

| Strategy | Sharpe | CAGR | Max DD |
|---|---|---|---|
| SMA(20,50) | 0.527 | 11.37% | −14.76% |
| SMA(10,30) | 0.685 | 13.25% | −14.64% |
| RSI(14,30,70) | 0.307 | 9.80% | −32.77% |
| Momentum(20) | 0.186 | 7.43% | −10.28% |
| **Buy-and-hold benchmark** | **0.746** | **19.07%** | −32.93% |

- Cost drag on momentum: **₹12,995** on ₹1,00,000 (Sharpe −48.2%)
- CPCV probability of backtest overfitting: **64.29%** (8 splits, 2 test, 1% embargo)
- Golden-master paisa example: ₹1,00,000 → buy ₹1,00,192.28 / sell ₹1,09,807.47 / net +₹9,615.19

## Development

```bash
PYTHONPATH=. python -m pytest tests/ -q          # 35 passed
PYTHONPATH=. python -m pytest tests/ --cov=src   # coverage
```

See [`AGENTS.md`](./AGENTS.md) for the operating protocol and [`.agent/01_verification_ledger.md`](./.agent/01_verification_ledger.md) for the per-claim evidence record.

**The engine (`src/engine`, `src/analytics`, `src/strategies`, `src/data`) is never rewritten.** Bugs are fixed with regression tests.

## License & Disclaimer

Licensed under **Apache License 2.0** — see [LICENSE](./LICENSE). You may use, modify, and distribute this commercially; preserve license and notices.

**Pramaan is a simulation and research tool. It is not financial advice, not a recommendation, and not a substitute for a SEBI-registered advisor.** Statutory rates are model approximations — verify against current NSE/SEBI circulars and your broker's rate card before relying on them. See [terms-of-service.md](./terms-of-service.md) and [privacy-policy.md](./privacy-policy.md).
