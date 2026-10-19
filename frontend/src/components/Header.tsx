"use client";
import React from "react";

interface HeaderProps {
  demoMode: boolean;
  engineOnline: boolean;
  theme: "dark" | "light";
  onToggleTheme: () => void;
  onOpenGuide: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  demoMode,
  engineOnline,
  theme,
  onToggleTheme,
  onOpenGuide,
}) => {
  return (
    <header className="h-14 shrink-0 bg-panel border-b border-rule flex flex-col justify-between select-none relative z-30">
      <div className="h-full px-5 flex items-center justify-between">
        {/* Left: Brand Identity */}
        <div className="flex items-center gap-3.5">
          <div className="w-8 h-8 rounded bg-gradient-to-br from-pacificCyan to-turquoise flex items-center justify-center font-bold text-darkSlate text-base shadow-sm font-mono">
            प्र
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-base tracking-tight text-inkText">
                PRAMAAN
              </span>
              <span className="text-[11px] font-mono text-mutedText">
                (प्रमाण)
              </span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-canvas border border-rule text-turquoise font-semibold">
                GTU DI05000341
              </span>
            </div>
            <div className="text-[11px] text-mutedText flex items-center gap-2">
              <span>The Honest Indian Equity Backtester</span>
              <span>·</span>
              <span className="text-turquoise">Realistic Execution & Taxes</span>
            </div>
          </div>
        </div>

        {/* Center: Live Universe & Invariant Ticker */}
        <div className="hidden lg:flex items-center gap-3.5 text-xs bg-canvas/60 border border-rule px-3.5 py-1.5 rounded-md">
          <div className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-turquoise animate-pulse" />
            <span className="text-mutedText">Universe:</span>
            <span className="text-inkText font-semibold">10 NIFTY Equities</span>
          </div>
          <span className="text-rule">|</span>
          <div>
            <span className="text-mutedText">Historical Window:</span>
            <span className="text-inkText font-semibold ml-1">2019–2024</span>
          </div>
          <span className="text-rule">|</span>
          <div className="text-mutedText">
            Statutory Taxes: <span className="text-crimson font-semibold">STT 0.1% + GST 18%</span>
          </div>
        </div>

        {/* Right: Actions & Status */}
        <div className="flex items-center gap-2.5 text-xs">
          <button
            type="button"
            onClick={onOpenGuide}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-canvas border border-rule hover:border-turquoise text-mutedText hover:text-turquoise transition-all cursor-pointer"
            title="Read Pramaan Field Guide & Examiner Reference"
          >
            <span className="text-turquoise font-bold">📘</span>
            <span className="font-medium">Quick Guide</span>
          </button>

          <button
            type="button"
            onClick={onToggleTheme}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-canvas border border-rule hover:border-turquoise text-inkText transition-all cursor-pointer"
            title="Toggle Dark vs Light Mode"
          >
            <span>{theme === "dark" ? "☀️ Light" : "🌙 Dark"}</span>
          </button>

          <div className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-canvas border border-rule">
            <span
              className={`w-2 h-2 rounded-full ${
                engineOnline ? "bg-turquoise shadow-sm shadow-turquoise" : "bg-crimson"
              }`}
            />
            <span className="text-[11px] text-mutedText">
              <span className="text-inkText font-medium">{engineOnline ? "Engine Ready" : "Offline Cache"}</span>
            </span>
          </div>

          {demoMode ? (
            <span className="px-2 py-1 rounded text-[10px] font-bold bg-turquoise/15 border border-turquoise/40 text-turquoise">
              VERIFIED NSE DATA
            </span>
          ) : (
            <span className="px-2 py-1 rounded text-[10px] font-bold bg-pacificCyan/20 border border-pacificCyan text-pacificCyan">
              LIVE SIMULATION
            </span>
          )}
        </div>
      </div>

      {/* Signature User Color Gradient Edge */}
      <div className="h-[2px] w-full bg-gradient-banner" />
    </header>
  );
};
