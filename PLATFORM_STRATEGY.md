# QuantLab Platform Strategy

**Product:** QuantLab — event-driven backtesting & overfitting diagnostic engine for Indian equities
**Audience:** Mobile / Desktop Engineer subagent
**Status:** Recommendation (pre-implementation)

---

## 1. Executive Summary

**Recommended stack:**

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Core engine | Python (pandas/numpy) — unchanged | Reuses ~1,008 LOC existing investment; no rewrite |
| Desktop (Linux/Windows/macOS) | **PyInstaller** or **Briefcase** wrapping Streamlit | Reuses Python directly; single codebase; fastest path |
| Web / Mobile-browser | Streamlit deployed (Streamlit Cloud / self-hosted) + **PWA manifest** | Gives cross-platform reach incl. mobile browsers without native mobile dev |
| Native mobile (Android/iOS) | **Deferred** — PWA wrapper only | Native mobile requires engine rewrite or client-server; not justified for this repo |

**Where computation runs:** 100% **local, client-side** (in-process Python). No backend, no API, no cloud dependency.

**Shared vs platform-specific:** 100% of engine/analytics/data code shared. UI layer is the only platform-specific surface (Streamlit for desktop/web; thin PWA shell for mobile browsers).

---

## 2. Constraint Analysis (Why This Repo Dictates the Stack)

| Constraint | Evidence in repo | Implication |
|-----------|-----------------|-------------|
| Core engine is Python | `src/engine/` (~8 files), pandas/numpy heavy | Mobile native (Kotlin/Dart/JS) cannot reuse it directly |
| No backend/API | `requirements.txt` has no FastAPI/Flask; no server code | Client-server is an added architectural cost, not a free option |
| Local in-process computation | `BacktestEngine.run()` executes in-process | Offline-first desktop works naturally; mobile needs Python-on-mobile or server |
| Daily bars, 10-symbol Indian universe | `src/data/universe.py`, README scope | Light compute load — local client machine is sufficient |
| Streamlit + Plotly UI (~96 LOC total) | `app.py:64`, `components.py:32` | Thin UI layer; easy to port/wrap |
| GTU academic project (DI05000341) | README, `DI05000341.pdf` | Small team, timeline-constrained; avoid immature mobile-Python stacks |

**The key constraint:** Reusing the Python engine on mobile requires one of:
1. Python-on-mobile (Kivy/BeeWare) — immature, performance concerns, APK size
2. Rewrite engine in Dart/JS/Kotlin — loses existing code investment
3. Client-server — adds backend ops burden contrary to repo's "no backend" design

Given the academic scope and daily-bar compute load, **local Python execution on desktop is the sweet spot**; mobile is reached via browser/PWA, not native.

---

## 3. Option-by-Option Evaluation

### 1. Native Android (Kotlin)
- **Verdict:** Reject for v1
- **Pros:** Best Android UX, Play Store distribution
- **Cons:** Cannot reuse Python engine; full rewrite of engine + UI in Kotlin; no iOS; two codebases if desktop also wanted
- **Fit for this repo:** Poor — throws away the Python investment

### 2. Flutter (Dart)
- **Verdict:** Reject for v1
- **Pros:** Mobile + desktop from one Dart codebase, nice UI
- **Cons:** Cannot reuse Python directly; engine rewrite required; Dart/Python bridge adds complexity
- **Fit for this repo:** Poor

### 3. React Native (JS)
- **Verdict:** Reject for v1
- **Pros:** Mobile (Android/iOS), large ecosystem
- **Cons:** Mobile-only (no desktop); engine rewrite; bridge complexity
- **Fit for this repo:** Poor

### 4. Tauri (Rust + web frontend)
- **Verdict:** Consider for v2 desktop
- **Pros:** Small binary, native desktop feel, web frontend
- **Cons:** Python integration requires PyO3 or sidecar (adds build complexity); Rust learning curve; mobile support immature
- **Fit for this repo:** Medium — good desktop alternative if Streamlit wrapper feels "web-app-like"

### 5. Electron (Node + Chromium)
- **Verdict:** Reject
- **Pros:** Mature desktop packaging, Python via child process
- **Cons:** Heavy binary (~100+ MB), Node bridge complexity, overkill for a local backtest tool
- **Fit for this repo:** Poor

### 6. PyInstaller / Briefcase (Python desktop)
- **Verdict:** **Recommended for desktop**
- **Pros:** Reuses Python engine directly; single codebase; offline; no new language; well-understood; small binary relative to Electron
- **Cons:** PyInstaller single-file can trigger AV false positives; Briefcase mobile targets immature
- **Fit for this repo:** Excellent — aligns with "reuse Python" constraint

### 7. Streamlit + PyInstaller (quick desktop path)
- **Verdict:** **Recommended (fastest desktop path)**
- **Pros:** Existing `app.py`/`components.py` work unchanged; wrap with PyInstaller; minutes to package
- **Cons:** Feels like a web app in a window (acceptable for internal/academic tool)
- **Fit for this repo:** Best time-to-value

### 8. PWA (web)
- **Verdict:** Recommended for mobile reach
- **Pros:** Works on mobile browsers; no app store; "installable" via manifest; shares desktop UI
- **Cons:** Limited offline storage, iOS PWA restrictions, yfinance needs network
- **Fit for this repo:** Good — gives mobile-browser access without native mobile dev

