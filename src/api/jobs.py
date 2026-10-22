from __future__ import annotations

import concurrent.futures
import logging
import time
import uuid
from typing import TYPE_CHECKING, Any

from src.api.adapter import execute_backtest
from src.api.cache import compute_run_id
from src.api.db import get_cached_run, save_run

if TYPE_CHECKING:
    from src.api.schemas import BacktestRequest

logger = logging.getLogger(__name__)


class JobManager:
    """Manages asynchronous background backtesting jobs."""

    def __init__(self, max_workers: int = 4):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self.jobs: dict[str, dict[str, Any]] = {}

    def _execute(self, job_id: str, req: BacktestRequest):
        self.jobs[job_id]["status"] = "running"
        t0 = time.time()
        try:
            run_id = compute_run_id(
                strategy=req.strategy,
                params=req.params,
                start=req.start_date,
                end=req.end_date,
                universe=req.universe,
                apply_costs=req.apply_costs,
                initial_cash=req.initial_capital,
                cost_profile=req.cost_profile,
            )

            # Check cache
            cached = get_cached_run(run_id)
            if cached:
                cached["is_cached"] = True
                cached["served_from"] = "cache"
                self.jobs[job_id]["status"] = "completed"
                self.jobs[job_id]["result"] = cached
                self.jobs[job_id]["duration_ms"] = round((time.time() - t0) * 1000.0, 2)
                return

            res = execute_backtest(
                strategy_name=req.strategy,
                params=req.params,
                universe_symbols=req.universe,
                start_date=req.start_date,
                end_date=req.end_date,
                initial_capital=req.initial_capital,
                apply_costs=req.apply_costs,
                cost_profile=req.cost_profile,
                slippage_floor_bps=req.slippage_floor_bps,
            )

            response_data = {
                "run_id": run_id,
                "strategy": req.strategy,
                "is_cached": False,
                "served_from": "live",
                "replay_reason": None,
                "engine_version": res.get("engine_version", "1.0.0"),
                "data_hash": res.get("data_hash", ""),
                "cost_profile": res.get("cost_profile", req.cost_profile),
                "execution_time_ms": res["execution_time_ms"],
                "dates": res["dates"],
                "gross_equity": res["gross_equity"],
                "net_equity": res["net_equity"],
                "metrics": res["metrics"],
                "costs": res["costs"],
                "trades": res["trades"],
                "diagnostics": res["diagnostics"],
            }
            save_run(run_id, req.model_dump(), response_data)

            self.jobs[job_id]["status"] = "completed"
            self.jobs[job_id]["result"] = response_data
            self.jobs[job_id]["duration_ms"] = round((time.time() - t0) * 1000.0, 2)
        except Exception as e:
            logger.exception(f"Job {job_id} failed: {e}")
            self.jobs[job_id]["status"] = "failed"
            self.jobs[job_id]["error"] = str(e)
            self.jobs[job_id]["duration_ms"] = round((time.time() - t0) * 1000.0, 2)

    def submit_job(self, req: BacktestRequest) -> str:
        job_id = f"job_{uuid.uuid4().hex[:12]}"
        self.jobs[job_id] = {
            "job_id": job_id,
            "status": "queued",
            "submitted_at": time.time(),
            "request": req.model_dump(),
            "result": None,
            "error": None,
        }
        self.executor.submit(self._execute, job_id, req)
        return job_id

    def get_job(self, job_id: str) -> dict[str, Any] | None:
        return self.jobs.get(job_id)


# Global singleton job manager
job_manager = JobManager()
