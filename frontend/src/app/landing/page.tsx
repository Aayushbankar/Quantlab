"use client";

import React, { useEffect, useRef, useState } from "react";
import Link from "next/link";
import {
  ShieldAlert,
  TrendingDown,
  Terminal,
  ArrowRight,
  Scale,
  Sparkles,
  Copy,
  Check,
  Sun,
  Moon,
  Contrast,
} from "lucide-react";
import { Reveal } from "../../components/Reveal";
import { CustomCursor } from "../../components/CustomCursor";
import {
  applyTheme,
  loadTheme,
  nextTheme,
  THEME_LABELS,
  type ThemeName,
} from "../../lib/theme";

const TICKER_ITEMS = [
  "0 of 4 active models beat passive buy-and-hold (2019–2024)",
  "₹5,064 statutory friction on ₹1,00,000 — 5.06% drag",
  "14,800 NIFTY-50 bars · zero look-ahead · T+1 fills",
  "PBO 60.0% [44.4%, 73.3%] across 133 configurations",
  "DSR p = 0.524 — no deflated Sharpe significance",
  "STT 0.10% · Stamp 0.015% · DP ₹13.50 · GST 18%",
];

const HERO_STATS = [
  { value: "0 / 4", label: "Models beating B&H", tone: "text-crimson" },
  { value: "5.06%", label: "Annual friction drag", tone: "text-crimson" },
  { value: "14,800", label: "Bars simulated", tone: "text-inkText" },
  { value: "60.0%", label: "Backtest overfitting (PBO)", tone: "text-turquoise" },
];

const MOAT_1_LINES = [
  { dot: "bg-crimson", text: "STT: 0.10% delivery on both buy & sell legs" },
  { dot: "bg-amber-400", text: "DP Charges: flat ₹13.50 + 18% GST per debit" },
  { dot: "bg-pacificCyan", text: "Stamp Duty: 0.015% buy-side statutory stamp" },
  { dot: "bg-turquoise", text: "NSE & SEBI: 0.00297% + ₹10/cr + IPFT" },
  { dot: "bg-indigo-400", text: "Almgren–Chriss: square-root slippage on ADV" },
];

const MOAT_2_LINES = [
  { n: "01", text: "Deflated Sharpe Ratio — corrects for trial count N and cross-trial variance V[SR]." },
  { n: "02", text: "Combinatorial Purged CV — 45 overlapping test paths with non-zero embargo." },
  { n: "03", text: "Probability of Backtest Overfitting — how often the in-sample winner fails OOS." },
  { n: "04", text: "Ground-truth sweep — 133 configurations, empirical PBO = 60.0% [44.4%, 73.3%]." },
];

const QUICKSTART_STEPS = [
  { n: "01", title: "Clone the repository", cmd: "git clone https://github.com/aayushbankar/pramaan.git" },
  { n: "02", title: "Install in editable mode", cmd: 'pip install -e ".[dev,api]"' },
  { n: "03", title: "Verify the test suite offline", cmd: "pytest tests/ -q" },
  { n: "04", title: "Start engine + terminal UI", cmd: "python -m src.api.main  ·  cd frontend && npm run dev" },
];

