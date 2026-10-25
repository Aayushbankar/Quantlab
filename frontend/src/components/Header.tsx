"use client";
import React from "react";
import { FileText, History, Globe, BookOpen, Sun, Moon, Contrast } from "lucide-react";
import { THEME_LABELS, type ThemeName } from "../lib/theme";

interface HeaderProps {
  demoMode: boolean;
  engineOnline: boolean;
  theme: ThemeName;
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
  const ThemeIcon = theme === "abyss" ? Moon : theme === "vellum" ? Sun : Contrast;
  const [landingUrl, setLandingUrl] = React.useState("/landing");

  React.useEffect(() => {
    if (typeof window !== "undefined" && window.location.pathname.includes("/Quantlab")) {
      setLandingUrl("/Quantlab/index.html");
    }
  }, []);

  const actionBtn =
    "inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-md border border-rule bg-card/70 hover:bg-cardHover hover:border-turquoise/45 text-mutedText hover:text-inkText transition-all duration-micro text-[11px] font-medium cursor-pointer";

  return (
    <header className="h-14 shrink-0 bg-panel/95 backdrop-blur border-b border-rule flex flex-col justify-between select-none relative z-30">
      <div className="h-full px-4 sm:px-5 flex items-center justify-between gap-4">
        <div className="flex items-center gap-3 min-w-0">
          <div className="w-8 h-8 rounded-md bg-gradient-signal flex items-center justify-center font-bold text-canvas text-base shadow-glow shrink-0">
            <span className="font-serif italic">प्र</span>
          </div>
          <div className="min-w-0">
            <div className="flex items-center gap-2">
              <span className="label-caps text-inkText">Pramaan</span>
              <span className="font-serif italic text-[13px] text-turquoise leading-none">
                प्रमाण
              </span>
              <span className="hidden sm:inline text-[10px] font-mono px-1.5 py-0.5 rounded bg-canvas border border-rule text-tertiaryText">
                GTU DI05000341
              </span>
            </div>
            <div className="hidden sm:flex text-[10px] text-tertiaryText items-center gap-2 mt-0.5">
              <span className="eyebrow !text-[9px]">Honest NSE Backtester</span>
              <span>·</span>
              <span className="text-turquoise/90">Tax Tollgate &amp; Overfitting Guard</span>
            </div>
          </div>
        </div>

        <div className="hidden lg:flex items-center gap-2.5 text-xs bg-canvas/70 border border-rule px-3 py-1.5 rounded-md">
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

          <div
            className="flex items-center gap-1 font-mono text-[11px]"
            title={`Data Hash: ${dataHash || "offline"}`}
          >
            <span className="text-tertiaryText">Data:</span>
            <span className="text-inkText font-medium">{shortHash}</span>
          </div>

          <span className="text-rule">|</span>

          <div
            className="text-[11px]"
            title={`Statutory Cost Card: ${costProfile || "zerodha_delivery_2024"}`}
          >
            <span className="text-tertiaryText">Rates: </span>
            <span className="text-turquoise font-medium">
              {costProfile?.includes("2024")
                ? "Oct 2024 True-to-Label"
                : costProfile || "Indian Delivery"}
            </span>
          </div>
        </div>

        <div className="flex items-center gap-1.5 text-xs">
          {runId && onDownloadReport && (
            <button type="button" onClick={onDownloadReport} className={actionBtn} title="Download Printable HTML Audit Report with Cost Waterfall and Diagnostics">
              <FileText className="w-3.5 h-3.5 text-turquoise" />
              <span className="hidden sm:inline">Honesty Report</span>
            </button>
          )}

          {onOpenHistory && (
            <button type="button" onClick={onOpenHistory} className={actionBtn} title="Open Trial History Ledger">
              <History className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">History</span>
            </button>
          )}

          <a href={landingUrl} className={actionBtn} title="View Product Landing Page & Interactive Cost Calculator">
            <Globe className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Overview</span>
          </a>

          <button type="button" onClick={onOpenGuide} className={actionBtn} title="Read Pramaan Field Guide & Examiner Reference">
            <BookOpen className="w-3.5 h-3.5 text-turquoise" />
            <span className="hidden sm:inline">Guide</span>
          </button>

          <button
            type="button"
            onClick={onToggleTheme}
            className="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-md border border-rule bg-card/70 hover:border-turquoise/45 text-inkText transition-all duration-micro text-[11px] cursor-pointer"
            title={`Theme: ${THEME_LABELS[theme]} — click to cycle`}
            aria-label="Cycle color theme"
          >
            <ThemeIcon className="w-3.5 h-3.5" />
            <span className="hidden xl:inline font-mono text-[10px] text-mutedText">
              {THEME_LABELS[theme]}
            </span>
          </button>

          <div
            className="hidden sm:flex items-center gap-1.5 px-2.5 py-1.5 rounded-md bg-card/70 border border-rule text-[11px]"
            title={engineOnline ? "Engine connected on localhost:8000" : "Running in client fallback mode"}
          >
            <span
              className={`w-2 h-2 rounded-full ${
                engineOnline ? "bg-turquoise shadow-sm shadow-turquoise" : "bg-crimson"
              }`}
            />
            <span className="text-mutedText">{engineOnline ? "Engine" : "Offline"}</span>
          </div>

          {demoMode && (
            <span
              className="hidden sm:inline-block px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-turquoise/15 border border-turquoise/40 text-turquoise"
              title="Running against offline verified demo cache"
            >
              DEMO
            </span>
          )}
        </div>
      </div>

      <div className="h-[2px] w-full bg-gradient-banner" />
    </header>
  );
};
