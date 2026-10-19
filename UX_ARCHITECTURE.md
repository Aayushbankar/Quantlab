# QuantLab UX Architecture Document

**Product:** QuantLab — Realistic Backtesting Engine  
**Audience:** Retail traders, quants, students (GTU DI05000341 Minor Project)  
**Status:** Streamlit MVP exists (`src/dashboard/app.py`, 64 lines)  
**Author:** UX / Product Design subagent  
**Version:** 1.0

---

## 0. Executive Summary

QuantLab's current UI is a functional college CRUD app: a single Streamlit page with a sidebar, four hard metrics, two charts, and no safety nets. It hard-fails without `data/raw/`, shows nothing before a backtest runs, has no loading/empty/error/offline states, and never surfaces its own advanced analytics (DSR p-value, 2D stability heatmap, Profit Mirage costs overlay, IS/OOS comparison).

This document defines the target user journey, information architecture, visual direction, and priority-ranked changes to move QuantLab from "works on my machine" to a serious retail backtesting product.

---

## 1. The User Journey (Step-by-Step)

### 1.1 First Launch — Empty State (No Data Yet)

**Trigger:** App opens and `data/raw/` is missing or empty (current app calls `st.stop()` here).

**UI:**
- Full-bleed empty-state panel centered in the app window.
- Large illustrative icon (chart with a downward arrow into a "no data" placeholder).
- Headline: "No market data found."
- Sub-headline: "QuantLab needs historical price data to run backtests. Upload CSVs or connect a data source to begin."
- Primary CTA: "Upload market data" (opens file uploader).
- Secondary CTA: "Connect data source" (opens Settings → Data Source).
- Tertiary link: "Use demo data" (loads a bundled synthetic equity so the user can explore immediately without external data).
- Footer note: "Supported: CSV (OHLCV), Parquet. Max 500MB per file."

**User actions:**
- Click a CTA → data source/flow begins.
- Dismiss → remains on empty state; no dashboard renders.

**System response:**
- Validates file on upload (columns: date, open, high, low, close, volume).
- On success: persists to local cache, transitions to Dashboard (Main Screen).
- On failure: shows inline error card (see Error States).

**Edge cases:**
- Uploaded file missing required columns → error: "Missing required columns: date, close."
- File too large → error: "File exceeds 500MB limit."
- Corrupt CSV → error: "Unable to parse file. Please check encoding (UTF-8)."

---

### 1.2 Onboarding (First-Time User)

**Trigger:** `localStorage` / `st.session_state` flag `onboarding_completed == false` (or first launch ever).

**UI:** 4-step modal or full-screen stepped wizard.

| Step | Title | Copy | Action |
|------|-------|------|--------|
| 1 | Welcome to QuantLab | "Backtests lie unless you account for costs, slippage, and overfitting. QuantLab shows you the truth before you risk capital." | Next |
| 2 | The Profit Mirage | "A strategy that looks profitable in backtest often turns negative once fees and slippage are applied. Toggle costs on/off to see the Mirage in action." | Next |
| 3 | Run your first backtest | "Pick a strategy, set parameters, and run. We'll flag overfitting risk with DSR and CPCV automatically." | Next |
| 4 | All set | "You're ready. Your data stays local unless you choose to sync." | Get Started |

**User actions:** Next / Back / Skip onboarding (link at bottom).

**System response:**
- Persists `onboarding_completed = true`.
- Skips onboarding on all subsequent launches.
- "Skip" jumps to step 4.

**Edge cases:**
- User closes browser mid-onboarding → resume at last completed step next launch.
- Onboarding modal must be dismissible via ESC and backdrop click.

---

### 1.3 Account / Setup (Local-Only by Default)

**Positioning:** QuantLab is local-first. No mandatory account. "Account" = local preferences persisted to `~/.quantlab/` or browser `localStorage` (PWA).

