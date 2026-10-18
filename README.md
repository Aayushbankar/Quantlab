# Pramaan (प्रमाण)

> **"Prove your edge before you deploy a rupee."**

Pramaan is the honest backtesting engine for Indian equities. It runs event-driven simulations under **zero look-ahead T+1 execution**, deducts the **full statutory Indian cost stack** to the paisa, and reports **overfitting diagnostics** (Deflated Sharpe Ratio, Combinatorial Purged Cross-Validation) — so you never mistake a paper illusion for a real edge.

- **Web app:** https://pramaan.app _(deploy during Phase 3)_
- **Desktop:** [GitHub Releases](https://github.com/&lt;org&gt;/pramaan/releases) — Windows · Linux · macOS _(Phase 4)_
- **Landing page:** https://pramaan.app _(Phase 3)_

---

## Backtests lie. Three specific lies.

A strategy that looks profitable in a backtest usually breaks live because of three silent killers:

| Lie | What it hides | How Pramaan kills it |
|---|---|---|
| **Hidden costs** | STT 0.1% both sides, stamp duty 0.015% buy-only, GST 18%, NSE turnover 0.00297%, SEBI fee, brokerage, market impact | `src/engine/cost_model.py` models every Indian delivery levy, not just brokerage |
| **Hidden slippage** | Order size vs. average daily volume moves your fill price | Almgren–Chriss square-root impact model, computed per order from trailing volatility and ADV |
| **Hidden look-ahead** | Signals generated on data that includes the future; Sharpe inflated by parameter fishing | Signal at day *t* Close → fill at day *t+1* Open, enforced by construction; DSR + CPCV/purging with embargo |

**See it in one click:** toggle costs ON/OFF and watch an equity curve turn negative. That's the *Profit Mirage*.

## What it does NOT do (explicit scope)

- **No live trading or broker integration** — simulation and validation only
- **No intraday / tick / derivatives** — daily bars, NSE cash equities, long-only
- **No bundled commercial data** — bring your own data key (BYOK); the shipped demo dataset is NIFTY-50 daily 2019–2024
- **Not investment advice** — past performance does not guarantee future results

These boundaries are deliberate. Limitations are documented because they are defensible, not because they are missing.

---

## Quickstart

```bash
git clone https://github.com/<org>/pramaan && cd pramaan
pip install -r requirements.txt

# Replay the committed NIFTY-50 dataset (no network needed)
DEMO_DATA=1 python -m src.api.main          # API on :8000
# or run the Streamlit fallback
streamlit run src/dashboard/app.py
```

Web UI: `cd frontend && npm install && npm run dev` → http://localhost:3000

Desktop binaries are on the [Releases page](https://github.com/&lt;org&gt;/pramaan/releases).

## Bring your own key

Data is fetched at runtime from your own provider. Set your key locally (never commit it):

```bash
cp .env.example .env          # then add your key
# The key is stored in your OS keyring — Pramaan never sends it anywhere
```

The open-source distribution fetches data on **your** machine under **your** key — Pramaan redistributes no market data.

## Architecture

```
frontend/     Next.js 15 + TypeScript + Tailwind + shadcn/ui + Recharts  (web + Tauri desktop)
     │  REST
src/api/      FastAPI — wraps the engine; contract in docs/api-contract.md
     │
src/engine/   UNTOUCHED CORE — backtest loop, portfolio, position, cost model
src/analytics/UNTOUCHED — metrics, DSR, CPCV + embargo, parameter stability
src/data/     fetch → Parquet/SQLite cache, NSE universe
     │
SQLite (local) → Supabase (optional: auth, sync, run history)
```

**Computation runs on your machine.** No cloud account, no telemetry, no data leaving the device unless you opt in.

## The numbers that matter

From the committed NIFTY-50 2019–2024 dataset (reproduce with `experiments/experiment_log.csv`):

- Golden-master paisa example: ₹1,00,000 → buy ₹1,00,192.28 / sell ₹1,09,807.47 / net **+₹9,615.19** after the full statutory stack
- AR(1) embargo test: PBO **28.89% → 37.78%** — leakage was masking true overfitting
- Four documented redesigns: cash→total-equity sizing, O(1) engine slicing, flat→Almgren-Chriss slippage, CPCV embargo

## Development

See [`AGENTS.md`](./AGENTS.md) for the operating protocol and [`.agent/plan.md`](./.agent/plan.md) for the current phase and gates.

```bash
pytest -q                    # engine invariants, cost model, DSR, CPCV
pytest --cov=src             # coverage report
```

**The engine (`src/engine`, `src/analytics`, `src/strategies`, `src/data`) is never rewritten.** Bugs are fixed with regression tests.

## License & Disclaimer

Licensed under **Apache License 2.0** — see [LICENSE](./LICENSE). You may use, modify, and distribute this commercially; preserve license and notices.

**Pramaan is a simulation and research tool. It is not financial advice, not a recommendation, and not a substitute for a SEBI-registered advisor.** Statutory rates are model approximations — verify against current NSE/SEBI circulars and your broker's rate card before relying on them.
