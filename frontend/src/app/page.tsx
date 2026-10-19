"use client";

import React, { useState, useEffect, useCallback } from "react";
import { Header } from "../components/Header";
import { RunConfigurator } from "../components/RunConfigurator";
import { ProfitMirageDissector } from "../components/ProfitMirageDissector";
import { StatutoryTollgate } from "../components/StatutoryTollgate";
import { DeflatedSharpeGauge } from "../components/DeflatedSharpeGauge";
import { CpcvEmbargoMatrix } from "../components/CpcvEmbargoMatrix";
import { ExecutionLedger } from "../components/ExecutionLedger";
import { MethodologyGuideModal } from "../components/MethodologyGuideModal";
import { InteractiveTourHUD } from "../components/InteractiveTourHUD";
import { RunHistoryDrawer } from "../components/RunHistoryDrawer";
import {
  runBacktest,
  checkHealth,
  fetchUniverse,
  fetchSweepSummary,
  getReportUrl,
  API_BASE_URL,
  StrategyType,
  BacktestResponse,
  SweepSummaryResponse,
} from "../lib/api";

// Honest baseline fallback when API is offline
const DEFAULT_FALLBACK_DATA: BacktestResponse = {
  run_id: "bf3f93a2fb4a",
  strategy: "sma_crossover",
  is_cached: true,
  served_from: "cache",
  replay_reason: "Offline demonstration fallback",
  engine_version: "1.0.0",
  data_hash: "a574f52a53925590",
  cost_profile: "zerodha_delivery_2024",
  execution_time_ms: 18.5,
  dates: [
    "2019-01-01", "2019-06-01", "2020-01-01", "2020-06-01",
    "2021-01-01", "2021-06-01", "2022-01-01", "2022-06-01",
    "2023-01-01", "2023-06-01", "2024-01-01", "2024-12-30"
  ],
  gross_equity: [
    100000, 105200, 114800, 122100, 138400, 149200, 158900, 169200, 178400, 185100, 191200, 194529
  ],
  net_equity: [
    100000, 104100, 112900, 119800, 135200, 145100, 154200, 163900, 172800, 179100, 184900, 188207
  ],
  metrics: {
    total_return: 0.8821,
    cagr: 0.1137,
    sharpe_ratio: 0.5266,
    sortino_ratio: 0.7609,
    max_drawdown: -0.1476,
    calmar_ratio: 0.7704,
    average_exposure: 0.618,
    alpha: 0.042,
    beta: 0.784,
    exposure_matched_return: 0.712,
  },
  costs: {
    brokerage: 0.0,
    stt: 2680.0,
    stamp_duty: 201.0,
    turnover_fees: 82.28,
    gst: 274.01,
    dp_charges: 180.0,
    sebi_fees: 1.20,
    ipft: 1.20,
    market_impact: 1644.84,
    total_friction: 5064.53,
    friction_drag_pct: 5.06,
  },
  trades: [
    { timestamp: "2019-01-22", symbol: "RELIANCE", side: "BUY", quantity: 45, raw_price: 2210.0, fill_price: 2212.4, total_cost: 122.5, status: "FILLED" },
    { timestamp: "2019-04-18", symbol: "TCS", side: "BUY", quantity: 38, raw_price: 1980.0, fill_price: 1981.8, total_cost: 98.4, status: "FILLED" },
    { timestamp: "2020-03-24", symbol: "INFY", side: "BUY", quantity: 120, raw_price: 650.0, fill_price: 651.2, total_cost: 84.1, status: "FILLED" },
    { timestamp: "2021-02-15", symbol: "HDFCBANK", side: "BUY", quantity: 65, raw_price: 1420.0, fill_price: 1421.5, total_cost: 110.2, status: "FILLED" },
    { timestamp: "2022-07-12", symbol: "ICICIBANK", side: "BUY", quantity: 80, raw_price: 810.0, fill_price: 811.1, total_cost: 78.6, status: "FILLED" },
    { timestamp: "2023-05-19", symbol: "LT", side: "BUY", quantity: 40, raw_price: 2250.0, fill_price: 2252.8, total_cost: 114.8, status: "FILLED" },
    { timestamp: "2024-01-10", symbol: "BHARTIARTL", side: "BUY", quantity: 85, raw_price: 1040.0, fill_price: 1041.3, total_cost: 92.0, status: "FILLED" }
  ],
  diagnostics: {
    dsr_p_value: 0.524,
    expected_max_sharpe: 0.746,
    pbo: 0.6000,
    pbo_reason: "Empirical CPCV PBO computed across 133 configs in parameter sweep",
    n_trials: 133,
  },
};

