"use client";
import React, { useState } from "react";

export interface Trade {
  timestamp: string;
  symbol: string;
  side: string;
  quantity: number;
  raw_price: number;
  fill_price: number;
  total_cost: number;
  status: string;
  reason?: string | null;
}

interface LedgerProps {
  trades: Trade[];
}

export const ExecutionLedger: React.FC<LedgerProps> = ({ trades }) => {
  const [filterSymbol, setFilterSymbol] = useState<string>("ALL");
  const [filterStatus, setFilterStatus] = useState<string>("ALL");

  const symbols = ["ALL", ...Array.from(new Set(trades.map((t) => t.symbol)))];

  const displayedTrades = trades.filter((t) => {
    if (filterSymbol !== "ALL" && t.symbol !== filterSymbol) return false;
    if (filterStatus === "FILLED" && t.status === "REJECTED") return false;
    if (filterStatus === "REJECTED" && t.status !== "REJECTED") return false;
    return true;
  });

  const rejectedCount = trades.filter((t) => t.status === "REJECTED").length;

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

          {/* Filters */}
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1.5 text-xs text-mutedText">
              <span>Status:</span>
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="bg-canvas border border-rule text-inkText text-xs px-2 py-1 outline-none font-mono rounded focus:border-pacificCyan"
              >
                <option value="ALL">All ({trades.length})</option>
                <option value="FILLED">Filled ({trades.length - rejectedCount})</option>
                <option value="REJECTED">Rejected ({rejectedCount})</option>
              </select>
            </div>

            <div className="flex items-center gap-1.5 text-xs text-mutedText">
              <span>Symbol:</span>
              <select
                value={filterSymbol}
                onChange={(e) => setFilterSymbol(e.target.value)}
                className="bg-canvas border border-rule text-inkText text-xs px-2 py-1 outline-none font-mono rounded focus:border-pacificCyan"
              >
                {symbols.map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {displayedTrades.length === 0 ? (
          <div className="py-12 text-center text-xs text-mutedText font-mono">
            No trade fills recorded matching the selected filter.
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
                  <th className="py-2 px-3 text-center">Status / Invariant</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-rule/40 font-mono text-[11px]">
                {displayedTrades.map((t, idx) => {
                  const slippageDelta = t.fill_price - t.raw_price;
                  const isRejected = t.status === "REJECTED";

                  return (
                    <tr
                      key={idx}
                      className={`hover:bg-panelHover transition-colors ${
                        isRejected ? "bg-crimson/5 opacity-80" : ""
                      }`}
                    >
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
                      <td className="py-2 px-3 text-right font-medium">
                        {isRejected ? "—" : t.quantity}
                      </td>
                      <td className="py-2 px-3 text-right text-mutedText">
                        ₹{t.raw_price.toFixed(2)}
                      </td>
                      <td className="py-2 px-3 text-right font-semibold text-inkText">
                        {isRejected ? "—" : `₹${t.fill_price.toFixed(2)}`}
                      </td>
                      <td className="py-2 px-3 text-right text-crimson">
                        {isRejected ? (
                          <span className="text-mutedText">₹0.00</span>
                        ) : (
                          <>
                            +₹{t.total_cost.toFixed(2)}
                            {slippageDelta !== 0 && (
                              <span className="text-[10px] text-mutedText block">
                                (Δ ₹{slippageDelta.toFixed(2)})
                              </span>
                            )}
                          </>
                        )}
                      </td>
                      <td className="py-2 px-3 text-center">
                        {isRejected ? (
                          <span
                            className="text-crimson text-[10px] bg-crimson/15 px-1.5 py-0.5 rounded border border-crimson/40 cursor-help"
                            title={t.reason || "Order rejected due to risk limit or insufficient cash"}
                          >
                            REJECTED: {t.reason ? t.reason.slice(0, 22) : "NO CASH"}...
                          </span>
                        ) : (
                          <span className="text-turquoise text-[10px] bg-turquoise/10 px-1 py-0.5 rounded border border-turquoise/30">
                            T+1 ZERO-LOOKAHEAD
                          </span>
                        )}
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
        <span>
          Recorded Trades: <span className="text-inkText font-bold">{displayedTrades.length}</span>
          {rejectedCount > 0 && (
            <span className="text-crimson ml-2">({rejectedCount} rejected)</span>
          )}
        </span>
        <span>Execution Engine: <span className="text-turquoise font-medium">T+1 Next Bar Open</span></span>
      </div>
    </div>
  );
};
