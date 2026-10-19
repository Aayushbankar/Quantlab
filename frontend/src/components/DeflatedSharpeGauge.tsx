"use client";
import React from "react";

interface DSRProps {
  observedSharpe: number;
  expectedMaxSharpe?: number | null;
  dsrPValue?: number | null;
  nTrials: number;
}

export const DeflatedSharpeGauge: React.FC<DSRProps> = ({
  observedSharpe,
  expectedMaxSharpe = 0.746,
  dsrPValue = 0.041,
  nTrials = 30,
}) => {
  const pVal = dsrPValue ?? 0.041;
  const ems = expectedMaxSharpe ?? 0.746;
  const isSignificant = pVal >= 0.95;

  return (
    <div className="bg-panel border border-rule p-5 flex flex-col justify-between rounded-sm h-full">
      <div>
        <div className="flex items-baseline justify-between border-b border-rule pb-3">
          <h3 className="text-inkText text-sm font-semibold tracking-tight">
            Deflated Sharpe Ratio (DSR)
          </h3>
          <span
            className={`font-mono text-xs px-2 py-0.5 rounded border font-semibold ${
              isSignificant
                ? "bg-turquoise/15 border-turquoise/40 text-turquoise"
                : "bg-crimson/15 border-crimson/40 text-crimson"
            }`}
          >
            {isSignificant ? "STATISTICALLY VALID" : "OVERFITTING DETECTED"}
          </span>
        </div>
        <p className="text-mutedText text-xs mt-2 mb-4">
          Marcos López de Prado selection-bias discount: adjusts observed Sharpe for non-normality (skewness, kurtosis) and multiple testing ($N = {nTrials}$).
        </p>

        {/* Metric Cards */}
        <div className="grid grid-cols-2 gap-3 mb-4 font-tabular">
          <div className="bg-canvas border border-rule p-3 rounded">
            <div className="text-mutedText text-[11px]">Observed Sharpe (SR)</div>
            <div className="text-turquoise font-mono text-lg font-bold mt-0.5">
              {observedSharpe.toFixed(3)}
            </div>
          </div>
          <div className="bg-canvas border border-rule p-3 rounded">
            <div className="text-mutedText text-[11px]">Expected Max SR (EVT)</div>
            <div className="text-stamp font-mono text-lg font-bold mt-0.5">
              {ems.toFixed(3)}
            </div>
          </div>
        </div>

        {/* DSR P-value Bar */}
        <div className="space-y-1.5 font-tabular text-xs">
          <div className="flex justify-between items-baseline">
            <span className="text-mutedText">DSR Significance Level:</span>
            <span className={`font-mono font-bold ${isSignificant ? "text-turquoise" : "text-crimson"}`}>
              {(pVal * 100).toFixed(1)}% (p-val: {pVal.toFixed(3)})
            </span>
          </div>
          <div className="w-full bg-canvas border border-rule h-2 rounded-full overflow-hidden">
            <div
              className={`h-full transition-all ${isSignificant ? "bg-turquoise" : "bg-crimson"}`}
              style={{ width: `${Math.min(100, Math.max(5, pVal * 100))}%` }}
            />
          </div>
          <div className="flex justify-between text-[10px] text-mutedText font-mono pt-0.5">
            <span>0% (Spurious Noise)</span>
            <span className="text-stamp">95% Significance Threshold</span>
            <span>100% (True Edge)</span>
          </div>
        </div>
      </div>

      <div className="mt-4 pt-3 border-t border-rule text-[11px] text-mutedText">
        {isSignificant ? (
          <span className="text-turquoise">✓ Strategy survives multiple testing discount. False discovery unlikely.</span>
        ) : (
          <span className="text-crimson">⚠ Strategy Sharpe ratio fails EVT hurdle. Edge likely phantom of backtest overfitting.</span>
        )}
      </div>
    </div>
  );
};