**Setup screen (Settings → Account):**
- User name (optional, for report headers).
- Default initial capital (default ₹1,00,000).
- Default position sizing (fixed / % of equity).
- Default cost model (brokerage, STT, GST, stamp duty, slippage bps).
- Data source: "Local files (default)" vs "Connected provider (future)".
- Reset local data button (destructive, requires confirmation).

**User actions:** Toggle settings, save.

**System response:** Writes to local config file; validates numeric inputs (capital > 0, slippage >= 0).

**Edge cases:**
- Corrupt config file → reset to defaults with toast: "Settings reset to defaults."
- Invalid numeric entry → inline field error, block save.

---

### 1.4 Main Screen (Dashboard)

**Layout:** Three vertical zones (desktop), stacked (mobile).

```
┌─────────────────────────────────────────────────────────┐
│ Header: QuantLab  │ Universe  │ Timeframe  │ Refresh   │
├──────────┬──────────────────────────────────────────────┤
│ Sidebar  │                                              │
│ - Nav    │        KPI Row: CAGR  Sharpe  MDD  Calmar    │
│ - Strategy│                                            │
│ - Params │   [Equity Curve Chart]  [Drawdown Chart]    │
│ - Costs  │                                              │
│ - Run    │   [Profit Mirage Toggle]  [IS/OOS Tabs]     │
└──────────┴──────────────────────────────────────────────┘
```

**Sidebar (Configuration):**
- Strategy selector (SMA Crossover, RSI Mean Reversion, Momentum — future-proofed to accept custom).
- Parameter sliders with live min/max/step from strategy metadata.
- "Apply Transaction Costs & Slippage" toggle (default ON — honesty by default).
- Initial capital input.
- "Run Backtest" primary button (disabled while a run is in progress).
- Secondary: "Grid Search" (opens Advanced workflow).
- Secondary: "Save as Template."

**Main panel:**
- KPI strip: 4 metric cards (CAGR, Sharpe, Max Drawdown, Calmar) + DSR p-value badge.
- Equity curve (interactive Plotly).
- Underwater drawdown chart.
- Profit Mirage toggle hero (section 4).
- IS/OOS comparison tabs (advanced workflow).

**User actions:**
- Change strategy → parameter controls swap dynamically.
- Adjust slider → no auto-run; user must click Run.
- Toggle costs → metrics + charts re-render instantly on cached last result (no re-run needed if only cost toggle changed).
- Click Run → loading state → results.

**System response:**
- Validates params (e.g., slow > fast for SMA) before allowing Run.
- On Run: persists last-run result to local cache for offline viewing.

**Edge cases:**
- No data loaded → Run button disabled with tooltip: "Load data first."
- Invalid param combo → inline error under the offending slider.

---

### 1.5 Core Workflow — Run a Backtest

**Flow:**
1. User lands on Dashboard (data present).
2. Selects strategy + parameters.
3. Confirms cost toggle (default ON).
4. Clicks "Run Backtest."
5. App enters Loading State (section 5).
6. Engine runs; results render: KPI strip, equity curve, drawdown, Profit Mirage, DSR badge.
7. User can toggle costs ON/OFF to compare (Profit Mirage moment).
8. User can save result, export report, or open Advanced workflow.

**System response:**
- Disables Run button during execution (prevents double-submit).
- Shows elapsed-time progress spinner.
- On completion: stores result in session + local cache.
- On engine crash: Error State (section 8) with "Retry with defaults" action.

**Edge cases:**
- Engine returns empty equity history → Empty State: "Backtest produced no trades. Try different parameters or a longer timeframe."
- Data has gaps → warning toast: "Gaps detected in data; results may be unreliable."

---

### 1.6 Advanced Workflow — Parameter Grid, CPCV, DSR

**Trigger:** "Grid Search" button on Dashboard or from results page.

**UI:** Dedicated Advanced view (modal or full page).

**Parameter Grid:**
- User selects up to 2 parameters to sweep (e.g., SMA fast 10–50 step 5, slow 20–200 step 20).
- Grid runs N backtests; renders 2D Stability Heatmap (already exists in `components.py:plot_2d_heatmap` but never called).
- Heatmap axes = the two parameters; color = selected metric (CAGR / Sharpe / DSR p-value).
- Hover cell shows exact parameter combo + metric.

