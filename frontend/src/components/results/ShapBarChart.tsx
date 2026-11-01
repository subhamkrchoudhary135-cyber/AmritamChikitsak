"use client";

import React, { useState } from "react";
import { ShapFactor } from "@/lib/api";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Info, AlertCircle, CheckCircle2, ChevronDown, ChevronUp } from "lucide-react";

interface ShapBarChartProps {
  factors: ShapFactor[];
}

export function ShapBarChart({ factors }: ShapBarChartProps) {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);

  if (!factors || factors.length === 0) {
    return null;
  }

  // Find max impact score for proportional bar widths
  const maxImpact = Math.max(...factors.map((f) => Math.abs(f.impact_score)), 0.01);

  return (
    <Card className="border-medical-teal/20 shadow-sm overflow-hidden">
      <CardHeader className="bg-slate-50/60 dark:bg-slate-900/40 border-b pb-4">
        <div className="flex items-center gap-2">
          <div className="p-2 bg-medical-teal/10 text-medical-teal rounded-lg">
            <Info className="h-5 w-5" />
          </div>
          <div>
            <CardTitle className="text-lg font-bold text-slate-900 dark:text-slate-100">
              Why Did the AI Calculate This Risk? (SHAP Breakdown)
            </CardTitle>
            <CardDescription className="text-xs text-slate-500">
              Top 5 biological and lifestyle drivers explained in simple words (Class 8 reading level).
            </CardDescription>
          </div>
        </div>
      </CardHeader>

      <CardContent className="p-4 sm:p-6 space-y-4">
        {factors.map((factor, index) => {
          const isExpanded = expandedIndex === index;
          const percentage = Math.min(100, Math.round((Math.abs(factor.impact_score) / maxImpact) * 100));
          const isIncreasing = factor.direction === "increases_risk";
          const isDecreasing = factor.direction === "decreases_risk";

          const barColor = isIncreasing
            ? "bg-rose-500 dark:bg-rose-600"
            : isDecreasing
            ? "bg-emerald-500 dark:bg-emerald-600"
            : "bg-slate-400";

          const badgeColor = isIncreasing
            ? "bg-rose-50 text-rose-700 border-rose-200 dark:bg-rose-950/60 dark:text-rose-400 dark:border-rose-800"
            : isDecreasing
            ? "bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-950/60 dark:text-emerald-400 dark:border-emerald-800"
            : "bg-slate-100 text-slate-700 border-slate-200 dark:bg-slate-800 dark:text-slate-300";

          return (
            <div
              key={factor.feature}
              className="border rounded-xl p-3 sm:p-4 bg-white dark:bg-slate-900/60 hover:border-medical-teal/40 transition-colors"
            >
              <div
                className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 cursor-pointer select-none"
                onClick={() => setExpandedIndex(isExpanded ? null : index)}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === "Enter" || e.key === " ") {
                    setExpandedIndex(isExpanded ? null : index);
                  }
                }}
                aria-expanded={isExpanded}
                aria-label={`Factor ${factor.feature_name_friendly}: ${isIncreasing ? "Increases" : "Decreases"} risk`}
              >
                <div className="flex items-center gap-3">
                  <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800 text-xs font-bold text-slate-600 dark:text-slate-300">
                    {index + 1}
                  </span>
                  <div>
                    <h4 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                      {factor.feature_name_friendly}
                    </h4>
                    <span className="text-xs text-slate-500 dark:text-slate-400">
                      Your Value: <strong className="text-slate-700 dark:text-slate-200">{String(factor.patient_value)}</strong>
                    </span>
                  </div>
                </div>

                <div className="flex items-center justify-between sm:justify-end gap-3 w-full sm:w-auto">
                  <span className={`text-[11px] font-semibold px-2.5 py-0.5 rounded-full border ${badgeColor}`}>
                    {isIncreasing ? "Increases Risk" : isDecreasing ? "Protective Factor" : "Neutral"}
                  </span>
                  {isExpanded ? (
                    <ChevronUp className="h-4 w-4 text-slate-400" />
                  ) : (
                    <ChevronDown className="h-4 w-4 text-slate-400" />
                  )}
                </div>
              </div>

              {/* Relative Impact Progress Bar */}
              <div className="mt-3">
                <div className="h-2 w-full bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all duration-700 ease-out ${barColor}`}
                    style={{ width: `${percentage}%` }}
                  />
                </div>
              </div>

              {/* Expandable Plain-Language Advice and Reference Range */}
              {isExpanded && (
                <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 text-xs space-y-2 animate-in fade-in duration-200">
                  <div className="flex items-start gap-2 text-slate-600 dark:text-slate-300">
                    <Info className="h-4 w-4 text-sky-600 mt-0.5 shrink-0" />
                    <div>
                      <span className="font-semibold text-slate-900 dark:text-slate-100">Recommended Range: </span>
                      {factor.clinical_reference}
                    </div>
                  </div>

                  <div className="flex items-start gap-2 bg-medical-teal/5 dark:bg-medical-teal/10 p-2.5 rounded-lg border border-medical-teal/15 text-medical-dark dark:text-teal-300">
                    {isIncreasing ? (
                      <AlertCircle className="h-4 w-4 text-amber-600 mt-0.5 shrink-0" />
                    ) : (
                      <CheckCircle2 className="h-4 w-4 text-emerald-600 mt-0.5 shrink-0" />
                    )}
                    <div>
                      <span className="font-semibold">Actionable Tip: </span>
                      {factor.actionable_advice}
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
}
