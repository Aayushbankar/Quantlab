import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set seaborn style for professional charts
sns.set_theme(style="darkgrid", palette="deep")
plt.rcParams.update({'font.size': 12, 'figure.figsize': (12, 8)})

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    charts_dir = os.path.join(base_dir, 'docs', 'charts')
    os.makedirs(charts_dir, exist_ok=True)
    
    # 1. Monthly Returns Heatmap (Mocked realistically based on CAGR)
    # We will generate a realistic monthly return matrix
    np.random.seed(42)
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    years = [2022, 2023, 2024]
    
    # Generate realistic returns with some negative months to show realism
    returns_matrix = np.random.normal(0.005, 0.04, (len(years), len(months)))
    
    plt.figure(figsize=(12, 5))
    sns.heatmap(returns_matrix, annot=True, fmt=".2%", cmap="RdYlGn", center=0, xticklabels=months, yticklabels=years)
    plt.title("Strategy Monthly Returns Heatmap (Cost-Adjusted)\n(Illustrative, not derived from live backtest run)", fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'monthly_heatmap_SIMULATED.png'), dpi=300)
    plt.close()

    # 2. Advanced Equity Curve with Drawdown (Underwater Plot)
    days = 750
    daily_returns = np.random.normal(0.0001, 0.015, days)
    cum_returns = np.cumprod(1 + daily_returns)
    running_max = np.maximum.accumulate(cum_returns)
    drawdown = (cum_returns - running_max) / running_max

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 1]})
    
    ax1.plot(cum_returns, color='blue', linewidth=2, label='Strategy Equity')
    ax1.plot(running_max, color='red', linestyle='--', alpha=0.6, label='High Water Mark')
    ax1.fill_between(range(days), cum_returns, running_max, color='red', alpha=0.1)
    ax1.set_title("Cumulative Equity Curve & High Water Mark\n(Illustrative, not derived from live backtest run)", fontsize=16, fontweight='bold')
    ax1.set_ylabel("Portfolio Multiplier", fontsize=12)
    ax1.legend(loc="upper left")
    
    ax2.fill_between(range(days), drawdown, 0, color='red', alpha=0.5)
    ax2.set_title("Underwater Drawdown Plot (Illustrative)", fontsize=14, fontweight='bold')
    ax2.set_ylabel("Drawdown %", fontsize=12)
    ax2.set_xlabel("Trading Days", fontsize=12)
    
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'advanced_equity_drawdown_SIMULATED.png'), dpi=300)
    plt.close()
    
    # 3. Market Impact Visualization (Almgren-Chriss)
    order_sizes = np.linspace(1000, 100000, 100)
    adv = 1000000
    vol = 0.02
    gamma = 0.1
    
    impact_pct = gamma * vol * np.sqrt(order_sizes / adv)
    impact_bps = impact_pct * 10000 # basis points
    
    plt.figure(figsize=(10, 6))
    plt.plot(order_sizes, impact_bps, color='purple', linewidth=3)
    plt.fill_between(order_sizes, impact_bps, 0, color='purple', alpha=0.2)
    plt.title("Almgren-Chriss Square Root Market Impact", fontsize=16, fontweight='bold')
    plt.xlabel("Order Size (Shares)", fontsize=12)
    plt.ylabel("Estimated Slippage (Basis Points)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'almgren_chriss_impact.png'), dpi=300)
    plt.close()

    print("Advanced charts generated.")

if __name__ == "__main__":
    main()
