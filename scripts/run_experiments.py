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
    
    # Minimal data for test
    symbols = get_universe()[:2]
    data_dict = {}
    for sym in symbols:
        df = fetch_stock_data(sym, "2023-01-01", "2024-01-01")
        if df is not None:
            data_dict[sym] = clean_data(df)
            
    if not data_dict:
        print("No data. Exiting.")
        return
        
    log_file = "experiments/experiment_log.csv"
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    results = []
    
    # Run matrix
    for apply_costs in [False, True]:
        strategy = SMACrossoverStrategy(20, 50)
        engine = BacktestEngine(data_dict, strategy, apply_costs=apply_costs)
        equity_history = engine.run()
        
        metrics = MetricsEngine(equity_history).compute_all()
        
        res = {
            "run_id": datetime.now().strftime("%Y%m%d%H%M%S") + f"_{apply_costs}",
            "strategy": "SMACrossover(20,50)",
            "universe": ",".join(symbols),
            "date_range": "2023-2024",
            "apply_costs": apply_costs,
            "cagr": metrics.get("CAGR", 0),
            "sharpe": metrics.get("Sharpe Ratio", 0)
        }
        results.append(res)
        
    df_res = pd.DataFrame(results)
    df_res.to_csv(log_file, index=False)
    print(f"Saved experiment log to {log_file}")

if __name__ == "__main__":
    main()
