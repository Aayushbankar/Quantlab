import pandas as pd
import numpy as np
from typing import Dict, Any, Callable
from src.engine.backtest_engine import BacktestEngine
from src.analytics.metrics import MetricsEngine

class ValidationEngine:
    """
    Handles 2D Parameter Stability Grid Search and 
    In-Sample / Out-of-Sample testing.
    """
    def __init__(self, data: Dict[str, pd.DataFrame]):
        self.data = data
        
    def run_grid_search(self, strategy_class, param_grid: Dict[str, list], 
                        is_start: str, is_end: str, apply_costs=True) -> pd.DataFrame:
        """
        Runs a grid search over parameters and returns a DataFrame of results.
        param_grid e.g.: {'fast_window': [10,20], 'slow_window': [50,100]}
        Only supports exactly 2 parameters for a 2D surface.
        """
        results = []
        
        # Filter data to in-sample period
        is_data = {}
        for symbol, df in self.data.items():
            mask = (df['date'] >= pd.to_datetime(is_start)) & (df['date'] <= pd.to_datetime(is_end))
            is_data[symbol] = df[mask]
            
        param_names = list(param_grid.keys())
        if len(param_names) != 2:
            raise ValueError("Exactly 2 parameters required for 2D surface grid search.")
            
        p1_name, p2_name = param_names[0], param_names[1]
        
        for p1_val in param_grid[p1_name]:
            for p2_val in param_grid[p2_name]:
                kwargs = {p1_name: p1_val, p2_name: p2_val}
                strategy = strategy_class(**kwargs)
                
                engine = BacktestEngine(is_data, strategy, apply_costs=apply_costs)
                equity_history = engine.run()
                
                metrics_engine = MetricsEngine(equity_history)
                metrics = metrics_engine.compute_all()
                
                res = {
                    p1_name: p1_val,
                    p2_name: p2_val,
                    'Sharpe Ratio': metrics.get('Sharpe Ratio', 0),
                    'CAGR': metrics.get('CAGR', 0)
                }
                results.append(res)
                
        return pd.DataFrame(results)
