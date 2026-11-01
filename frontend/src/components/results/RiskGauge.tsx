"use client";

import React from "react";
import { RiskLevel } from "@/lib/api";

interface RiskGaugeProps {
  score: number; // 0.0 to 1.0
  level: RiskLevel;
  conditionName: string;
  threshold: number;
}

export function RiskGauge({ score, level, conditionName, threshold }: RiskGaugeProps) {
  const percentage = Math.round(score * 100);
  const thresholdPct = Math.round(threshold * 100);

  // SVG Gauge Calculations
  const radius = 70;
  const stroke = 14;
  const normalizedRadius = radius - stroke * 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  // Half gauge arc (180 degrees)
  const strokeDashoffset = circumference - (percentage / 100) * (circumference / 2);

  const colors = {
    LOW: {
      text: "text-emerald-700 dark:text-emerald-400",
      bg: "bg-emerald-50 dark:bg-emerald-950/60",
      border: "border-emerald-200 dark:border-emerald-800",
      stroke: "#10b981",
    },
    MODERATE: {
      text: "text-amber-700 dark:text-amber-400",
      bg: "bg-amber-50 dark:bg-amber-950/60",
      border: "border-amber-200 dark:border-amber-800",
      stroke: "#f59e0b",
    },
    HIGH: {
      text: "text-orange-700 dark:text-orange-400",
      bg: "bg-orange-50 dark:bg-orange-950/60",
      border: "border-orange-200 dark:border-orange-800",
      stroke: "#f97316",
    },
    CRITICAL: {
      text: "text-red-700 dark:text-red-400",
      bg: "bg-red-50 dark:bg-red-950/60",
      border: "border-red-200 dark:border-red-800",
      stroke: "#ef4444",
    },
  }[level] || {
    text: "text-slate-700",
    bg: "bg-slate-50",
    border: "border-slate-200",
    stroke: "#0f766e",
  };

  return (
    <div className={`rounded-2xl border p-5 flex flex-col items-center text-center ${colors.bg} ${colors.border}`}>
      <span className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1">
        {conditionName}
      </span>

      {/* Radial Semi-Circle Meter */}
      <div className="relative w-40 h-24 flex items-end justify-center overflow-hidden my-1">
        <svg height="160" width="160" className="absolute top-0">
          {/* Background Track */}
          <circle
            stroke="currentColor"
            fill="transparent"
            strokeWidth={stroke}
            strokeDasharray={`${circumference / 2} ${circumference}`}
            style={{ strokeDashoffset: 0 }}
            r={normalizedRadius}
            cx="80"
            cy="80"
            className="text-slate-200 dark:text-slate-800 transform rotate-180 origin-center"
          />
          {/* Active Value Arc */}
          <circle
            stroke={colors.stroke}
            fill="transparent"
            strokeWidth={stroke}
            strokeDasharray={`${circumference / 2} ${circumference}`}
            style={{ strokeDashoffset }}
            strokeLinecap="round"
            r={normalizedRadius}
            cx="80"
            cy="80"
            className="transform rotate-180 origin-center transition-all duration-1000 ease-out"
          />
        </svg>

        <div className="text-center z-10 pb-1">
          <span className="text-3xl font-extrabold text-slate-900 dark:text-slate-100">
            {percentage}%
          </span>
          <span className="block text-[11px] font-semibold text-slate-500 -mt-1">
            Calibrated Risk
          </span>
        </div>
      </div>

      <div className="mt-2 space-y-1">
        <span className={`inline-block px-3 py-1 rounded-full text-xs font-extrabold ${colors.text} bg-white dark:bg-slate-900 shadow-sm border border-current`}>
          {level} RISK
        </span>
        <span className="block text-[11px] text-slate-500 dark:text-slate-400">
          Screening Threshold: {thresholdPct}%
        </span>
      </div>
    </div>
  );
}
