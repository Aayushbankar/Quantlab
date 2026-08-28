import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set seaborn style for professional charts
sns.set_theme(style="whitegrid", palette="muted")

def main():
    # Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_path = os.path.join(base_dir, 'experiments', 'experiment_log.csv')
    charts_dir = os.path.join(base_dir, 'docs', 'charts')
    
    # Ensure charts directory exists
    os.makedirs(charts_dir, exist_ok=True)
    
    # Read the data
    if not os.path.exists(log_path):
        print(f"File not found: {log_path}")
        return
        
    df = pd.read_csv(log_path)
    if df.empty:
        print("Experiment log is empty.")
        return
        
    df['apply_costs'] = df['apply_costs'].astype(str)
    
    # 1. Bar chart comparing CAGR with and without costs
    plt.figure(figsize=(8, 6))
    ax1 = sns.barplot(data=df, x='strategy', y='cagr', hue='apply_costs')
    plt.title('CAGR by Strategy (With vs Without Costs)', fontsize=14)
    plt.ylabel('Compound Annual Growth Rate (CAGR)', fontsize=12)
    plt.xlabel('Strategy', fontsize=12)
    plt.legend(title='Apply Costs', loc='upper right')
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'cagr_comparison.png'), dpi=300)
    plt.close()
    
    # 2. Bar chart comparing Sharpe Ratio with and without costs
    plt.figure(figsize=(8, 6))
    ax2 = sns.barplot(data=df, x='strategy', y='sharpe', hue='apply_costs')
    plt.title('Sharpe Ratio by Strategy (With vs Without Costs)', fontsize=14)
    plt.ylabel('Sharpe Ratio', fontsize=12)
    plt.xlabel('Strategy', fontsize=12)
    plt.legend(title='Apply Costs', loc='upper right')
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'sharpe_comparison.png'), dpi=300)
    plt.close()
    
    # 3. Simulated Equity Curve based on CAGR
    # Simulate a daily equity curve over 252 days for each run
    days = 252
    plt.figure(figsize=(10, 6))
    
    for idx, row in df.iterrows():
        cagr = row['cagr']
        # Convert annual CAGR to daily return roughly
        daily_return = (1 + cagr) ** (1/days) - 1
        
        # Simulate a random walk around this daily return
        np.random.seed(42 + idx) # for reproducibility
        daily_vol = 0.15 / np.sqrt(days) # 15% annualized volatility
        returns = np.random.normal(daily_return, daily_vol, days)
        
        equity_curve = np.cumprod(1 + returns)
        
        label = f"{row['strategy']} (Costs: {row['apply_costs']})"
        plt.plot(equity_curve, label=label)
        
    plt.title('Simulated Equity Curve (1 Year)\n(Illustrative, not derived from live backtest run)', fontsize=14)
    plt.ylabel('Cumulative Return', fontsize=12)
    plt.xlabel('Days', fontsize=12)
    plt.legend(title='Scenarios', loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'simulated_equity_curve_SIMULATED.png'), dpi=300)
    plt.close()

    print(f"Charts successfully generated in {charts_dir}")

if __name__ == "__main__":
    main()
