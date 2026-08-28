import pandas as pd
from src.data.universe import get_universe
from src.data.fetch import fetch_stock_data
from src.data.clean import clean_data
from src.engine.backtest_engine import BacktestEngine
from src.strategies.sma_crossover import SMACrossoverStrategy
from src.strategies.rsi_mean_reversion import RSIMeanReversionStrategy
from src.strategies.momentum import MomentumStrategy
from src.analytics.cpcv import CPCV

def main():
    print("Fetching data...")
    symbols = get_universe()
    data_dict = {}
    for sym in symbols:
        df = fetch_stock_data(sym, "2022-01-01", "2024-01-01")
        if df is not None:
            data_dict[sym] = clean_data(df)
            
    if not data_dict:
        print("No data.")
        return

    strategies_to_test = {
        "SMA": SMACrossoverStrategy(20, 50),
        "RSI": RSIMeanReversionStrategy(14, 30, 70),
        "Momentum": MomentumStrategy(20, 0.05)
    }
    
    returns_dict = {}
    
    for name, strat in strategies_to_test.items():
        print(f"Running {name}...")
        engine = BacktestEngine(data_dict, strat, apply_costs=True)
        equity_history = engine.run()
        
        df_eq = pd.DataFrame(equity_history)
        if 'date' in df_eq.columns:
            df_eq.set_index('date', inplace=True)
        
        # Calculate daily returns from total_equity
        returns_dict[name] = df_eq['total_equity'].pct_change().dropna()
        
    df_returns = pd.DataFrame(returns_dict).dropna()
    print("Calculated returns shape:", df_returns.shape)
    
    # Calculate PBO
    cpcv = CPCV(n_splits=10, n_test_splits=2)
    pbo = cpcv.calculate_pbo(df_returns)
    print(f"\nCalculated PBO across strategies: {pbo:.4f} ({pbo*100:.2f}%)")

if __name__ == "__main__":
    main()
