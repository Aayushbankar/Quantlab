# QuantLab: Honest Algorithmic Backtesting

QuantLab is a realistic, event-driven backtesting engine and overfitting diagnostic platform designed for Indian equities. Built as a GTU academic project (DI05000341), its core philosophy is to expose the hidden frictions and statistical illusions that make trading strategies look good on paper but fail in live markets.

## Why This Matters (The "Cash vs. Equity" Illusion)
In algorithmic trading, minor coding oversights silently compound into massive illusions of profitability. For example, during our development, an early bug incorrectly sized positions based on *available cash* rather than *total portfolio equity*. Because the strategy held positions and cash dwindled, it artificially traded smaller sizes as the portfolio grew—completely masking the reality of market impact on compounded returns. 

By enforcing rigorous financial and architectural invariants, QuantLab ensures your backtest doesn't lie to you.

## Verifiable Core Features
- **Zero-Lookahead T+1 Execution:** Signal generation firmly occurs on Day $t$ Close; order fills happen on Day $t+1$ Open. Future data cannot leak into signal generation.
- **Real Indian Statutory Cost Model:** Automatically deducts Brokerage, STT, Stamp Duty, Exchange Turnover, GST, and slippage (via Almgren-Chriss Square Root model).
- **Deflated Sharpe Ratio (DSR):** Statistically evaluates the probability that a strategy's Sharpe ratio is merely a product of multiple testing.
- **Combinatorial Purged Cross-Validation (CPCV):** Includes genuine time-series purging and embargo logic. Our synthetic AR(1) tests prove that our embargo drops sample leakage at block boundaries, capturing the true Out-Of-Sample performance decay of serially correlated returns.

## What QuantLab Does NOT Do (Explicit Scope Limitations)
To maintain focus on backtesting integrity, QuantLab explicitly omits:
- **No Live Execution:** This is exclusively a simulation and diagnostic engine, not a trading bot.
- **No Bundled Licensed Data:** We use `yfinance` to fetch data. This is strictly for academic simulation and is **not licensed for commercial redistribution**.
- **Daily Bars Only:** We do not model intraday tick-level data.
- **No Derivatives:** Equities only; no options or futures support.

## License
This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
