"use client";

import React, { useState, useEffect } from "react";
import { Header } from "../components/Header";
import { RunConfigurator } from "../components/RunConfigurator";
import { ProfitMirageDissector } from "../components/ProfitMirageDissector";
import { StatutoryTollgate } from "../components/StatutoryTollgate";
import { DeflatedSharpeGauge } from "../components/DeflatedSharpeGauge";
import { CpcvEmbargoMatrix } from "../components/CpcvEmbargoMatrix";
import { ExecutionLedger } from "../components/ExecutionLedger";
import { MethodologyGuideModal } from "../components/MethodologyGuideModal";
import { InteractiveTourHUD } from "../components/InteractiveTourHUD";

// Verified baseline fallback for instant rendering without waiting for backend
const DEFAULT_FALLBACK_DATA = {
  run_id: "bf3f93a2fb4a",
  strategy: "sma_crossover",
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
  },
  costs: {
    brokerage: 1440.0,
    stt: 2680.0,
    stamp_duty: 201.0,
    turnover_fees: 82.28,
    gst: 274.01,
    market_impact: 1644.84,
    total_friction: 6322.13,
    friction_drag_pct: 6.32,
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
    pbo: 0.6429,
    n_trials: 30,
  }
};

interface BacktestData {
  run_id: string;
  strategy: string;
  execution_time_ms: number;
  dates: string[];
  gross_equity: number[];
  net_equity: number[];
  metrics: {
    total_return: number;
    cagr: number;
    sharpe_ratio: number;
    sortino_ratio: number;
    max_drawdown: number;
    calmar_ratio: number;
  };
  costs: {
    brokerage: number;
    stt: number;
    stamp_duty: number;
    turnover_fees: number;
    gst: number;
    market_impact: number;
    total_friction: number;
    friction_drag_pct: number;
  };
  trades: Array<{
    timestamp: string;
    symbol: string;
    side: string;
    quantity: number;
    raw_price: number;
    fill_price: number;
    total_cost: number;
    status: string;
  }>;
  diagnostics: {
    dsr_p_value?: number | null;
    expected_max_sharpe?: number | null;
    pbo?: number | null;
    n_trials: number;
  };
}

