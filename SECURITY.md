# Security & Privacy Threat Model — QuantLab

**Document owner:** Security Engineering  
**Scope:** QuantLab backtesting engine (Python), GTU DI05000341 Minor Project  
**Status:** Draft / pre-release  
**Last updated:** 2026-10-16

---

## 1. Executive Summary

QuantLab is a local, event-driven backtesting engine for Indian equities built on pandas, numpy, streamlit, yfinance, plotly, and scipy. It fetches historical OHLCV data from Yahoo Finance via the unofficial `yfinance` scraper, stores it as plaintext CSV under `data/raw/`, and runs strategy simulations through a Streamlit dashboard.

**Security posture:** The application currently has **no authentication, no authorization, no encryption, no secrets management, no code signing, no input validation on strategy parameters, no sandboxing, and no privacy policy**. Data is stored in plaintext on the local filesystem. The application has no network exposure beyond the outbound yfinance fetch to Yahoo Finance.

Because the application is local-only with no accounts, no API, and no multi-user surface, several classic threats (spoofing of remote users, elevation of privilege across tenants, network-based DoS) are inherently limited. However, supply-chain, data-integrity, privacy, and legal/compliance risks are material and must be addressed before any release or commercial use.

---

## 2. Trust Boundaries

| Boundary | Description | Trust Level | Controls Today |
|----------|-------------|-------------|----------------|
| **Local host / user** | The machine running QuantLab; the user has full filesystem access. | Trusted (single-user, local) | None |
| **`data/raw/` directory** | Plaintext CSV storage of fetched OHLCV data. | Trusted local storage | None — plaintext, no integrity checks |
| **Streamlit dashboard** | Local UI exposing strategy parameters and backtest execution. | Trusted local UI | None — no auth, no validation |
| **Strategy code** | User-selectable / user-extendable strategy classes executed in-process. | Untrusted if user-supplied | None — no sandboxing |
| **yfinance → Yahoo Finance** | Outbound network fetch of public market data. | Untrusted external source | None — no signature/pin verification |
| **PyPI / package index** | Dependency source (pandas, numpy, yfinance, scipy, streamlit, plotly). | Partially trusted | None — unpinned/transitive deps not pinned |
| **OS / Python interpreter** | Underlying runtime executing QuantLab. | Trusted | None |

**Key trust assumption:** The operator of the local machine is the sole trusted actor. Anything executed within the QuantLab process (including user-supplied strategy code) runs with the full privileges of that user.

---

## 3. Attack Surface

### 3.1 In-scope attack vectors
1. **Local file read/write** — `data/raw/*.csv`, any local files the process can access (the process runs with user privileges).
2. **Streamlit dashboard inputs** — strategy parameter sliders (fast/slow window, RSI period, lookback) fed directly into strategy constructors with no type/range validation beyond the UI slider bounds.
3. **Strategy execution** — `generate_signals` runs arbitrary user-defined logic in the same process as the engine.
4. **yfinance network fetch** — DNS + HTTP to Yahoo Finance; response parsed and persisted without integrity verification.
5. **Dependency installation** — `pip install -r requirements.txt` pulls transitive dependencies from PyPI.
6. **Local execution of `python src/...`** — arbitrary code execution via the repository itself.

### 3.2 Out-of-scope (by design)
- Live brokerage execution (QuantLab does not connect to brokers).
- Multi-user / SaaS deployment (no backend, no API, no accounts).
- Intraday / tick data (daily bars only).
- Derivatives (options/futures not supported).

---

## 4. Sensitive Data Inventory

| Data | Location | Sensitivity | Protection Today |
|------|----------|-------------|------------------|
| OHLCV market data (public) | `data/raw/*.csv` | Low (public market data) | Plaintext |
| Strategy parameters (user-configured) | Streamlit session state (ephemeral) | Low | None |
| Backtest results / equity curves | In-memory only (ephemeral) | Low | None |
| User identity / credentials | N/A (no accounts) | N/A | N/A |
| API keys / secrets | N/A (none used) | N/A | N/A |
| Process memory | RAM | Low | None |

**Conclusion:** No high-sensitivity PII, credentials, or financial account data is handled by QuantLab today. The primary sensitive assets are integrity of market data and integrity of backtest results.

---

## 5. STRIDE Threat Model

