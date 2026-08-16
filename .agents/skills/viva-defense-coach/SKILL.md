---
name: viva-defense-coach
description: >-
  GTU DI05000341 Viva Voce & Defense Master Coach.
  Prepares team members (Aayush & Meet) to answer challenging examiner questions,
  cross-defend each other's subsystems, articulate mathematical and architectural tradeoffs,
  and score 50/50 on the ESE External Viva.
---

# GTU Viva Voce & Defense Master Coach

This skill prepares students to defend their project in front of GTU internal evaluators (Seminars 1–4) and the external examiner (End Semester Exam Viva).

## 1. The 10 Critical Viva Defense Questions & Winning Responses

### Q1: "Why did you build your own backtest engine instead of using Backtrader, Zipline, or TradingView?"
- **Winning Answer**: *"Existing open-source frameworks like Backtrader are 15,000+ line monoliths with black-box execution assumptions. Building from scratch allowed us to enforce strict chronological event ordering to eliminate look-ahead bias (signal on Day $t$ Close, execution on Day $t+1$ Open), embed exact Indian statutory delivery taxes (STT, GST, Stamp Duty), and build first-class overfitting diagnostics like López de Prado's Deflated Sharpe Ratio, which no standard retail platform provides."*

### Q2: "What is look-ahead bias, and how does your engine mathematically prevent it?"
- **Winning Answer**: *"Look-ahead bias occurs when future information is accidentally used in current decisions. Our engine prevents this structurally through an event-driven queue: when evaluating Bar $t$, the strategy only has access to price history up to index $t$. The signal generated at Market Close of Day $t$ is queued and executed at the OPEN price of Day $t+1$."*

### Q3: "What is the difference between In-Sample and Out-of-Sample testing?"
- **Winning Answer**: *"In-Sample (2019–2022) is used exclusively for formulating hypotheses and parameter tuning. Out-of-Sample (2023–2024) is strictly unseen data used only once to validate whether the strategy's apparent edge survives in a different market regime without parameter re-tuning."*

### Q4: "What does the Sharpe ratio fail to capture?"
- **Winning Answer**: *"The Sharpe ratio assumes a normal distribution of returns and penalizes upside volatility equally with downside volatility. It ignores tail risk, skewness, and kurtosis. That is why we also implemented Sortino (downside deviation only), Calmar (CAGR over Max Drawdown), and the Deflated Sharpe Ratio (which adjusts for non-normality and multi-testing)."*

### Q5: "How does the Deflated Sharpe Ratio (DSR) work?"
- **Winning Answer**: *"When a trader runs $N$ parameter trials, the maximum observed Sharpe ratio increases purely by chance. DSR calculates the expected maximum Sharpe ratio under the Null Hypothesis (pure noise across $N$ trials) and computes the p-value that the observed Sharpe ratio is genuine, adjusting for the variance, skewness, and kurtosis of returns."*

---

## 2. Cross-Subsystem Defense Rule (Seminar 4 & ESE)

GTU examiners often ask Student A about Student B's subsystem and vice versa:
- **Aayush (Data & Strategies Lead) must master**: The event simulation loop, order fill price calculations, cash invariants, and portfolio state updates.
- **Meet (Engine & UI Lead) must master**: Strategy signal equations, RSI/SMA indicator calculations, data cleaning rules, and parameter grid search logic.
