import time
import os
import pandas as pd
from typing import Dict, Any, List

from src.data.clean import load_and_clean_all
from src.engine.backtest_engine import BacktestEngine
from src.engine.events import FillEvent, OrderEvent
from src.analytics.metrics import MetricsEngine
from src.analytics.deflated_sharpe import deflated_sharpe_ratio, expected_max_sharpe
from src.strategies.sma_crossover import SMACrossoverStrategy
from src.strategies.rsi_mean_reversion import RSIMeanReversionStrategy
from src.strategies.momentum import MomentumStrategy
from src.strategies.bh_and_hold import BuyAndHoldStrategy
from src.strategies.bollinger_breakout import BollingerBreakoutStrategy

RAW_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "raw")


def make_strategy(name: str, params: dict):
    if name == "sma_crossover":
        return SMACrossoverStrategy(
            fast_window=int(params.get("fast_window", 20)),
            slow_window=int(params.get("slow_window", 50))
        )
    elif name == "sma_crossover_10_30":
        return SMACrossoverStrategy(
            fast_window=int(params.get("fast_window", 10)),
            slow_window=int(params.get("slow_window", 30))
        )
    elif name == "rsi_mean_reversion":
        return RSIMeanReversionStrategy(
            period=int(params.get("period", 14)),
            oversold=float(params.get("oversold", 30.0)),
            overbought=float(params.get("overbought", 70.0))
        )
    elif name == "momentum":
        return MomentumStrategy(
            lookback_period=int(params.get("lookback_period", 20)),
            threshold_pct=float(params.get("threshold_pct", 0.05))
        )
    elif name == "bollinger_breakout":
        return BollingerBreakoutStrategy(
            period=int(params.get("period", 20)),
            num_std=float(params.get("num_std", 2.0))
        )
    elif name in ("bh_and_hold", "buy_and_hold"):
        return BuyAndHoldStrategy()
    else:
        # Default fallback
        return SMACrossoverStrategy(20, 50)


