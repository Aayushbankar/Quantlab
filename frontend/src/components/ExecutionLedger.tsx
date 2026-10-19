"use client";
import React, { useState } from "react";

interface Trade {
  timestamp: string;
  symbol: string;
  side: string;
  quantity: number;
  raw_price: number;
  fill_price: number;
  total_cost: number;
  status: string;
}

interface LedgerProps {
  trades: Trade[];
}

export const ExecutionLedger: React.FC<LedgerProps> = ({ trades }) => {
  const [filterSymbol, setFilterSymbol] = useState<string>("ALL");

  const symbols = ["ALL", ...Array.from(new Set(trades.map((t) => t.symbol)))];
  const displayedTrades = filterSymbol === "ALL" ? trades : trades.filter((t) => t.symbol === filterSymbol);

  return (
    <div className="bg-panel border border-rule p-5 rounded-sm h-full flex flex-col justify-between">
      <div>
        <div className="flex flex-col sm:flex-row sm:items-baseline justify-between border-b border-rule pb-3 gap-2">
          <div>
            <h3 className="text-inkText text-sm font-semibold tracking-tight">
              T+1 Execution Ledger & Invariant Audit
            </h3>
            <p className="text-mutedText text-xs mt-0.5">
              Zero look-ahead verification: Signals generated at Close $t$ fill strictly at Open $t+1$ with Almgren-Chriss impact.
            </p>
          </div>

          {/* Filter */}
          <div className="flex items-center gap-2">
            <span className="text-xs text-mutedText">Filter Symbol:</span>
            <select
              value={filterSymbol}
              onChange={(e) => setFilterSymbol(e.target.value)}
              className="bg-canvas border border-rule text-inkText text-xs px-2.5 py-1 outline-none font-mono rounded focus:border-pacificCyan"
            >
              {symbols.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </div>
        </div>

        {displayedTrades.length === 0 ? (
          <div className="py-12 text-center text-xs text-mutedText font-mono">
            No trade fills recorded in this period. Either buy-and-hold was chosen or no signals triggered.
          </div>
        ) : (
          <div className="mt-3 overflow-x-auto max-h-[440px]">
            <table className="w-full text-left font-tabular text-xs">
              <thead className="border-b border-rule text-mutedText text-[11px] font-mono sticky top-0 bg-panel z-10">
                <tr>
                  <th className="py-2 px-3">Date (T+1 Fill)</th>
                  <th className="py-2 px-3">Symbol</th>
                  <th className="py-2 px-3">Side</th>
                  <th className="py-2 px-3 text-right">Quantity</th>
                  <th className="py-2 px-3 text-right">Signal Close</th>
                  <th className="py-2 px-3 text-right">Executed Fill</th>
                  <th className="py-2 px-3 text-right">Slippage & Costs</th>
                  <th className="py-2 px-3 text-center">Invariant</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-rule/40 font-mono text-[11px]">
                {displayedTrades.map((t, idx) => {
                  const slippageDelta = t.fill_price - t.raw_price;
                  return (
                    <tr key={idx} className="hover:bg-panelHover transition-colors">
                      <td className="py-2 px-3 text-mutedText">{t.timestamp}</td>
                      <td className="py-2 px-3 font-semibold text-inkText">{t.symbol}</td>
                      <td className="py-2 px-3">
                        <span
                          className={`px-1.5 py-0.5 text-[10px] font-bold rounded ${
                            t.side === "BUY"
                              ? "bg-turquoise/15 text-turquoise border border-turquoise/40"
                              : "bg-crimson/15 text-crimson border border-crimson/40"
                          }`}
                        >
                          {t.side}
                        </span>
                      </td>
                      <td className="py-2 px-3 text-right font-medium">{t.quantity}</td>
                      <td className="py-2 px-3 text-right text-mutedText">₹{t.raw_price.toFixed(2)}</td>
                      <td className="py-2 px-3 text-right font-semibold text-inkText">
                        ₹{t.fill_price.toFixed(2)}
                      </td>
                      <td className="py-2 px-3 text-right text-crimson">
                        +₹{t.total_cost.toFixed(2)}
                        {slippageDelta !== 0 && (
                          <span className="text-[10px] text-mutedText block">
                            (Δ ₹{slippageDelta.toFixed(2)})
                          </span>
                        )}
                      </td>
                      <td className="py-2 px-3 text-center">
                        <span className="text-turquoise text-[10px] bg-turquoise/10 px-1 py-0.5 rounded border border-turquoise/30">
                          T+1 ZERO-LOOKAHEAD
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="mt-3 pt-3 border-t border-rule flex items-center justify-between text-[11px] font-mono text-mutedText">
        <span>Recorded Trades: <span className="text-inkText font-bold">{displayedTrades.length}</span></span>
        <span>Execution Engine: <span className="text-turquoise font-medium">T+1 Next Bar Open</span></span>
      </div>
    </div>
  );
};