### Spoofing
| Threat | Description | Impact | Likelihood | Rating | Mitigation |
|--------|-------------|--------|------------|--------|------------|
| Impersonation of Yahoo Finance | MITM or DNS spoofing of yfinance fetch returns falsified OHLCV data. | Backtest results based on falsified data; silent integrity failure. | Medium (unauthenticated HTTP, no pinning) | Medium | Pin Yahoo Finance host/TLS, verify response schema, consider licensed vendor data. |
| Spoofed local strategy module | A malicious `src/strategies/*.py` file masquerades as a legitimate strategy. | Arbitrary code execution with user privileges. | Low (local file write required) | Low | Code signing / integrity checks on strategy modules. |

### Tampering
| Threat | Description | Impact | Likelihood | Rating | Mitigation |
|--------|-------------|--------|------------|--------|------------|
| Local CSV tampering | Attacker with local access edits `data/raw/*.csv` to alter OHLCV values. | Backtest produces misleading performance metrics. | High (plaintext, local write) | High | Encrypt-at-rest, file integrity hashes, read-only data directory where possible. |
| Dependency tampering | Compromised PyPI package or typosquatting in `requirements.txt` transitive deps. | Supply-chain code execution. | Medium | High | Pin all dependencies, use hashes (`--require-hashes`), private/internal index. |
| Strategy parameter manipulation | UI sliders allow extreme or invalid parameter values (no server-side validation). | Backtest errors or misleading metrics. | Low | Low | Input validation on strategy constructors. |

### Repudiation
| Threat | Description | Impact | Likelihood | Rating | Mitigation |
|--------|-------------|--------|------------|--------|------------|
| No audit trail | No logging of which user ran which backtest with which parameters/data. | Cannot attribute actions; no non-repudiation. | High (no logging) | Medium | Add structured audit logging (user, timestamp, strategy, parameters, data source, output hash). |

### Information Disclosure
| Threat | Description | Impact | Likelihood | Rating | Mitigation |
|--------|-------------|--------|------------|--------|------------|
| Local plaintext data | `data/raw/*.csv` readable by any local user/process. | Disclosure of watched symbols / user's universe of interest. | High | Low (data is public) | Encrypt-at-rest, filesystem permissions. |
| Streamlit session data | Strategy params/results in browser session; no TLS (localhost only). | Local network eavesdropping if exposed beyond localhost. | Low | Low | Bind to localhost only; TLS if remotely exposed. |
| yfinance metadata | Yahoo Finance may log IP/UA of fetcher. | User's data-fetching activity visible to Yahoo. | Medium | Low | Use licensed data vendor; limit fetch frequency. |

### Denial of Service
| Threat | Description | Impact | Likelihood | Rating | Mitigation |
|--------|-------------|--------|------------|--------|------------|
| Yahoo Finance rate limiting / blocking | yfinance is an unofficial scraper; Yahoo may block or throttle the IP. | Data fetch fails; backtests cannot run with fresh data. | High (unofficial scraper) | High | Cache data locally, add retry/backoff, switch to licensed vendor, respect rate limits. |
| Excessive strategy parameter ranges | Very large lookback/window values cause long compute or memory spikes. | Local DoS of the dashboard process. | Low | Low | Input validation, parameter caps, execution timeout. |
| Large universe download | `download_universe` over many symbols may exhaust local disk/network. | Local resource exhaustion. | Low | Low | Limit universe size, disk-space check. |

### Elevation of Privilege
| Threat | Description | Impact | Likelihood | Rating | Mitigation |
|--------|-------------|--------|------------|--------|------------|
| In-process strategy code execution | User-supplied strategy runs with full user privileges; no sandbox. | Arbitrary code execution, file system access, environment variable exfiltration. | Low (local only) | Medium | Sandbox strategy execution (seccomp/restricted Python), run as unprivileged user, code signing. |
| Streamlit RCE via crafted input | Streamlit vulnerabilities exploited through the local dashboard. | Code execution with user privileges. | Low | Low | Keep Streamlit pinned/updated, bind localhost only. |

---

## 6. Attack Surface Summary