export default function Home() {
  const [data, setData] = useState<BacktestResponse>(DEFAULT_FALLBACK_DATA);
  const [strategy, setStrategy] = useState<string>("sma_crossover");
  const [period, setPeriod] = useState<string>("full");
  const [applyCosts, setApplyCosts] = useState<boolean>(true);
  const [costProfile, setCostProfile] = useState<string>("zerodha_delivery_2024");
  const [slippageFloorBps, setSlippageFloorBps] = useState<number>(0);
  const [demoMode, setDemoMode] = useState<boolean>(false);
  const [initialCapital, setInitialCapital] = useState<number>(100000);
  const [params, setParams] = useState<Record<string, number>>({ fast_window: 20, slow_window: 50 });
  const [universe, setUniverse] = useState<string[]>([
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "SBIN.NS", "ITC.NS", "HINDUNILVR.NS", "LT.NS", "BHARTIARTL.NS",
  ]);
  const [survivorshipWarning, setSurvivorshipWarning] = useState<string | null>(null);

  const [activeTab, setActiveTab] = useState<"mirage" | "costs" | "overfitting" | "ledger" | "unified">("mirage");
  const [engineOnline, setEngineOnline] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [toastMessage, setToastMessage] = useState<{ text: string; type: "success" | "error" | "info" } | null>(null);
  const [theme, setTheme] = useState<"dark" | "light">("dark");
  const [isGuideOpen, setIsGuideOpen] = useState<boolean>(false);
  const [isHistoryOpen, setIsHistoryOpen] = useState<boolean>(false);
  const [sweepSummary, setSweepSummary] = useState<SweepSummaryResponse | null>(null);

  const [lastRunStats, setLastRunStats] = useState<{
    strategyName: string;
    period: string;
    initialCapital: number;
    terminalNet: number;
    terminalGross: number;
    totalReturn: number;
    totalFriction: number;
    tradesCount: number;
    executionTimeMs: number;
    timestamp: string;
  } | null>(null);
  const [isResultsFresh, setIsResultsFresh] = useState<boolean>(false);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const searchParams = new URLSearchParams(window.location.search);
      const urlTheme = searchParams.get("theme") as "dark" | "light" | null;
      if (urlTheme === "dark" || urlTheme === "light") {
        setTheme(urlTheme);
        document.documentElement.setAttribute("data-theme", urlTheme);
        return;
      }
      const saved = localStorage.getItem("pramaan_theme") as "dark" | "light" | null;
      if (saved) {
        setTheme(saved);
        document.documentElement.setAttribute("data-theme", saved);
      } else {
        document.documentElement.setAttribute("data-theme", "dark");
      }
    }
  }, []);

  const toggleTheme = () => {
    const next = theme === "dark" ? "light" : "dark";
    setTheme(next);
    if (typeof window !== "undefined") {
      localStorage.setItem("pramaan_theme", next);
      document.documentElement.setAttribute("data-theme", next);
    }
  };

  const loadBacktest = useCallback(async () => {
    setLoading(true);
    setToastMessage({ text: "Simulating portfolio across Indian equity market bars...", type: "info" });

    const startDate = period === "IS" ? "2019-01-01" : period === "OOS" ? "2023-01-01" : "2019-01-01";
    const endDate = period === "IS" ? "2022-12-31" : "2024-12-30";

    try {
      const resp = await runBacktest({
        strategy: strategy as StrategyType,
        params,
        universe,
        start_date: startDate,
        end_date: endDate,
        initial_capital: initialCapital,
        apply_costs: applyCosts,
        cost_profile: costProfile,
        slippage_floor_bps: slippageFloorBps,
        demo_mode: demoMode,
      });

      setData(resp);
      setIsResultsFresh(true);
      setTimeout(() => setIsResultsFresh(false), 2500);

      const netEq = resp.net_equity[resp.net_equity.length - 1] ?? initialCapital;
      const grossEq = resp.gross_equity[resp.gross_equity.length - 1] ?? initialCapital;

      setLastRunStats({
        strategyName: strategy,
        period,
        initialCapital,
        terminalNet: netEq,
        terminalGross: grossEq,
        totalReturn: resp.metrics.total_return,
        totalFriction: resp.costs.total_friction,
        tradesCount: resp.trades.length,
        executionTimeMs: resp.execution_time_ms,
        timestamp: new Date().toLocaleTimeString(),
      });

      setLoading(false);
      setToastMessage({
        text: `Backtest complete: Evaluated ${universe.length} stocks (${resp.served_from.toUpperCase()}) in ${resp.execution_time_ms.toFixed(0)} ms.`,
        type: "success",
      });
    } catch (err: unknown) {
      setLoading(false);
      const msg = err instanceof Error ? err.message : "Failed to execute backtest";
      setToastMessage({
        text: `Simulation error: ${msg}. Showing cached baseline.`,
        type: "error",
      });
    }
  }, [strategy, period, applyCosts, costProfile, slippageFloorBps, demoMode, params, universe, initialCapital]);

  // Initial data loading: Health check, Universe metadata, Sweep summary
  useEffect(() => {
    checkHealth()
      .then(() => setEngineOnline(true))
      .catch(() => setEngineOnline(false));

    fetchUniverse()
      .then((u) => {
        if (u.survivorship_bias_warning) {
          setSurvivorshipWarning(u.survivorship_bias_warning);
        }
      })
      .catch(() => {});

    fetchSweepSummary()
      .then((summary) => setSweepSummary(summary))
      .catch(() => {});

    loadBacktest();
  }, [loadBacktest]);

  const metrics = data?.metrics || DEFAULT_FALLBACK_DATA.metrics;
  const costs = data?.costs || DEFAULT_FALLBACK_DATA.costs;
  const diag = data?.diagnostics || DEFAULT_FALLBACK_DATA.diagnostics;

  return (
    <div className="h-screen w-screen overflow-hidden flex flex-col bg-canvas text-inkText font-sans select-none">
      {/* Header with Served_From Provenance Pill & Honesty Report Export */}
      <Header
        demoMode={demoMode}
        engineOnline={engineOnline}
        theme={theme}
        servedFrom={data.served_from}
        replayReason={data.replay_reason}
        dataHash={data.data_hash}
        costProfile={data.cost_profile}
        runId={data.run_id}
        onToggleTheme={toggleTheme}
        onOpenGuide={() => setIsGuideOpen(true)}
        onOpenHistory={() => setIsHistoryOpen(true)}
        onDownloadReport={() => {
          if (data?.run_id) {
            window.open(getReportUrl(data.run_id), "_blank");
          }
        }}
      />

      <MethodologyGuideModal
        isOpen={isGuideOpen}
        onClose={() => setIsGuideOpen(false)}
      />

      <RunHistoryDrawer
        isOpen={isHistoryOpen}
        onClose={() => setIsHistoryOpen(false)}
        onSelectTrial={(trial) => {
          setStrategy(trial.strategy);
          setParams(trial.params as Record<string, number>);
          if (trial.universe?.length) setUniverse(trial.universe);
          setIsHistoryOpen(false);
          setToastMessage({
            text: `Loaded parameters from trial #${trial.trial_id}`,
            type: "info",
          });
        }}
      />

      {/* Main Viewport Shell: 100vw x 100vh Fill */}
      <div className="flex-1 w-full min-h-0 flex overflow-hidden">
        {/* Left Sidebar Control Dock (320px) */}
        <aside className="w-[320px] 2xl:w-[350px] shrink-0 h-full overflow-y-auto border-r border-rule bg-panel p-4 flex flex-col justify-between">
          <RunConfigurator
            strategy={strategy}
            setStrategy={setStrategy}
            period={period}
            setPeriod={setPeriod}
            applyCosts={applyCosts}
            setApplyCosts={setApplyCosts}
            costProfile={costProfile}
            setCostProfile={setCostProfile}
            slippageFloorBps={slippageFloorBps}
            setSlippageFloorBps={setSlippageFloorBps}
            demoMode={demoMode}
            setDemoMode={setDemoMode}
            initialCapital={initialCapital}
            setInitialCapital={setInitialCapital}
            params={params}
            setParams={setParams}
            universe={universe}
            setUniverse={setUniverse}
            survivorshipWarning={survivorshipWarning}
            onRun={loadBacktest}
            loading={loading}
            lastExecutionMs={data?.execution_time_ms}
          />
        </aside>

        {/* Right Main Stage (Expansive Full Canvas) */}
        <main className="flex-1 min-w-0 h-full overflow-y-auto p-4 lg:p-5 flex flex-col justify-between space-y-3.5">
          <div className="space-y-3.5 flex-1 flex flex-col">
            {/* Offline Replay Banner (Never fails silently) */}
            {!engineOnline && (
              <div
                role="alert"
                aria-live="polite"
                className="px-4 py-2.5 rounded border border-amber-500/40 bg-amber-500/10 text-amber-200 text-xs font-mono flex items-center justify-between shrink-0"
              >
                <div className="flex items-center gap-2.5">
                  <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/25 border border-amber-500/50 text-amber-300">
                    REPLAY (offline demo)
                  </span>
                  <span>
                    Backend API unreachable at <code className="bg-canvas/50 px-1 py-0.5 rounded text-amber-100">{API_BASE_URL}</code>. Displaying committed baseline replay artifact.
                  </span>
                </div>
                <button
                  onClick={() => {
                    checkHealth()
                      .then(() => {
                        setEngineOnline(true);
                        loadBacktest();
                      })
                      .catch(() => {
                        setToastMessage({ text: "API still unreachable. Ensure `python -m src.api.main` is running.", type: "error" });
                      });
                  }}
                  className="px-2.5 py-1 rounded bg-amber-500/20 hover:bg-amber-500/30 text-amber-100 border border-amber-500/30 text-[11px] font-medium transition-colors"
                >
                  Retry Connection
                </button>
              </div>
            )}

            {/* Toast Alert */}
            {toastMessage && (
              <div
                className={`px-4 py-2 rounded border text-xs font-mono flex items-center justify-between transition-all shrink-0 ${
                  toastMessage.type === "success"
                    ? "bg-turquoise/15 border-turquoise/40 text-turquoise"
                    : toastMessage.type === "error"
                    ? "bg-crimson/15 border-crimson/40 text-crimson"
                    : "bg-pacificCyan/15 border-pacificCyan/40 text-pacificCyan"
                }`}
              >
                <div className="flex items-center gap-2">
                  <span className="font-bold">{toastMessage.type === "success" ? "✓" : "ℹ"}</span>
                  <span>{toastMessage.text}</span>
                </div>
                <button
                  onClick={() => setToastMessage(null)}
                  className="text-mutedText hover:text-inkText ml-4 font-bold"
                >
                  ✕
                </button>
              </div>
            )}

            {/* Run Completion & Delta Feedback Banner */}
            {lastRunStats && (
              <div
                className={`p-3 rounded-md border flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs shrink-0 transition-all duration-300 ${
                  isResultsFresh
                    ? "bg-turquoise/15 border-turquoise shadow-md shadow-turquoise/15 ring-1 ring-turquoise/40"
                    : "bg-panel border-rule"
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <span className={`w-2.5 h-2.5 rounded-full bg-turquoise shrink-0 ${isResultsFresh ? "animate-ping" : "animate-pulse"}`} />
                  <div>
                    <div className="font-bold text-inkText flex items-center gap-2">
                      <span>✓ Backtest Results Updated ({data.served_from.toUpperCase()})</span>
                      <span className="text-[10px] text-mutedText font-normal">at {lastRunStats.timestamp}</span>
                    </div>
                    <div className="text-mutedText text-[11px] mt-0.5">
                      Tested <strong className="text-turquoise">{lastRunStats.strategyName.replace(/_/g, " ").toUpperCase()}</strong> with starting capital of <strong className="text-inkText">₹{lastRunStats.initialCapital.toLocaleString("en-IN")}</strong>.
                    </div>
                  </div>
                </div>

                <div className="flex flex-wrap items-center gap-2 font-mono text-[11px]">
                  <div className="bg-canvas px-2.5 py-1 rounded border border-rule">
                    <span className="text-mutedText">Net Wealth: </span>
                    <span className="text-turquoise font-bold">₹{lastRunStats.terminalNet.toLocaleString("en-IN", { maximumFractionDigits: 0 })}</span>
                    <span className="text-turquoise text-[10px] ml-1 font-bold">({(lastRunStats.totalReturn * 100).toFixed(1)}%)</span>
                  </div>

                  <div className="bg-canvas px-2.5 py-1 rounded border border-rule">
                    <span className="text-mutedText">Tax Drag: </span>
                    <span className="text-crimson font-bold">-₹{lastRunStats.totalFriction.toLocaleString("en-IN", { maximumFractionDigits: 0 })}</span>
                  </div>

                  <div className="bg-canvas px-2.5 py-1 rounded border border-rule">
                    <span className="text-mutedText">Exposure: </span>
                    <span className="text-pacificCyan font-bold">{((metrics.average_exposure ?? 0.6) * 100).toFixed(0)}%</span>
                  </div>

                  <div className="bg-canvas px-2.5 py-1 rounded border border-rule">
                    <span className="text-mutedText">Trades: </span>
                    <span className="text-inkText font-bold">{lastRunStats.tradesCount} fills</span>
                  </div>
                </div>
              </div>
            )}

            {/* Top KPI Ribbon (5 Spacious Institutional Cards) */}
            <div className={`grid grid-cols-2 sm:grid-cols-3 xl:grid-cols-5 gap-3 font-tabular shrink-0 transition-all duration-500 rounded-md p-0.5 ${
              isResultsFresh ? "ring-1 ring-turquoise/60 shadow-lg shadow-turquoise/15 bg-turquoise/5" : ""
            }`}>
              <div
                className="bg-panel border border-rule border-t-2 border-t-turquoise p-3.5 rounded-md hover:border-turquoise transition-all cursor-help shadow-xs"
                title="Compound Annual Growth Rate: Annualized geometric return. Passive Buy & Hold achieved 19.07% over 2019–2024."
              >
                <div className="flex items-center justify-between">
                  <div className="text-mutedText text-[11px] font-mono uppercase tracking-wider">CAGR (Annualized)</div>
                  <span className="text-[10px] text-turquoise">ℹ</span>
                </div>
                <div className="text-2xl font-bold font-mono text-turquoise mt-1">
                  {(metrics.cagr * 100).toFixed(2)}%
                </div>
                <div className="text-[11px] text-mutedText font-mono mt-0.5">
                  Exp-Matched: {((metrics.exposure_matched_return ?? 0.15) * 100).toFixed(1)}%
                </div>
              </div>

              <div
                className="bg-panel border border-rule border-t-2 border-t-pacificCyan p-3.5 rounded-md hover:border-turquoise transition-all cursor-help shadow-xs"
                title="Sharpe Ratio: Excess return per unit of volatility above 6.0% Indian risk-free hurdle."
              >
                <div className="flex items-center justify-between">
                  <div className="text-mutedText text-[11px] font-mono uppercase tracking-wider">Sharpe Ratio</div>
                  <span className="text-[10px] text-turquoise">ℹ</span>
                </div>
                <div className="text-2xl font-bold font-mono text-inkText mt-1">
                  {metrics.sharpe_ratio.toFixed(3)}
                </div>
                <div className="text-[11px] text-mutedText font-mono mt-0.5">
                  Alpha: {(metrics.alpha * 100).toFixed(1)}% · β: {metrics.beta.toFixed(2)}
                </div>
              </div>

              <div
                className="bg-panel border border-rule border-t-2 border-t-crimson p-3.5 rounded-md hover:border-crimson transition-all cursor-help shadow-xs"
                title="Maximum Drawdown: Peak-to-trough decline of portfolio equity."
              >
                <div className="flex items-center justify-between">
                  <div className="text-mutedText text-[11px] font-mono uppercase tracking-wider">Max Drawdown</div>
                  <span className="text-[10px] text-crimson">ℹ</span>
                </div>
                <div className="text-2xl font-bold font-mono text-crimson mt-1">
                  {(metrics.max_drawdown * 100).toFixed(2)}%
                </div>
                <div className="text-[11px] text-mutedText font-mono mt-0.5">Deepest trough</div>
              </div>

              <div
                className="bg-panel border border-rule border-t-2 border-t-stormyTeal p-3.5 rounded-md hover:border-turquoise transition-all cursor-help shadow-xs"
                title="Market Exposure: Average fraction of capital deployed in equities vs sitting in cash."
              >
                <div className="flex items-center justify-between">
                  <div className="text-mutedText text-[11px] font-mono uppercase tracking-wider">Market Exposure</div>
                  <span className="text-[10px] text-turquoise">ℹ</span>
                </div>
                <div className="text-2xl font-bold font-mono text-inkText mt-1">
                  {((metrics.average_exposure ?? 0.6) * 100).toFixed(1)}%
                </div>
                <div className="text-[11px] text-mutedText font-mono mt-0.5">
                  Calmar: {metrics.calmar_ratio.toFixed(2)}
                </div>
              </div>

              <div
                className="bg-panel border border-rule border-t-2 border-t-turquoise p-3.5 col-span-2 sm:col-span-1 rounded-md hover:border-turquoise transition-all cursor-help shadow-xs"
                title="Terminal Net Equity: Final capital remaining after deducting all statutory taxes (STT, GST, Stamp, DP) and market slippage."
              >
                <div className="flex items-center justify-between">
                  <div className="text-mutedText text-[11px] font-mono uppercase tracking-wider">Terminal Net Equity</div>
                  <span className="text-[10px] text-turquoise">ℹ</span>
                </div>
                <div className="text-2xl font-bold font-mono text-turquoise mt-1">
                  ₹{(data?.net_equity?.[data.net_equity.length - 1] ?? 100000).toLocaleString("en-IN", { maximumFractionDigits: 0 })}
                </div>
                <div className="text-[11px] text-crimson font-mono mt-0.5">
                  -₹{costs.total_friction.toLocaleString("en-IN", { maximumFractionDigits: 0 })} lost to friction
                </div>
              </div>
            </div>

            {/* Interactive Concept Tour HUD */}
            <div className="shrink-0">
              <InteractiveTourHUD onOpenMethodology={() => setIsGuideOpen(true)} />
            </div>

            {/* Institutional Workspace Tab Bar */}
            <div className="border-b border-rule flex items-center justify-between gap-4 shrink-0 pb-px">
              <div className="flex items-center gap-1 font-mono text-xs">
                {[
                  { id: "mirage", label: "📈 The Profit Mirage" },
                  { id: "costs", label: "🏛️ Statutory Tollgate" },
                  { id: "overfitting", label: "🛡️ Overfitting Diagnostics" },
                  { id: "ledger", label: "📋 T+1 Execution Ledger" },
                  { id: "unified", label: "🔲 Unified Master View" },
                ].map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as typeof activeTab)}
                    className={`px-4 py-2 font-medium border-b-2 whitespace-nowrap transition-all ${
                      activeTab === tab.id
                        ? "border-turquoise text-turquoise bg-panel font-bold shadow-sm"
                        : "border-transparent text-mutedText hover:text-inkText hover:bg-panel/50"
                    }`}
                  >
                    {tab.label}
                  </button>
                ))}
              </div>

              <div className="flex items-center gap-2">
                {data.run_id && (
                  <a
                    href={getReportUrl(data.run_id)}
                    target="_blank"
                    rel="noreferrer"
                    className="hidden sm:inline-flex items-center gap-1 text-xs text-turquoise hover:underline font-mono px-3 py-1 rounded bg-canvas border border-rule hover:border-turquoise"
                  >
                    <span>Download Audit Report (HTML)</span>
                    <span>↗</span>
                  </a>
                )}
                <button
                  onClick={() => setIsGuideOpen(true)}
                  className="hidden sm:inline-flex items-center gap-1.5 text-xs text-mutedText hover:text-turquoise font-mono px-3 py-1 rounded bg-canvas border border-rule"
                >
                  <span>Methodology</span>
                  <span>→</span>
                </button>
              </div>
            </div>

            {/* Dynamic Full Height Workspace View */}
            <div className="flex-1 min-h-0 flex flex-col">
              {/* View 1: Profit Mirage Hero */}
              {(activeTab === "mirage" || activeTab === "unified") && (
                <div className="flex-1 min-h-0 flex flex-col">
                  <ProfitMirageDissector
                    dates={data.dates}
                    grossEquity={data.gross_equity}
                    netEquity={data.net_equity}
                    initialCapital={initialCapital}
                    strategyName={strategy}
                  />
                </div>
              )}

              {/* View 2: Statutory Indian Tollgate */}
              {(activeTab === "costs" || activeTab === "unified") && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
                  <div className="md:col-span-2">
                    <StatutoryTollgate
                      brokerage={costs.brokerage}
                      stt={costs.stt}
                      stampDuty={costs.stamp_duty}
                      turnoverFees={costs.turnover_fees}
                      gst={costs.gst}
                      dpCharges={costs.dp_charges}
                      sebiFees={costs.sebi_fees}
                      ipft={costs.ipft}
                      marketImpact={costs.market_impact}
                      totalFriction={costs.total_friction}
                      initialCapital={initialCapital}
                      costProfile={data.cost_profile}
                    />
                  </div>
                  <div className="bg-panel border border-rule p-5 rounded space-y-4 text-xs font-mono">
                    <h3 className="text-sm font-bold text-inkText border-b border-rule pb-2 font-sans">
                      Indian Statutory Toll Breakdown
                    </h3>
                    <div className="space-y-2.5">
                      <div className="flex justify-between py-1 border-b border-rule/50">
                        <span className="text-mutedText">Gross Paper Gain:</span>
                        <span className="text-pacificCyan font-bold">
                          ₹{(data?.gross_equity?.[data.gross_equity.length - 1] ?? initialCapital) - initialCapital > 0 ? "+" : ""}
                          {((data?.gross_equity?.[data.gross_equity.length - 1] ?? initialCapital) - initialCapital).toLocaleString("en-IN", { maximumFractionDigits: 0 })}
                        </span>
                      </div>
                      <div className="flex justify-between py-1 border-b border-rule/50">
                        <span className="text-mutedText">Statutory Taxes (STT, Stamp, GST):</span>
                        <span className="text-crimson font-bold">
                          -₹{(costs.stt + costs.stamp_duty + costs.gst + costs.turnover_fees + costs.dp_charges).toLocaleString("en-IN", { maximumFractionDigits: 0 })}
                        </span>
                      </div>
                      <div className="flex justify-between py-1 border-b border-rule/50">
                        <span className="text-mutedText">Execution Slippage:</span>
                        <span className="text-crimson font-bold">
                          -₹{costs.market_impact.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
                        </span>
                      </div>
                      <div className="flex justify-between py-1 border-b border-rule/50">
                        <span className="text-mutedText">Realized Net Profit:</span>
                        <span className="text-turquoise font-bold">
                          ₹{(data?.net_equity?.[data.net_equity.length - 1] ?? initialCapital) - initialCapital > 0 ? "+" : ""}
                          {((data?.net_equity?.[data.net_equity.length - 1] ?? initialCapital) - initialCapital).toLocaleString("en-IN", { maximumFractionDigits: 0 })}
                        </span>
                      </div>
                      <div className="pt-2 text-[11px] text-mutedText leading-relaxed font-sans">
                        Friction absorbed <span className="text-crimson font-bold">{costs.friction_drag_pct}%</span> of capital. Every rupee of STT (0.10%) and Stamp Duty (0.015%) compounds against the trader.
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* View 3: Overfitting Diagnostics */}
              {(activeTab === "overfitting" || activeTab === "unified") && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                  <DeflatedSharpeGauge
                    observedSharpe={metrics.sharpe_ratio}
                    expectedMaxSharpe={diag.expected_max_sharpe}
                    dsrPValue={diag.dsr_p_value}
                    nTrials={diag.n_trials || sweepSummary?.n_configs_evaluated || 133}
                  />

                  <CpcvEmbargoMatrix
                    pbo={diag.pbo ?? sweepSummary?.pbo}
                    pboReason={diag.pbo_reason}
                    ciLower={sweepSummary?.pbo_ci_lower_95}
                    ciUpper={sweepSummary?.pbo_ci_upper_95}
                    cpcvPaths={sweepSummary?.cpcv_paths || 45}
                    nConfigs={sweepSummary?.n_configs_evaluated || 133}
                  />
                </div>
              )}

              {/* View 4: T+1 Execution Ledger */}
              {(activeTab === "ledger" || activeTab === "unified") && (
                <div className="flex-1 min-h-0">
                  <ExecutionLedger trades={data.trades || []} />
                </div>
              )}
            </div>
          </div>

          {/* Minimal Persistent Status Footer */}
          <footer className="pt-2 border-t border-rule text-center text-[11px] text-mutedText font-mono shrink-0">
            Pramaan (प्रमाण) · GTU DI05000341 Sem-5 Minor Project · Aayush Avinash Bankar & Meet Jayeshbhai Patel · Apache 2.0
          </footer>
        </main>
      </div>
    </div>
  );
}
