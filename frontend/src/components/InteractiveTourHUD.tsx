"use client";

import React, { useState } from "react";
import { ChevronDown, ChevronUp, Sparkles, BookOpen } from "lucide-react";

interface InteractiveTourHUDProps {
  onOpenMethodology: () => void;
}

export const InteractiveTourHUD: React.FC<InteractiveTourHUDProps> = ({
  onOpenMethodology,
}) => {
  const [activeConcept, setActiveConcept] = useState<"mirage" | "taxes" | "reality" | null>(null);
  const [isCollapsed, setIsCollapsed] = useState(false);

  const concepts = [
    {
      id: "mirage" as const,
      color: "border-pacificCyan text-pacificCyan bg-pacificCyan/10",
      badgeBg: "bg-pacificCyan",
      title: "1. The Paper Mirage",
      tagline: "Gross returns before taxes",
      detail:
        "Naive backtesters assume trades execute at exact close prices with 0% taxes and 0 slippage. This creates an illusion of 40%–80% annual returns that vanish in live trading.",
    },
    {
      id: "taxes" as const,
      color: "border-crimson text-crimson bg-crimson/10",
      badgeBg: "bg-crimson",
      title: "2. Indian Tax Tollgate",
      tagline: "Statutory friction drag",
      detail:
        "Pramaan deducts statutory Indian delivery taxes: STT (0.1% on buy & sell), Stamp Duty (0.015% buy-only), GST (18%), and Almgren-Chriss square-root market impact.",
    },
    {
      id: "reality" as const,
      color: "border-turquoise text-turquoise bg-turquoise/10",
      badgeBg: "bg-turquoise",
      title: "3. Bankable Net Alpha",
      tagline: "Real cash in hand",
      detail:
        "Realistic next-day (T+1 Open) execution with full costs deducted. If an active strategy cannot beat a passive Buy & Hold baseline here, it possesses no true edge.",
    },
  ];

  return (
    <div className="bg-panel/90 border border-rule rounded-md shadow-sm overflow-hidden transition-all duration-200">
      {/* Top Banner Bar */}
      <div className="px-3.5 py-2 flex items-center justify-between border-b border-rule/60 bg-canvas/40">
        <div className="flex items-center gap-2">
          <div className="w-5 h-5 rounded bg-turquoise/20 flex items-center justify-center text-turquoise text-xs font-bold font-mono">
            प्र
          </div>
          <span className="text-xs font-bold text-inkText tracking-tight">
            How to Read Pramaan
          </span>
          <span className="text-[10px] text-mutedText hidden sm:inline">
            · The 3 core principles of honest backtesting
          </span>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={onOpenMethodology}
            className="text-[11px] text-turquoise hover:underline flex items-center gap-1 font-medium cursor-pointer"
          >
            <BookOpen size={12} />
            <span>Full Syllabus Guide</span>
          </button>
          <span className="text-rule">|</span>
          <button
            type="button"
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="text-mutedText hover:text-inkText text-xs p-1 rounded hover:bg-canvas transition-colors cursor-pointer"
            title={isCollapsed ? "Expand guidance" : "Collapse guidance"}
          >
            {isCollapsed ? <ChevronDown size={14} /> : <ChevronUp size={14} />}
          </button>
        </div>
      </div>

      {/* Main Content Tray */}
      {!isCollapsed && (
        <div className="p-3 space-y-2.5">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
            {concepts.map((c) => {
              const isSelected = activeConcept === c.id;
              return (
                <div
                  key={c.id}
                  onClick={() => setActiveConcept(isSelected ? null : c.id)}
                  className={`p-2.5 rounded border transition-all cursor-pointer ${
                    isSelected
                      ? `${c.color} shadow-sm ring-1 ring-current`
                      : "bg-canvas/50 border-rule/80 hover:border-rule hover:bg-canvas"
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs font-semibold text-inkText">
                      {c.title}
                    </span>
                    <span
                      className={`w-2 h-2 rounded-full ${c.badgeBg}`}
                    />
                  </div>
                  <div className="text-[11px] text-mutedText font-medium">
                    {c.tagline}
                  </div>
                  <p className="text-[11px] text-mutedText/90 mt-1 leading-relaxed">
                    {c.detail}
                  </p>
                </div>
              );
            })}
          </div>

          <div className="px-2.5 py-1.5 rounded bg-canvas/70 border border-rule/50 flex items-center justify-between text-[11px] text-mutedText">
            <span className="flex items-center gap-1.5">
              <Sparkles size={12} className="text-turquoise" />
              <span>
                <strong>Quick Tip:</strong> Click any of the 3 cards above or change parameters on the left to watch how statutory taxes compress the gross paper curve.
              </span>
            </span>
          </div>
        </div>
      )}
    </div>
  );
};