| Vector | Entry Point | Asset at Risk | Current Controls |
|--------|-------------|---------------|------------------|
| Local filesystem | `data/raw/` | Market data integrity | None (plaintext) |
| Streamlit UI | Sidebar parameters | Strategy integrity | UI slider bounds only |
| Python process | Strategy modules | Full host compromise | None (no sandbox) |
| Network (outbound) | yfinance → Yahoo | Data integrity, availability | None (no pinning, no retry) |
| Supply chain | PyPI dependencies | Code execution | None (partial pinning, scipy missing) |

---

## 7. Authentication Model Recommendation

**Current state:** No users, no accounts, no authentication. Single-user local application.

**Recommendation:** Because QuantLab has no backend and no multi-user surface, **do not build authentication for the local desktop version**. Authentication should only be introduced if/when:
- A backend API or multi-user deployment is added, or
- The application is exposed over a network.

If authentication is added later:
- Use OIDC/OAuth2 (e.g., Keycloak, Auth0, or Google OIDC) rather than custom password storage.
- Store only hashed passwords (bcrypt/argon2) if local accounts are ever required.
- Session cookies with `HttpOnly`, `Secure`, `SameSite=Strict`.
- MFA for any account with access to stored data or strategy IP.

---

## 8. Authorization Model Recommendation

**Current state:** No authorization model; single user, no roles.

**Recommendation:** Maintain a **single-user, local-only trust boundary**. If multi-user support is added:
- Role-Based Access Control (RBAC) with roles: `Viewer` (read backtests), `Analyst` (run backtests), `Admin` (manage data/users).
- Resource-level permissions on backtest runs, strategy definitions, and data universes.
- Principle of least privilege: the backtest engine process should not have network or filesystem access beyond `data/` and its config.
- Mediate all strategy execution through a sandboxed worker; users cannot execute arbitrary code in the engine process.

---

## 9. Encryption Strategy

### At rest
| Asset | Recommendation | Priority |
|-------|----------------|----------|
| `data/raw/*.csv` (market data) | AES-256-GCM or age-encrypted local store; filesystem-level encryption (LUKS/BitLocker) as baseline. | Medium |
| Backtest results / equity curves | Encrypt if persisted; currently ephemeral/in-memory only. | Low |
| Any future credentials/secrets | Never store plaintext; use OS keyring or a secrets manager. | High |

### In transit
| Path | Recommendation | Priority |
|------|----------------|----------|
| yfinance → Yahoo Finance | Enforce HTTPS/TLS 1.2+; certificate pinning where feasible. | High |
| Streamlit dashboard (if network-exposed) | TLS termination; bind to `localhost` by default. | Medium |

**Immediate fix:** Add filesystem permissions (`0600` on data files) and document full-disk encryption as a deployment requirement.

---

## 10. Secret Management

**Current state:** No secrets used; no secret management.

**Recommendation:**
- Do not commit API keys, tokens, or credentials to git. Add `*.env`, `.env`, `secrets/`, `*.key` to `.gitignore`.
- If future integrations require API keys (licensed data vendor, broker API), use the OS keyring (`keyring` Python package) or environment variables loaded from a protected file (`0600`).
- Rotate any credentials on a 90-day schedule.
- Never log secrets or query parameters that may contain tokens.

---

## 11. Local Security

| Area | Recommendation |
|------|----------------|
| Process privileges | Run QuantLab as a non-root, unprivileged OS user. |
| Filesystem permissions | `data/raw/` and config files `0600` / `0700`; avoid world-readable data. |
| Sandboxing | Execute user-supplied strategy code in a restricted subprocess (seccomp-bpf, no network, read-only filesystem except output dir). |
| Code signing | Sign releases (Git + GPG, or `signify`/`minisign`) and verify signatures before execution. |
| Secure updates | No auto-update today. If added: signed artifacts over HTTPS, hash verification, rollback capability. |
| Logging | Structured audit logs: timestamp, user, action (fetch/backtest/export), strategy, parameters, output hash. Logs rotated, access-controlled. |
| Input validation | Validate all strategy parameters (type, range, `fast < slow`, positive lookback) at the strategy constructor, not just the UI. |

---

## 12. API Security

QuantLab has **no API** and **no backend**. This section applies only if an API is introduced in future:

