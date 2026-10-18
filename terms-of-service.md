---
title: "Terms of Service"
date: 2026-10-19
project: [pramaan]
tier: [academic]
tags: [terms, legal, disclaimer]
status: active
---

# Terms of Service — Pramaan

**Effective date:** 2026-10-19

---

## 1. What Pramaan is

Pramaan is a backtesting simulation and statistical validation tool. It computes, from historical data, what a stated trading rule would have done under a stated cost and execution model.

## 2. What Pramaan is not

**Pramaan is not investment advice, and it is not a recommendation engine.**

- It does not recommend any security.
- It does not predict future returns.
- It does not tell you to buy, sell, or hold anything.
- A simulated result is a historical measurement, not a forecast.

## 3. No warranty

The software is provided under **Apache License 2.0** — `AS IS`, without warranty of any kind, express or implied, including but not limited to warranties of merchantability, fitness for a particular purpose, or non-infringement.

**Specifically, Pramaan does not warrant that:**
- its cost model matches the rate card of your broker or current circulars;
- its market-impact model matches your actual execution;
- its statistical diagnostics are sufficient to validate a strategy for deployment;
- any simulated result resembles what you will achieve in live trading.

## 4. Assumption of risk

You are solely responsible for any decision you make and any capital you deploy. Backtested performance does not guarantee future performance. Trading securities involves risk of loss, including total loss of capital.

## 5. Accuracy limitations you must understand

| Limitation | Consequence |
|---|---|
| Daily bars only | Int raday effects, including better prices available within a bar, are not modelled. |
| Full-fill assumption | Partial fills and queue position are not modelled. |
| Point-in-time universe | Delisted symbols are not retroactively removed; survivorship bias exists. |
| Cost model is an approximation | Statutory rates change; verify against your broker and current NSE/SEBI circulars. |
| Impact model is parametric | Almgren–Chriss with a fixed γ is an approximation, not an execution guarantee. |
| Long-only, NSE cash equities | No short selling, derivatives, commodities, or other markets. |

## 6. Data

Market data is obtained by you from your configured provider. You are responsible for complying with that provider's terms. Pramaan does not redistribute market data.

## 7. Intellectual property

The engine source is licensed under Apache License 2.0. You may use, modify, and distribute it commercially, provided you preserve the license and attribution notices. The Pramaan name and associated marks remain the property of the project maintainers and may not be used to imply endorsement without permission.

## 8. Export and publication of results

If you publish or present results produced with Pramaan, we ask — as a matter of intellectual honesty, not as a legal condition — that you credit the tool, state the parameters used, and disclose limitations.

## 9. Governing jurisdiction

These terms are governed by the laws of India. Any dispute is subject to the exclusive jurisdiction of the courts of Gujarat, India.

## 10. Severability

If any provision is held unenforceable, the remaining provisions continue in full force.
