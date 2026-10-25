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
  Download,
  PackageCheck,
  Cpu,
  Layers,
  FileSpreadsheet,
  ExternalLink,
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

const GITHUB_REPO = "https://github.com/Aayushbankar/Quantlab";
const GITHUB_RELEASE = `${GITHUB_REPO}/releases/tag/v1.0.0`;
const DOWNLOAD_DEB = `${GITHUB_REPO}/releases/download/v1.0.0/pramaan-desktop_1.0.0_amd64.deb`;
const DOWNLOAD_TAR = `${GITHUB_REPO}/releases/download/v1.0.0/pramaan-desktop-linux-x86_64.tar.gz`;
const DOWNLOAD_PPTX = `${GITHUB_REPO}/releases/download/v1.0.0/Pramaan_Presentation.pptx`;

const TICKER_ITEMS = [
  "0 of 4 active models beat passive buy-and-hold (2019–2024)",
  "₹5,064 statutory friction on ₹1,00,000 — 5.06% annual drag",
  "14,800 NIFTY-50 bars — zero look-ahead — T+1 fills",
  "PBO 60.0% [44.4%, 73.3%] across 133 configurations",
  "DSR p = 0.524 — no deflated Sharpe significance",
  "STT 0.10% · Stamp 0.015% · DP ₹13.50 · GST 18%",
];

const HERO_STATS = [
  { value: "0 / 4", label: "Active Models Beating B&H", tone: "text-crimson" },
  { value: "5.06%", label: "Annual Friction Drag", tone: "text-crimson" },
  { value: "14,800", label: "NSE Daily Bars Verified", tone: "text-inkText" },
  { value: "60.0%", label: "Probability of Backtest Overfitting", tone: "text-turquoise" },
];

const MOAT_1_LINES = [
  { dot: "bg-crimson", text: "Securities Transaction Tax (STT): 0.10% delivery on both buy & sell legs" },
  { dot: "bg-amber-400", text: "Depository Charges: flat ₹13.50 + 18% GST per debit transaction" },
  { dot: "bg-pacificCyan", text: "Stamp Duty: 0.015% buy-side statutory charge (Indian Stamp Act)" },
  { dot: "bg-turquoise", text: "NSE & SEBI Charges: 0.00297% turnover fee + ₹10/crore SEBI fee + IPFT" },
  { dot: "bg-indigo-400", text: "Almgren–Chriss Impact: square-root non-linear slippage on ADV" },
];

const MOAT_2_LINES = [
  { n: "01", text: "Deflated Sharpe Ratio (DSR): Penalizes selection bias and trial count N across parameter sweeps." },
  { n: "02", text: "Combinatorial Purged CV (CPCV): 45 overlapping test paths with non-zero purge and embargo intervals." },
  { n: "03", text: "Probability of Backtest Overfitting (PBO): Measures how frequently in-sample winners underperform OOS." },
  { n: "04", text: "Empirical Ground Truth: 133 configurations evaluated on NIFTY-50 — empirical PBO reaches 60.0%." },
];

const QUICKSTART_STEPS = [
  { n: "01", title: "Clone the official repository", cmd: `git clone ${GITHUB_REPO}.git` },
  { n: "02", title: "Install in editable mode with dependencies", cmd: 'pip install -e ".[dev,api]"' },
  { n: "03", title: "Verify the test suite offline (72 tests)", cmd: "pytest tests/ -q" },
  { n: "04", title: "Launch engine API + web interface", cmd: "python -m src.api.main" },
];

