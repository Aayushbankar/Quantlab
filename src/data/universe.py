# src/data/universe.py

INDIAN_EQUITIES = [
    "RELIANCE.NS",  # Energy
    "TCS.NS",       # IT
    "INFY.NS",      # IT
    "HDFCBANK.NS",  # Banking
    "ICICIBANK.NS", # Banking
    "SBIN.NS",      # Banking
    "ITC.NS",       # FMCG
    "HINDUNILVR.NS",# FMCG
    "LT.NS",        # Infra
    "BHARTIARTL.NS" # Telecom
]

BENCHMARK = "^NSEI"  # Nifty 50 Index

def get_universe():
    """Returns the list of 10 liquid Indian equities for the study."""
    return INDIAN_EQUITIES

def get_benchmark():
    """Returns the benchmark ticker symbol."""
    return BENCHMARK
