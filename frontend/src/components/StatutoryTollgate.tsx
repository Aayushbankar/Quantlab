"use client";
import React from "react";

interface TollgateProps {
  brokerage: number;
  stt: number;
  stampDuty: number;
  turnoverFees: number;
  gst: number;
  dpCharges?: number;
  sebiFees?: number;
  ipft?: number;
  marketImpact: number;
  totalFriction: number;
  initialCapital: number;
  costProfile?: string;
}

export const StatutoryTollgate: React.FC<TollgateProps> = ({
  brokerage,
  stt,
  stampDuty,
  turnoverFees,
  gst,
  dpCharges = 0,
  sebiFees = 0,
  ipft = 0,
  marketImpact,
  totalFriction,
  initialCapital,
  costProfile = "zerodha_delivery_2024",
}) => {
  const items = [
    {
      label: "Securities Transaction Tax (STT)",
      amount: stt,
      desc: "0.10% on delivery turnover (buy + sell legs)",
      share: totalFriction ? (stt / totalFriction) * 100 : 0,
      color: "bg-crimson",
    },
    {
      label: "Almgren–Chriss Market Impact & Slippage",
      amount: marketImpact,
      desc: "Execution slippage relative to Average Daily Volume (ADV)",
      share: totalFriction ? (marketImpact / totalFriction) * 100 : 0,
      color: "bg-crimson/80",
    },
    {
      label: "Depository Participant (DP) Charges",
      amount: dpCharges,
      desc: "Flat ₹13.50 + GST per debit transaction (CDSL/NSDL)",
      share: totalFriction ? (dpCharges / totalFriction) * 100 : 0,
      color: "bg-amber-600",
    },
    {
      label: "Brokerage Commission",
      amount: brokerage,
      desc: costProfile.includes("zerodha")
        ? "₹0 Delivery brokerage (True-to-Label)"
        : "₹20 / order discount brokerage",
      share: totalFriction ? (brokerage / totalFriction) * 100 : 0,
      color: "bg-stamp",
    },
    {
      label: "GST (18%)",
      amount: gst,
      desc: "18% Goods & Services Tax on brokerage, exchange fees & DP charges",
      share: totalFriction ? (gst / totalFriction) * 100 : 0,
      color: "bg-stormyTeal",
    },
    {
      label: "Stamp Duty",
      amount: stampDuty,
      desc: "0.015% buy-side statutory tax (Indian Stamp Act)",
      share: totalFriction ? (stampDuty / totalFriction) * 100 : 0,
      color: "bg-pacificCyan",
    },
    {
      label: "NSE Turnover & SEBI Fees",
      amount: turnoverFees + sebiFees,
      desc: "0.00297% NSE exchange charge + ₹10/crore SEBI fee",
      share: totalFriction ? ((turnoverFees + sebiFees) / totalFriction) * 100 : 0,
      color: "bg-turquoise",
    },
    {
      label: "Investor Protection Fund (IPFT)",
      amount: ipft,
      desc: "₹10 per crore exchange tariff to IPF trust",
      share: totalFriction ? (ipft / totalFriction) * 100 : 0,
      color: "bg-teal-600",
    },
  ];

  return (
    <div className="bg-panel border border-rule p-5 h-full flex flex-col justify-between rounded-sm">
      <div>
        <div className="flex items-baseline justify-between border-b border-rule pb-3">
          <div>
            <h3 className="text-inkText text-sm font-semibold tracking-tight">
              Statutory Friction Tollgate
            </h3>
            <span className="text-[10px] text-mutedText font-mono">
              Profile: {costProfile}
            </span>
          </div>
          <span className="text-crimson font-mono text-xs font-semibold">
            -₹{totalFriction.toLocaleString("en-IN", { maximumFractionDigits: 2 })}
          </span>
        </div>
        <p className="text-mutedText text-xs mt-2 mb-3">
          Exact paisa-level statutory deductions applied to every filled bar execution per SEBI & NSE circulars (Oct 2024 True-to-Label compliant).
        </p>

        {/* Visual Share Bar */}
        <div className="w-full h-2.5 bg-canvas flex overflow-hidden border border-rule mb-3.5 rounded-full">
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
        <div className="space-y-2 font-tabular text-xs max-h-[360px] overflow-y-auto pr-1">
          {items.map((item, idx) => (
            <div
              key={idx}
              className="flex items-center justify-between py-1 border-b border-rule/40 last:border-0"
            >
              <div className="flex items-center gap-2">
                <span className={`w-2 h-2 rounded-full shrink-0 ${item.color}`} />
                <div>
                  <div className="text-inkText font-medium text-[11px]">{item.label}</div>
                  <div className="text-[9px] text-mutedText">{item.desc}</div>
                </div>
              </div>
              <div className="text-right font-mono">
                <div className="text-inkText font-medium text-[11px]">
                  ₹{item.amount.toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                </div>
                <div className="text-[9px] text-mutedText">{item.share.toFixed(1)}%</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="mt-4 pt-3 border-t border-rule flex items-center justify-between text-xs font-mono">
        <span className="text-mutedText">Statutory Drag (% of Capital):</span>
        <span className="text-crimson font-bold font-tabular">
          {initialCapital ? ((totalFriction / initialCapital) * 100).toFixed(2) : "0.00"}%
        </span>
      </div>
    </div>
  );
};
