"use client";
import React, { useEffect, useState } from "react";
import { fetchTrials, TrialRecord, getReportUrl } from "../lib/api";
import { X, ExternalLink, RefreshCw } from "lucide-react";

interface HistoryDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectTrial?: (trial: TrialRecord) => void;
}

export const RunHistoryDrawer: React.FC<HistoryDrawerProps> = ({
  isOpen,
  onClose,
  onSelectTrial,
}) => {
  const [trials, setTrials] = useState<TrialRecord[]>([]);
  const [totalTrials, setTotalTrials] = useState<number>(0);
  const [crossTrialVar, setCrossTrialVar] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const loadTrials = async () => {
    setLoading(true);
    setError(null);
    try {
      const resp = await fetchTrials();
      setTrials(resp.trials);
      setTotalTrials(resp.total_trials);
      setCrossTrialVar(resp.cross_trial_variance);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to load trial history from Pramaan SQLite ledger";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      loadTrials();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/60 backdrop-blur-xs animate-in fade-in select-none">
      <div className="w-full max-w-md h-full bg-panel border-l border-rule shadow-2xl flex flex-col justify-between p-5 overflow-hidden">
        {/* Header */}
        <div>
          <div className="flex items-center justify-between border-b border-rule pb-3.5">
            <div>
              <h2 className="text-sm font-bold text-inkText flex items-center gap-2">
                <span>📜 Trial History Ledger</span>
              </h2>
              <p className="text-[11px] text-mutedText mt-0.5">
                Every backtest configuration evaluated is recorded in SQLite for DSR variance calculation.
              </p>
            </div>
            <div className="flex items-center gap-1.5">
              <button
                type="button"
                onClick={loadTrials}
                className="p-1.5 rounded hover:bg-canvas text-mutedText hover:text-turquoise transition-colors"
                title="Refresh trial ledger"
              >
                <RefreshCw size={14} className={loading ? "animate-spin" : ""} />
              </button>
              <button
                type="button"
                onClick={onClose}
                className="p-1.5 rounded hover:bg-canvas text-mutedText hover:text-inkText transition-colors"
              >
                <X size={16} />
              </button>
            </div>
          </div>

          {/* Ledger Summary Stats */}
          <div className="grid grid-cols-2 gap-2 mt-3 p-2.5 bg-canvas/80 border border-rule rounded text-xs font-mono">
            <div>
              <span className="text-mutedText text-[10px]">Total Evaluated Runs:</span>
              <div className="text-inkText font-bold text-sm">{totalTrials}</div>
            </div>
            <div>
              <span className="text-mutedText text-[10px]">Cross-Trial Var (V[SR]):</span>
              <div className="text-turquoise font-bold text-sm">
                {crossTrialVar.toFixed(4)}
              </div>
            </div>
          </div>
        </div>

        {/* Content List */}
        <div className="flex-1 overflow-y-auto my-3 pr-1 space-y-2">
          {loading && (
            <div className="py-12 text-center text-xs text-mutedText font-mono animate-pulse">
              Querying SQLite trial ledger...
            </div>
          )}

          {error && (
            <div className="p-3 bg-crimson/10 border border-crimson/30 rounded text-xs text-crimson">
              {error}
            </div>
          )}

          {!loading && !error && trials.length === 0 && (
            <div className="py-12 text-center text-xs text-mutedText font-mono">
              No historical trials recorded yet. Run backtests to populate the trial ledger.
            </div>
          )}

          {!loading &&
            trials.map((t) => {
              const reportUrl = t.run_id ? getReportUrl(t.run_id) : null;
              return (
                <div
                  key={t.trial_id}
                  className="p-3 bg-canvas/60 hover:bg-canvas border border-rule hover:border-turquoise/50 rounded-md transition-all text-xs font-mono group"
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="font-bold text-inkText uppercase text-[11px]">
                      {t.strategy.replace(/_/g, " ")}
                    </span>
                    <span className="text-[10px] text-mutedText">{t.created_at}</span>
                  </div>

                  <div className="grid grid-cols-3 gap-1 text-[11px] mb-2 font-tabular">
                    <div>
                      <span className="text-[9px] text-mutedText block">Sharpe:</span>
                      <span className={t.sharpe >= 0.5 ? "text-turquoise font-bold" : "text-inkText font-medium"}>
                        {t.sharpe.toFixed(2)}
                      </span>
                    </div>
                    <div>
                      <span className="text-[9px] text-mutedText block">Return:</span>
                      <span className="text-inkText font-medium">
                        {(t.total_return * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div>
                      <span className="text-[9px] text-mutedText block">Max DD:</span>
                      <span className="text-crimson font-medium">
                        {(t.max_drawdown * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center justify-between pt-2 border-t border-rule/50 text-[10px]">
                    {reportUrl ? (
                      <a
                        href={reportUrl}
                        target="_blank"
                        rel="noreferrer"
                        className="text-turquoise hover:underline flex items-center gap-1"
                      >
                        <ExternalLink size={10} />
                        Honesty Audit
                      </a>
                    ) : (
                      <span className="text-mutedText">Trial #{t.trial_id}</span>
                    )}

                    {onSelectTrial && (
                      <button
                        type="button"
                        onClick={() => onSelectTrial(t)}
                        className="px-2 py-0.5 rounded bg-panel border border-rule text-mutedText hover:text-turquoise hover:border-turquoise transition-colors"
                      >
                        Load Config
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
        </div>

        {/* Footer */}
        <div className="pt-3 border-t border-rule text-[10px] font-mono text-mutedText flex justify-between items-center">
          <span>Pramaan Honest SQLite DB</span>
          <span className="text-turquoise">DSR Multiple Testing Guard</span>
        </div>
      </div>
    </div>
  );
};
