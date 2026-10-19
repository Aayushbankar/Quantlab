import yfinance as yf
import pandas as pd
import os
from typing import List, Optional

def fetch_stock_data(symbol: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
    """
    Fetches historical OHLCV data for a given symbol from Yahoo Finance.
    
    Args:
        symbol: The stock ticker symbol (e.g., 'RELIANCE.NS' for NSE).
        start_date: The start date in 'YYYY-MM-DD' format.
        end_date: The end date in 'YYYY-MM-DD' format.
        
    Returns:
        pd.DataFrame containing OHLCV data, or None if fetch fails.
    """
    try:
        print(f"Fetching data for {symbol} from {start_date} to {end_date}...")
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date, end=end_date)
        
        if df.empty:
            print(f"Warning: No data found for {symbol}.")
            return None
            
        # Reset index to make Date a column and ensure it's timezone naive
        df = df.reset_index()
        df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
        
        # Standardize column names
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        df['symbol'] = symbol
        
        return df
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def download_universe(symbols: List[str], start_date: str, end_date: str, save_dir: str = "data/raw"):
    """
    Downloads and saves historical data for a list of symbols.
    """
    os.makedirs(save_dir, exist_ok=True)
    
    for symbol in symbols:
        df = fetch_stock_data(symbol, start_date, end_date)
        if df is not None:
            file_path = os.path.join(save_dir, f"{symbol.replace('.NS', '')}.csv")
            df.to_csv(file_path, index=False)
            print(f"Saved {symbol} data to {file_path}")

if __name__ == "__main__":
    # Test script
    universe = ["RELIANCE.NS", "TCS.NS"]
    download_universe(universe, "2019-01-01", "2024-01-01")