export default function LandingPage() {
  const [calcCapital, setCalcCapital] = useState(200000);
  const [calcTurnover, setCalcTurnover] = useState(6);
  const [theme, setTheme] = useState<ThemeName>("abyss");
  const [navHidden, setNavHidden] = useState(false);
  const [copied, setCopied] = useState(false);
  const lastY = useRef(0);

  useEffect(() => {
    const saved = loadTheme();
    setTheme(saved);
    document.documentElement.setAttribute("data-theme", saved);
  }, []);

  useEffect(() => {
    const onScroll = () => {
      const y = window.scrollY;
      setNavHidden(y > 140 && y > lastY.current);
      lastY.current = y;
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const cycleTheme = () => {
    const next = nextTheme(theme);
    setTheme(next);
    applyTheme(next);
  };

  const ThemeIcon = theme === "abyss" ? Moon : theme === "vellum" ? Sun : Contrast;

  const tradesPerYear = Math.max(2, Math.round((calcTurnover * calcCapital) / 30000));
  const annualVolume = calcCapital * calcTurnover;
  const buyTurnover = annualVolume / 2;

  const stt = annualVolume * 0.001;
  const stampDuty = buyTurnover * 0.00015;
  const nseTurnoverFee = annualVolume * 0.0000297;
  const sebiFee = (annualVolume / 10000000) * 10;
  const ipft = (annualVolume / 10000000) * 10;
  const dpCharges = Math.round(tradesPerYear / 2) * 13.5 * 1.18;
  const exchangeGst = (nseTurnoverFee + sebiFee) * 0.18;
  const brokerage = 0;

  const totalFriction =
    stt + stampDuty + nseTurnoverFee + sebiFee + ipft + dpCharges + brokerage + exchangeGst;
  const frictionDragPct = (totalFriction / calcCapital) * 100;

  const costRows = [
    { label: "STT — Securities Transaction Tax 0.10%", value: stt, color: "bg-crimson" },
    { label: "DP Charges — ₹13.50 + 18% GST on debit", value: dpCharges, color: "bg-amber-400" },
    { label: "Stamp Duty — 0.015% buy-side", value: stampDuty, color: "bg-pacificCyan" },
    { label: "NSE turnover + SEBI fee + IPFT", value: nseTurnoverFee + sebiFee + ipft, color: "bg-stormyTeal" },
    { label: "Exchange GST — 18% on exchange charges", value: exchangeGst, color: "bg-indigo-400" },
    { label: "Brokerage — zero-delivery rate card", value: brokerage, color: "bg-turquoise" },
  ];
  const maxCost = Math.max(...costRows.map((r) => r.value), 1);

  const copyQuickstart = async () => {
    const script = [
      "git clone https://github.com/aayushbankar/pramaan.git",
      "cd pramaan",
      'pip install -e ".[dev,api]"',
      "pytest tests/ -q",
      "python -m src.api.main",
      "cd frontend && npm run dev",
    ].join("\n");
    try {
      await navigator.clipboard.writeText(script);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    } catch {
      setCopied(false);
    }
  };

  return (
    <div className="min-h-screen bg-canvas text-inkText font-sans antialiased selection:bg-turquoise selection:text-canvas">
      <CustomCursor />

      <header
        className={`fixed top-0 inset-x-0 z-50 transition-transform duration-medium ease-out backdrop-blur-xl bg-canvas/80 border-b border-rule/70 ${
          navHidden ? "-translate-y-full" : "translate-y-0"
        }`}
      >
        <div className="max-w-[1240px] mx-auto px-5 sm:px-8 h-16 flex items-center justify-between">
          <Link href="/landing" className="flex items-center gap-3 group">
            <span className="w-8 h-8 rounded-md bg-gradient-signal flex items-center justify-center font-bold text-canvas text-base font-serif italic shadow-glow">
              प्र
            </span>
            <span className="flex flex-col leading-none">
              <span className="label-caps text-inkText group-hover:text-turquoise transition-colors duration-micro">
                Pramaan
              </span>
              <span className="text-[10px] font-mono text-tertiaryText mt-1 tracking-wide">
                GTU DI05000341
              </span>
            </span>
          </Link>

          <nav className="flex items-center gap-1 sm:gap-2 text-xs font-medium">
            <a href="#moats" className="hidden sm:inline px-3 py-2 rounded-md text-mutedText hover:text-inkText hover:bg-card transition-colors duration-micro">
              The 2 Moats
            </a>
            <a href="#calculator" className="hidden sm:inline px-3 py-2 rounded-md text-mutedText hover:text-inkText hover:bg-card transition-colors duration-micro">
              Cost Calculator
            </a>
            <a href="#quickstart" className="hidden md:inline px-3 py-2 rounded-md text-mutedText hover:text-inkText hover:bg-card transition-colors duration-micro">
              Quickstart
            </a>

            <button
              type="button"
              onClick={cycleTheme}
              className="ml-1 w-9 h-9 grid place-items-center rounded-md border border-rule text-mutedText hover:text-turquoise hover:border-turquoise/50 transition-all duration-micro"
              title={`Theme: ${THEME_LABELS[theme]} — click to cycle`}
              aria-label="Cycle color theme"
            >
              <ThemeIcon className="w-4 h-4" />
            </button>

            <Link
              href="/"
              className="ml-1 inline-flex items-center gap-1.5 px-4 py-2 rounded-full bg-turquoise text-canvas font-semibold hover:shadow-glow hover:-translate-y-0.5 transition-all duration-small"
            >
              <Terminal className="w-3.5 h-3.5" />
              Launch Terminal
            </Link>
          </nav>
        </div>
      </header>

      <section className="relative min-h-[100svh] flex flex-col justify-center pt-28 pb-16 overflow-hidden">
        <div className="absolute inset-0 grid-instrument pointer-events-none opacity-70" aria-hidden="true" />
        <div
          className="absolute top-[-18%] left-1/2 -translate-x-1/2 w-[min(760px,90vw)] aspect-square rounded-full bg-gradient-to-tr from-pacificCyan/25 via-turquoise/20 to-crimson/10 blur-[130px] animate-glowPulse pointer-events-none"
          aria-hidden="true"
        />

        <div className="relative max-w-[1240px] mx-auto w-full px-5 sm:px-8">
          <div className="line-mask" style={{ "--line-delay": "60ms" } as React.CSSProperties}>
            <span>
              <span className="inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full border border-rule bg-card/70 backdrop-blur text-turquoise text-xs font-mono mb-8">
                <ShieldAlert className="w-3.5 h-3.5 text-crimson" />
                Zero-Lookahead T+1 Execution · Paisa-Exact Indian Friction
              </span>
            </span>
          </div>

          <h1 className="t-display max-w-[16ch]">
            <span className="line-mask" style={{ "--line-delay": "160ms" } as React.CSSProperties}>
              <span>Prove your edge</span>
            </span>
            <span className="line-mask" style={{ "--line-delay": "300ms" } as React.CSSProperties}>
              <span>
                before you deploy{" "}
                <em className="serif-accent text-turquoise">a rupee.</em>
              </span>
            </span>
          </h1>

          <Reveal delay={520} className="mt-8 max-w-[62ch]">
            <p className="t-lead">
              The honest backtesting engine for Indian (NSE) equities. It eliminates the two fatal
              illusions that destroy algorithmic capital: unmodeled statutory tax drag and
              statistical overfitting.
            </p>
          </Reveal>

          <Reveal delay={620} className="mt-10 flex flex-wrap items-center gap-4">
            <Link href="/" className="btn-primary">
              Run Live Backtest
              <ArrowRight className="w-4 h-4" />
            </Link>
            <a
              href="https://github.com/aayushbankar/pramaan"
              target="_blank"
              rel="noopener noreferrer"
              className="btn-ghost font-mono text-xs"
            >
              <Terminal className="w-4 h-4 text-turquoise" />
              GitHub Repository
            </a>
          </Reveal>

          <Reveal delay={740} className="mt-14 max-w-3xl p-4 sm:p-5 rounded-2xl border border-rule bg-card/60 backdrop-blur flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div className="flex items-center gap-3.5">
              <span className="w-10 h-10 rounded-lg bg-crimson/15 border border-crimson/40 grid place-items-center shrink-0">
                <TrendingDown className="w-5 h-5 text-crimson" />
              </span>
              <div>
                <div className="text-xs font-mono font-semibold text-inkText">
                  Empirical Finding: 0 of 4 active models beat passive buy-and-hold
                </div>
                <p className="text-[11px] text-mutedText mt-1 leading-relaxed">
                  NIFTY-50 (2019–2024, 14,800 bars). Gross alpha vanishes after STT, DP charges,
                  and GST are accounted for.
                </p>
              </div>
            </div>
            <span className="shrink-0 px-2.5 py-1 rounded-md text-[11px] font-mono bg-canvas text-turquoise border border-rule">
              NFR-1 Deterministic
            </span>
          </Reveal>
        </div>

        <div className="relative max-w-[1240px] mx-auto w-full px-5 sm:px-8 mt-14">
          <Reveal delay={840} className="grid grid-cols-2 lg:grid-cols-4 gap-px bg-rule/60 border border-rule rounded-xl overflow-hidden">
            {HERO_STATS.map((stat) => (
              <div key={stat.label} className="bg-panel px-5 py-5 sm:px-6 sm:py-6">
                <div className={`num text-2xl sm:text-3xl font-semibold ${stat.tone}`}>
                  {stat.value}
                </div>
                <div className="eyebrow mt-2">{stat.label}</div>
              </div>
            ))}
          </Reveal>
        </div>
      </section>

      <div className="border-y border-rule bg-panel/70 overflow-hidden py-3" aria-hidden="true">
        <div className="marquee-track flex w-max gap-10 whitespace-nowrap">
          {[...TICKER_ITEMS, ...TICKER_ITEMS].map((item, i) => (
            <span key={i} className="flex items-center gap-10 font-mono text-[11px] tracking-wide text-tertiaryText">
              <span className="w-1.5 h-1.5 rounded-full bg-turquoise/70 inline-block" />
              {item}
            </span>
          ))}
        </div>
      </div>

      <section id="moats" className="py-[var(--space-section)] px-5 sm:px-8">
        <div className="max-w-[1240px] mx-auto">
          <Reveal className="max-w-3xl">
            <span className="eyebrow text-turquoise">Institutional Moats</span>
            <h2 className="t-h1 mt-4">
              Why other backtesters <span className="serif-accent text-turquoise">lie</span> to you
            </h2>
            <p className="t-lead mt-5 max-w-[64ch]">
              Generic international libraries assume zero friction and evaluate in-sample models
              that fail the moment real capital touches an exchange.
            </p>
          </Reveal>

          <Reveal delay={120} className="mt-14 grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
            <div className="lg:col-span-5 surface p-7 sm:p-8 flex flex-col justify-between bg-card">
              <div>
                <div className="w-12 h-12 rounded-lg bg-crimson/15 border border-crimson/35 grid place-items-center text-crimson">
                  <Scale className="w-6 h-6" />
                </div>
                <span className="eyebrow text-crimson block mt-6">Moat 01 · Statutory Microstructure</span>
                <h3 className="t-h3 mt-3">The full Indian delivery cost stack</h3>
                <p className="t-body text-mutedText mt-4 leading-relaxed">
                  Most platforms model a flat 0.05% brokerage. Pramaan applies the{" "}
                  <strong className="text-inkText">actual legal statutory tariff</strong> per SEBI
                  circulars down to exact paise.
                </p>
              </div>
              <div className="mt-8 pt-5 hairline font-mono text-xs text-turquoise">
                Result: 48.2% of momentum alpha destroyed by statutory friction alone.
              </div>
            </div>

            <div className="lg:col-span-7 surface p-7 sm:p-8 bg-panel">
              <div className="eyebrow mb-5">Rate card · Zerodha Oct 2024 True-to-Label</div>
              <ul className="space-y-0">
                {MOAT_1_LINES.map((line) => (
                  <li
                    key={line.text}
                    className="flex items-center gap-3.5 py-3.5 border-b border-rule/70 last:border-0 font-mono text-[13px] text-mutedText"
                  >
                    <span className={`w-1.5 h-1.5 rounded-full shrink-0 ${line.dot}`} />
                    <span>{line.text}</span>
                  </li>
                ))}
              </ul>
            </div>
          </Reveal>

          <Reveal delay={120} className="mt-6 grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
            <div className="lg:col-span-7 surface p-7 sm:p-8 bg-panel order-2 lg:order-1">
              <div className="eyebrow mb-5">López de Prado diagnostic stack</div>
              <ul className="space-y-0">
                {MOAT_2_LINES.map((line) => (
                  <li
                    key={line.n}
                    className="flex items-start gap-4 py-3.5 border-b border-rule/70 last:border-0 text-[13px] text-mutedText"
                  >
                    <span className="num text-turquoise text-xs pt-0.5">{line.n}</span>
                    <span>{line.text}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="lg:col-span-5 surface p-7 sm:p-8 bg-card flex flex-col justify-between order-1 lg:order-2">
              <div>
                <div className="w-12 h-12 rounded-lg bg-turquoise/15 border border-turquoise/35 grid place-items-center text-turquoise">
                  <Sparkles className="w-6 h-6" />
                </div>
                <span className="eyebrow text-turquoise block mt-6">Moat 02 · Statistical Guardrails</span>
                <h3 className="t-h3 mt-3">Backtest overfitting, measured</h3>
                <p className="t-body text-mutedText mt-4 leading-relaxed">
                  Overfitting is selection bias masquerading as skill. Pramaan reports the
                  probability that your in-sample winner was luck.
                </p>
              </div>
              <div className="mt-8 pt-5 hairline flex items-end justify-between">
                <span className="font-mono text-xs text-turquoise max-w-[18ch]">
                  Defends your capital from statistical self-deception.
                </span>
                <span className="num text-3xl font-semibold text-inkText">60.0%</span>
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      <section id="calculator" className="py-[var(--space-section)] px-5 sm:px-8 bg-panel border-y border-rule">
        <div className="max-w-[1240px] mx-auto">
          <Reveal className="max-w-3xl">
            <span className="eyebrow text-turquoise">Interactive Tollgate Simulator</span>
            <h2 className="t-h1 mt-4">
              Calculate your real <span className="serif-accent text-crimson">statutory drag</span>
            </h2>
            <p className="t-lead mt-5 max-w-[64ch]">
              See how much edge Indian taxes and exchange charges extract from your portfolio
              before your strategy generates a single rupee of net profit.
            </p>
          </Reveal>

          <Reveal delay={120} className="mt-12 grid grid-cols-1 lg:grid-cols-12 gap-6">
            <div className="lg:col-span-5 surface bg-card p-6 sm:p-7 space-y-7">
              <div>
                <div className="flex justify-between items-baseline mb-3">
                  <span className="eyebrow">Trading Capital</span>
                  <span className="num text-lg font-semibold text-inkText">
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
                  className="w-full accent-turquoise h-1.5 cursor-pointer"
                  aria-label="Trading capital"
                />
                <div className="flex justify-between text-[10px] font-mono text-tertiaryText mt-2">
                  <span>₹50K</span>
                  <span>₹10L</span>
                  <span>₹20L</span>
                </div>
              </div>

              <div>
                <div className="flex justify-between items-baseline mb-3">
                  <span className="eyebrow">Annual Portfolio Turnover</span>
                  <span className="num text-lg font-semibold text-inkText">{calcTurnover}x / year</span>
                </div>
                <input
                  type="range"
                  min={1}
                  max={20}
                  step={1}
                  value={calcTurnover}
                  onChange={(e) => setCalcTurnover(Number(e.target.value))}
                  className="w-full accent-turquoise h-1.5 cursor-pointer"
                  aria-label="Annual portfolio turnover"
                />
                <div className="flex justify-between text-[10px] font-mono text-tertiaryText mt-2">
                  <span>1x Passive</span>
                  <span>10x Swing</span>
                  <span>20x Frequent</span>
                </div>
              </div>

              <div className="rounded-lg bg-canvas border border-rule p-4 font-mono text-[11px] text-mutedText space-y-2.5">
                <div className="flex justify-between">
                  <span>Annual trading volume</span>
                  <span className="text-inkText font-semibold">₹{annualVolume.toLocaleString("en-IN")}</span>
                </div>
                <div className="flex justify-between">
                  <span>Est. completed trades</span>
                  <span className="text-inkText font-semibold">{tradesPerYear} executions</span>
                </div>
                <div className="flex justify-between">
                  <span>Rate card applied</span>
                  <span className="text-turquoise font-semibold">Zerodha Oct 2024</span>
                </div>
              </div>
            </div>

            <div className="lg:col-span-7 surface bg-canvas p-6 sm:p-7">
              <div className="flex flex-wrap items-end justify-between gap-4 pb-5 mb-5 border-b border-rule">
                <div>
                  <span className="eyebrow">Total annual statutory drag</span>
                  <div className="num text-3xl sm:text-4xl font-semibold text-crimson mt-1.5">
                    -₹{totalFriction.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
                  </div>
                </div>
                <div className="text-right">
                  <span className="eyebrow">Drag as % of capital</span>
                  <div className="num text-3xl sm:text-4xl font-semibold text-crimson mt-1.5">
                    {frictionDragPct.toFixed(2)}%
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                {costRows.map((row) => (
                  <div key={row.label}>
                    <div className="flex justify-between items-baseline font-mono text-[11px] mb-1.5">
                      <span className="text-mutedText">{row.label}</span>
                      <span className="text-inkText font-semibold">
                        ₹{row.value.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
                      </span>
                    </div>
                    <div className="h-1.5 rounded-full bg-rule/60 overflow-hidden">
                      <div
                        className={`h-full rounded-full ${row.color} transition-[width] duration-medium ease-out`}
                        style={{ width: `${Math.max((row.value / maxCost) * 100, 0.6)}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>

              <p className="mt-6 text-[11px] text-mutedText leading-relaxed">
                Notice: even with ₹0 brokerage, taxes and depository fees consume{" "}
                <span className="text-crimson font-semibold">{frictionDragPct.toFixed(2)}%</span>{" "}
                of your capital every year at {calcTurnover}x turnover.
              </p>
            </div>
          </Reveal>
        </div>
      </section>

      <section id="quickstart" className="py-[var(--space-section)] px-5 sm:px-8">
        <div className="max-w-[1240px] mx-auto grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-14 items-start">
          <Reveal className="lg:col-span-5">
            <span className="eyebrow text-turquoise">100% offline &amp; clean-clone reproducible</span>
            <h2 className="t-h1 mt-4">
              Reproduce every metric <span className="serif-accent text-turquoise">locally</span>
            </h2>
            <p className="t-lead mt-5">
              Pramaan does not hide behind cloud endpoints. The complete engine, CLI, test suite,
              and synthetic fixtures run offline on your machine.
            </p>

            <ol className="mt-9 space-y-0">
              {QUICKSTART_STEPS.map((step) => (
                <li key={step.n} className="flex gap-4 py-4 border-b border-rule/70 last:border-0">
                  <span className="num text-xs text-tertiaryText pt-1">{step.n}</span>
                  <div className="min-w-0">
                    <div className="text-sm font-semibold text-inkText">{step.title}</div>
                    <code className="block mt-1.5 font-mono text-[11px] text-turquoise break-all">
                      {step.cmd}
                    </code>
                  </div>
                </li>
              ))}
            </ol>
          </Reveal>

          <Reveal delay={140} className="lg:col-span-7">
            <div className="surface bg-canvas overflow-hidden shadow-card">
              <div className="flex items-center justify-between px-4 py-3 border-b border-rule bg-panel">
                <div className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-red-500/80" />
                  <span className="w-2.5 h-2.5 rounded-full bg-yellow-500/80" />
                  <span className="w-2.5 h-2.5 rounded-full bg-emerald-500/80" />
                  <span className="text-[11px] ml-2 text-mutedText font-medium">bash — pramaan</span>
                </div>
                <button
                  type="button"
                  onClick={copyQuickstart}
                  className="flex items-center gap-1.5 text-[11px] font-mono text-tertiaryText hover:text-turquoise transition-colors duration-micro"
                  title="Copy quickstart commands"
                >
                  {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                  {copied ? "Copied" : "Copy"}
                </button>
              </div>

              <pre className="p-5 sm:p-6 font-mono text-[12px] leading-[1.9] overflow-x-auto text-inkText">
                <span className="text-tertiaryText"># 1. Clone the open-source repository</span>{"\n"}
                <span>git clone https://github.com/aayushbankar/pramaan.git</span>{"\n"}
                <span>cd pramaan</span>{"\n\n"}
                <span className="text-tertiaryText"># 2. Install dependencies in editable mode</span>{"\n"}
                <span>pip install -e &quot;.[dev,api]&quot;</span>{"\n\n"}
                <span className="text-tertiaryText"># 3. Verify the complete 72-test suite offline</span>{"\n"}
                <span className="text-turquoise">pytest tests/ -q</span>{"\n"}
                <span className="text-emerald-400"># Output: 72 passed in ~7s</span>{"\n\n"}
                <span className="text-tertiaryText"># 4. Start the honest backtest engine API</span>{"\n"}
                <span>python -m src.api.main</span>{"\n\n"}
                <span className="text-tertiaryText"># 5. Launch the desktop terminal UI</span>{"\n"}
                <span>cd frontend &amp;&amp; npm run dev</span>
              </pre>
            </div>
          </Reveal>
        </div>
      </section>

      <section className="relative py-[var(--space-section)] px-5 sm:px-8 overflow-hidden border-t border-rule">
        <div
          className="absolute inset-x-0 bottom-[-40%] h-[420px] bg-gradient-to-t from-turquoise/12 to-transparent pointer-events-none"
          aria-hidden="true"
        />
        <Reveal className="relative max-w-[1240px] mx-auto text-center">
          <span className="eyebrow">Stop trusting your own backtest</span>
          <h2 className="t-h1 mt-5 max-w-[18ch] mx-auto">
            Prove it before you <span className="serif-accent text-turquoise">risk</span> it
          </h2>
          <div className="mt-9 flex flex-wrap items-center justify-center gap-4">
            <Link href="/" className="btn-primary">
              Open the terminal
              <ArrowRight className="w-4 h-4" />
            </Link>
            <a
              href="https://github.com/aayushbankar/pramaan"
              target="_blank"
              rel="noopener noreferrer"
              className="btn-ghost font-mono text-xs"
            >
              Star on GitHub
            </a>
          </div>
        </Reveal>
      </section>

      <footer className="py-12 px-5 sm:px-8 border-t border-rule bg-panel">
        <div className="max-w-[1240px] mx-auto flex flex-col md:flex-row items-start md:items-center justify-between gap-6 text-xs font-mono text-mutedText">
          <div>
            <div className="flex items-center gap-2 text-inkText font-semibold">
              <span>PRAMAAN (प्रमाण)</span>
              <span className="text-tertiaryText">·</span>
              <span className="text-mutedText font-normal">GTU DI05000341 Minor Project</span>
            </div>
            <p className="mt-1.5 text-[11px]">
              Authors: Aayush Avinash Bankar &amp; Meet Jayeshbhai Patel
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-5">
            <Link href="/" className="hover:text-turquoise transition-colors duration-micro">
              Trading Terminal
            </Link>
            <a
              href="https://github.com/aayushbankar/pramaan"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-turquoise transition-colors duration-micro"
            >
              GitHub
            </a>
            <span className="text-tertiaryText">|</span>
            <span className="text-tertiaryText">No Live Trading · Simulation &amp; Audit Only</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