### 9. Kivy / BeeWare (Python mobile)
- **Verdict:** Reject for v1
- **Pros:** Reuses Python on mobile
- **Cons:** Immature toolchains, APK/IPA size, performance concerns, limited community, debugging hard
- **Fit for this repo:** Poor — academic project can't afford toolchain risk

---

## 4. Recommended Stack & Placement

### Phase 1 — Desktop (Linux/Windows/macOS)
- **Packaging:** PyInstaller (one-dir or one-file) or Briefcase
- **UI:** Existing Streamlit `app.py` + `components.py`, unchanged
- **Compute:** Local Python process; `yfinance` fetches data at runtime; backtest runs in-process
- **Distribution:** Executable installer / ZIP; no app store required

### Phase 2 — Web / Mobile-browser
- **Hosting:** Streamlit Cloud (free tier) or self-hosted on any server
- **PWA:** Add `manifest.json` + service worker so mobile users can "install" to home screen
- **Compute:** Runs on the server OR client-local if packaged; for Streamlit Cloud, compute is server-side (acceptable since no sensitive IP)
- **Mobile UX:** Streamlit is responsive; touch-friendly sliders/buttons work on mobile browsers

### Phase 3 (Deferred) — Native mobile
- Only if a stakeholder demands Play Store/App Store presence
- Option A: PWA → Trusted Web Activity (TWA) wrapper for Android (minimal native code)
- Option B: Thin client + Python backend (FastAPI) — contradicts current "no backend" design; only if compute must move off-device

---

## 5. Shared vs Platform-Specific Code

```
shared/ (100% Python, zero platform code)
  src/engine/        backtest engine — unchanged
  src/analytics/     DSR, CPCV, metrics — unchanged
  src/data/          fetch, clean, universe — unchanged
  src/strategies/    SMA, RSI, Momentum — unchanged

platform/desktop/
  src/dashboard/     Streamlit app.py, components.py — unchanged, wrapped by PyInstaller
  packaging/         PyInstaller spec, Briefcase config, installer scripts

platform/web/
  manifest.json      PWA manifest (mobile home-screen install)
  streamlit config   headless, port, CORS for cloud hosting

platform/mobile/     (deferred — none in v1)
```

**Rule:** Zero engine logic is duplicated or rewritten. Any mobile/desktop difference lives only in the UI shell and packaging config.

---

## 6. UI Strategy

- **Keep Streamlit** for desktop + web. It's already written (~96 LOC), responsive, and requires no frontend build step.
- **Plotly charts** (`components.py`) render identically in Streamlit desktop and browser.
- **No new UI framework** for v1. Avoid introducing Flutter/Dart/React/Native UI code.
- **Mobile-browser:** Streamlit's mobile layout is acceptable; add PWA manifest for home-screen installability.
- **Desktop packaging:** Streamlit runs in a local browser window via PyInstaller; alternatively use `streamlit run` with `--browser.gatherUsageStats=false`.

---

## 7. Where Computation Runs

| Scenario | Location | Reasoning |
|----------|----------|-----------|
| Backtest engine | Local client (in-process Python) | Already works; no latency; offline capable |
| Data fetch (`yfinance`) | Local client → Yahoo Finance | Needs network; no API key; academic use |
| Metrics (DSR, CPCV) | Local client | Pure pandas/numpy; cheap |
| Mobile browser (PWA) | Server (Streamlit Cloud) OR local | If hosted, compute moves to server — acceptable for this non-sensitive academic tool |

**No backend API is introduced.** Adding FastAPI + mobile thin-client would double the codebase and violate the repo's "no backend" design principle.

---

## 8. Why This Stack Is Appropriate for THIS Repository

1. **Reuses the existing investment.** ~1,008 LOC of Python engine stays untouched. No rewrite in Kotlin/Dart/JS/Rust.
2. **Matches the architecture.** The engine is local, in-process, synchronous. Desktop Python packaging fits naturally; client-server would be a forced mismatch.
3. **Fits the team/timeline.** GTU academic project, small team. PyInstaller + Streamlit is hours of work, not months.
4. **Cross-platform reach without native mobile.** Desktop (executable) + web/PWA (mobile browser) covers Android/iOS/Windows/Linux/macOS from one codebase.
5. **No new dependencies/languages.** requirements.txt already has everything needed (pandas, numpy, streamlit, plotly, yfinance). PyInstaller is the only addition.

---

## 9. Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| PyInstaller AV false positives | Use one-dir build, sign executable, or distribute via Briefcase |
| Streamlit "web app in a window" feel | Acceptable for internal/academic tool; Tauri (v2) if native chrome needed |
| yfinance rate limits / network dependency | Cache data locally (`data/raw/`); document offline limitation |
| iOS PWA limitations | PWA is reach, not primary target; native iOS deferred |
| Mobile compute if hosted on Streamlit Cloud | Server-side compute is fine for daily-bar backtests on 10 symbols |

---

## 10. Decision

**Build desktop-first via PyInstaller/Briefcase wrapping the existing Streamlit UI. Add PWA manifest for mobile-browser reach. Defer native mobile entirely.** Computation stays local and Python-based. No backend, no engine rewrite, no new language.
