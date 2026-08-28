import os
import pandas as pd
from datetime import datetime
from src.data.universe import get_universe
from src.data.fetch import fetch_stock_data
from src.data.clean import clean_data
from src.engine.backtest_engine import BacktestEngine
from src.strategies.sma_crossover import SMACrossoverStrategy
from src.analytics.metrics import MetricsEngine

def main():
    print("Running automated experiments matrix...")
    
    # Full 10-symbol universe
    symbols = get_universe()
    data_dict = {}
    for sym in symbols:
        df = fetch_stock_data(sym, "2022-01-01", "2024-01-01") # Get a good amount of data
        if df is not None:
            data_dict[sym] = clean_data(df)
            
    if not data_dict:
        print("No data. Exiting.")
        return
        
    log_file = "experiments/experiment_log.csv"
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    results = []
    
    from src.strategies.rsi_mean_reversion import RSIMeanReversionStrategy
    from src.strategies.momentum import MomentumStrategy
    
    strategies_to_test = [
        ("SMACrossover(20,50)", SMACrossoverStrategy(20, 50)),
        ("RSIMeanReversion(14,30,70)", RSIMeanReversionStrategy(14, 30, 70)),
        ("Momentum(20)", MomentumStrategy(20, 0.05))
    ]
    
    # Run matrix
    for strategy_name, strategy_instance in strategies_to_test:
        for apply_costs in [False, True]:
            print(f"Running {strategy_name} (Costs: {apply_costs})...")
            engine = BacktestEngine(data_dict, strategy_instance, apply_costs=apply_costs)
            equity_history = engine.run()
            
            metrics = MetricsEngine(equity_history).compute_all()
            
            res = {
                "run_id": datetime.now().strftime("%Y%m%d%H%M%S") + f"_{apply_costs}_{strategy_name}",
                "strategy": strategy_name,
                "universe": "10-Symbol-Universe",
                "date_range": "2022-2024",
                "apply_costs": apply_costs,
                "cagr": metrics.get("CAGR", 0),
                "sharpe": metrics.get("Sharpe Ratio", 0)
            }
            results.append(res)
        
    df_res = pd.DataFrame(results)
    
    # If the file exists, we could append, but a full matrix run should just overwrite or append
    df_res.to_csv(log_file, index=False)
    print(f"Saved experiment log to {log_file}")

if __name__ == "__main__":
    main()
