import plotly.graph_objects as go
import pandas as pd

def plot_equity_curve(history: pd.DataFrame, title="Equity Curve"):
    """Returns a Plotly Figure for the equity curve."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=history['date'], y=history['total_equity'], mode='lines', name='Total Equity'))
    fig.update_layout(title=title, xaxis_title="Date", yaxis_title="Equity (INR)", template="plotly_white")
    return fig

def plot_drawdown_underwater(history: pd.DataFrame):
    """Returns a Plotly Figure for the underwater drawdown chart."""
    roll_max = history['total_equity'].cummax()
    drawdown = (history['total_equity'] / roll_max) - 1.0
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=history['date'], y=drawdown, mode='lines', name='Drawdown', fill='tozeroy', fillcolor='rgba(255,0,0,0.3)', line=dict(color='red')))
    fig.update_layout(title="Underwater Drawdown", xaxis_title="Date", yaxis_title="Drawdown (%)", template="plotly_white")
    return fig

def plot_2d_heatmap(results_df: pd.DataFrame, x_col: str, y_col: str, z_col: str):
    """Plots a 2D stability heatmap."""
    pivot = results_df.pivot(index=y_col, columns=x_col, values=z_col)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale='Viridis'
    ))
    fig.update_layout(title=f"Parameter Stability Heatmap ({z_col})", xaxis_title=x_col, yaxis_title=y_col)
    return fig