export default function LandingPage() {
  const [calcCapital, setCalcCapital] = useState(200000);
  const [calcTurnover, setCalcTurnover] = useState(6);
  const [theme, setTheme] = useState<ThemeName>("abyss");
  const [navHidden, setNavHidden] = useState(false);
  const [copied, setCopied] = useState(false);
  const [copiedDebCmd, setCopiedDebCmd] = useState(false);
  const [terminalUrl, setTerminalUrl] = useState("/");
  const lastY = useRef(0);

  useEffect(() => {
    const saved = loadTheme();
    setTheme(saved);
    document.documentElement.setAttribute("data-theme", saved);

    if (typeof window !== "undefined" && window.location.pathname.includes("/Quantlab")) {
      setTerminalUrl("/Quantlab/app.html");
    }
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
    { label: "Securities Transaction Tax (STT) — 0.10% delivery", value: stt, color: "bg-crimson", authority: "Govt of India" },
    { label: "DP Charges — ₹13.50 + 18% GST per debit", value: dpCharges, color: "bg-amber-400", authority: "Depository (CDSL/NSDL)" },
    { label: "Stamp Duty — 0.015% buy-side statutory stamp", value: stampDuty, color: "bg-pacificCyan", authority: "Indian Stamp Act" },
    { label: "NSE Turnover Charges + SEBI Fee + IPFT", value: nseTurnoverFee + sebiFee + ipft, color: "bg-stormyTeal", authority: "Exchange & Regulator" },
    { label: "Exchange GST — 18% on statutory turnover charges", value: exchangeGst, color: "bg-indigo-400", authority: "CBIC" },
    { label: "Brokerage — Zero delivery standard rate card", value: brokerage, color: "bg-turquoise", authority: "Discount Broker" },
  ];
  const maxCost = Math.max(...costRows.map((r) => r.value), 1);

  const copyQuickstart = async () => {
    const script = [
      `git clone ${GITHUB_REPO}.git`,
      "cd Quantlab",
      'pip install -e ".[dev,api]"',
      "pytest tests/ -q",
      "python -m src.api.main",
    ].join("\n");
    try {
      await navigator.clipboard.writeText(script);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    } catch {
      setCopied(false);
    }
  };

  const copyDebCommand = async () => {
    const script = `curl -LO ${DOWNLOAD_DEB} && sudo dpkg -i pramaan-desktop_1.0.0_amd64.deb`;
    try {
      await navigator.clipboard.writeText(script);
      setCopiedDebCmd(true);
      setTimeout(() => setCopiedDebCmd(false), 1800);
    } catch {
      setCopiedDebCmd(false);
    }
  };

  return (
    <div className="min-h-screen bg-canvas text-inkText font-sans antialiased selection:bg-turquoise selection:text-canvas">
      <CustomCursor />

      {/* Top Navbar */}
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
              Cost Tollgate
            </a>
            <a href="#desktop" className="hidden md:inline px-3 py-2 rounded-md text-mutedText hover:text-inkText hover:bg-card transition-colors duration-micro">
              Desktop App (.deb)
            </a>
            <a href="#quickstart" className="hidden lg:inline px-3 py-2 rounded-md text-mutedText hover:text-inkText hover:bg-card transition-colors duration-micro">
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

            <a
              href={terminalUrl}
              className="ml-1 inline-flex items-center gap-1.5 px-4 py-2 rounded-full bg-turquoise text-canvas font-semibold hover:shadow-glow hover:-translate-y-0.5 transition-all duration-small"
            >
              <Terminal className="w-3.5 h-3.5" />
              Launch Terminal
            </a>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative min-h-[92svh] flex flex-col justify-center pt-28 pb-16 overflow-hidden">
        <div className="absolute inset-0 grid-instrument pointer-events-none opacity-50" aria-hidden="true" />

        <div className="relative max-w-[1240px] mx-auto w-full px-5 sm:px-8">
          <div className="line-mask" style={{ "--line-delay": "60ms" } as React.CSSProperties}>
            <span>
              <span className="inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full border border-rule bg-card/70 backdrop-blur text-turquoise text-xs font-mono mb-8">
                <ShieldAlert className="w-3.5 h-3.5 text-crimson" />
                Zero-Lookahead T+1 Execution · Statutory Indian Friction Stack
              </span>
            </span>
          </div>

          <h1 className="t-display max-w-[18ch]">
            <span className="line-mask" style={{ "--line-delay": "160ms" } as React.CSSProperties}>
              <span>Prove your edge</span>
            </span>
            <span className="line-mask" style={{ "--line-delay": "300ms" } as React.CSSProperties}>
              <span>before you deploy a rupee.</span>
            </span>
          </h1>

          <Reveal delay={520} className="mt-8 max-w-[66ch]">
            <p className="t-lead">
              The honest backtesting engine for Indian (NSE) equities. Eliminates the structural
              deceptions that destroy real trading capital: unmodeled statutory taxes (STT, Stamp Duty, GST)
              and selection-biased overfitting.
            </p>
          </Reveal>

          <Reveal delay={620} className="mt-10 flex flex-wrap items-center gap-4">
            <a href={terminalUrl} className="btn-primary">
              Launch Interactive Terminal
              <ArrowRight className="w-4 h-4" />
            </a>
            <a
              href="#desktop"
              className="btn-ghost font-mono text-xs flex items-center gap-2"
            >
              <Download className="w-4 h-4 text-turquoise" />
              Download Desktop App (.deb)
            </a>
            <a
              href={GITHUB_REPO}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-ghost font-mono text-xs flex items-center gap-2"
            >
              <Terminal className="w-4 h-4 text-turquoise" />
              GitHub Repository
              <ExternalLink className="w-3 h-3 text-tertiaryText" />
            </a>
          </Reveal>

          {/* Key Finding Banner */}
          <Reveal delay={740} className="mt-14 max-w-3xl p-4 sm:p-5 rounded-xl border border-rule bg-card/80 backdrop-blur flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div className="flex items-center gap-3.5">
              <span className="w-10 h-10 rounded-lg bg-crimson/15 border border-crimson/40 grid place-items-center shrink-0">
                <TrendingDown className="w-5 h-5 text-crimson" />
              </span>
              <div>
                <div className="text-xs font-mono font-semibold text-inkText">
                  Empirical Ground Truth: 0 of 4 active strategies beat passive buy-and-hold
                </div>
                <p className="text-[11px] text-mutedText mt-1 leading-relaxed">
                  Evaluated on 10 NIFTY-50 symbols over 2019–2024 (14,800 bars). Gross alpha vanishes
                  completely once legal STT, exchange turnover, and depository charges are deducted.
                </p>
              </div>
            </div>
            <span className="shrink-0 px-2.5 py-1 rounded-md text-[11px] font-mono bg-canvas text-turquoise border border-rule">
              NFR-1 Deterministic
            </span>
          </Reveal>
        </div>

        {/* Hero Metric Grid */}
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

      {/* Marquee ticker */}
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

      {/* Moats Section */}
      <section id="moats" className="py-[var(--space-section)] px-5 sm:px-8">
        <div className="max-w-[1240px] mx-auto">
          <Reveal className="max-w-3xl">
            <span className="eyebrow text-turquoise">Institutional Moats</span>
            <h2 className="t-h1 mt-4">
              Why traditional retail backtests fail live
            </h2>
            <p className="t-lead mt-5 max-w-[64ch]">
              Standard backtesting packages assume frictionless fills and report overfitted in-sample
              returns that dissolve the moment orders hit the National Stock Exchange.
            </p>
          </Reveal>

          {/* Moat 1: Cost Stack */}
          <Reveal delay={120} className="mt-14 grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
            <div className="lg:col-span-5 surface p-7 sm:p-8 flex flex-col justify-between bg-card">
              <div>
                <div className="w-12 h-12 rounded-lg bg-crimson/15 border border-crimson/35 grid place-items-center text-crimson">
                  <Scale className="w-6 h-6" />
                </div>
                <span className="eyebrow text-crimson block mt-6">Moat 01 · Statutory Indian Microstructure</span>
                <h3 className="t-h3 mt-3">The legal Indian delivery cost stack</h3>
                <p className="t-body text-mutedText mt-4 leading-relaxed">
                  While generic software applies a flat 0.05% brokerage, Pramaan implements the exact
                  statutory tariff prescribed by SEBI and the Indian Stamp Act down to individual paise.
                </p>
              </div>
              <div className="mt-8 pt-5 hairline font-mono text-xs text-turquoise">
                Empirical Finding: 48.2% of momentum strategy alpha is consumed by statutory friction alone.
              </div>
            </div>

            <div className="lg:col-span-7 surface p-7 sm:p-8 bg-panel">
              <div className="eyebrow mb-5">Statutory Rate Card · Zerodha Delivery Standard</div>
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

          {/* Moat 2: Overfitting */}
          <Reveal delay={120} className="mt-6 grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
            <div className="lg:col-span-7 surface p-7 sm:p-8 bg-panel order-2 lg:order-1">
              <div className="eyebrow mb-5">Marcos López de Prado Diagnostic Suite</div>
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
                <h3 className="t-h3 mt-3">Quantifying selection bias &amp; overfitting</h3>
                <p className="t-body text-mutedText mt-4 leading-relaxed">
                  Testing multiple parameter sets inevitably yields false discoveries. Pramaan computes the
                  Probability of Backtest Overfitting (PBO) to determine whether edge is real or accidental.
                </p>
              </div>
              <div className="mt-8 pt-5 hairline flex items-end justify-between">
                <span className="font-mono text-xs text-turquoise max-w-[20ch]">
                  Evaluated across 133 combinatorial parameter configs.
                </span>
                <span className="num text-3xl font-semibold text-inkText">60.0% PBO</span>
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      {/* Interactive Tollgate Simulator */}
      <section id="calculator" className="py-[var(--space-section)] px-5 sm:px-8 bg-panel border-y border-rule">
        <div className="max-w-[1240px] mx-auto">
          <Reveal className="max-w-3xl">
            <span className="eyebrow text-turquoise">Interactive Tollgate Simulator</span>
            <h2 className="t-h1 mt-4">
              Calculate your statutory drag before trading
            </h2>
            <p className="t-lead mt-5 max-w-[64ch]">
              Quantify how much alpha Indian statutory taxes, depository fees, and turnover charges
              strip away from your equity curve before you generate a single rupee of net profit.
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
                  <span>1x (Positional)</span>
                  <span>6x (Swing)</span>
                  <span>20x (Frequent)</span>
                </div>
              </div>

              <div className="rounded-lg bg-canvas border border-rule p-4 font-mono text-[11px] text-mutedText space-y-2.5">
                <div className="flex justify-between">
                  <span>Annual Trading Volume</span>
                  <span className="text-inkText font-semibold">₹{annualVolume.toLocaleString("en-IN")}</span>
                </div>
                <div className="flex justify-between">
                  <span>Estimated Executions</span>
                  <span className="text-inkText font-semibold">{tradesPerYear} round-trips</span>
                </div>
                <div className="flex justify-between">
                  <span>Statutory Standard Applied</span>
                  <span className="text-turquoise font-semibold">NSE Delivery Oct 2024</span>
                </div>
              </div>
            </div>

            <div className="lg:col-span-7 surface bg-canvas p-6 sm:p-7">
              <div className="flex flex-wrap items-end justify-between gap-4 pb-5 mb-5 border-b border-rule">
                <div>
                  <span className="eyebrow">Total Annual Statutory Friction</span>
                  <div className="num text-3xl sm:text-4xl font-semibold text-crimson mt-1.5">
                    -₹{totalFriction.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
                  </div>
                </div>
                <div className="text-right">
                  <span className="eyebrow">Friction as % of Capital</span>
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
                Notice: Even with zero brokerage, statutory Indian taxes and depository fees extract{" "}
                <span className="text-crimson font-semibold">{frictionDragPct.toFixed(2)}%</span>{" "}
                of your portfolio equity annually at {calcTurnover}x turnover.
              </p>
            </div>
          </Reveal>
        </div>
      </section>

      {/* Desktop App & Debian Package Section */}
      <section id="desktop" className="py-[var(--space-section)] px-5 sm:px-8">
        <div className="max-w-[1240px] mx-auto">
          <Reveal className="max-w-3xl">
            <span className="eyebrow text-turquoise">Native Linux Distribution</span>
            <h2 className="t-h1 mt-4">
              Packaged desktop application with embedded backend
            </h2>
            <p className="t-lead mt-5 max-w-[64ch]">
              Run Pramaan completely locally as a compiled desktop binary. The desktop app
              automatically monitors and auto-spawns the local FastAPI simulation engine on launch,
              requiring zero manual server orchestration.
            </p>
          </Reveal>

          <Reveal delay={120} className="mt-12 grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
            {/* Left Card: Features */}
            <div className="lg:col-span-5 surface bg-card p-6 sm:p-7 flex flex-col justify-between">
              <div>
                <div className="w-12 h-12 rounded-lg bg-turquoise/15 border border-turquoise/35 grid place-items-center text-turquoise">
                  <Cpu className="w-6 h-6" />
                </div>
                <h3 className="t-h3 mt-6">Embedded Lifecycle Management</h3>
                <div className="mt-4 space-y-3 text-xs text-mutedText leading-relaxed">
                  <div className="flex items-start gap-2.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-turquoise mt-1.5 shrink-0" />
                    <span><strong>Auto-Spawn Architecture:</strong> Rust Tauri runtime probes <code>127.0.0.1:8000</code>; if absent, spawns <code>python3 -m src.api.main</code>.</span>
                  </div>
                  <div className="flex items-start gap-2.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-turquoise mt-1.5 shrink-0" />
                    <span><strong>Clean Process Teardown:</strong> Backend child process terminates synchronously upon desktop window exit.</span>
                  </div>
                  <div className="flex items-start gap-2.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-turquoise mt-1.5 shrink-0" />
                    <span><strong>Zero Network Dependency:</strong> Runs completely offline using committed NIFTY-50 Parquet &amp; SQLite cache.</span>
                  </div>
                </div>
              </div>

              <div className="mt-8 pt-5 hairline">
                <a
                  href={GITHUB_RELEASE}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="font-mono text-xs text-turquoise hover:underline inline-flex items-center gap-1.5"
                >
                  View GitHub Release v1.0.0
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              </div>
            </div>

            {/* Right Card: Downloads & Commands */}
            <div className="lg:col-span-7 surface bg-panel p-6 sm:p-7 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-5">
                  <span className="eyebrow">Official Binaries (x86_64)</span>
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-500/15 text-emerald-400 border border-emerald-500/40">
                    Release v1.0.0
                  </span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {/* Debian Package Card */}
                  <a
                    href={DOWNLOAD_DEB}
                    className="p-4 rounded-xl border border-rule bg-canvas hover:border-turquoise/50 hover:shadow-glow transition-all group flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex items-center justify-between">
                        <PackageCheck className="w-5 h-5 text-turquoise" />
                        <span className="text-[10px] font-mono text-tertiaryText">2.4 MB</span>
                      </div>
                      <div className="font-semibold text-sm mt-3 text-inkText group-hover:text-turquoise transition-colors">
                        Debian Package (.deb)
                      </div>
                      <p className="text-[11px] text-mutedText mt-1">
                        For Ubuntu, Debian, Linux Mint, and derivatives.
                      </p>
                    </div>
                    <div className="mt-4 font-mono text-xs text-turquoise flex items-center gap-1">
                      Download .deb <Download className="w-3.5 h-3.5" />
                    </div>
                  </a>

                  {/* Tarball Card */}
                  <a
                    href={DOWNLOAD_TAR}
                    className="p-4 rounded-xl border border-rule bg-canvas hover:border-turquoise/50 hover:shadow-glow transition-all group flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex items-center justify-between">
                        <Layers className="w-5 h-5 text-pacificCyan" />
                        <span className="text-[10px] font-mono text-tertiaryText">2.4 MB</span>
                      </div>
                      <div className="font-semibold text-sm mt-3 text-inkText group-hover:text-turquoise transition-colors">
                        Standalone Tarball (.tar.gz)
                      </div>
                      <p className="text-[11px] text-mutedText mt-1">
                        Pre-compiled binary for any generic Linux x86_64 system.
                      </p>
                    </div>
                    <div className="mt-4 font-mono text-xs text-turquoise flex items-center gap-1">
                      Download .tar.gz <Download className="w-3.5 h-3.5" />
                    </div>
                  </a>
                </div>

                {/* Quick install snippet */}
                <div className="mt-6 rounded-lg bg-canvas border border-rule p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-[11px] font-mono text-tertiaryText">Terminal Installation:</span>
                    <button
                      type="button"
                      onClick={copyDebCommand}
                      className="text-[10px] font-mono text-tertiaryText hover:text-turquoise transition-colors inline-flex items-center gap-1"
                    >
                      {copiedDebCmd ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                      {copiedDebCmd ? "Copied" : "Copy"}
                    </button>
                  </div>
                  <code className="font-mono text-xs text-turquoise break-all block">
                    curl -LO {DOWNLOAD_DEB} &amp;&amp; sudo dpkg -i pramaan-desktop_1.0.0_amd64.deb
                  </code>
                </div>
              </div>

              <div className="mt-6 pt-4 border-t border-rule flex flex-wrap items-center justify-between gap-3 text-xs font-mono text-mutedText">
                <span>SHA-256 verified build</span>
                <a
                  href={DOWNLOAD_PPTX}
                  className="hover:text-turquoise transition-colors inline-flex items-center gap-1.5"
                >
                  <FileSpreadsheet className="w-3.5 h-3.5" />
                  Presentation Deck (.pptx)
                </a>
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      {/* Quickstart Section */}
      <section id="quickstart" className="py-[var(--space-section)] px-5 sm:px-8 bg-panel border-t border-rule">
        <div className="max-w-[1240px] mx-auto grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-14 items-start">
          <Reveal className="lg:col-span-5">
            <span className="eyebrow text-turquoise">Offline &amp; Clean-Clone Reproducible</span>
            <h2 className="t-h1 mt-4">
              Reproduce every experiment locally
            </h2>
            <p className="t-lead mt-5">
              Pramaan operates with zero cloud dependencies. The complete simulation engine,
              CLI, automated tests, and offline fixtures run directly on your workstation.
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
                  <span className="text-[11px] ml-2 text-mutedText font-medium">bash — pramaan-reproduce</span>
                </div>
                <button
                  type="button"
                  onClick={copyQuickstart}
                  className="flex items-center gap-1.5 text-[11px] font-mono text-tertiaryText hover:text-turquoise transition-colors duration-micro"
                  title="Copy quickstart commands"
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                  {copied ? "Copied" : "Copy"}
                </button>
              </div>

              <pre className="p-5 sm:p-6 font-mono text-[12px] leading-[1.9] overflow-x-auto text-inkText">
                <span className="text-tertiaryText"># 1. Clone the official repository</span>{"\n"}
                <span>git clone {GITHUB_REPO}.git</span>{"\n"}
                <span>cd Quantlab</span>{"\n\n"}
                <span className="text-tertiaryText"># 2. Install dependencies in editable mode</span>{"\n"}
                <span>pip install -e &quot;.[dev,api]&quot;</span>{"\n\n"}
                <span className="text-tertiaryText"># 3. Verify the complete 72-test suite offline</span>{"\n"}
                <span className="text-turquoise">pytest tests/ -q</span>{"\n"}
                <span className="text-emerald-400"># Output: 72 passed in ~7s</span>{"\n\n"}
                <span className="text-tertiaryText"># 4. Start the honest backtest engine API</span>{"\n"}
                <span>python -m src.api.main</span>{"\n\n"}
                <span className="text-tertiaryText"># 5. Launch desktop or web UI</span>{"\n"}
                <span>cd frontend &amp;&amp; npm run dev</span>
              </pre>
            </div>
          </Reveal>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative py-[var(--space-section)] px-5 sm:px-8 overflow-hidden border-t border-rule">
        <Reveal className="relative max-w-[1240px] mx-auto text-center">
          <span className="eyebrow">GTU DI05000341 Minor Project</span>
          <h2 className="t-h1 mt-5 max-w-[20ch] mx-auto">
            Prove your edge before deploying real capital
          </h2>
          <div className="mt-9 flex flex-wrap items-center justify-center gap-4">
            <a href={terminalUrl} className="btn-primary">
              Open Trading Terminal
              <ArrowRight className="w-4 h-4" />
            </a>
            <a
              href={GITHUB_REPO}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-ghost font-mono text-xs"
            >
              Star on GitHub
            </a>
          </div>
        </Reveal>
      </section>

      {/* Footer */}
      <footer className="py-12 px-5 sm:px-8 border-t border-rule bg-panel">
        <div className="max-w-[1240px] mx-auto flex flex-col md:flex-row items-start md:items-center justify-between gap-6 text-xs font-mono text-mutedText">
          <div>
            <div className="flex items-center gap-2 text-inkText font-semibold">
              <span>PRAMAAN (प्रमाण)</span>
              <span className="text-tertiaryText">·</span>
              <span className="text-mutedText font-normal">GTU DI05000341 Minor Project (Sem-5)</span>
            </div>
            <p className="mt-1.5 text-[11px]">
              Authors: Aayush Avinash Bankar (246230316006) &amp; Meet Jayeshbhai Patel (246230316133)
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-5">
            <a href={terminalUrl} className="hover:text-turquoise transition-colors duration-micro">
              Trading Terminal
            </a>
            <a
              href={GITHUB_REPO}
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-turquoise transition-colors duration-micro"
            >
              GitHub
            </a>
            <a
              href={GITHUB_RELEASE}
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-turquoise transition-colors duration-micro"
            >
              Releases (v1.0.0)
            </a>
            <span className="text-tertiaryText">|</span>
            <span className="text-tertiaryText">No Live Trading · Simulation &amp; Audit Only</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
