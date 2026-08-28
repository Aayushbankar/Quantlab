import pandas as pd
import os
import glob
from typing import Dict

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans OHLCV data according to project specifications.
    - Drops days with missing OHLC values rather than forward filling to avoid look-ahead bias.
    - Ensures correct datatypes.
    - Sorts chronologically.
    """
    # Create a copy to avoid SettingWithCopyWarning
    cleaned_df = df.copy()
    
    # Ensure date is datetime
    cleaned_df['date'] = pd.to_datetime(cleaned_df['date'])
    
    # Sort chronologically
    cleaned_df = cleaned_df.sort_values('date')
    
    # Drop rows with any NaN in OHLC
    # Note: Using adjusted close is handled natively by yfinance's history() by default
    cleaned_df = cleaned_df.dropna(subset=['open', 'high', 'low', 'close'])
    
    # Ensure volume is integer
    cleaned_df['volume'] = cleaned_df['volume'].astype(int, errors='ignore')
    
    # Reset index
    cleaned_df = cleaned_df.reset_index(drop=True)
    
    return cleaned_df

def load_and_clean_all(raw_dir: str = "data/raw") -> Dict[str, pd.DataFrame]:
    """
    Loads and cleans all CSVs in the raw data directory.
    Returns a dictionary mapping symbol to its cleaned DataFrame.
    """
    if not os.path.exists(raw_dir):
        print(f"Directory {raw_dir} does not exist.")
        return {}
        
    data_dict = {}
    csv_files = glob.glob(os.path.join(raw_dir, "*.csv"))
    
    for file in csv_files:
        symbol = os.path.basename(file).replace(".csv", "")
        df = pd.read_csv(file)
        cleaned_df = clean_data(df)
        data_dict[symbol] = cleaned_df
        
    return data_dict