**CPCV / Overfitting Diagnostics:**
- "Run CPCV" button.
- Shows: PBO (Probability of Backtest Overfitting), number of paths, embargo size.
- Result card: "PBO = 0.34 — Moderate overfitting risk" with copy explaining what to do (reduce parameter count, expand universe, increase embargo).

**DSR p-value:**
- Deflated Sharpe Ratio p-value shown next to Sharpe on KPI strip.
- Tooltip: "Probability that this Sharpe is due to chance given multiple testing."
- Red badge if p > 0.05 ("Not statistically significant"), green if p < 0.05.

**IS/OOS Comparison:**
- Tabs: In-Sample / Out-of-Sample / Combined.
- Side-by-side equity curves + metric deltas.
- Warns if OOS Sharpe << IS Sharpe (overfitting signal).

**User actions:**
- Select parameters for grid.
- Choose metric for heatmap color.
- Click Run Grid / Run CPCV.
- Toggle IS/OOS tabs.

**System response:**
- Grid/CPCV are compute-heavy → dedicated loading state with progress (e.g., "Run 12/45").
- Can be cancelled (abort button).
- Results persist to cache.

**Edge cases:**
- Grid too large (>500 combos) → warning: "Large grid may take several minutes. Reduce parameter range?"
- CPCV with too few splits → error: "Need at least 3 splits for CPCV."
- DSR not computable (fewer than 30 trades) → show "Insufficient trades" instead of p-value.

---

### 1.7 Settings

**Sections:**
1. **Cost Model** — brokerage per trade, STT %, GST %, stamp duty %, slippage bps. Presets: Zerodha, Upstox, Angel One, Custom.
2. **Data Source** — local files (default), connected provider (future disabled state).
3. **Universe** — default watchlist symbols, data directory path.
4. **Appearance** — dark/light/system theme, chart theme.
5. **Account** — initial capital, position sizing (section 1.3).
6. **Danger Zone** — clear cache, reset all data, export data.

**User actions:** Toggle, type, select preset, save.

**System response:** Validates, writes config, shows "Saved" toast.

**Edge cases:**
- Invalid preset selection → falls back to Custom.
- Clearing cache while a run is active → blocked with toast: "Stop active backtest first."

---

### 1.8 Errors

| Error | Trigger | UI | Copy | Recovery |
|-------|---------|----|------|----------|
| No data | First launch, `data/raw/` empty | Full-page Empty State | "No market data found. Upload CSVs or use demo data to begin." | Upload / Connect / Demo |
| Bad upload | Wrong columns, corrupt, too large | Inline error card under uploader | "Unable to load [file]. Missing columns: close. Please check your file and try again." | Re-upload |
| Invalid params | slow <= fast, negative lookback | Inline field error under slider | "Slow window must be greater than fast window." | Fix slider |
| Engine crash | Exception during backtest | Full-width error banner + retry button | "Backtest failed. The engine encountered an unexpected error." | Retry with defaults / Contact support |
| No network (PWA) | Offline, no cached data | Offline State banner | "You're offline. Cached results only. Some features unavailable." | Reconnect |
| Corrupt cache | Bad local data file | Error modal on launch | "Your local data cache is corrupted. Would you like to reset it?" | Reset / Cancel |
| Insufficient trades | DSR / metrics not computable | Inline metric shows "—" | "Not enough trades to compute DSR significance." | Adjust params / longer timeframe |

**Error copy principles:**
- Never say "An error occurred" without saying what to do next.
- Human-readable, no stack traces.
- Every error has a labeled recovery action.

---

### 1.9 Empty States

