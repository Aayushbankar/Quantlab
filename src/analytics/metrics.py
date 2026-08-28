import pandas as pd
import numpy as np

class MetricsEngine:
    """Calculates performance metrics from equity history."""
    
    def __init__(self, equity_history: pd.DataFrame, risk_free_rate: float = 0.05):
        self.history = equity_history.copy()
        self.rf = risk_free_rate
        
        # Calculate daily returns
        if 'total_equity' in self.history.columns:
            self.history['return'] = self.history['total_equity'].pct_change()
        else:
            self.history['return'] = 0.0
            
    def compute_all(self) -> dict:
        if self.history.empty or len(self.history) < 2:
            return {}
            
        returns = self.history['return'].dropna()
        if len(returns) == 0:
            return {}
            
        metrics = {
            'Total Return': self._total_return(),
            'CAGR': self._cagr(),
            'Max Drawdown': self._max_drawdown(),
            'Sharpe Ratio': self._sharpe_ratio(returns),
            'Sortino Ratio': self._sortino_ratio(returns),
            'Calmar Ratio': self._calmar_ratio()
        }
        return metrics
        
    def _total_return(self) -> float:
        start_equity = self.history['total_equity'].iloc[0]
        end_equity = self.history['total_equity'].iloc[-1]
        return (end_equity - start_equity) / start_equity
        
    def _cagr(self) -> float:
        start_equity = self.history['total_equity'].iloc[0]
        end_equity = self.history['total_equity'].iloc[-1]
        years = len(self.history) / 252.0
        if years == 0: return 0.0
        return (end_equity / start_equity) ** (1 / years) - 1
        
    def _max_drawdown(self) -> float:
        roll_max = self.history['total_equity'].cummax()
        drawdown = self.history['total_equity'] / roll_max - 1.0
        return drawdown.min()
        
    def _sharpe_ratio(self, returns: pd.Series) -> float:
        excess_returns = returns - (self.rf / 252.0)
        std = excess_returns.std()
        if std == 0: return 0.0
        return (excess_returns.mean() / std) * np.sqrt(252)
        
    def _sortino_ratio(self, returns: pd.Series) -> float:
        excess_returns = returns - (self.rf / 252.0)
        downside = excess_returns[excess_returns < 0]
        std_downside = downside.std()
        if std_downside == 0 or pd.isna(std_downside): return 0.0
        return (excess_returns.mean() / std_downside) * np.sqrt(252)
        
    def _calmar_ratio(self) -> float:
        mdd = abs(self._max_drawdown())
        if mdd == 0: return 0.0
        return self._cagr() / mdd
