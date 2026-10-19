import numpy as np
import pandas as pd


class MetricsEngine:
    """Calculates performance metrics from equity history with exposure controls."""

    def __init__(
        self,
        equity_history: pd.DataFrame,
        risk_free_rate: float = 0.06,
        benchmark_returns: pd.Series | None = None,
        cash_yield: float = 0.06,
    ):
        self.history = equity_history.copy()
        self.rf = risk_free_rate
        self.benchmark_returns = benchmark_returns
        self.cash_yield = cash_yield

        # Calculate daily returns
        if "total_equity" in self.history.columns:
            self.history["return"] = self.history["total_equity"].pct_change()
        else:
            self.history["return"] = 0.0

    def compute_all(self) -> dict:
        if self.history.empty or len(self.history) < 2:
            return {}

        returns = self.history["return"].dropna()
        if len(returns) == 0:
            return {}

        alpha, beta, exp_matched = self._benchmark_analytics(returns)

        metrics = {
            "Total Return": self._total_return(),
            "CAGR": self._cagr(),
            "Max Drawdown": self._max_drawdown(),
            "Sharpe Ratio": self._sharpe_ratio(returns),
            "Sortino Ratio": self._sortino_ratio(returns),
            "Calmar Ratio": self._calmar_ratio(),
            "Average Exposure": self._average_exposure(),
            "Alpha": float(round(alpha, 4)),
            "Beta": float(round(beta, 4)),
            "Exposure Matched Return": float(round(exp_matched, 4)),
        }
        return metrics

    def _average_exposure(self) -> float:
        if "cash" in self.history.columns and "total_equity" in self.history.columns:
            total_eq = self.history["total_equity"]
            cash = self.history["cash"]
            valid = total_eq > 0
            if not valid.any():
                return 0.0
            invested = np.maximum(0.0, total_eq - cash)
            exposure = (invested / total_eq).where(valid, 0.0)
            return float(np.clip(exposure.mean(), 0.0, 1.0))
        return 1.0

    def _benchmark_analytics(self, strategy_returns: pd.Series) -> tuple[float, float, float]:
        avg_exp = self._average_exposure()
        strat_cagr = self._cagr()

        if self.benchmark_returns is not None and len(self.benchmark_returns) > 1:
            bm_ret = self.benchmark_returns.reindex(strategy_returns.index).fillna(0.0)
            var_bm = float(bm_ret.var())
            if var_bm > 1e-12:
                cov = float(np.cov(strategy_returns, bm_ret)[0, 1])
                beta = cov / var_bm
            else:
                beta = 1.0 if avg_exp > 0.5 else 0.0
            bm_cum = float((1.0 + bm_ret).prod() - 1.0)
            years = len(strategy_returns) / 252.0
            bm_cagr = float((1.0 + bm_cum) ** (1.0 / max(years, 0.01)) - 1.0)
        else:
            # Fallback estimation against passive null
            beta = round(avg_exp, 2)
            bm_cum = strat_cagr
            bm_cagr = strat_cagr

        alpha = (strat_cagr - self.rf) - beta * (bm_cagr - self.rf)
        cash_rate = self.cash_yield if self.cash_yield is not None else self.rf
        exposure_matched_return = avg_exp * bm_cum + (1.0 - avg_exp) * cash_rate

        return alpha, beta, exposure_matched_return

    def _total_return(self) -> float:
        start_equity = self.history["total_equity"].iloc[0]
        end_equity = self.history["total_equity"].iloc[-1]
        return (end_equity - start_equity) / start_equity

    def _cagr(self) -> float:
        start_equity = self.history["total_equity"].iloc[0]
        end_equity = self.history["total_equity"].iloc[-1]
        years = len(self.history) / 252.0
        if years == 0:
            return 0.0
        return (end_equity / start_equity) ** (1 / years) - 1

    def _max_drawdown(self) -> float:
        roll_max = self.history["total_equity"].cummax()
        drawdown = self.history["total_equity"] / roll_max - 1.0
        return drawdown.min()

    def _sharpe_ratio(self, returns: pd.Series) -> float:
        excess_returns = returns - (self.rf / 252.0)
        std = excess_returns.std()
        if std == 0:
            return 0.0
        return (excess_returns.mean() / std) * np.sqrt(252)

    def _sortino_ratio(self, returns: pd.Series) -> float:
        excess_returns = returns - (self.rf / 252.0)
        # Measure downside semi-deviation across all T trading days per Sortino & Price (1994)
        downside_deviations = np.minimum(0.0, excess_returns)
        downside_dev = np.sqrt(np.mean(downside_deviations**2))
        if downside_dev == 0.0 or pd.isna(downside_dev):
            return 0.0
        return float((excess_returns.mean() / downside_dev) * np.sqrt(252))

    def _calmar_ratio(self) -> float:
        mdd = abs(self._max_drawdown())
        if mdd == 0:
            return 0.0
        return self._cagr() / mdd