| Context | When | Headline | Sub-headline | CTA |
|---------|------|----------|--------------|-----|
| No data (first launch) | `data/raw/` missing | No market data found | QuantLab needs historical prices to backtest. | Upload data / Demo data |
| No results | Dashboard fresh, never ran | No backtest results yet | Run a backtest to see performance metrics and equity curves. | Run Backtest |
| No trades | Ran but zero trades | No trades executed | Your strategy didn't trigger any signals with these parameters. Try widening the range or changing the timeframe. | Adjust parameters |
| No significance | DSR not computable | Not enough data for significance | DSR requires at least 30 trades. Run a longer backtest or loosen parameters. | Adjust parameters |

**Empty state pattern:**
- Illustration (48px–64px icon).
- Headline (h3, semantic color).
- Sub-headline (muted, 1 line max).
- One primary CTA button + optional secondary text link.
- Centered vertically in the content area; sidebar remains visible.

---

### 1.10 Loading States

| Context | When | UI |
|---------|------|----|
| Initial data load | First load, parsing CSVs | Skeleton cards in place of metrics/charts; subtle "Loading data…" |
| Backtest running | After Run button | Full-page or panel overlay: spinner + "Running backtest…" + elapsed time + Cancel button |
| Grid / CPCV running | Advanced workflow | Progress bar: "Run 12 / 45" + cancel |
| File upload | During parse | Inline spinner on upload button |

**Loading pattern:**
- Never leave a blank screen where content should be.
- Show skeleton state shaped like final content (metric cards, chart placeholders) to prevent layout shift.
- Backtest loading includes Cancel (aborts engine, returns to previous state).
- Time elapsed shown (e.g., "Running backtest… 3.2s").

---

### 1.11 Offline States (PWA / Cached Data Only)

**Trigger:** No network + PWA installed / service worker active.

**UI:**
- Persistent top banner (dismissible): "You're offline. Viewing cached data."
- Cloud-dependent features disabled (future data connectors, sync, export to cloud) with disabled-state styling and tooltip: "Available when online."
- Local features fully functional: run backtests on cached data, view saved results, adjust settings.

**User actions:** Reconnect (banner has "Retry connection" link).

**System response:**
- Service worker serves cached shell + data.
- Queues any write actions (save report, export) for sync on reconnect; shows sync badge when pending.

**Edge cases:**
- Offline + no cache at all → Empty State: "No cached data available offline."
- Comes back online → sync queue processes, banner clears, toast: "Synced."

---

### 1.12 Recovery Flows

| Scenario | Detection | Recovery UI |
|----------|-----------|-------------|
| App crash mid-backtest | On next launch, `session_state` has incomplete run flag | Toast: "A previous backtest didn't finish. Discard results and start fresh?" [Discard] [Resume if possible] |
| Corrupted data file | Load fails validation on startup | Error modal: "Data cache is corrupted. Reset to defaults?" [Reset] [Cancel] → reset wipes `data/raw/` cache, shows Empty State |
| Corrupted config | Config parse fails on launch | Silent fallback to defaults + toast: "Settings reset to defaults." |
| Engine exception | Try/catch around BacktestEngine.run() | Error banner with "Retry with defaults" (resets params to strategy defaults, re-runs) |
| Browser tab closed | N/A (local-first) | On reopen, last result restored from cache; no data loss |

---

## 2. Information Architecture

### Navigation Structure (Desktop)

```
QuantLab
├── Dashboard (main)
│   └── Run Backtest → Results inline
├── Advanced
│   ├── Parameter Grid (2D Heatmap)
│   ├── CPCV / Overfitting (PBO)
│   └── IS/OOS Comparison
├── Settings
│   ├── Cost Model
│   ├── Data Source
│   ├── Universe
│   ├── Appearance
│   └── Account
└── Help / Docs
    ├── Onboarding (relaunch)
    ├── Keyboard shortcuts
    └── About
```

**Mobile (PWA):**
- Bottom tab bar: Dashboard | Advanced | Settings | Profile.
- Hamburger menu for secondary (Help, About, Sign out).
- Dashboard collapses sidebar into a "Configure" drawer overlay.

