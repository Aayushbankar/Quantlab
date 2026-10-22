"use client";
import React from "react";

interface CpcvProps {
  pbo?: number | null;
  pboReason?: string | null;
  ciLower?: number | null;
  ciUpper?: number | null;
  cpcvPaths?: number;
  nConfigs?: number;
}

export const CpcvEmbargoMatrix: React.FC<CpcvProps> = ({
  pbo,
  pboReason,
  ciLower = 0.4444,
  ciUpper = 0.7333,
  cpcvPaths = 45,
  nConfigs = 133,
}) => {
  const hasPbo = typeof pbo === "number";
  const pboPct = hasPbo ? (pbo * 100).toFixed(1) : null;
  const isOverfit = hasPbo && pbo > 0.5;

  // 6 representative combinatorial CPCV paths out of 45
  const samplePaths = [
    { id: "Path 01", testBlocks: [1, 2] },
    { id: "Path 09", testBlocks: [2, 5] },
    { id: "Path 18", testBlocks: [3, 7] },
    { id: "Path 27", testBlocks: [4, 8] },
    { id: "Path 36", testBlocks: [5, 9] },
    { id: "Path 45", testBlocks: [8, 10] },
  ];

  return (
    <div className="bg-panel border border-rule p-5 flex flex-col justify-between rounded-sm h-full">
      <div>
        <div className="flex items-baseline justify-between border-b border-rule pb-3">
          <h3 className="text-inkText text-sm font-semibold tracking-tight">
            Combinatorial Purged CV & PBO Matrix
          </h3>
          {hasPbo ? (
            <span
              className={`font-mono text-xs px-2 py-0.5 rounded border font-semibold ${
                isOverfit
                  ? "bg-crimson/15 border-crimson/40 text-crimson"
                  : "bg-turquoise/15 border-turquoise/40 text-turquoise"
              }`}
            >
              PBO: {pboPct}% ({isOverfit ? "HIGH OVERFIT RISK" : "ROBUST"})
            </span>
          ) : (
            <span className="font-mono text-[10px] px-2 py-0.5 rounded border bg-amber-500/10 border-amber-500/30 text-amber-400">
              REQUIRES SWEEP
            </span>
          )}
        </div>

        <p className="text-mutedText text-xs mt-2 mb-3">
          Marcos López de Prado Combinatorial Purged Cross-Validation ({cpcvPaths} paths, 10 splits, 2 test folds).
          Purges overlapping market returns and enforces a 1% temporal embargo to detect serial correlation leakage.
        </p>

        {/* Combinatorial Path Grid Preview */}
        <div className="space-y-1.5 font-mono text-[11px] mb-4">
          {samplePaths.map((p, idx) => (
            <div key={idx} className="flex items-center gap-2">
              <span className="text-mutedText w-14 text-[10px]">{p.id}</span>
              <div className="flex-1 flex gap-1 h-3.5">
                {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((blk) => {
                  const isTest = p.testBlocks.includes(blk);
                  const isEmbargo = p.testBlocks.some((t) => Math.abs(t - blk) === 1);
                  return (
                    <div
                      key={blk}
                      className={`flex-1 rounded-[1px] ${
                        isTest
                          ? "bg-crimson"
                          : isEmbargo
                          ? "bg-stamp/40 border border-stamp/60"
                          : "bg-canvas border border-rule"
                      }`}
                      title={isTest ? `Test Fold ${blk}` : isEmbargo ? `1% Embargo Buffer` : `Train Fold ${blk}`}
                    />
                  );
                })}
              </div>
            </div>
          ))}
        </div>

        {/* Legend */}
        <div className="flex items-center gap-4 text-[11px] font-mono text-mutedText border-t border-rule/50 pt-2.5">
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 bg-canvas border border-rule inline-block" />
            <span>Train Fold</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 bg-crimson inline-block" />
            <span>Test Fold</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 bg-stamp/50 border border-stamp/60 inline-block" />
            <span>1% Embargo</span>
          </div>
        </div>

        {/* Sweep Benchmark Card */}
        {hasPbo ? (
          <div className="mt-4 p-3 bg-canvas/70 border border-rule rounded text-xs font-mono space-y-1">
            <div className="flex justify-between">
              <span className="text-mutedText">Configs Evaluated:</span>
              <span className="text-inkText font-bold">{nConfigs} models</span>
            </div>
            <div className="flex justify-between">
              <span className="text-mutedText">Empirical PBO:</span>
              <span className={`font-bold ${isOverfit ? "text-crimson" : "text-turquoise"}`}>
                {pboPct}%
              </span>
            </div>
            {ciLower !== null && ciUpper !== null && (
              <div className="flex justify-between text-[10px]">
                <span className="text-mutedText">95% Bootstrap CI:</span>
                <span className="text-mutedText font-medium">
                  [{(ciLower * 100).toFixed(1)}%, {(ciUpper * 100).toFixed(1)}%]
                </span>
              </div>
            )}
          </div>
        ) : (
          <div className="mt-4 p-3 bg-canvas/70 border border-amber-500/30 rounded text-xs text-mutedText">
            <span className="text-amber-400 font-medium">Notice:</span> {pboReason || "PBO is computed across candidate strategy sweeps, not a single standalone backtest. Run parameter sweep to assess universe-wide selection bias."}
          </div>
        )}
      </div>

      <div className="mt-4 pt-3 border-t border-rule text-[11px] font-mono text-mutedText flex justify-between items-center">
        <span>Combinatorial Paths: <strong className="text-inkText">{cpcvPaths}</strong></span>
        <span>Selection Guard: <strong className="text-turquoise">Bailey & López de Prado (2014)</strong></span>
      </div>
    </div>
  );
};
