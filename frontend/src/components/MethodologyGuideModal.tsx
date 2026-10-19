"use client";
import React from "react";

interface GuideModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const MethodologyGuideModal: React.FC<GuideModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-canvas/80 backdrop-blur-sm animate-fade-in">
      <div 
        className="bg-panel border border-ruleHighlight max-w-3xl w-full max-h-[85vh] flex flex-col shadow-2xl rounded-sm overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Header */}
        <div className="border-b border-rule p-5 flex items-center justify-between bg-panelElevated">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-primary/20 border border-primary/40 flex items-center justify-center font-bold text-sm text-primary font-mono rounded">
              प्र
            </div>
            <div>
              <h2 className="text-base font-bold text-inkText">
                Pramaan Field Guide & Examiner Reference
              </h2>
              <p className="text-xs text-mutedText">
                How Pramaan unmasks the retail backtest mirage (GTU DI05000341).
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-mutedText hover:text-inkText text-lg px-2 py-1 rounded border border-transparent hover:border-rule transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Modal Scrollable Content */}
        <div className="p-6 overflow-y-auto space-y-6 text-xs text-mutedText leading-relaxed font-sans">
          {/* Section 1: The Core Thesis */}
          <div className="space-y-2">
            <h3 className="text-sm font-semibold text-inkText flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-alpha"></span>
              1. The Core Problem: The Profit Mirage
            </h3>
            <p>
              Most retail backtests (TradingView PineScript, naive Python scripts) report 40%–80% annual returns because they commit two fatal sins:
            </p>
            <ul className="list-disc pl-5 space-y-1">
              <li>
                <strong className="text-inkText">Zero-Execution Friction:</strong> They assume trades execute at the exact close price with zero taxes, zero exchange fees, and zero market impact.
              </li>
              <li>
                <strong className="text-inkText">Lookahead & Fill Bias:</strong> They generate a signal at Bar $t$ close and magically execute at Bar $t$ close.
              </li>
            </ul>
            <div className="p-3 bg-canvas border border-rule text-inkText font-mono text-[11px] rounded">
              Pramaan Invariant: Signal on Bar $t$ Close $\longrightarrow$ Order queued $\longrightarrow$ Executed on Bar $t+1$ Open.
            </div>
          </div>

          {/* Section 2: Statutory Indian Cost Stack */}
          <div className="space-y-2">
            <h3 className="text-sm font-semibold text-inkText flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-stamp"></span>
              2. The Statutory Indian Tollgate
            </h3>
            <p>
              Indian equity delivery transactions bear unavoidable statutory friction modeled to the exact paise:
            </p>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 font-mono text-[11px]">
              <div className="p-2.5 bg-canvas border border-rule">
                <div className="text-inkText font-medium">STT (Securities Tax)</div>
                <div className="text-stamp">0.10% on BUY & SELL</div>
              </div>
              <div className="p-2.5 bg-canvas border border-rule">
                <div className="text-inkText font-medium">Stamp Duty</div>
                <div className="text-stamp">0.015% on BUY</div>
              </div>
              <div className="p-2.5 bg-canvas border border-rule">
                <div className="text-inkText font-medium">Exchange Turnover</div>
                <div className="text-stamp">0.00297% (NSE)</div>
              </div>
              <div className="p-2.5 bg-canvas border border-rule">
                <div className="text-inkText font-medium">SEBI Turnover Fee</div>
                <div className="text-stamp">₹10 per crore</div>
              </div>
              <div className="p-2.5 bg-canvas border border-rule">
                <div className="text-inkText font-medium">GST</div>
                <div className="text-stamp">18% on fees</div>
              </div>
              <div className="p-2.5 bg-canvas border border-rule">
                <div className="text-inkText font-medium">Almgren-Chriss Impact</div>
                <div className="text-friction">Volume-weighted slippage</div>
              </div>
            </div>
          </div>

          {/* Section 3: Metric Reference */}
          <div className="space-y-2">
            <h3 className="text-sm font-semibold text-inkText flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-primary"></span>
              3. Metric & Diagnostic Glossary
            </h3>
            <div className="space-y-2.5">
              <div className="border-l-2 border-alpha pl-3 py-0.5">
                <div className="text-inkText font-medium">CAGR (Compound Annual Growth Rate)</div>
                <div>Annualized geometric return. Benchmarked against Nifty 10 Buy & Hold (19.07% over 2019–2024).</div>
              </div>
              <div className="border-l-2 border-primary pl-3 py-0.5">
                <div className="text-inkText font-medium">Sharpe & Sortino Ratios</div>
                <div>Risk-adjusted return measured against a 6.0% Indian risk-free hurdle. Sortino isolates downside deviation.</div>
              </div>
              <div className="border-l-2 border-friction pl-3 py-0.5">
                <div className="text-inkText font-medium">Maximum Drawdown</div>
                <div>The peak-to-trough depth of portfolio equity decline. Critical for risk management.</div>
              </div>
              <div className="border-l-2 border-stamp pl-3 py-0.5">
                <div className="text-inkText font-medium">Deflated Sharpe Ratio (DSR) & PBO</div>
                <div>
                  Marcos López de Prado (2014) mathematical formulation that deflates the observed Sharpe ratio for multiple hypothesis testing ($N$ trials, variance, skewness, kurtosis). A p-value &ge; 0.05 indicates statistical overfitting.
                </div>
              </div>
            </div>
          </div>

          {/* Section 4: Why These Strategies? */}
          <div className="space-y-2">
            <h3 className="text-sm font-semibold text-inkText flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-cyan"></span>
              4. Why Are The Strategies Canonical?
            </h3>
            <p>
              In quantitative academic research, the engine itself is the contribution. The strategies included (SMA Trend, RSI Mean Reversion, Momentum ROC, Bollinger Breakout, Buy & Hold) are the universal canonical baselines. They serve as the exact benchmark strategies promoted across retail media — allowing Pramaan to scientifically prove how their reported profits evaporate under real-world market microstructure.
            </p>
          </div>
        </div>

        {/* Modal Footer */}
        <div className="border-t border-rule p-4 bg-panelElevated flex items-center justify-between">
          <span className="text-[11px] text-mutedText font-mono">
            Pramaan Engine · Academic Viva Edition
          </span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 bg-primary hover:bg-primaryHover text-white font-medium text-xs rounded transition-colors"
          >
            Got It, Proceed to Terminal
          </button>
        </div>
      </div>
    </div>
  );
};
