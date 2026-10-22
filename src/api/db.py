from __future__ import annotations

import json
import logging
import os
import sqlite3
from typing import Any

logger = logging.getLogger(__name__)

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "pramaan_runs.db",
)

_db_initialized = False


def get_db() -> sqlite3.Connection:
    """Returns a SQLite connection configured with WAL mode for concurrent performance."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def init_db(force: bool = False):
    """Initializes tables and migrations. Idempotent; runs once per process by default."""
    global _db_initialized
    if _db_initialized and not force:
        return

    with get_db() as conn:
        # 1. Schema migrations table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version INTEGER PRIMARY KEY,
                description TEXT NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 2. Runs table (cached complete backtest runs)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS runs (
                run_id TEXT PRIMARY KEY,
                strategy TEXT NOT NULL,
                params_json TEXT NOT NULL,
                universe_json TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                initial_capital REAL NOT NULL,
                apply_costs INTEGER NOT NULL,
                total_return REAL NOT NULL,
                cagr REAL NOT NULL,
                sharpe REAL NOT NULL,
                sortino REAL NOT NULL,
                max_drawdown REAL NOT NULL,
                calmar REAL NOT NULL,
                dsr_p_value REAL,
                pbo REAL,
                total_friction REAL NOT NULL,
                execution_time_ms REAL NOT NULL,
                response_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_runs_created ON runs(created_at)")

        # 3. Trials table (FR-12 & D1/D7: ledger of all strategy/param trials tested)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS trials (
                trial_id INTEGER PRIMARY KEY AUTOINCREMENT,
                strategy TEXT NOT NULL,
                params_json TEXT NOT NULL,
                universe_json TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                sharpe REAL NOT NULL,
                total_return REAL NOT NULL,
                max_drawdown REAL NOT NULL,
                run_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_trials_strategy ON trials(strategy)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_trials_created ON trials(created_at)")

        # Mark migration v1 applied
        conn.execute(
            "INSERT OR IGNORE INTO schema_migrations (version, description) VALUES (1, 'initial_runs_and_trials_schema')"
        )
        conn.commit()

    _db_initialized = True


def record_trial(
    strategy: str,
    params: dict[str, Any],
    universe: list[str],
    start_date: str,
    end_date: str,
    sharpe: float,
    total_return: float,
    max_drawdown: float,
    run_id: str | None = None,
) -> int:
    """Records an evaluated strategy trial into the SQLite trials ledger."""
    init_db()
    with get_db() as conn:
        cur = conn.execute(
            """
            INSERT INTO trials (
                strategy, params_json, universe_json, start_date, end_date,
                sharpe, total_return, max_drawdown, run_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                strategy,
                json.dumps(params, sort_keys=True),
                json.dumps(sorted(universe)),
                start_date,
                end_date,
                float(sharpe),
                float(total_return),
                float(max_drawdown),
                run_id,
            ),
        )
        conn.commit()
        return cur.lastrowid or 0


def get_trials_count(strategy: str | None = None) -> int:
    """Returns the total number of recorded trials, optionally filtered by strategy."""
    init_db()
    with get_db() as conn:
        if strategy:
            cur = conn.execute("SELECT COUNT(*) FROM trials WHERE strategy = ?", (strategy,))
        else:
            cur = conn.execute("SELECT COUNT(*) FROM trials")
        row = cur.fetchone()
        return row[0] if row else 0


def list_trials(
    strategy: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[dict[str, Any]]:
    """Lists trials from the ledger with pagination and optional filtering."""
    init_db()
    with get_db() as conn:
        if strategy:
            cur = conn.execute(
                """
                SELECT trial_id, strategy, params_json, universe_json, start_date,
                       end_date, sharpe, total_return, max_drawdown, run_id, created_at
                FROM trials WHERE strategy = ? ORDER BY trial_id DESC LIMIT ? OFFSET ?
            """,
                (strategy, limit, offset),
            )
        else:
            cur = conn.execute(
                """
                SELECT trial_id, strategy, params_json, universe_json, start_date,
                       end_date, sharpe, total_return, max_drawdown, run_id, created_at
                FROM trials ORDER BY trial_id DESC LIMIT ? OFFSET ?
            """,
                (limit, offset),
            )
        rows = []
        for r in cur.fetchall():
            d = dict(r)
            try:
                d["params"] = json.loads(d.pop("params_json"))
                d["universe"] = json.loads(d.pop("universe_json"))
            except Exception:
                pass
            rows.append(d)
        return rows


def get_trial_sharpes(strategy: str | None = None) -> list[float]:
    """Returns all recorded Sharpe ratios across trials to compute empirical cross-trial variance."""
    init_db()
    with get_db() as conn:
        if strategy:
            cur = conn.execute("SELECT sharpe FROM trials WHERE strategy = ?", (strategy,))
        else:
            cur = conn.execute("SELECT sharpe FROM trials")
        return [float(r[0]) for r in cur.fetchall()]


def get_cached_run(run_id: str) -> dict[str, Any] | None:
    init_db()
    with get_db() as conn:
        cur = conn.execute("SELECT response_json FROM runs WHERE run_id = ?", (run_id,))
        row = cur.fetchone()
        if row:
            res = json.loads(row["response_json"])
            res["is_cached"] = True
            return res
    return None


def save_run(run_id: str, request_data: dict, response_data: dict):
    init_db()
    with get_db() as conn:
        metrics = response_data.get("metrics", {})
        costs = response_data.get("costs", {})
        diag = response_data.get("diagnostics", {})
        conn.execute(
            """
            INSERT OR REPLACE INTO runs (
                run_id, strategy, params_json, universe_json, start_date, end_date,
                initial_capital, apply_costs, total_return, cagr, sharpe, sortino,
                max_drawdown, calmar, dsr_p_value, pbo, total_friction,
                execution_time_ms, response_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                run_id,
                request_data.get("strategy"),
                json.dumps(request_data.get("params", {})),
                json.dumps(request_data.get("universe", [])),
                request_data.get("start_date"),
                request_data.get("end_date"),
                float(request_data.get("initial_capital", 100000.0)),
                1 if request_data.get("apply_costs", True) else 0,
                float(metrics.get("total_return", 0.0)),
                float(metrics.get("cagr", 0.0)),
                float(metrics.get("sharpe_ratio", 0.0)),
                float(metrics.get("sortino_ratio", 0.0)),
                float(metrics.get("max_drawdown", 0.0)),
                float(metrics.get("calmar_ratio", 0.0)),
                diag.get("dsr_p_value"),
                diag.get("pbo"),
                float(costs.get("total_friction", 0.0)),
                float(response_data.get("execution_time_ms", 0.0)),
                json.dumps(response_data),
            ),
        )
        conn.commit()


def list_recent_runs(limit: int = 20) -> list[dict[str, Any]]:
    init_db()
    with get_db() as conn:
        cur = conn.execute(
            """
            SELECT run_id, strategy, start_date, end_date, initial_capital,
                   apply_costs, cagr, sharpe, max_drawdown, total_friction, created_at
            FROM runs ORDER BY created_at DESC LIMIT ?
        """,
            (limit,),
        )
        return [dict(r) for r in cur.fetchall()]