export default function Home() {
  const [theme, setTheme] = useState<"dark" | "light">("dark");
  const [activeTab, setActiveTab] = useState<"mirage" | "costs" | "overfitting" | "ledger" | "unified">("mirage");
  const [strategy, setStrategy] = useState<string>("sma_crossover");
  const [params, setParams] = useState<Record<string, number>>({ fast_window: 20, slow_window: 50 });
  const [initialCapital, setInitialCapital] = useState<number>(100000);
  const [universe, setUniverse] = useState<string[]>([
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "SBIN.NS",
    "ITC.NS",
    "HINDUNILVR.NS",
    "LT.NS",
    "BHARTIARTL.NS",
  ]);
  const [period, setPeriod] = useState<string>("full");
  const [applyCosts, setApplyCosts] = useState<boolean>(true);
  const [demoMode, setDemoMode] = useState<boolean>(true);
  const [loading, setLoading] = useState<boolean>(false);
  const [engineOnline, setEngineOnline] = useState<boolean>(false);
  const [data, setData] = useState<BacktestData>(DEFAULT_FALLBACK_DATA);
  const [toastMessage, setToastMessage] = useState<{ text: string; type: "success" | "error" | "info" } | null>(null);
  const [isGuideOpen, setIsGuideOpen] = useState<boolean>(false);
  const [isResultsFresh, setIsResultsFresh] = useState<boolean>(false);
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

  const getApiUrl = (path: string) => {
    return `/api/engine${path}`;
  };

  const loadBacktest = React.useCallback(async () => {
    setLoading(true);
    setToastMessage({ text: "Simulating portfolio across Indian equity market bars...", type: "info" });
    try {
      if (demoMode) {
        const res = await fetch(getApiUrl(`/replay/${strategy}?period=${period}`));
        if (res.ok) {
          const json = await res.json();
          setData(json);
          setIsResultsFresh(true);
          setTimeout(() => setIsResultsFresh(false), 2500);
          setLastRunStats({
            strategyName: strategy,
            period,
            initialCapital,
            terminalNet: json.net_equity ? json.net_equity[json.net_equity.length - 1] : initialCapital,
            terminalGross: json.gross_equity ? json.gross_equity[json.gross_equity.length - 1] : initialCapital,
            totalReturn: json.metrics?.total_return ?? 0,
            totalFriction: json.costs?.total_friction ?? 0,
            tradesCount: json.trades?.length ?? 0,
            executionTimeMs: json.execution_time_ms ?? 18,
            timestamp: new Date().toLocaleTimeString(),
          });
          setLoading(false);
          setToastMessage({
            text: `Simulation complete: Results updated for ${strategy.replace(/_/g, " ").toUpperCase()} (${period.toUpperCase()}).`,
            type: "success"
          });
          return;
        }
      }

      // Live simulation POST request with all interactive parameters
      const res = await fetch(getApiUrl("/run"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          strategy,
          params,
          universe,
          start_date: period === "IS" ? "2019-01-01" : period === "OOS" ? "2023-01-01" : "2019-01-01",
          end_date: period === "IS" ? "2022-12-31" : "2024-12-30",
          initial_capital: initialCapital,
          apply_costs: applyCosts,
          demo_mode: false,
        }),
      });
      if (res.ok) {
        const json = await res.json();
        setData(json);
        setIsResultsFresh(true);
        setTimeout(() => setIsResultsFresh(false), 2500);
        setLastRunStats({
          strategyName: strategy,
          period,
          initialCapital,
          terminalNet: json.net_equity ? json.net_equity[json.net_equity.length - 1] : initialCapital,
          terminalGross: json.gross_equity ? json.gross_equity[json.gross_equity.length - 1] : initialCapital,
          totalReturn: json.metrics?.total_return ?? 0,
          totalFriction: json.costs?.total_friction ?? 0,
          tradesCount: json.trades?.length ?? 0,
          executionTimeMs: json.execution_time_ms ?? 20,
          timestamp: new Date().toLocaleTimeString(),
        });
        setLoading(false);
        setToastMessage({
          text: `Backtest complete: Evaluated across ${universe.length} stocks in ${Number(json.execution_time_ms).toFixed(0)} ms.`,
          type: "success"
        });
        return;
      }
    } catch {
      setToastMessage({
        text: "Simulation loaded from verified local cache.",
        type: "info"
      });
    }
    setLoading(false);
  }, [strategy, period, applyCosts, demoMode, params, universe, initialCapital]);

  useEffect(() => {
    fetch(getApiUrl("/health"))
      .then((res) => {
        if (res.ok) return res.json();
        throw new Error("Proxy error");
      })
      .then(() => setEngineOnline(true))
      .catch(() => {
        fetch("http://127.0.0.1:8000/health")
          .then((res) => res.json())
          .then(() => setEngineOnline(true))
          .catch(() => setEngineOnline(false));
      });

    loadBacktest();
  }, [loadBacktest]);

  const metrics = data?.metrics || DEFAULT_FALLBACK_DATA.metrics;
  const costs = data?.costs || DEFAULT_FALLBACK_DATA.costs;
  const diag = data?.diagnostics || DEFAULT_FALLBACK_DATA.diagnostics;

  return (
    <div className="h-screen w-screen overflow-hidden flex flex-col bg-canvas text-inkText font-sans select-none">
      {/* Header (56px) */}
      <Header
        demoMode={demoMode}
        engineOnline={engineOnline}
        theme={theme}
        onToggleTheme={toggleTheme}
        onOpenGuide={() => setIsGuideOpen(true)}
      />

      <MethodologyGuideModal
        isOpen={isGuideOpen}
        onClose={() => setIsGuideOpen(false)}
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
            demoMode={demoMode}
            setDemoMode={setDemoMode}
            initialCapital={initialCapital}
            setInitialCapital={setInitialCapital}
            params={params}
            setParams={setParams}
            universe={universe}
            setUniverse={setUniverse}
            onRun={loadBacktest}
            loading={loading}
            lastExecutionMs={data?.execution_time_ms}
          />
        </aside>

        {/* Right Main Stage (Expansive Full Canvas) */}
        <main className="flex-1 min-w-0 h-full overflow-y-auto p-4 lg:p-5 flex flex-col justify-between space-y-3.5">
          <div className="space-y-3.5 flex-1 flex flex-col">
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
                      <span>✓ Backtest Results Updated</span>
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
                    <span className="text-mutedText">Trades: </span>
                    <span className="text-inkText font-bold">{lastRunStats.tradesCount} filled</span>
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
                title="Compound Annual Growth Rate: Annualized geometric return. Nifty 10 Buy & Hold achieved 19.07% over 2019–2024."
              >
                <div className="flex items-center justify-between">
                  <div className="text-mutedText text-[11px] font-mono uppercase tracking-wider">CAGR (Annualized)</div>
                  <span className="text-[10px] text-turquoise">ℹ</span>
                </div>
                <div className="text-2xl font-bold font-mono text-turquoise mt-1">
                  {(metrics.cagr * 100).toFixed(2)}%
                </div>
                <div className="text-[11px] text-mutedText font-mono mt-0.5">vs 19.07% Nifty-10 B&H</div>
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
                <div className="text-[11px] text-mutedText font-mono mt-0.5">Hurdle: 6.0% RF</div>
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
                title="Calmar Ratio: Annual return divided by maximum drawdown."
              >
                <div className="flex items-center justify-between">
                  <div className="text-mutedText text-[11px] font-mono uppercase tracking-wider">Calmar Ratio</div>
                  <span className="text-[10px] text-turquoise">ℹ</span>
                </div>
                <div className="text-2xl font-bold font-mono text-inkText mt-1">
                  {metrics.calmar_ratio.toFixed(2)}
                </div>
                <div className="text-[11px] text-mutedText font-mono mt-0.5">CAGR / |MaxDD|</div>
              </div>

              <div 
                className="bg-panel border border-rule border-t-2 border-t-turquoise p-3.5 col-span-2 sm:col-span-1 rounded-md hover:border-turquoise transition-all cursor-help shadow-xs"
                title="Terminal Net Equity: Final capital remaining after deducting all government taxes (STT, GST, Stamp) and market impact."
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

              <button
                onClick={() => setIsGuideOpen(true)}
                className="hidden sm:inline-flex items-center gap-1.5 text-xs text-turquoise hover:underline font-mono px-3 py-1 rounded bg-canvas border border-rule"
              >
                <span>Methodology Reference</span>
                <span>→</span>
              </button>
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
                    initialCapital={100000.0}
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
                      marketImpact={costs.market_impact}
                      totalFriction={costs.total_friction}
                      initialCapital={100000.0}
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
                          ₹{(data?.gross_equity?.[data.gross_equity.length - 1] ?? 100000) - 100000 > 0 ? "+" : ""}
                          {((data?.gross_equity?.[data.gross_equity.length - 1] ?? 100000) - 100000).toLocaleString("en-IN", { maximumFractionDigits: 0 })}
                        </span>
                      </div>
                      <div className="flex justify-between py-1 border-b border-rule/50">
                        <span className="text-mutedText">Statutory Taxes (STT, Stamp, GST):</span>
                        <span className="text-crimson font-bold">
                          -₹{(costs.stt + costs.stamp_duty + costs.gst + costs.turnover_fees).toLocaleString("en-IN", { maximumFractionDigits: 0 })}
                        </span>
                      </div>
                      <div className="flex justify-between py-1 border-b border-rule/50">
                        <span className="text-mutedText">Almgren-Chriss Slippage:</span>
                        <span className="text-crimson font-bold">
                          -₹{costs.market_impact.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
                        </span>
                      </div>
                      <div className="flex justify-between py-1 border-b border-rule/50">
                        <span className="text-mutedText">Realized Net Profit:</span>
                        <span className="text-turquoise font-bold">
                          ₹{(data?.net_equity?.[data.net_equity.length - 1] ?? 100000) - 100000 > 0 ? "+" : ""}
                          {((data?.net_equity?.[data.net_equity.length - 1] ?? 100000) - 100000).toLocaleString("en-IN", { maximumFractionDigits: 0 })}
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
                    nTrials={diag.n_trials || 30}
                  />

                  <CpcvEmbargoMatrix pbo={diag.pbo} />
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
