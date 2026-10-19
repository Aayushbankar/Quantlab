"use client";
import React from "react";

interface TollgateProps {
  brokerage: number;
  stt: number;
  stampDuty: number;
  turnoverFees: number;
  gst: number;
  marketImpact: number;
  totalFriction: number;
  initialCapital: number;
}

export const StatutoryTollgate: React.FC<TollgateProps> = ({
  brokerage,
  stt,
  stampDuty,
  turnoverFees,
  gst,
  marketImpact,
  totalFriction,
  initialCapital,
}) => {
  const items = [
    { label: "Securities Transaction Tax (STT)", amount: stt, desc: "0.10% delivery on both buy and sell legs", share: totalFriction ? (stt / totalFriction) * 100 : 0, color: "bg-crimson" },
    { label: "Almgren–Chriss Market Impact", amount: marketImpact, desc: "Square-root execution slippage vs ADV", share: totalFriction ? (marketImpact / totalFriction) * 100 : 0, color: "bg-crimson/80" },
    { label: "Brokerage Commission", amount: brokerage, desc: "min(₹20, 0.03%) per executed order", share: totalFriction ? (brokerage / totalFriction) * 100 : 0, color: "bg-stamp" },
    { label: "GST (18%)", amount: gst, desc: "18% statutory tax on brokerage and turnover", share: totalFriction ? (gst / totalFriction) * 100 : 0, color: "bg-stormyTeal" },
    { label: "Stamp Duty", amount: stampDuty, desc: "0.015% buy-side only (Indian Stamp Act)", share: totalFriction ? (stampDuty / totalFriction) * 100 : 0, color: "bg-pacificCyan" },
    { label: "NSE & SEBI Turnover Charges", amount: turnoverFees, desc: "0.00297% NSE + 0.0001% SEBI fee", share: totalFriction ? (turnoverFees / totalFriction) * 100 : 0, color: "bg-turquoise" },
  ];

  return (
    <div className="bg-panel border border-rule p-5 h-full flex flex-col justify-between rounded-sm">
      <div>
        <div className="flex items-baseline justify-between border-b border-rule pb-3">
          <h3 className="text-inkText text-sm font-semibold tracking-tight">
            Statutory Friction Tollgate
          </h3>
          <span className="text-crimson font-mono text-xs font-semibold">
            -₹{totalFriction.toLocaleString("en-IN", { maximumFractionDigits: 2 })}
          </span>
        </div>
        <p className="text-mutedText text-xs mt-2 mb-4">
          Paise-level statutory deductions applied to every filled bar execution per SEBI & NSE circulars.
        </p>

        {/* Visual Share Bar */}
        <div className="w-full h-2.5 bg-canvas flex overflow-hidden border border-rule mb-4 rounded-full">
          {items.map((item, idx) => (
            <div
              key={idx}
              style={{ width: `${item.share}%` }}
              className={`${item.color} transition-all`}
              title={`${item.label}: ₹${item.amount.toFixed(0)} (${item.share.toFixed(1)}%)`}
            />
          ))}
        </div>

        {/* Breakdown Items */}
        <div className="space-y-3 font-tabular text-xs">
          {items.map((item, idx) => (
            <div key={idx} className="flex items-center justify-between py-0.5 border-b border-rule/40 last:border-0">
              <div className="flex items-center gap-2">
                <span className={`w-2 h-2 rounded-full ${item.color}`} />
                <div>
                  <div className="text-inkText font-medium">{item.label}</div>
                  <div className="text-[10px] text-mutedText">{item.desc}</div>
                </div>
              </div>
              <div className="text-right font-mono">
                <div className="text-inkText font-medium">₹{item.amount.toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</div>
                <div className="text-[10px] text-mutedText">{item.share.toFixed(1)}%</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="mt-4 pt-3 border-t border-rule flex items-center justify-between text-xs font-mono">
        <span className="text-mutedText">Friction as % of Capital:</span>
        <span className="text-crimson font-bold font-tabular">
          {initialCapital ? ((totalFriction / initialCapital) * 100).toFixed(2) : "0.00"}%
        </span>
      </div>
    </div>
  );
};