**URL routing (if migrated from pure Streamlit):**
- `/` Dashboard
- `/advanced/grid`
- `/advanced/cpcv`
- `/settings`
- `/settings/costs`
- `/results/[run-id]`

*Note: Current Streamlit uses `st.sidebar` + `st.stop()`; target architecture keeps the same mental model but adds route-like section headers and persistent navigation.*

---

## 3. Visual Design Direction

### Theme
- **Default:** Dark theme (finance terminals, TradingView, Bloomberg aesthetic). Reduces eye strain for screen-staring traders; signals "serious tool."
- **Light:** Available via Appearance toggle; system-follows-OS by default.
- **Chart template:** `plotly_dark` for dark mode; `plotly_white` for light. Replace current hardcoded `template="plotly_white"`.

### Color Semantics (Finance)

| Meaning | Color | Usage |
|---------|-------|-------|
| Profit / Gain / Up | `#0ECC71` (green) | Positive returns, equity curve up |
| Loss / Drawdown / Down | `#FF4D4F` (red) | Drawdown fill, negative P&L |
| Neutral / Info | `#5B6BC0` (indigo) | Primary actions, neutral metrics |
| Warning / Caution | `#FAAD14` (amber) | DSR not significant, data gaps |
| Error / Danger | `#FF4D4F` (red) | Error banners, invalid fields |
| Success | `#52C41A` | Saved, completed |
| Muted text | `#8C94A6` | Sub-headlines, captions |
| Surface bg | `#0F172A` (dark slate) | App background |
| Card bg | `#1E293B` | Metric cards, panels |
| Border | `#334155` | Dividers, input borders |

### Typography
- Headlines: Inter / system sans-serif, 600 weight.
- Metric values: Mono (JetBrains Mono / Consolas) for numbers — trading-terminal feel.
- Body: Inter, 14px.

### Layout Tokens
- Sidebar width: 280px (desktop), full-width drawer (mobile).
- Content padding: 24px.
- KPI cards: 4-up desktop, 2-up tablet, 1-up mobile.
- Border radius: 8px cards, 4px inputs/buttons.
- Elevation: subtle borders (no heavy shadows in dark mode).

### Chart Standards
- All charts: interactive Plotly, `use_container_width=True`, dark template by default.
- Equity curve: line, green when above starting capital, red when below.
- Drawdown: fill-to-zero red, as current `plot_drawdown_underwater`.
- Heatmap: Viridis (existing `plot_2d_heatmap`), now actually wired.
- Missing charts to add: Profit Mirage waterfall (costs ON vs OFF overlay), IS/OOS side-by-side equity curves.

---

## 4. The "Profit Mirage" Moment (Hero Demo)

**Concept:** The single most compelling QuantLab differentiator — show how transaction costs turn a "profitable" backtest into a losing one. Named after the retail complaint: *"fees turned profits negative."*

**UI placement:** Dedicated hero section below KPI strip on Dashboard, above equity curves.

```
┌─────────────────────────────────────────────────────────────┐
│  Profit Mirage                                              │
│  See how costs change the story                             │
│                                                             │
│  [ Costs: ON ───────●─────── OFF ]   ← toggle (default ON)  │
│                                                             │
│  Equity curve overlay:                                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Without costs  ───────────────────  ↗  +12.4%       │   │
│  │  With costs     ───────────────────  ↘   −3.1%       │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  "Costs wiped out ₹15,400 of profit (15.5% of gross return)"│
└─────────────────────────────────────────────────────────────┘
```

**Behavior:**
- Default: Costs ON (honesty by default). User sees realistic result first.
- Toggle to OFF: second equity curve fades in (dashed line), showing the "mirage" profit.
- Delta callout card auto-computes: gross return − net return = cost drag, in ₹ and %.
- Toggle is sticky across session; persists to settings.
- First time user sees it: subtle pulse animation draws eye; onboarding step 2 previews it.

