import json
import os
import sqlite3
from typing import Any

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "pramaan_runs.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
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
        conn.commit()


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
        conn.execute("""
            INSERT OR REPLACE INTO runs (
                run_id, strategy, params_json, universe_json, start_date, end_date,
                initial_capital, apply_costs, total_return, cagr, sharpe, sortino,
                max_drawdown, calmar, dsr_p_value, pbo, total_friction,
                execution_time_ms, response_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
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
            json.dumps(response_data)
        ))
        conn.commit()


def list_recent_runs(limit: int = 20) -> list[dict[str, Any]]:
    init_db()
    with get_db() as conn:
        cur = conn.execute("""
            SELECT run_id, strategy, start_date, end_date, initial_capital,
                   apply_costs, cagr, sharpe, max_drawdown, total_friction, created_at
            FROM runs ORDER BY created_at DESC LIMIT ?
        """, (limit,))
        return [dict(r) for r in cur.fetchall()]
