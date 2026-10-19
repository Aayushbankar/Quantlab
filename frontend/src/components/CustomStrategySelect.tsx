"use client";

import React, { useState, useRef, useEffect } from "react";
import { ChevronDown, Check, Sparkles } from "lucide-react";

export interface StrategyOption {
  id: string;
  name: string;
  category: string;
  description: string;
  paramsSummary: string;
}

interface CustomStrategySelectProps {
  value: string;
  onChange: (strategyId: string) => void;
  strategies: StrategyOption[];
}

export const CustomStrategySelect: React.FC<CustomStrategySelectProps> = ({
  value,
  onChange,
  strategies,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const selectedStrategy = strategies.find((s) => s.id === value) || strategies[0];

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
      document.addEventListener("keydown", handleKeyDown);
    }
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [isOpen]);

  return (
    <div className="relative w-full" ref={containerRef}>
      {/* Trigger Button */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className={`w-full flex items-center justify-between px-3 py-2 text-left bg-canvas border rounded font-mono transition-all duration-150 ${
          isOpen
            ? "border-turquoise ring-1 ring-turquoise/40 shadow-sm"
            : "border-rule hover:border-turquoise/60"
        }`}
        aria-haspopup="listbox"
        aria-expanded={isOpen}
      >
        <div className="flex flex-col min-w-0 pr-2">
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold text-inkText truncate">
              {selectedStrategy.name}
            </span>
            <span className="text-[10px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded bg-stormyTeal/30 text-turquoise border border-stormyTeal/60 shrink-0">
              {selectedStrategy.category}
            </span>
          </div>
          <span className="text-[10px] text-mutedText truncate mt-0.5 font-sans">
            {selectedStrategy.description}
          </span>
        </div>
        <ChevronDown
          size={16}
          className={`text-mutedText transition-transform duration-200 shrink-0 ${
            isOpen ? "rotate-180 text-turquoise" : ""
          }`}
        />
      </button>

      {/* Floating Dropdown Menu */}
      {isOpen && (
        <div className="absolute left-0 right-0 top-full mt-1.5 z-50 bg-panel border border-stormyTeal rounded-md shadow-2xl py-1 overflow-hidden backdrop-blur-lg animate-in fade-in-0 zoom-in-95 duration-100">
          <div className="px-2.5 py-1.5 border-b border-rule/50 flex items-center justify-between text-[10px] font-mono text-mutedText uppercase tracking-wider">
            <span>Select Model Architecture</span>
            <span className="text-turquoise flex items-center gap-1">
              <Sparkles size={11} /> 6 Calibrated
            </span>
          </div>
          <ul role="listbox" className="max-h-60 overflow-y-auto divide-y divide-rule/30">
            {strategies.map((s) => {
              const isSelected = s.id === value;
              return (
                <li
                  key={s.id}
                  role="option"
                  aria-selected={isSelected}
                  onClick={() => {
                    onChange(s.id);
                    setIsOpen(false);
                  }}
                  className={`px-3 py-2 cursor-pointer transition-colors flex items-start justify-between gap-2 ${
                    isSelected
                      ? "bg-turquoise/15 text-turquoise"
                      : "hover:bg-stormyTeal/20 text-inkText"
                  }`}
                >
                  <div className="flex flex-col min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold font-mono truncate">
                        {s.name}
                      </span>
                      <span
                        className={`text-[9px] font-mono uppercase px-1.5 py-0.2 rounded border ${
                          isSelected
                            ? "bg-turquoise/20 text-turquoise border-turquoise/50"
                            : "bg-canvas text-mutedText border-rule"
                        }`}
                      >
                        {s.category}
                      </span>
                    </div>
                    <p className="text-[11px] text-mutedText mt-0.5 font-sans line-clamp-1">
                      {s.description}
                    </p>
                    <span className="text-[9px] font-mono text-pacificCyan/80 mt-0.5">
                      Default: {s.paramsSummary}
                    </span>
                  </div>

                  {isSelected && (
                    <Check size={15} className="text-turquoise shrink-0 mt-0.5" />
                  )}
                </li>
              );
            })}
          </ul>
        </div>
      )}
    </div>
  );
};
