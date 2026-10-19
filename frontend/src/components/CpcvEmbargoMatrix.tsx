"use client";
import React from "react";

interface CpcvProps {
  pbo?: number | null;
}

export const CpcvEmbargoMatrix: React.FC<CpcvProps> = ({ pbo = 0.6429 }) => {
  const pboPct = ((pbo ?? 0.6429) * 100).toFixed(1);
  const splits = 8;
  const testSplits = 2;
  const totalCombinations = 28;

  // Render a sample of 6 representative paths out of 28
  const samplePaths = [
    { id: "Path 01", testBlocks: [1, 2] },
    { id: "Path 07", testBlocks: [2, 5] },
    { id: "Path 14", testBlocks: [3, 7] },
    { id: "Path 20", testBlocks: [4, 6] },
    { id: "Path 25", testBlocks: [5, 8] },
    { id: "Path 28", testBlocks: [7, 8] },
  ];

  return (
    <div className="bg-panel border border-rule p-5 flex flex-col justify-between rounded-sm h-full">
      <div>
        <div className="flex items-baseline justify-between border-b border-rule pb-3">
          <h3 className="text-inkText text-sm font-semibold tracking-tight">
            Combinatorial Purged CV & Embargo
          </h3>
          <span className="font-mono text-xs px-2 py-0.5 rounded border bg-crimson/15 border-crimson/40 text-crimson font-semibold">
            PBO: {pboPct}%
          </span>
        </div>
        <p className="text-mutedText text-xs mt-2 mb-3">
          CPCV generates {totalCombinations} combinatorial paths ({splits} splits, {testSplits} test blocks). Purges overlapping labels and applies a 1% embargo to detect serial leakage.
        </p>

        {/* Combinatorial Path Grid Preview */}
        <div className="space-y-1.5 font-mono text-[11px] mb-4">
          {samplePaths.map((p, idx) => (
            <div key={idx} className="flex items-center gap-2">
              <span className="text-mutedText w-14 text-[10px]">{p.id}</span>
              <div className="flex-1 flex gap-1 h-3.5">
                {[1, 2, 3, 4, 5, 6, 7, 8].map((blk) => {
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
                      title={isTest ? `Test Block ${blk}` : isEmbargo ? `Embargo Window` : `Train Block ${blk}`}
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
      </div>

      <div className="mt-4 pt-3 border-t border-rule text-[11px] font-mono text-mutedText">
        <span>Probability of Backtest Overfitting (PBO): </span>
        <span className="text-crimson font-bold font-tabular">{pboPct}%</span>
        <span className="text-[10px] block mt-0.5 text-mutedText">
          High PBO indicates strategy rank does not generalize across combinatorial folds.
        </span>
      </div>
    </div>
  );
};