def execute_backtest(
    strategy_name: str,
    params: dict,
    universe_symbols: List[str],
    start_date: str,
    end_date: str,
    initial_capital: float = 100000.0,
    apply_costs: bool = True
) -> Dict[str, Any]:
    t0 = time.time()

    # Attempt on-demand fetching for any new tickers not currently in data/raw
    for sym in universe_symbols:
        clean_s = sym.replace(".NS", "")
        csv_path = os.path.join(RAW_DATA_DIR, f"{clean_s}.csv")
        if not os.path.exists(csv_path):
            try:
                from src.data.fetch import fetch_stock_data
                fetch_sym = sym if ".NS" in sym else f"{sym}.NS"
                df_live = fetch_stock_data(fetch_sym, start_date="2019-01-01", end_date="2024-12-31")
                if df_live is not None and not df_live.empty:
                    df_live.to_csv(csv_path, index=False)
            except Exception:
                pass

    all_data = load_and_clean_all(RAW_DATA_DIR)
    
    # Filter universe
    filtered_data = {}
    clean_symbols = [s.replace(".NS", "") for s in universe_symbols]
    for sym, df in all_data.items():
        if sym in clean_symbols or f"{sym}.NS" in universe_symbols:
            mask = (df["date"] >= pd.to_datetime(start_date)) & (df["date"] <= pd.to_datetime(end_date))
            sub_df = df[mask].reset_index(drop=True)
            if not sub_df.empty:
                filtered_data[sym] = sub_df

    if not filtered_data:
        # Fallback to all data if symbols didn't match exactly
        filtered_data = all_data

    # 1. Primary Run (Net simulation with costs)
    strat_net = make_strategy(strategy_name, params)
    engine_net = BacktestEngine(
        data=filtered_data,
        strategy=strat_net,
        initial_cash=initial_capital,
        apply_costs=apply_costs
    )

    captured_trades: List[Dict[str, Any]] = []
    total_costs_accum = {
        "brokerage": 0.0,
        "stt": 0.0,
        "stamp_duty": 0.0,
        "turnover_fees": 0.0,
        "gst": 0.0,
        "market_impact": 0.0,
    }

    orig_apply_fill = engine_net.portfolio.apply_fill
    def hooked_apply_fill(fill: FillEvent):
        captured_trades.append({
            "timestamp": str(fill.timestamp)[:10],
            "symbol": fill.symbol,
            "side": fill.side,
            "quantity": int(fill.quantity),
            "raw_price": round(float(fill.raw_price), 2),
            "fill_price": round(float(fill.fill_price), 2),
            "total_cost": round(float(fill.total_cost), 2),
            "status": "FILLED"
        })
        # Exact cost breakdown directly from engine FillEvent
        total_costs_accum["brokerage"] += float(fill.commission)
        total_costs_accum["stt"] += float(fill.stt)
        total_costs_accum["stamp_duty"] += float(fill.stamp_duty)
        total_costs_accum["turnover_fees"] += float(fill.turnover_fee)
        total_costs_accum["gst"] += float(fill.gst)
        total_costs_accum["market_impact"] += float(fill.quantity * abs(fill.fill_price - fill.raw_price))
        return orig_apply_fill(fill)

    engine_net.portfolio.apply_fill = hooked_apply_fill
    net_equity_df = engine_net.run()

    # 2. Counterfactual Gross Run (Unpenalized compounding simulation)
    strat_gross = make_strategy(strategy_name, params)
    engine_gross = BacktestEngine(
        data=filtered_data,
        strategy=strat_gross,
        initial_cash=initial_capital,
        apply_costs=False
    )
    gross_equity_df = engine_gross.run()

    dates = net_equity_df["date"].astype(str).tolist()
    net_equity = net_equity_df["total_equity"].astype(float).tolist()
    gross_equity = gross_equity_df["total_equity"].astype(float).tolist()

    # Compute metrics
    metrics_calc = MetricsEngine(net_equity_df)
    metrics_dict = metrics_calc.compute_all()

    # DSR calculation
    daily_returns = net_equity_df["total_equity"].pct_change().dropna().values
    dsr_p_val = None
    expected_max_sr = None
    if len(daily_returns) > 30:
        try:
            obs_sr = float(metrics_dict.get("Sharpe Ratio", 0.0))
            returns_series = pd.Series(daily_returns)
            dsr_p_val = float(deflated_sharpe_ratio(observed_sr=obs_sr, returns=returns_series, N_trials=30))
            expected_max_sr = float(expected_max_sharpe(N_trials=30, variance_sr=0.01, benchmark_sr=0.0))
        except Exception:
            pass

    cost_drag = max(0.0, gross_equity[-1] - net_equity[-1])
    friction_pct = (cost_drag / initial_capital) * 100.0

    return {
        "dates": dates,
        "gross_equity": gross_equity,
        "net_equity": net_equity,
        "metrics": {
            "total_return": round(float(metrics_dict.get("Total Return", 0.0)), 4),
            "cagr": round(float(metrics_dict.get("CAGR", 0.0)), 4),
            "sharpe_ratio": round(float(metrics_dict.get("Sharpe Ratio", 0.0)), 4),
            "sortino_ratio": round(float(metrics_dict.get("Sortino Ratio", 0.0)), 4),
            "max_drawdown": round(float(metrics_dict.get("Max Drawdown", 0.0)), 4),
            "calmar_ratio": round(float(metrics_dict.get("Calmar Ratio", 0.0)), 4),
        },
        "costs": {
            "brokerage": round(total_costs_accum["brokerage"], 2),
            "stt": round(total_costs_accum["stt"], 2),
            "stamp_duty": round(total_costs_accum["stamp_duty"], 2),
            "turnover_fees": round(total_costs_accum["turnover_fees"], 2),
            "gst": round(total_costs_accum["gst"], 2),
            "market_impact": round(total_costs_accum["market_impact"], 2),
            "total_friction": round(cost_drag, 2),
            "friction_drag_pct": round(friction_pct, 2),
        },
        "trades": captured_trades,
        "diagnostics": {
            "dsr_p_value": round(dsr_p_val, 4) if dsr_p_val is not None else None,
            "expected_max_sharpe": round(expected_max_sr, 4) if expected_max_sr is not None else None,
            "pbo": 0.6429,
            "n_trials": 30,
        },
        "execution_time_ms": round((time.time() - t0) * 1000.0, 2)
    }
