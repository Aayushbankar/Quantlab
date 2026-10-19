"use client";
import React, { useState, useId } from "react";

interface DissectorProps {
  dates: string[];
  grossEquity: number[];
  netEquity: number[];
  initialCapital: number;
  strategyName: string;
}

export const ProfitMirageDissector: React.FC<DissectorProps> = ({
  dates,
  grossEquity,
  netEquity,
  initialCapital,
  strategyName,
}) => {
  const [hoverIndex, setHoverIndex] = useState<number | null>(null);
  const patternId = useId();
  const gradientId = useId();

  if (!dates || dates.length === 0 || !netEquity || netEquity.length === 0) {
    return (
      <div className="bg-panel border border-rule p-12 text-center text-mutedText rounded-sm h-full flex items-center justify-center font-mono">
        No equity curve data available. Execute a backtest to inspect the Profit Mirage.
      </div>
    );
  }

  const n = dates.length;
  const currentGross = grossEquity[n - 1] ?? initialCapital;
  const currentNet = netEquity[n - 1] ?? initialCapital;
  const totalDrag = Math.max(0, currentGross - currentNet);
  const dragPct = ((totalDrag / initialCapital) * 100).toFixed(1);

  // Bounds for SVG scaling
  const allValues = [...grossEquity, ...netEquity, initialCapital];
  const minVal = Math.min(...allValues) * 0.98;
  const maxVal = Math.max(...allValues) * 1.02;
  const range = maxVal - minVal || 1;

  // Widescreen High-Definition Viewport 1400 x 460
  const width = 1400;
  const height = 460;
  const padLeft = 95;
  const padRight = 40;
  const padTop = 30;
  const padBottom = 45;

  const chartW = width - padLeft - padRight;
  const chartH = height - padTop - padBottom;

  const getX = (i: number) => padLeft + (i / (n - 1 || 1)) * chartW;
  const getY = (val: number) => padTop + chartH - ((val - minVal) / range) * chartH;

  // Build SVG Paths
  const grossPoints = grossEquity.map((v, i) => `${getX(i)},${getY(v)}`);
  const netPoints = netEquity.map((v, i) => `${getX(i)},${getY(v)}`);

  const grossPath = `M ${grossPoints.join(" L ")}`;
  const netPath = `M ${netPoints.join(" L ")}`;

  // Evaporation fill polygon between Gross and Net
  const netPointsRev = [...netPoints].reverse();
  const fillPolygon = `M ${grossPoints[0]} L ${grossPoints.slice(1).join(" L ")} L ${netPointsRev.join(" L ")} Z`;

  const activeIdx = hoverIndex !== null ? hoverIndex : n - 1;
  const activeDate = dates[activeIdx] || dates[n - 1];
  const activeGross = grossEquity[activeIdx] ?? currentGross;
  const activeNet = netEquity[activeIdx] ?? currentNet;
  const activeLoss = Math.max(0, activeGross - activeNet);

  return (
    <div className="bg-panel border border-rule p-5 rounded-sm shadow-sm flex flex-col justify-between h-full select-none">
      {/* Top Header & HUD Scrub Ribbon */}
      <div className="border-b border-rule pb-3.5">
        <div className="flex flex-col xl:flex-row xl:items-center justify-between gap-3">
          <div>
            <div className="flex items-center gap-2.5">
              <h2 className="text-inkText text-base font-bold tracking-tight">
                The Profit Mirage Dissector
              </h2>
              <span className="text-xs font-mono px-2.5 py-0.5 bg-canvas border border-rule text-turquoise font-bold rounded">
                {strategyName.replace(/_/g, " ").toUpperCase()}
              </span>
            </div>
            <p className="text-mutedText text-xs mt-0.5 font-sans">
              Compare your gross paper returns against real cash delivered after Indian statutory taxes (STT, Stamp Duty, GST) and market slippage.
            </p>
          </div>

          {/* Interactive Inspection Ribbon */}
          <div className="flex flex-wrap items-center gap-4 font-tabular text-xs bg-canvas/80 border border-rule px-4 py-2 rounded shadow-inner">
            <div>
              <span className="text-mutedText text-[11px] font-mono">Bar Date: </span>
              <span className="font-mono text-inkText font-bold">{activeDate}</span>
            </div>
            <div className="h-3 w-px bg-rule" />
            <div>
              <span className="text-pacificCyan text-[11px] font-mono">Gross Paper: </span>
              <span className="font-mono font-bold text-pacificCyan">₹{activeGross.toLocaleString("en-IN", { maximumFractionDigits: 0 })}</span>
            </div>
            <div className="h-3 w-px bg-rule" />
            <div>
              <span className="text-turquoise text-[11px] font-mono">T+1 Net: </span>
              <span className="font-mono font-bold text-turquoise">₹{activeNet.toLocaleString("en-IN", { maximumFractionDigits: 0 })}</span>
            </div>
            <div className="h-3 w-px bg-rule" />
            <div>
              <span className="text-crimson text-[11px] font-mono">Evaporated: </span>
              <span className="font-mono font-bold text-crimson">-₹{activeLoss.toLocaleString("en-IN", { maximumFractionDigits: 0 })}</span>
            </div>
          </div>
        </div>
      </div>

      {/* High-Resolution SVG Canvas */}
      <div className="relative my-2 w-full flex-1 flex items-center justify-center overflow-hidden">
        <svg
          viewBox={`0 0 ${width} ${height}`}
          className="w-full h-full max-h-[520px]"
          onMouseLeave={() => setHoverIndex(null)}
          onMouseMove={(e) => {
            const rect = e.currentTarget.getBoundingClientRect();
            const svgX = ((e.clientX - rect.left) / rect.width) * width;
            if (svgX >= padLeft && svgX <= width - padRight) {
              const ratio = (svgX - padLeft) / chartW;
              const idx = Math.min(n - 1, Math.max(0, Math.round(ratio * (n - 1))));
              setHoverIndex(idx);
            }
          }}
        >
          <defs>
            {/* Deep Crimson Evaporation Diagonal Hatch */}
            <pattern
              id={patternId}
              width="10"
              height="10"
              patternUnits="userSpaceOnUse"
              patternTransform="rotate(45)"
            >
              <line x1="0" y1="0" x2="0" y2="10" stroke="#931621" strokeWidth="2.5" strokeOpacity="0.45" />
            </pattern>
            {/* Deep Crimson Gradient Fill */}
            <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#931621" stopOpacity="0.45" />
              <stop offset="100%" stopColor="#931621" stopOpacity="0.08" />
            </linearGradient>
          </defs>

          {/* Horizontal Gridlines */}
          {[0, 0.25, 0.5, 0.75, 1].map((frac, idx) => {
            const val = minVal + frac * range;
            const y = padTop + chartH - frac * chartH;
            return (
              <g key={idx}>
                <line
                  x1={padLeft}
                  y1={y}
                  x2={width - padRight}
                  y2={y}
                  stroke="#326771"
                  strokeWidth="1"
                  strokeDasharray="4 4"
                  strokeOpacity="0.5"
                />
                <text
                  x={padLeft - 14}
                  y={y + 4}
                  textAnchor="end"
                  fill="rgb(var(--text-muted-rgb))"
                  className="text-[11px] font-mono font-medium"
                >
                  ₹{val.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
                </text>
              </g>
            );
          })}

          {/* Capital Base Line ₹100,000 */}
          {initialCapital >= minVal && initialCapital <= maxVal && (
            <g>
              <line
                x1={padLeft}
                y1={getY(initialCapital)}
                x2={width - padRight}
                y2={getY(initialCapital)}
                stroke="#42D9C8"
                strokeWidth="1"
                strokeDasharray="4 4"
                strokeOpacity="0.4"
              />
              <text
                x={width - padRight - 5}
                y={getY(initialCapital) - 6}
                textAnchor="end"
                fill="#42D9C8"
                className="text-[10px] font-mono"
                fillOpacity="0.75"
              >
                Capital Base ₹1,00,000
              </text>
            </g>
          )}

          {/* Evaporation Shaded Polygon (Gradient + Hatch Pattern) */}
          <path d={fillPolygon} fill={`url(#${gradientId})`} />
          <path d={fillPolygon} fill={`url(#${patternId})`} />

          {/* Gross Paper Mirage (Pacific Cyan #2C8C99) */}
          <path
            d={grossPath}
            fill="none"
            stroke="#2C8C99"
            strokeWidth="3.2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />

          {/* Net Reality Curve (Turquoise #42D9C8) */}
          <path
            d={netPath}
            fill="none"
            stroke="#42D9C8"
            strokeWidth="3.4"
            strokeLinecap="round"
            strokeLinejoin="round"
          />

          {/* Hover Crosshair & Data Indicator */}
          {hoverIndex !== null && (
            <g>
              <line
                x1={getX(hoverIndex)}
                y1={padTop}
                x2={getX(hoverIndex)}
                y2={padTop + chartH}
                stroke="#F2FBFA"
                strokeWidth="1.5"
                strokeDasharray="3 3"
                strokeOpacity="0.75"
              />
              <circle
                cx={getX(hoverIndex)}
                cy={getY(grossEquity[hoverIndex] ?? initialCapital)}
                r="5.5"
                fill="#2C8C99"
                stroke="#17282B"
                strokeWidth="2"
              />
              <circle
                cx={getX(hoverIndex)}
                cy={getY(netEquity[hoverIndex] ?? initialCapital)}
                r="5.5"
                fill="#42D9C8"
                stroke="#17282B"
                strokeWidth="2"
              />
            </g>
          )}

          {/* Timeline X-Axis Dates */}
          {[0, 0.25, 0.5, 0.75, 1].map((frac, idx) => {
            const i = Math.min(n - 1, Math.round(frac * (n - 1)));
            const dateStr = dates[i] ?? "";
            return (
              <text
                key={idx}
                x={getX(i)}
                y={height - padBottom + 25}
                textAnchor={idx === 0 ? "start" : idx === 4 ? "end" : "middle"}
                fill="rgb(var(--text-muted-rgb))"
                className="text-[11px] font-mono"
              >
                {dateStr}
              </text>
            );
          })}
        </svg>
      </div>

      {/* Legend & Aggregate Summary Footer */}
      <div className="flex flex-wrap items-center justify-between pt-3 border-t border-rule text-xs gap-3">
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2">
            <span className="w-4 h-1.5 rounded-full inline-block bg-pacificCyan" />
            <span className="text-inkText font-medium">Paper Return (Before Taxes)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-4 h-1.5 rounded-full inline-block bg-turquoise" />
            <span className="text-turquoise font-medium">Real Return (After Taxes & Slippage)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-4 h-3 rounded inline-block border border-crimson bg-crimson/35" />
            <span className="text-crimson font-medium">Tax & Friction Drag</span>
          </div>
        </div>

        <div className="text-mutedText">
          Total Friction Loss: <span className="text-crimson font-bold font-mono">-₹{totalDrag.toLocaleString("en-IN", { maximumFractionDigits: 0 })}</span> ({dragPct}% of initial capital)
        </div>
      </div>
    </div>
  );
};
