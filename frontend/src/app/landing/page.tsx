"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  ShieldAlert,
  TrendingDown,
  Activity,
  Terminal,
  ArrowRight,
  Scale,
  Sparkles,
} from "lucide-react";

export default function LandingPage() {
  // Interactive Cost Calculator Preview State
  const [calcCapital, setCalcCapital] = useState(200000); // 2 Lakhs
  const [calcTurnover, setCalcTurnover] = useState(6); // 6x turnover / year

  // Indian Equity Delivery Statutory Calculations
  const tradesPerYear = Math.max(2, Math.round((calcTurnover * calcCapital) / 30000));
  const annualVolume = calcCapital * calcTurnover;
  const buyTurnover = annualVolume / 2;

  // Exact statutory formulas (Zerodha 2024 True-to-Label rate card)
  const stt = annualVolume * 0.001; // 0.10% buy + sell
  const stampDuty = buyTurnover * 0.00015; // 0.015% buy only
  const nseTurnoverFee = annualVolume * 0.0000297; // 0.00297%
  const sebiFee = (annualVolume / 10000000) * 10; // Rs 10 / crore
  const ipft = (annualVolume / 10000000) * 10; // Rs 10 / crore
  const dpCharges = Math.round(tradesPerYear / 2) * 13.5 * 1.18; // Rs 13.50 + 18% GST on sells
  const brokerage = 0; // True-to-label free delivery
  const exchangeGst = (nseTurnoverFee + sebiFee) * 0.18; // 18% on exchange charges

  const totalFriction =
    stt + stampDuty + nseTurnoverFee + sebiFee + ipft + dpCharges + brokerage + exchangeGst;
  const frictionDragPct = (totalFriction / calcCapital) * 100;

  return (
    <div className="min-h-screen bg-[#10191B] text-[#E0EBF0] font-sans antialiased selection:bg-[#42D9C8] selection:text-[#10191B]">
      {/* Top Ambient Navigation Bar */}
      <header className="sticky top-0 z-50 backdrop-blur-md bg-[#10191B]/85 border-b border-[#326771]/40 px-6 py-3.5 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded bg-gradient-to-br from-[#2C8C99] to-[#42D9C8] flex items-center justify-center font-bold text-[#10191B] text-lg font-mono shadow-lg shadow-[#42D9C8]/10">
            प्र
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-base tracking-tight text-white font-mono">
                PRAMAAN
              </span>
              <span className="px-1.5 py-0.2 rounded text-[10px] font-mono font-semibold bg-[#42D9C8]/15 text-[#42D9C8] border border-[#42D9C8]/30">
                v1.0.0
              </span>
            </div>
            <p className="text-[10px] text-[#8CA0A8] font-mono tracking-wide">
              GTU DI05000341 · Honest NSE Backtester
            </p>
          </div>
        </div>

        <nav className="flex items-center gap-4 text-xs font-mono">
          <a
            href="#moats"
            className="text-[#8CA0A8] hover:text-[#42D9C8] transition-colors hidden sm:inline"
          >
            The 2 Moats
          </a>
          <a
            href="#calculator"
            className="text-[#8CA0A8] hover:text-[#42D9C8] transition-colors hidden sm:inline"
          >
            Cost Calculator
          </a>
          <a
            href="#quickstart"
            className="text-[#8CA0A8] hover:text-[#42D9C8] transition-colors hidden md:inline"
          >
            Quickstart
          </a>
          <Link
            href="/"
            className="px-3.5 py-1.5 rounded bg-[#42D9C8] hover:bg-[#42D9C8]/90 text-[#10191B] font-semibold transition-all shadow-md shadow-[#42D9C8]/20 flex items-center gap-1.5"
          >
            <Terminal className="w-3.5 h-3.5" />
            Launch Terminal
          </Link>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="relative overflow-hidden pt-20 pb-24 px-6 max-w-6xl mx-auto text-center">
        <div className="absolute inset-0 -z-10 flex items-center justify-center opacity-20 pointer-events-none">
          <div className="w-[600px] h-[600px] rounded-full bg-gradient-to-tr from-[#2C8C99] to-[#42D9C8] blur-[140px]" />
        </div>

        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[#326771] bg-[#28464B]/40 text-[#42D9C8] text-xs font-mono mb-6 backdrop-blur">
          <ShieldAlert className="w-3.5 h-3.5 text-[#931621]" />
          <span>Zero-Lookahead T+1 Execution · Paisa-Exact Indian Friction</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white max-w-4xl mx-auto leading-[1.12]">
          Prove your edge{" "}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#42D9C8] via-[#2C8C99] to-[#931621]">
            before you deploy a rupee.
          </span>
        </h1>

        <p className="mt-6 text-base sm:text-lg text-[#A0B4BC] max-w-2xl mx-auto font-normal leading-relaxed">
          The honest backtesting engine for Indian (NSE) equities. Eliminates
          the two fatal illusions that destroy algorithmic capital: unmodeled statutory tax drag and statistical overfitting.
        </p>

        <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
          <Link
            href="/"
            className="px-6 py-3 rounded bg-gradient-to-r from-[#2C8C99] to-[#42D9C8] hover:opacity-95 text-[#10191B] font-bold text-sm tracking-wide shadow-lg shadow-[#42D9C8]/20 flex items-center gap-2 transition-all hover:scale-[1.02]"
          >
            <Activity className="w-4 h-4" />
            Run Live Backtest
            <ArrowRight className="w-4 h-4 ml-1" />
          </Link>
          <a
            href="https://github.com/aayushbankar/pramaan"
            target="_blank"
            rel="noopener noreferrer"
            className="px-6 py-3 rounded border border-[#326771] bg-[#28464B]/50 hover:bg-[#28464B] text-white font-mono text-sm tracking-wide transition-all flex items-center gap-2"
          >
            <Terminal className="w-4 h-4 text-[#42D9C8]" />
            GitHub Repository
          </a>
        </div>

        {/* Real Finding Callout Pill */}
        <div className="mt-14 max-w-3xl mx-auto p-4 rounded-lg border border-[#326771]/60 bg-[#28464B]/30 backdrop-blur text-left flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded bg-[#931621]/20 border border-[#931621]/40 flex items-center justify-center shrink-0">
              <TrendingDown className="w-5 h-5 text-[#931621]" />
            </div>
            <div>
              <div className="text-xs font-mono font-semibold text-white">
                Empirical Finding: 0 of 4 Active Models Beat Passive Buy-and-Hold
              </div>
              <p className="text-[11px] text-[#8CA0A8] mt-0.5">
                NIFTY-50 (2019–2024, 14,800 bars). Gross alpha vanishes after STT, DP charges, and GST are accounted for.
              </p>
            </div>
          </div>
          <span className="shrink-0 px-2.5 py-1 rounded text-[11px] font-mono bg-[#10191B] text-[#42D9C8] border border-[#326771]">
            NFR-1 Deterministic
          </span>
        </div>
      </section>

      {/* The 2 Moats Section */}
      <section id="moats" className="py-20 px-6 max-w-6xl mx-auto border-t border-[#326771]/30">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <span className="text-xs font-mono text-[#42D9C8] uppercase tracking-widest">
            Institutional Moats
          </span>
          <h2 className="text-3xl font-bold text-white mt-2">
            Why Other Backtesters Lie to You
          </h2>
          <p className="text-sm text-[#8CA0A8] mt-3">
            Generic international libraries assume zero friction and evaluate in-sample models that fail the moment real capital touches an exchange.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Moat 1 */}
          <div className="p-7 rounded-xl border border-[#326771] bg-[#28464B]/40 flex flex-col justify-between hover:border-[#42D9C8]/40 transition-colors">
            <div>
              <div className="w-12 h-12 rounded-lg bg-[#931621]/20 border border-[#931621]/40 flex items-center justify-center mb-5 text-[#931621]">
                <Scale className="w-6 h-6" />
              </div>
              <span className="text-[11px] font-mono text-[#931621] font-semibold uppercase tracking-wider">
                Moat 01 · Statutory Microstructure
              </span>
              <h3 className="text-xl font-bold text-white mt-1.5">
                The Full Indian Delivery Cost Stack
              </h3>
              <p className="text-sm text-[#A0B4BC] mt-3 leading-relaxed">
                Most platforms model a flat 0.05% brokerage. Pramaan applies the <strong>actual legal statutory tariff</strong> per SEBI circulars down to exact paise:
              </p>
              <ul className="mt-4 space-y-2 text-xs font-mono text-[#8CA0A8]">
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#931621]" />
                  <span><strong>STT:</strong> 0.10% delivery on both buy & sell legs (dominates retail size)</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-500" />
                  <span><strong>DP Charges:</strong> Flat ₹13.50 + 18% GST per debit transaction (CDSL/NSDL)</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#2C8C99]" />
                  <span><strong>Stamp Duty:</strong> 0.015% buy-side statutory stamp</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#42D9C8]" />
                  <span><strong>NSE & SEBI:</strong> 0.00297% turnover fee + ₹10/cr SEBI charge + IPFT</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-indigo-400" />
                  <span><strong>Almgren–Chriss Impact:</strong> Square-root slippage based on ADV</span>
                </li>
              </ul>
            </div>
            <div className="mt-6 pt-5 border-t border-[#326771]/40 text-xs font-mono text-[#42D9C8]">
              Result: 48.2% of momentum alpha destroyed by statutory friction alone.
            </div>
          </div>

          {/* Moat 2 */}
          <div className="p-7 rounded-xl border border-[#326771] bg-[#28464B]/40 flex flex-col justify-between hover:border-[#42D9C8]/40 transition-colors">
            <div>
              <div className="w-12 h-12 rounded-lg bg-[#2C8C99]/20 border border-[#2C8C99]/40 flex items-center justify-center mb-5 text-[#42D9C8]">
                <Sparkles className="w-6 h-6" />
              </div>
              <span className="text-[11px] font-mono text-[#42D9C8] font-semibold uppercase tracking-wider">
                Moat 02 · Statistical Guardrails
              </span>
              <h3 className="text-xl font-bold text-white mt-1.5">
                Marcos López de Prado Diagnostics
              </h3>
              <p className="text-sm text-[#A0B4BC] mt-3 leading-relaxed">
                Backtest overfitting is selection bias masquerading as skill. Pramaan integrates the statistical gold standard:
              </p>
              <ul className="mt-4 space-y-2 text-xs font-mono text-[#8CA0A8]">
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#42D9C8]" />
                  <span><strong>Deflated Sharpe Ratio (DSR):</strong> Corrects for trial counts (N) and cross-trial variance V[SR].</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#2C8C99]" />
                  <span><strong>Combinatorial Purged Cross-Validation (CPCV):</strong> 45 overlapping test paths with non-zero embargo.</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-400" />
                  <span><strong>Probability of Backtest Overfitting (PBO):</strong> Measures how often the in-sample winner underperforms OOS.</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#931621]" />
                  <span><strong>Ground-Truth Sweep:</strong> 133 configurations evaluated; empirical PBO = 60.0% [44.4%, 73.3%].</span>
                </li>
              </ul>
            </div>
            <div className="mt-6 pt-5 border-t border-[#326771]/40 text-xs font-mono text-[#42D9C8]">
              Result: Defends your capital from statistical self-deception.
            </div>
          </div>
        </div>
      </section>

      {/* Interactive Cost Calculator Preview */}
      <section id="calculator" className="py-20 px-6 max-w-6xl mx-auto border-t border-[#326771]/30">
        <div className="text-center max-w-2xl mx-auto mb-14">
          <span className="text-xs font-mono text-[#42D9C8] uppercase tracking-widest">
            Interactive Tollgate Simulator
          </span>
          <h2 className="text-3xl font-bold text-white mt-2">
            Calculate Your Real Statutory Drag
          </h2>
          <p className="text-sm text-[#8CA0A8] mt-3">
            See how much edge Indian taxes and exchange charges extract from your portfolio before your strategy generates a single rupee of net profit.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center bg-[#28464B]/30 border border-[#326771] rounded-2xl p-6 lg:p-8">
          {/* Controls */}
          <div className="lg:col-span-5 space-y-6">
            <div>
              <div className="flex justify-between text-xs font-mono mb-2">
                <span className="text-[#8CA0A8]">Trading Capital</span>
                <span className="text-white font-bold">
                  ₹{calcCapital.toLocaleString("en-IN")}
                </span>
              </div>
              <input
                type="range"
                min={50000}
                max={2000000}
                step={25000}
                value={calcCapital}
                onChange={(e) => setCalcCapital(Number(e.target.value))}
                className="w-full accent-[#42D9C8] bg-[#10191B] rounded cursor-pointer h-2"
              />
              <div className="flex justify-between text-[10px] text-[#8CA0A8] font-mono mt-1">
                <span>₹50K</span>
                <span>₹10L</span>
                <span>₹20L</span>
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs font-mono mb-2">
                <span className="text-[#8CA0A8]">Annual Portfolio Turnover</span>
                <span className="text-white font-bold">{calcTurnover}x / year</span>
              </div>
              <input
                type="range"
                min={1}
                max={20}
                step={1}
                value={calcTurnover}
                onChange={(e) => setCalcTurnover(Number(e.target.value))}
                className="w-full accent-[#42D9C8] bg-[#10191B] rounded cursor-pointer h-2"
              />
              <div className="flex justify-between text-[10px] text-[#8CA0A8] font-mono mt-1">
                <span>1x (Passive)</span>
                <span>10x (Active Swing)</span>
                <span>20x (Frequent)</span>
              </div>
            </div>

            <div className="p-4 rounded-lg bg-[#10191B]/60 border border-[#326771]/50 text-xs font-mono text-[#8CA0A8] space-y-2">
              <div className="flex justify-between">
                <span>Annual Trading Volume:</span>
                <span className="text-white font-bold">
                  ₹{annualVolume.toLocaleString("en-IN")}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Est. Completed Trades:</span>
                <span className="text-white font-bold">{tradesPerYear} executions</span>
              </div>
              <div className="flex justify-between">
                <span>Rate Card Applied:</span>
                <span className="text-[#42D9C8] font-semibold">
                  Zerodha Oct 2024 True-to-Label
                </span>
              </div>
            </div>
          </div>

          {/* Results Visualizer */}
          <div className="lg:col-span-7 bg-[#10191B] border border-[#326771] rounded-xl p-6">
            <div className="flex items-center justify-between border-b border-[#326771]/50 pb-4 mb-4">
              <div>
                <span className="text-xs font-mono text-[#8CA0A8]">Total Annual Statutory Drag</span>
                <div className="text-2xl font-bold font-mono text-[#931621] mt-0.5">
                  -₹{totalFriction.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
                </div>
              </div>
              <div className="text-right">
                <span className="text-xs font-mono text-[#8CA0A8]">Drag as % of Capital</span>
                <div className="text-2xl font-bold font-mono text-[#931621] mt-0.5">
                  {frictionDragPct.toFixed(2)}%
                </div>
              </div>
            </div>

            {/* Breakdown Bars */}
            <div className="space-y-2.5 text-xs font-mono">
              <div className="flex justify-between items-center py-1 border-b border-[#326771]/30">
                <span className="text-[#8CA0A8]">STT (Securities Transaction Tax 0.10%)</span>
                <span className="text-white font-bold">
                  ₹{stt.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
                </span>
              </div>
              <div className="flex justify-between items-center py-1 border-b border-[#326771]/30">
                <span className="text-[#8CA0A8]">DP Charges (₹13.50 + 18% GST on debit)</span>
                <span className="text-amber-400 font-bold">
                  ₹{dpCharges.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
                </span>
              </div>
              <div className="flex justify-between items-center py-1 border-b border-[#326771]/30">
                <span className="text-[#8CA0A8]">Stamp Duty (0.015% buy-side)</span>
                <span className="text-white font-bold">
                  ₹{stampDuty.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
                </span>
              </div>
              <div className="flex justify-between items-center py-1 border-b border-[#326771]/30">
                <span className="text-[#8CA0A8]">NSE Turnover & SEBI Fees & IPFT</span>
                <span className="text-white font-bold">
                  ₹{(nseTurnoverFee + sebiFee + ipft).toLocaleString("en-IN", { maximumFractionDigits: 0 })}
                </span>
              </div>
              <div className="flex justify-between items-center py-1">
                <span className="text-[#8CA0A8]">Brokerage Commission</span>
                <span className="text-[#42D9C8] font-bold">₹0.00 (Zero Delivery)</span>
              </div>
            </div>

            <p className="mt-4 text-[11px] text-[#8CA0A8] italic">
              Notice: Even with ₹0 brokerage, taxes and depository fees consume {frictionDragPct.toFixed(2)}% of your capital every year at {calcTurnover}x turnover!
            </p>
          </div>
        </div>
      </section>

      {/* Reproducibility & Quickstart Section */}
      <section id="quickstart" className="py-20 px-6 max-w-6xl mx-auto border-t border-[#326771]/30">
        <div className="text-center max-w-2xl mx-auto mb-14">
          <span className="text-xs font-mono text-[#42D9C8] uppercase tracking-widest">
            100% Offline & Clean-Clone Reproducible
          </span>
          <h2 className="text-3xl font-bold text-white mt-2">
            Reproduce Every Metric Locally
          </h2>
          <p className="text-sm text-[#8CA0A8] mt-3">
            Pramaan does not hide behind cloud endpoints. The complete engine, CLI, test suite, and synthetic fixtures run offline on your machine.
          </p>
        </div>

        <div className="p-6 rounded-xl bg-[#10191B] border border-[#326771] font-mono text-xs text-[#A0B4BC] max-w-3xl mx-auto overflow-x-auto shadow-2xl">
          <div className="flex items-center justify-between pb-3 mb-3 border-b border-[#326771]/50 text-[#8CA0A8]">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-red-500/80 inline-block" />
              <span className="w-2.5 h-2.5 rounded-full bg-yellow-500/80 inline-block" />
              <span className="w-2.5 h-2.5 rounded-full bg-green-500/80 inline-block" />
              <span className="text-[11px] ml-2 text-white font-sans font-medium">bash — bash shell</span>
            </div>
            <span className="text-[10px]">Python 3.10+ / Linux & macOS</span>
          </div>

          <pre className="text-white space-y-1">
            <span className="text-[#8CA0A8]"># 1. Clone the open-source repository</span>{"\n"}
            <span>git clone https://github.com/aayushbankar/pramaan.git</span>{"\n"}
            <span>cd pramaan</span>{"\n\n"}
            <span className="text-[#8CA0A8]"># 2. Install dependencies in editable mode</span>{"\n"}
            <span>pip install -e &quot;.[dev,api]&quot;</span>{"\n\n"}
            <span className="text-[#8CA0A8]"># 3. Verify the complete 72-test suite offline</span>{"\n"}
            <span className="text-[#42D9C8]">pytest tests/ -q</span>{"\n"}
            <span className="text-emerald-400"># Output: 72 passed in ~7s</span>{"\n\n"}
            <span className="text-[#8CA0A8]"># 4. Start the honest backtest engine API</span>{"\n"}
            <span>python -m src.api.main</span>{"\n\n"}
            <span className="text-[#8CA0A8]"># 5. Launch the desktop terminal UI</span>{"\n"}
            <span>cd frontend &amp;&amp; npm run dev</span>
          </pre>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 border-t border-[#326771]/40 bg-[#10191B] text-xs font-mono text-[#8CA0A8]">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
          <div>
            <div className="flex items-center gap-2 text-white font-bold">
              <span>PRAMAAN (प्रमाण)</span>
              <span>·</span>
              <span className="text-[#8CA0A8] font-normal">GTU DI05000341 Minor Project</span>
            </div>
            <p className="mt-1 text-[11px]">
              Authors: Aayush Avinash Bankar &amp; Meet Jayeshbhai Patel
            </p>
          </div>

          <div className="flex items-center gap-6">
            <Link href="/" className="hover:text-[#42D9C8] transition-colors">
              Trading Terminal
            </Link>
            <a
              href="https://github.com/aayushbankar/pramaan"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-[#42D9C8] transition-colors"
            >
              GitHub
            </a>
            <span className="text-[#326771]">|</span>
            <span className="text-[#8CA0A8]">
              No Live Trading · Simulation &amp; Audit Only
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
}