- Expose via HTTPS only; bind to localhost by default.
- Authentication: OIDC/OAuth2 bearer tokens.
- Authorization: RBAC on endpoints.
- Input validation: schema-validated JSON bodies (e.g., Pydantic), reject unknown fields, enforce parameter bounds.
- Rate limiting: per-user/per-IP token bucket (e.g., 60 req/min).
- Request size limits; timeout on long-running backtests.
- CORS restricted to known origins; no `*` in production.
- Security headers: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Strict-Transport-Security`.
- No stack traces or internal details in error responses.

---

## 13. Abuse Prevention & Rate Limiting

| Control | Recommendation |
|---------|----------------|
| Yahoo Finance fetch rate | Respect yfinance/Yahoo rate limits; add exponential backoff and jitter; cache locally to avoid repeated fetches. |
| Universe download size | Cap number of symbols per download; validate symbol format (e.g., `RELIANCE.NS`); reject unreasonably large requests. |
| Backtest execution | Timeout per run; cap data window and symbol count; limit concurrent backtests to 1 (single-user local). |
| Strategy parameters | Enforce min/max on all numeric inputs; prevent extreme lookback/window values that cause memory/CPU spikes. |
| Local disk | Check available disk space before writing CSV outputs; prevent disk-fill abuse. |

---

## 14. Supply-Chain Risks

| Risk | Description | Severity | Release Blocker? | Fix Required |
|------|-------------|----------|------------------|--------------|
| yfinance ToS/legal risk | `yfinance` is an unofficial Yahoo Finance scraper, **not licensed for commercial redistribution** (per README). Commercial use may violate Yahoo's ToS. | Critical | Yes | Replace with licensed market-data vendor, or restrict to academic/personal use with clear ToS disclaimer; add legal review. |
| Missing scipy in requirements.txt | `scipy` is imported in the codebase but absent from `requirements.txt`; `pip install -r requirements.txt` will fail. | High | Yes | Add `scipy==<version>` to `requirements.txt`. |
| Unpinned transitive dependencies | `requirements.txt` pins direct deps but not transitive dependencies; `scipy` version unpinned if added. | Medium | No | Pin all dependencies with `pip freeze` / hash-checking (`--require-hashes`). |
| Typosquatting / compromised PyPI package | No hash verification of installed packages. | Medium | No | Use `pip install --require-hashes`; consider a private/internal package mirror. |
| No code signing | Releases unsigned; supply-of-trust not established. | Medium | No | Sign release artifacts (GPG/signify); verify on install. |

---

## 15. Dependency Risks

| Dependency | Risk | Mitigation |
|------------|------|------------|
| `yfinance==0.2.37` | Unofficial scraper; breaking changes when Yahoo alters HTML; legal/ToS risk; no SLA. | Pin exact version; plan migration to licensed vendor; add fallback cache. |
| `streamlit==1.33.0` | Local UI; potential XSS/RCE if exposed to network. | Bind localhost; keep pinned; monitor CVEs. |
| `pandas==2.2.2`, `numpy==1.26.4` | Core data/math; deserialization risks if loading untrusted pickles (CSV only — low risk). | Pin versions; avoid `pickle` for data exchange. |
| `scipy` (missing) | Missing from requirements; install failures. | Add to requirements with exact version. |
| `plotly==5.20.0`, `matplotlib==3.8.4` | Visualization only; low risk. | Pin versions. |
| `pytest==8.1.1` | Test-only dev dependency. | Pin; keep out of production builds. |

**Fix:** Regenerate `requirements.txt` with `pip freeze` after adding `scipy`, and add a `requirements-hashes.txt` or use `pip-compile`/`pip-sync` with hash verification.

---

## 16. Privacy Considerations

### India PDP Act (Digital Personal Data Protection Act, 2023)
QuantLab currently processes **no personal data** (only public market OHLCV data). If personal data is introduced (user accounts, email, watchlists):
- Obtain consent for processing; provide notice.
- Implement purpose limitation and data minimization.
- Honor data subject rights: access, correction, erasure, portability, grievance redressal.
- Data breach notification to the Data Protection Board and affected users.
- Store data within India or ensure lawful cross-border transfer.

### GDPR (if global users)
- Lawful basis for processing; consent where required.
- Data subject rights: access, rectification, erasure ("right to be forgotten"), portability, objection.
- Data Protection Impact Assessment (DPIA) if processing scales.
- Data breach notification within 72 hours to supervisory authority.
- Data retention limits and deletion on request.

### General privacy principles
- Do not log user IP addresses, location, or instrument watchlists unless necessary.
- Do not telemetry/phone-home by default.
- Provide a privacy policy and terms of service before release.

---

## 17. Data Retention Policy

| Data | Retention | Disposal |
|------|-----------|----------|
| OHLCV CSV (`data/raw/`) | Retain until manually deleted; no automatic retention. | Secure delete (overwrite) on removal. |
| Backtest results | Ephemeral (in-memory, session only). | Discarded on session end. |
| Audit logs (future) | 12 months minimum; then archive or delete. | Secure delete. |
| User account data (future) | Until account deletion; then purge per PDP/GDPR. | Secure delete; cryptographic erasure if encrypted. |

**Policy statement:** No data is retained beyond the local machine; QuantLab does not back up or sync user data to any cloud service. Users are responsible for local backups.

---

## 18. Account Deletion

**Current state:** No accounts exist; no account deletion functionality required.

**If accounts are added:**
- Provide a self-service account deletion mechanism (UI or API).
- On deletion: purge account credentials, personal data, and associated backtest results from all stores (including logs/backups where feasible).
- Confirm deletion to the user; retain only legally required records (e.g., transaction logs for compliance) in anonymized form.
- Confirm no backups retain the data, or cryptographically erase encrypted backups.

---

## 19. Export Functionality

**Current state:** Export is limited to local CSV writes via `download_universe` (already the storage format). No structured export of user data or backtest results beyond Streamlit display.

**Recommendations if export is added:**
- Export backtest results as JSON/CSV with user consent.
- Include only data the user owns or has rights to (public market data is fine; do not export vendor-proprietary data without license).
- Sanitize exports: no credentials, no internal identifiers, no PII.
- Export over a secure channel; checksum the exported file for integrity.
- Document export format and retention of exported copies is the user's responsibility.

---

## 20. Security Issues Requiring Fix Before Release

| # | Issue | Severity | Fix Required | Release Blocker |
|---|-------|----------|--------------|-----------------|
| 1 | yfinance ToS/legal risk — unofficial scraper, not licensed for commercial redistribution | Critical | Replace with licensed vendor OR restrict to academic/personal use with ToS disclaimer + legal review | Yes |
| 2 | `scipy` imported but missing from `requirements.txt` | High | Add `scipy==<exact version>` to requirements | Yes |
| 3 | No input validation on user strategy parameters | Medium | Add parameter validation at strategy constructors (type, range, `fast < slow`) | No |
| 4 | No sandboxing of strategy execution | Medium | Run user strategies in a restricted subprocess; drop privileges | No |
| 5 | No code signing of releases | Medium | GPG/signify sign release artifacts; verify on install | No |
| 6 | No secure update mechanism | Medium | Signed artifacts over HTTPS with hash verification; no auto-update until implemented | No |
| 7 | Local data stored in plaintext | Medium | Encrypt-at-rest (file-level or disk encryption); `0600` permissions | No |
| 8 | No privacy policy / terms | Medium | Publish privacy policy + terms; PDP Act/GDPR alignment | No (legal) |
| 9 | No audit logging | Low | Add structured audit logs for fetch/backtest/export actions | No |
| 10 | Unpinned transitive dependencies / no hash verification | Low | Pin all deps; `--require-hashes` | No |

---

## 21. Remediation Priority (Release Blockers First)

**P0 (must fix before release):**
1. Resolve yfinance ToS/legal risk (licensed vendor or academic-use restriction).
2. Add missing `scipy` to `requirements.txt` with pinned version.

**P1 (fix before production / any network exposure):**
3. Pin all dependencies with hash verification (`--require-hashes`).
4. Add input validation on strategy parameters.
5. Encrypt local data at rest; restrict filesystem permissions.
6. Publish privacy policy and terms of service.

**P2 (hardening, post-release):**
7. Add audit logging.
8. Add code signing and secure update mechanism.
9. Sandbox strategy execution.
10. Evaluate licensed market-data migration path.

---

## 22. Appendix: Assumptions & Limitations

- Single-user, local desktop application; no backend, no API, no accounts.
- No authentication/authorization model is required in the current scope.
- All threat ratings assume a local attacker with user-level access or a supply-chain attacker via PyPI/Yahoo.
- If the architecture changes (multi-user, SaaS, broker integration, live execution), this threat model must be revisited; several controls (authentication, authorization, API security, rate limiting) will become critical.
