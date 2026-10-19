"use client";
import React from "react";

interface HeaderProps {
  demoMode: boolean;
  engineOnline: boolean;
  theme: "dark" | "light";
  servedFrom?: "live" | "cache" | "replay";
  replayReason?: string | null;
  dataHash?: string;
  costProfile?: string;
  runId?: string;
  onToggleTheme: () => void;
  onOpenGuide: () => void;
  onOpenHistory?: () => void;
  onDownloadReport?: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  demoMode,
  engineOnline,
  theme,
  servedFrom = "live",
  replayReason,
  dataHash,
  costProfile,
  runId,
  onToggleTheme,
  onOpenGuide,
  onOpenHistory,
  onDownloadReport,
}) => {
  const shortHash = dataHash ? dataHash.slice(0, 8) : "offline";

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
              <span>Honest Indian Equities Backtester</span>
              <span>·</span>
              <span className="text-turquoise">Full Tax Tollgate & Overfitting Guard</span>
            </div>
          </div>
        </div>

        {/* Center: Provenance Pill & Live Indicator (C2) */}
        <div className="hidden md:flex items-center gap-2.5 text-xs bg-canvas/80 border border-rule px-3.5 py-1.5 rounded-md">
          {/* Served From Badge */}
          {servedFrom === "live" && (
            <span
              className="flex items-center gap-1.5 px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-turquoise/15 text-turquoise border border-turquoise/40"
              title="Computed live by FastAPI simulation engine"
            >
              <span className="w-1.5 h-1.5 rounded-full bg-turquoise animate-pulse" />
              SERVED: LIVE
            </span>
          )}
          {servedFrom === "cache" && (
            <span
              className="flex items-center gap-1.5 px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-500/15 text-amber-400 border border-amber-500/40"
              title="Retrieved from SQLite cache by deterministic request hash"
            >
              <span className="w-1.5 h-1.5 rounded-full bg-amber-400" />
              SERVED: CACHE
            </span>
          )}
          {servedFrom === "replay" && (
            <span
              className="flex items-center gap-1.5 px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-blue-500/15 text-blue-400 border border-blue-500/40"
              title={replayReason || "Loaded from committed deterministic experiment replay"}
            >
              <span className="w-1.5 h-1.5 rounded-full bg-blue-400" />
              SERVED: REPLAY
            </span>
          )}

          <span className="text-rule">|</span>

          {/* Data Hash */}
          <div className="flex items-center gap-1 font-mono text-[11px]" title={`Data Hash: ${dataHash || "offline"}`}>
            <span className="text-mutedText">Data:</span>
            <span className="text-inkText font-medium">{shortHash}</span>
          </div>

          <span className="text-rule">|</span>

          {/* Cost Profile */}
          <div className="text-[11px]" title={`Statutory Cost Card: ${costProfile || "zerodha_delivery_2024"}`}>
            <span className="text-mutedText">Rates: </span>
            <span className="text-turquoise font-medium">
              {costProfile?.includes("2024") ? "Oct 2024 True-to-Label" : costProfile || "Indian Delivery"}
            </span>
          </div>
        </div>

        {/* Right: Actions & Status */}
        <div className="flex items-center gap-2 text-xs">
          {runId && onDownloadReport && (
            <button
              type="button"
              onClick={onDownloadReport}
              className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-md bg-canvas border border-rule hover:border-turquoise text-inkText hover:text-turquoise transition-all cursor-pointer font-medium text-[11px]"
              title="Download Printable HTML Audit Report with Cost Waterfall and Diagnostics"
            >
              <span className="text-turquoise">📄</span>
              <span>Honesty Report</span>
            </button>
          )}

          {onOpenHistory && (
            <button
              type="button"
              onClick={onOpenHistory}
              className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-md bg-canvas border border-rule hover:border-turquoise text-mutedText hover:text-inkText transition-all cursor-pointer text-[11px]"
              title="Open Trial History Ledger"
            >
              <span>📜 History</span>
            </button>
          )}

          <button
            type="button"
            onClick={onOpenGuide}
            className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-md bg-canvas border border-rule hover:border-turquoise text-mutedText hover:text-turquoise transition-all cursor-pointer text-[11px]"
            title="Read Pramaan Field Guide & Examiner Reference"
          >
            <span className="text-turquoise font-bold">📘</span>
            <span>Guide</span>
          </button>

          <button
            type="button"
            onClick={onToggleTheme}
            className="flex items-center gap-1 px-2.5 py-1.5 rounded-md bg-canvas border border-rule hover:border-turquoise text-inkText transition-all cursor-pointer text-[11px]"
            title="Toggle Dark vs Light Mode"
          >
            <span>{theme === "dark" ? "☀️" : "🌙"}</span>
          </button>

          <div
            className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-md bg-canvas border border-rule text-[11px]"
            title={engineOnline ? "Engine connected on localhost:8000" : "Running in client fallback mode"}
          >
            <span
              className={`w-2 h-2 rounded-full ${
                engineOnline ? "bg-turquoise shadow-sm shadow-turquoise" : "bg-crimson"
              }`}
            />
            <span className="text-mutedText">
              {engineOnline ? "Engine" : "Offline"}
            </span>
          </div>

          {demoMode && (
            <span
              className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-turquoise/15 border border-turquoise/40 text-turquoise"
              title="Running against offline verified demo cache"
            >
              DEMO MODE
            </span>
          )}
        </div>
      </div>

      {/* Signature User Color Gradient Edge */}
      <div className="h-[2px] w-full bg-gradient-banner" />
    </header>
  );
};
