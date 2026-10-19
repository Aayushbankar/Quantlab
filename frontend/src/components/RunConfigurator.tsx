"use client";

import React, { useState, useEffect } from "react";
import { CustomStrategySelect, StrategyOption } from "./CustomStrategySelect";
import { Sliders, Plus, X, ChevronDown, ChevronUp, Sparkles, CheckCircle2 } from "lucide-react";

export type StrategyParamValue = number;

export interface ConfiguratorProps {
  strategy: string;
  setStrategy: (s: string) => void;
  period: string;
  setPeriod: (p: string) => void;
  applyCosts: boolean;
  setApplyCosts: (c: boolean) => void;
  demoMode: boolean;
  setDemoMode: (d: boolean) => void;
  initialCapital: number;
  setInitialCapital: (c: number) => void;
  params: Record<string, StrategyParamValue>;
  setParams: React.Dispatch<React.SetStateAction<Record<string, StrategyParamValue>>>;
  universe: string[];
  setUniverse: React.Dispatch<React.SetStateAction<string[]>>;
  onRun: () => void;
  loading: boolean;
  lastExecutionMs?: number;
}

export const STRATEGIES_LIST: StrategyOption[] = [
  {
    id: "sma_crossover",
    name: "SMA Crossover (20, 50)",
    category: "Trend Following",
    description: "Classic moving average crossover. Slower trading, lower turnover.",
    paramsSummary: "Fast: 20, Slow: 50",
  },
  {
    id: "sma_crossover_10_30",
    name: "SMA Aggressive (10, 30)",
    category: "High Turnover",
    description: "Fast-moving crossover that triggers frequent trades and high tax friction.",
    paramsSummary: "Fast: 10, Slow: 30",
  },
  {
    id: "rsi_mean_reversion",
    name: "RSI Mean Reversion (14)",
    category: "Mean Reversion",
    description: "Buys oversold pullbacks and sells overbought rallies.",
    paramsSummary: "Period: 14, Oversold: 30, Overbought: 70",
  },
  {
    id: "momentum",
    name: "Momentum Breakout (20-Day)",
    category: "Relative Strength",
    description: "Buys stocks exhibiting strong 20-day rate-of-change momentum.",
    paramsSummary: "Lookback: 20, Threshold: 5%",
  },
  {
    id: "bollinger_breakout",
    name: "Bollinger Breakout (20, 2σ)",
    category: "Volatility Channel",
    description: "Enters when price breaks out of the 2-standard-deviation volatility envelope.",
    paramsSummary: "Period: 20, Multiplier: 2.0σ",
  },
  {
    id: "bh_and_hold",
    name: "Buy & Hold Baseline",
    category: "Passive Control",
    description: "Passive index baseline to test if your active strategy truly generates alpha.",
    paramsSummary: "Zero parameters (Passive)",
  },
];

const DEFAULT_NSE_UNIVERSE = [
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
];

interface Preset {
  id: string;
  label: string;
  strategy: string;
  params: Record<string, StrategyParamValue>;
  period: string;
  costs: boolean;
  hint: string;
}