**Copy:**
- Headline: "Profit Mirage — see the cost of trading."
- Sub-headline: "Backtests that ignore fees lie. Toggle to see the real picture."
- Costs ON label: "Realistic (fees + slippage)"
- Costs OFF label: "Backtest myth (gross)"
- Delta card: "Costs ate ₹X,XXX (Y.Y% of gross profit)"
- Tooltip on toggle: "Includes brokerage, STT, GST, stamp duty, slippage."

---

## 5. Mobile-Responsive Considerations (PWA/Web)

- **Breakpoints:** ≤640px mobile, 641–1024px tablet, >1024px desktop.
- **Sidebar → Drawer:** On mobile, configuration is a slide-over drawer triggered by a "Configure" floating action button; results take full screen.
- **KPI strip:** 4 cards stack vertically on mobile (1 column), 2×2 on tablet, 1×4 on desktop.
- **Charts:** full-width, touch-interactive (Plotly handles zoom/pan); height reduced on mobile (240px vs 400px).
- **Heatmap:** horizontal scroll on mobile; metric selector above.
- **Sliders:** full-width, large touch targets (min 44px).
- **PWA:** service worker caches shell + last result; install prompt after first backtest run; offline banner when disconnected.
- **No hover-dependent interactions:** all info revealed on tap/click; tooltips become tap-to-show.

---

## 6. Empty State Copy

**No data (first launch):**
> Headline: No market data found
> Body: QuantLab needs historical price data to run backtests.
> Primary: Upload market data
> Secondary: Use demo data · Connect data source

**No results:**
> Headline: No backtest results yet
> Body: Run a backtest to see performance metrics, equity curves, and overfitting diagnostics.
> Primary: Run Backtest

**No trades:**
> Headline: No trades executed
> Body: Your strategy didn't trigger any signals with these parameters. Try widening the parameter range or extending the timeframe.
> Primary: Adjust parameters

**Not significant (DSR):**
> Headline: Not enough data for significance
> Body: DSR requires at least 30 trades to compute statistical significance. Run a longer backtest or loosen parameters.
> Primary: Adjust parameters

**Offline, no cache:**
> Headline: You're offline
> Body: No cached data is available. Reconnect to load data and run backtests.
> Primary: Retry connection

---

## 7. Error Copy

**Bad upload:**
> Unable to load "[file]". Missing required columns: date, close. Please check your file and try again.
> [Try again]

**Too large:**
> File exceeds 500MB. Please upload a smaller file or split it.
> [Try again]

**Invalid params:**
> Slow window must be greater than fast window.
> (inline under slider)

**Engine crash:**
> Backtest failed. The engine encountered an unexpected error.
> [Retry with defaults] [Dismiss]

**Corrupt cache:**
> Your local data cache is corrupted. Would you like to reset it? You'll need to re-upload data.
> [Reset] [Cancel]

**No network (PWA):**
> You're offline. Viewing cached data only. Some features are unavailable.
> [Retry connection]

**Insufficient trades:**
> Not enough trades to compute DSR significance. Run a longer backtest or loosen parameters.

---

## 8. Comparison: Current Streamlit MVP vs. Target Product UI

| Area | Current MVP (`app.py` 64 lines) | Target Product |
|------|---------------------------------|----------------|
| First launch | `st.stop()` with warning if `data/raw/` missing | Full empty state with upload/demo/connect CTAs |
| Onboarding | None | 4-step wizard, skippable |
| Account/setup | None | Local settings (capital, costs, theme, data source) |
| Main screen | Single page, sidebar + 4 metrics + 2 charts | Zoned layout: KPI strip, Profit Mirage hero, charts, IS/OOS tabs |
| Core workflow | Run button, spinner, render | Run with validation, cancel, loading skeleton, cached results |
| DSR p-value | Not computed/shown | Badge on KPI strip + tooltip |
| 2D heatmap | Exists in `components.py`, never called | Wired into Advanced Parameter Grid |
| Profit Mirage | Cost toggle exists, no overlay | Hero section with ON/OFF equity overlay + cost-drag callout |
| IS/OOS | None | Tabs + side-by-side equity + delta |
| Empty states | Warning + `st.stop()` | Designed empty states with copy + CTAs |
| Error states | None / Python traceback | Human-readable error cards with recovery actions |
| Loading states | `st.spinner` only | Skeletons, elapsed time, cancel, progress bar |
| Offline | Hard-fails | PWA cache + offline banner |
| Recovery | None | Crash resume, corrupt-cache reset, config fallback |
| Visual | Streamlit default (`plotly_white`, white bg) | Dark-first finance theme, indigo/green/red semantics |
| Mobile | Streamlit responsive (basic) | PWA, drawer sidebar, stacked KPIs, touch targets |

