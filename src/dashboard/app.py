import streamlit as st
import pandas as pd
import os
from src.data.clean import load_and_clean_all
from src.engine.backtest_engine import BacktestEngine
from src.strategies.sma_crossover import SMACrossoverStrategy
from src.strategies.rsi_mean_reversion import RSIMeanReversionStrategy
from src.strategies.momentum import MomentumStrategy
from src.analytics.metrics import MetricsEngine
from src.dashboard.components import plot_equity_curve, plot_drawdown_underwater

st.set_page_config(page_title="QuantLab Dashboard", layout="wide")

st.title("QuantLab: Realistic Backtesting Engine")
st.markdown("GTU DI05000341 Minor Project - Overfitting Diagnostic Platform")

@st.cache_data
def load_data():
    # Assuming data is downloaded in data/raw
    return load_and_clean_all("data/raw")

data_dict = load_data()

if not data_dict:
    st.warning("No data found in data/raw/. Please run the data fetcher first.")
    st.stop()

# Sidebar controls
st.sidebar.header("Configuration")
strategy_name = st.sidebar.selectbox("Select Strategy", ["SMA Crossover", "RSI Mean Reversion", "Momentum"])

apply_costs = st.sidebar.checkbox("Apply Transaction Costs & Slippage", value=True)

st.sidebar.subheader("Parameters")
if strategy_name == "SMA Crossover":
    fast = st.sidebar.slider("Fast Window", 5, 50, 20)
    slow = st.sidebar.slider("Slow Window", 20, 200, 50)
    strategy = SMACrossoverStrategy(fast, slow)
elif strategy_name == "RSI Mean Reversion":
    period = st.sidebar.slider("RSI Period", 5, 30, 14)
    strategy = RSIMeanReversionStrategy(period=period)
else:
    lookback = st.sidebar.slider("Lookback Period", 10, 100, 20)
    strategy = MomentumStrategy(lookback_period=lookback)

if st.sidebar.button("Run Backtest"):
    with st.spinner("Running event-driven simulation..."):
        engine = BacktestEngine(data_dict, strategy, apply_costs=apply_costs)
        equity_history = engine.run()
        
        metrics_engine = MetricsEngine(equity_history)
        metrics = metrics_engine.compute_all()
        
        # Display Metrics
        st.subheader("Performance Metrics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("CAGR", f"{metrics.get('CAGR', 0):.2%}")
        col2.metric("Sharpe Ratio", f"{metrics.get('Sharpe Ratio', 0):.2f}")
        col3.metric("Max Drawdown", f"{metrics.get('Max Drawdown', 0):.2%}")
        col4.metric("Calmar Ratio", f"{metrics.get('Calmar Ratio', 0):.2f}")
        
        # Display Charts
        st.plotly_chart(plot_equity_curve(equity_history), use_container_width=True)
        st.plotly_chart(plot_drawdown_underwater(equity_history), use_container_width=True)