export const RunConfigurator: React.FC<ConfiguratorProps> = ({
  strategy,
  setStrategy,
  period,
  setPeriod,
  applyCosts,
  setApplyCosts,
  demoMode,
  setDemoMode,
  initialCapital,
  setInitialCapital,
  params,
  setParams,
  universe,
  setUniverse,
  onRun,
  loading,
  lastExecutionMs,
}) => {
  const [stepIndex, setStepIndex] = useState(0);
  const [customTickerInput, setCustomTickerInput] = useState("");
  const [showAdvancedParams, setShowAdvancedParams] = useState(false);
  const [showUniverseManager, setShowUniverseManager] = useState(false);

  const steps = [
    `Analyzing ${universe.length} NSE equities...`,
    "Applying realistic execution queue...",
    "Deducting statutory STT, Stamp Duty & GST...",
    "Computing Sharpe ratio and overfitting score...",
  ];

  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (loading) {
      setStepIndex(0);
      timer = setInterval(() => {
        setStepIndex((prev) => (prev + 1) % steps.length);
      }, 700);
    }
    return () => clearInterval(timer);
  }, [loading, steps.length]);

  const presets: Preset[] = [
    {
      id: "mirage",
      label: "Retail Mirage",
      strategy: "sma_crossover",
      params: { fast_window: 20, slow_window: 50 },
      period: "full",
      costs: true,
      hint: "Demonstrates how statutory taxes consume gross returns",
    },
    {
      id: "volatility",
      label: "Volatility Breakout",
      strategy: "bollinger_breakout",
      params: { period: 20, num_std: 2.0 },
      period: "full",
      costs: true,
      hint: "Channel breakout model on 20-day standard deviation",
    },
    {
      id: "benchmark",
      label: "Passive Baseline",
      strategy: "bh_and_hold",
      params: {},
      period: "full",
      costs: false,
      hint: "Passive Buy & Hold benchmark for comparison",
    },
  ];

  const applyPreset = (p: Preset) => {
    setStrategy(p.strategy);
    setParams(p.params);
    setPeriod(p.period);
    setApplyCosts(p.costs);
  };

  const handleStrategyChange = (newStrategy: string) => {
    setStrategy(newStrategy);
    if (newStrategy === "sma_crossover") {
      setParams({ fast_window: 20, slow_window: 50 });
    } else if (newStrategy === "sma_crossover_10_30") {
      setParams({ fast_window: 10, slow_window: 30 });
    } else if (newStrategy === "rsi_mean_reversion") {
      setParams({ period: 14, oversold: 30, overbought: 70 });
    } else if (newStrategy === "momentum") {
      setParams({ lookback_period: 20, threshold_pct: 0.05 });
    } else if (newStrategy === "bollinger_breakout") {
      setParams({ period: 20, num_std: 2.0 });
    } else {
      setParams({});
    }
  };

  const toggleUniverseSymbol = (sym: string) => {
    if (universe.includes(sym)) {
      if (universe.length === 1) return;
      setUniverse(universe.filter((s) => s !== sym));
    } else {
      setUniverse([...universe, sym]);
    }
  };

  const handleAddCustomTicker = (e: React.FormEvent) => {
    e.preventDefault();
    let clean = customTickerInput.trim().toUpperCase();
    if (!clean) return;
    if (!clean.endsWith(".NS") && !clean.endsWith(".BO")) {
      clean = `${clean}.NS`;
    }
    if (!universe.includes(clean)) {
      setUniverse([...universe, clean]);
    }
    setCustomTickerInput("");
  };

  const formatINR = (val: number) => {
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    }).format(val);
  };

  return (
    <div className="flex flex-col justify-between h-full space-y-3.5 select-none text-xs">
      {/* Scrollable Setup Flow */}
      <div className="space-y-3.5 overflow-y-auto pr-1">
        {/* Header & Quick Guider */}
        <div className="border-b border-rule pb-2.5">
          <div className="flex items-center justify-between mb-1">
            <h2 className="text-xs font-bold tracking-tight text-inkText flex items-center gap-1.5">
              <Sparkles size={14} className="text-turquoise" /> Backtest Studio
            </h2>
            <span className="text-[10px] text-turquoise font-medium bg-turquoise/10 px-2 py-0.5 rounded border border-turquoise/30">
              3-Step Setup
            </span>
          </div>
          <p className="text-[11px] text-mutedText leading-relaxed">
            Configure your model, test on Indian equities, and expose real returns after taxes.
          </p>
        </div>

        {/* STEP 1: Strategy Model */}
        <div className="p-3 bg-canvas/60 border border-rule rounded-md space-y-2.5">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-semibold text-inkText flex items-center gap-1.5">
              <span className="w-4 h-4 rounded-full bg-pacificCyan/20 text-turquoise text-[10px] font-mono flex items-center justify-center font-bold">1</span>
              Choose Strategy
            </span>
            <span className="text-[10px] text-mutedText font-mono">
              {STRATEGIES_LIST.length} Available
            </span>
          </div>

          <CustomStrategySelect
            value={strategy}
            onChange={handleStrategyChange}
            strategies={STRATEGIES_LIST}
          />

          {/* Quick Curated Scenarios */}
          <div>
            <div className="text-[10px] text-mutedText mb-1.5 font-medium">Quick Scenarios:</div>
            <div className="grid grid-cols-3 gap-1">
              {presets.map((p) => {
                const isActive = strategy === p.strategy && period === p.period;
                return (
                  <button
                    key={p.id}
                    type="button"
                    onClick={() => applyPreset(p)}
                    className={`px-1.5 py-1 text-[10px] rounded border text-center truncate transition-all ${
                      isActive
                        ? "bg-pacificCyan/20 border-turquoise text-turquoise font-semibold shadow-xs"
                        : "bg-panel border-rule text-mutedText hover:border-turquoise/60 hover:text-inkText"
                    }`}
                    title={p.hint}
                  >
                    {p.label}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Collapsible Fine-Tuning */}
          {strategy !== "bh_and_hold" && (
            <div className="pt-1 border-t border-rule/50">
              <button
                type="button"
                onClick={() => setShowAdvancedParams(!showAdvancedParams)}
                className="w-full flex items-center justify-between text-[10px] text-mutedText hover:text-turquoise py-1 transition-colors"
              >
                <span className="flex items-center gap-1">
                  <Sliders size={11} /> Fine-Tune Parameters
                </span>
                {showAdvancedParams ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
              </button>

              {showAdvancedParams && (
                <div className="pt-2 space-y-2.5 border-t border-rule/40 mt-1">
                  {(strategy === "sma_crossover" || strategy === "sma_crossover_10_30") && (
                    <>
                      <div>
                        <div className="flex justify-between text-[10px] mb-1">
                          <span className="text-mutedText">Fast Moving Average:</span>
                          <span className="text-turquoise font-bold">{params.fast_window || 20} bars</span>
                        </div>
                        <input
                          type="range"
                          min="5"
                          max="50"
                          step="1"
                          value={params.fast_window || 20}
                          onChange={(e) =>
                            setParams({ ...params, fast_window: parseInt(e.target.value) })
                          }
                          className="w-full accent-turquoise h-1 bg-darkSlate rounded cursor-pointer"
                        />
                      </div>

                      <div>
                        <div className="flex justify-between text-[10px] mb-1">
                          <span className="text-mutedText">Slow Moving Average:</span>
                          <span className="text-turquoise font-bold">{params.slow_window || 50} bars</span>
                        </div>
                        <input
                          type="range"
                          min="20"
                          max="150"
                          step="1"
                          value={params.slow_window || 50}
                          onChange={(e) =>
                            setParams({ ...params, slow_window: parseInt(e.target.value) })
                          }
                          className="w-full accent-turquoise h-1 bg-darkSlate rounded cursor-pointer"
                        />
                      </div>
                    </>
                  )}

                  {strategy === "rsi_mean_reversion" && (
                    <>
                      <div>
                        <div className="flex justify-between text-[10px] mb-1">
                          <span className="text-mutedText">RSI Lookback Period:</span>
                          <span className="text-turquoise font-bold">{params.period || 14}</span>
                        </div>
                        <input
                          type="range"
                          min="5"
                          max="30"
                          step="1"
                          value={params.period || 14}
                          onChange={(e) =>
                            setParams({ ...params, period: parseInt(e.target.value) })
                          }
                          className="w-full accent-turquoise h-1 bg-darkSlate rounded cursor-pointer"
                        />
                      </div>

                      <div className="grid grid-cols-2 gap-2">
                        <div>
                          <div className="flex justify-between text-[9px] mb-1">
                            <span className="text-mutedText">Oversold:</span>
                            <span className="text-turquoise font-bold">{params.oversold || 30}</span>
                          </div>
                          <input
                            type="range"
                            min="15"
                            max="45"
                            value={params.oversold || 30}
                            onChange={(e) =>
                              setParams({ ...params, oversold: parseFloat(e.target.value) })
                            }
                            className="w-full accent-turquoise h-1 bg-darkSlate rounded cursor-pointer"
                          />
                        </div>
                        <div>
                          <div className="flex justify-between text-[9px] mb-1">
                            <span className="text-mutedText">Overbought:</span>
                            <span className="text-crimson font-bold">{params.overbought || 70}</span>
                          </div>
                          <input
                            type="range"
                            min="55"
                            max="85"
                            value={params.overbought || 70}
                            onChange={(e) =>
                              setParams({ ...params, overbought: parseFloat(e.target.value) })
                            }
                            className="w-full accent-crimson h-1 bg-darkSlate rounded cursor-pointer"
                          />
                        </div>
                      </div>
                    </>
                  )}

                  {strategy === "bollinger_breakout" && (
                    <>
                      <div>
                        <div className="flex justify-between text-[10px] mb-1">
                          <span className="text-mutedText">Envelope Period:</span>
                          <span className="text-turquoise font-bold">{params.period || 20} bars</span>
                        </div>
                        <input
                          type="range"
                          min="10"
                          max="50"
                          step="1"
                          value={params.period || 20}
                          onChange={(e) =>
                            setParams({ ...params, period: parseInt(e.target.value) })
                          }
                          className="w-full accent-turquoise h-1 bg-darkSlate rounded cursor-pointer"
                        />
                      </div>

                      <div>
                        <div className="flex justify-between text-[10px] mb-1">
                          <span className="text-mutedText">Band Width:</span>
                          <span className="text-turquoise font-bold">
                            {(params.num_std || 2.0).toFixed(1)}σ
                          </span>
                        </div>
                        <input
                          type="range"
                          min="1.0"
                          max="3.0"
                          step="0.1"
                          value={params.num_std || 2.0}
                          onChange={(e) =>
                            setParams({ ...params, num_std: parseFloat(e.target.value) })
                          }
                          className="w-full accent-turquoise h-1 bg-darkSlate rounded cursor-pointer"
                        />
                      </div>
                    </>
                  )}

                  {strategy === "momentum" && (
                    <>
                      <div>
                        <div className="flex justify-between text-[10px] mb-1">
                          <span className="text-mutedText">Lookback Period:</span>
                          <span className="text-turquoise font-bold">{params.lookback_period || 20}d</span>
                        </div>
                        <input
                          type="range"
                          min="5"
                          max="60"
                          step="1"
                          value={params.lookback_period || 20}
                          onChange={(e) =>
                            setParams({ ...params, lookback_period: parseInt(e.target.value) })
                          }
                          className="w-full accent-turquoise h-1 bg-darkSlate rounded cursor-pointer"
                        />
                      </div>

                      <div>
                        <div className="flex justify-between text-[10px] mb-1">
                          <span className="text-mutedText">Minimum Momentum:</span>
                          <span className="text-turquoise font-bold">
                            {((params.threshold_pct || 0.05) * 100).toFixed(1)}%
                          </span>
                        </div>
                        <input
                          type="range"
                          min="0.01"
                          max="0.15"
                          step="0.005"
                          value={params.threshold_pct || 0.05}
                          onChange={(e) =>
                            setParams({ ...params, threshold_pct: parseFloat(e.target.value) })
                          }
                          className="w-full accent-turquoise h-1 bg-darkSlate rounded cursor-pointer"
                        />
                      </div>
                    </>
                  )}
                </div>
              )}
            </div>
          )}
        </div>

        {/* STEP 2: Capital & Equities */}
        <div className="p-3 bg-canvas/60 border border-rule rounded-md space-y-2.5">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-semibold text-inkText flex items-center gap-1.5">
              <span className="w-4 h-4 rounded-full bg-pacificCyan/20 text-turquoise text-[10px] font-mono flex items-center justify-center font-bold">2</span>
              Capital & Equities
            </span>
            <span className="text-[10px] text-turquoise font-mono font-bold">
              {formatINR(initialCapital)}
            </span>
          </div>

          {/* Capital Input & Quick Pills */}
          <div className="space-y-1.5">
            <div className="relative">
              <span className="absolute left-2.5 top-1.5 text-mutedText text-xs font-mono">₹</span>
              <input
                type="number"
                min="10000"
                max="100000000"
                step="10000"
                value={initialCapital}
                onChange={(e) => setInitialCapital(Math.max(10000, Number(e.target.value)))}
                className="w-full pl-6 pr-2 py-1.5 bg-canvas border border-rule rounded text-inkText text-xs font-mono outline-none focus:border-turquoise"
                placeholder="Starting Amount"
              />
            </div>

            <div className="flex items-center gap-1 overflow-x-auto">
              {[50000, 100000, 500000, 1000000].map((amt) => (
                <button
                  key={amt}
                  type="button"
                  onClick={() => setInitialCapital(amt)}
                  className={`flex-1 py-1 text-[9px] rounded border transition-all text-center ${
                    initialCapital === amt
                      ? "bg-turquoise/20 border-turquoise text-turquoise font-bold"
                      : "bg-panel border-rule text-mutedText hover:border-turquoise/50"
                  }`}
                >
                  ₹{amt >= 100000 ? `${amt / 100000}L` : `${amt / 1000}K`}
                </button>
              ))}
            </div>
          </div>

          {/* Stock Universe Summary & Manager */}
          <div className="pt-1 border-t border-rule/50">
            <div className="flex items-center justify-between">
              <span className="text-[10px] text-mutedText">
                Active Stocks: <strong className="text-inkText">{universe.length} NSE Equities</strong>
              </span>
              <button
                type="button"
                onClick={() => setShowUniverseManager(!showUniverseManager)}
                className="text-[10px] text-pacificCyan hover:text-turquoise flex items-center gap-1"
              >
                <span>{showUniverseManager ? "Hide" : "Manage"}</span>
                {showUniverseManager ? <ChevronUp size={11} /> : <ChevronDown size={11} />}
              </button>
            </div>

            {showUniverseManager && (
              <div className="pt-2 space-y-2 border-t border-rule/40 mt-1">
                <div className="flex items-center justify-between text-[9px] text-mutedText">
                  <span>Toggle stocks:</span>
                  <div className="flex gap-1.5">
                    <button
                      type="button"
                      onClick={() => setUniverse(DEFAULT_NSE_UNIVERSE)}
                      className="text-turquoise hover:underline"
                    >
                      All 10
                    </button>
                    <span>·</span>
                    <button
                      type="button"
                      onClick={() => setUniverse(DEFAULT_NSE_UNIVERSE.slice(0, 5))}
                      className="text-turquoise hover:underline"
                    >
                      Top 5
                    </button>
                  </div>
                </div>

                <div className="flex flex-wrap gap-1 max-h-24 overflow-y-auto pr-0.5">
                  {DEFAULT_NSE_UNIVERSE.map((sym) => {
                    const clean = sym.replace(".NS", "");
                    const isSelected = universe.includes(sym);
                    return (
                      <button
                        key={sym}
                        type="button"
                        onClick={() => toggleUniverseSymbol(sym)}
                        className={`px-1.5 py-0.5 text-[9px] rounded border transition-all ${
                          isSelected
                            ? "bg-pacificCyan/20 border-turquoise text-turquoise font-medium"
                            : "bg-panel border-rule/60 text-mutedText/70 hover:border-rule"
                        }`}
                      >
                        {clean}
                      </button>
                    );
                  })}
                  {universe
                    .filter((s) => !DEFAULT_NSE_UNIVERSE.includes(s))
                    .map((sym) => (
                      <button
                        key={sym}
                        type="button"
                        onClick={() => toggleUniverseSymbol(sym)}
                        className="px-1.5 py-0.5 text-[9px] rounded border bg-turquoise/20 border-turquoise text-turquoise font-medium flex items-center gap-1"
                      >
                        <span className="w-1.5 h-1.5 rounded-full bg-turquoise animate-pulse" />
                        {sym.replace(".NS", "")}
                        <X
                          size={9}
                          onClick={(e) => {
                            e.stopPropagation();
                            setUniverse(universe.filter((s) => s !== sym));
                          }}
                        />
                      </button>
                    ))}
                </div>

                {/* Add Custom Ticker */}
                <form onSubmit={handleAddCustomTicker} className="flex gap-1 pt-1">
                  <input
                    type="text"
                    placeholder="Add NSE Stock (e.g. TATAMOTORS)"
                    value={customTickerInput}
                    onChange={(e) => setCustomTickerInput(e.target.value)}
                    className="flex-1 px-2 py-1 bg-canvas border border-rule rounded text-[10px] text-inkText placeholder:text-mutedText outline-none focus:border-turquoise uppercase"
                  />
                  <button
                    type="submit"
                    disabled={!customTickerInput.trim()}
                    className="px-2 py-1 bg-pacificCyan text-white text-[10px] font-bold rounded border border-turquoise/40 hover:bg-pacificCyan/90 disabled:opacity-50"
                  >
                    <Plus size={11} />
                  </button>
                </form>
              </div>
            )}
          </div>
        </div>

        {/* STEP 3: Timeline & Realistic Taxes */}
        <div className="p-3 bg-canvas/60 border border-rule rounded-md space-y-2.5">
          <span className="text-[11px] font-semibold text-inkText flex items-center gap-1.5">
            <span className="w-4 h-4 rounded-full bg-pacificCyan/20 text-turquoise text-[10px] font-mono flex items-center justify-center font-bold">3</span>
            Duration & Indian Taxes
          </span>

          <div className="grid grid-cols-3 gap-1">
            {[
              { id: "full", label: "Full Period", range: "2019–2024" },
              { id: "IS", label: "In-Sample", range: "2019–2022" },
              { id: "OOS", label: "Out-of-Sample", range: "2023–2024" },
            ].map((p) => (
              <button
                key={p.id}
                type="button"
                onClick={() => setPeriod(p.id)}
                className={`p-1.5 border text-center rounded transition-all ${
                  period === p.id
                    ? "bg-pacificCyan/20 border-turquoise text-turquoise font-bold"
                    : "bg-panel border-rule text-mutedText hover:border-turquoise/50"
                }`}
              >
                <div className="text-[10px] font-medium leading-tight">{p.label}</div>
                <div className="text-[8px] text-mutedText mt-0.5">{p.range}</div>
              </button>
            ))}
          </div>

          <div className="space-y-1.5 pt-1 border-t border-rule/50">
            <label className="flex items-center justify-between cursor-pointer py-1 bg-panel px-2 rounded border border-rule/50 hover:border-rule">
              <div>
                <div className="text-inkText font-medium text-[10px]">Deduct Statutory Indian Taxes</div>
                <div className="text-mutedText text-[9px]">STT (0.1%), Stamp Duty (0.015%), GST (18%)</div>
              </div>
              <input
                type="checkbox"
                checked={applyCosts}
                onChange={(e) => setApplyCosts(e.target.checked)}
                className="accent-turquoise w-3.5 h-3.5 cursor-pointer"
              />
            </label>

            <label className="flex items-center justify-between cursor-pointer py-1 bg-panel px-2 rounded border border-rule/50 hover:border-rule">
              <div>
                <div className="text-inkText font-medium text-[10px]">Instant Demo Mode</div>
                <div className="text-mutedText text-[9px]">Instant response from verified dataset</div>
              </div>
              <input
                type="checkbox"
                checked={demoMode}
                onChange={(e) => setDemoMode(e.target.checked)}
                className="accent-crimson w-3.5 h-3.5 cursor-pointer"
              />
            </label>
          </div>
        </div>
      </div>

      {/* Action Area: Clear Execution & Feedback */}
      <div className="pt-2 border-t border-rule space-y-2 shrink-0">
        {loading && (
          <div className="p-2.5 bg-canvas border border-turquoise/50 rounded-md space-y-1.5 animate-pulse">
            <div className="flex items-center justify-between text-[10px] text-turquoise font-medium">
              <span className="flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-turquoise animate-ping" />
                Simulating Market...
              </span>
              <span className="font-mono">Step {stepIndex + 1}/4</span>
            </div>
            <div className="text-[11px] text-inkText truncate">
              {steps[stepIndex]}
            </div>
            <div className="w-full bg-panel h-1.5 rounded-full overflow-hidden">
              <div
                className="bg-turquoise h-full transition-all duration-300"
                style={{ width: `${((stepIndex + 1) / steps.length) * 100}%` }}
              />
            </div>
          </div>
        )}

        <button
          type="button"
          onClick={onRun}
          disabled={loading}
          className={`w-full py-3 px-4 text-xs font-bold tracking-wider uppercase rounded-md transition-all shadow-md flex items-center justify-center gap-2 ${
            loading
              ? "bg-mutedText text-darkSlate cursor-not-allowed opacity-80"
              : "bg-pacificCyan hover:bg-pacificCyan/85 text-white active:scale-[0.99] border border-turquoise/50 hover:border-turquoise shadow-lg shadow-pacificCyan/10 cursor-pointer"
          }`}
        >
          {loading ? (
            <span>Crunching Numbers...</span>
          ) : (
            <>
              <CheckCircle2 size={14} className="text-turquoise" />
              <span>Run Backtest</span>
            </>
          )}
        </button>

        {lastExecutionMs !== undefined && !loading && (
          <div className="text-center text-[10px] text-mutedText">
            Results calculated in <span className="text-turquoise font-medium font-mono">{lastExecutionMs.toFixed(0)} ms</span>
          </div>
        )}
      </div>
    </div>
  );
};