---

## 9. Priority Ranking: P0 / P1 / P2

### P0 — Must ship (blocks "serious product" credibility)
1. **Empty state on first launch** — replace `st.stop()` with designed empty state + upload/demo CTAs.
2. **Error states** — human-readable copy + recovery for bad data, invalid params, engine crash, corrupt cache.
3. **Loading states** — skeleton + cancel + elapsed time (replace bare `st.spinner`).
4. **DSR p-value on KPI strip** — compute from `src/analytics/deflated_sharpe.py`, badge + tooltip.
5. **Wire 2D heatmap** — call `plot_2d_heatmap` in Advanced Parameter Grid.
6. **Profit Mirage hero** — costs ON/OFF equity overlay + cost-drag callout (toggle already exists in `app.py:32`, just needs visual wiring).
7. **Dark theme** — switch Plotly template to `plotly_dark` by default; indigo/green/red color semantics.

### P1 — Should ship (differentiates from CRUD app)
8. Onboarding wizard (4 steps, skippable).
9. IS/OOS comparison tabs.
10. Settings panel (cost model presets, universe, appearance, data source).
11. Local caching of last result (offline viewing).
12. Parameter grid sweep UI (Advanced view).
13. Mobile-responsive layout (drawer sidebar, stacked KPIs).

### P2 — Nice to have (polish / PWA)
14. PWA install prompt + service worker + offline banner + sync queue.
15. CPCV / PBO overfitting diagnostic panel.
16. Save/load templates, export reports.
17. Account/user name, default capital, position sizing.
18. Connected data source (future provider integration).
19. Keyboard shortcuts, help/docs.

---

## 10. Implementation Notes (for Engineering)

- **Keep `st.session_state`** as the client-side store; persist last result + config to `data/cache/` (local JSON/Parquet) for offline/recovery.
- **Validation before run:** check `slow > fast` for SMA, `period > 0`, data non-empty. Return inline errors, not exceptions.
- **Cache key for results:** `{strategy}_{params}_{costs_on}_{data_hash}` so cost-toggle flips re-render without re-running the engine.
- **DSR:** import from `src/analytics/deflated_sharpe.py`; guard `len(trades) < 30` → show "—" instead of p-value.
- **Heatmap:** reuse `components.py:plot_2d_heatmap`; add metric selector (CAGR / Sharpe / DSR p-value).
- **No new dependencies beyond plotly/streamlit/pandas** already in `requirements.txt`.

---

## 11. Acceptance Criteria (Definition of Done)

- [ ] First launch with empty `data/raw/` shows designed empty state, not `st.stop()`.
- [ ] Every user-facing error has copy + a labeled recovery action; no raw tracebacks reach the user.
- [ ] Backtest run shows loading state with cancel + elapsed time; never a blank screen.
- [ ] DSR p-value badge renders on KPI strip when ≥30 trades; "—" otherwise.
- [ ] 2D heatmap renders in Advanced Parameter Grid (previously dead code in `components.py`).
- [ ] Profit Mirage toggle shows ON/OFF equity overlay + cost-drag ₹ and % callout.
- [ ] Default theme is dark; Plotly charts use `plotly_dark`.
- [ ] Invalid parameter combos block Run with inline field error.
- [ ] Last result persists to local cache and restores on reopen (offline-capable shell).

---

**End of document.** Save to `/mnt/work/projects/Quantlab/UX_ARCHITECTURE.md`.
