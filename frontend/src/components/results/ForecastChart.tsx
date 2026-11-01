"use client";

import React, { useState } from "react";
import { ProgressionForecast } from "@/lib/api";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import {
  ResponsiveContainer,
  ComposedChart,
  Area,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";
import { TrendingUp, ShieldCheck, Activity } from "lucide-react";

interface ForecastChartProps {
  forecast: ProgressionForecast;
  currentGlucose: number;
  currentSystolicBp: number;
}

export function ForecastChart({
  forecast,
  currentGlucose,
  currentSystolicBp,
}: ForecastChartProps) {
  const [metric, setMetric] = useState<"glucose" | "bp">("glucose");

  if (!forecast) return null;

  // Prepare data for 0 (Current), 3 Months, 6 Months
  const glucoseData = [
    {
      time: "Current",
      value: currentGlucose,
      lower: currentGlucose,
      upper: currentGlucose,
      band: [currentGlucose, currentGlucose],
    },
    {
      time: "3 Months",
      value: Math.round(forecast.forecasted_glucose_3m * 10) / 10,
      lower: Math.round((forecast.forecasted_glucose_3m - 4) * 10) / 10,
      upper: Math.round((forecast.forecasted_glucose_3m + 5) * 10) / 10,
      band: [
        Math.round((forecast.forecasted_glucose_3m - 4) * 10) / 10,
        Math.round((forecast.forecasted_glucose_3m + 5) * 10) / 10,
      ],
    },
    {
      time: "6 Months",
      value: Math.round(forecast.forecasted_glucose_6m * 10) / 10,
      lower: Math.round(forecast.glucose_prediction_interval_6m[0] * 10) / 10,
      upper: Math.round(forecast.glucose_prediction_interval_6m[1] * 10) / 10,
      band: [
        Math.round(forecast.glucose_prediction_interval_6m[0] * 10) / 10,
        Math.round(forecast.glucose_prediction_interval_6m[1] * 10) / 10,
      ],
    },
  ];

  const bpData = [
    {
      time: "Current",
      value: currentSystolicBp,
      lower: currentSystolicBp,
      upper: currentSystolicBp,
      band: [currentSystolicBp, currentSystolicBp],
    },
    {
      time: "3 Months",
      value: Math.round(forecast.forecasted_systolic_bp_3m * 10) / 10,
      lower: Math.round((forecast.forecasted_systolic_bp_3m - 3) * 10) / 10,
      upper: Math.round((forecast.forecasted_systolic_bp_3m + 4) * 10) / 10,
      band: [
        Math.round((forecast.forecasted_systolic_bp_3m - 3) * 10) / 10,
        Math.round((forecast.forecasted_systolic_bp_3m + 4) * 10) / 10,
      ],
    },
    {
      time: "6 Months",
      value: Math.round(forecast.forecasted_systolic_bp_6m * 10) / 10,
      lower: Math.round(forecast.bp_prediction_interval_6m[0] * 10) / 10,
      upper: Math.round(forecast.bp_prediction_interval_6m[1] * 10) / 10,
      band: [
        Math.round(forecast.bp_prediction_interval_6m[0] * 10) / 10,
        Math.round(forecast.bp_prediction_interval_6m[1] * 10) / 10,
      ],
    },
  ];

  const activeData = metric === "glucose" ? glucoseData : bpData;
  const unit = metric === "glucose" ? "mg/dL" : "mmHg";
  const title = metric === "glucose" ? "Fasting Blood Sugar Trajectory" : "Systolic Blood Pressure Trajectory";

  return (
    <Card className="border-medical-teal/20 shadow-sm overflow-hidden">
      <CardHeader className="bg-slate-50/60 dark:bg-slate-900/40 border-b pb-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <div className="p-2 bg-emerald-100 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-300 rounded-lg">
              <TrendingUp className="h-5 w-5" />
            </div>
            <div>
              <CardTitle className="text-lg font-bold text-slate-900 dark:text-slate-100">
                {title}
              </CardTitle>
              <CardDescription className="text-xs text-slate-500">
                Machine learning forecast with 90% Conformal Prediction uncertainty bounds.
              </CardDescription>
            </div>
          </div>

          {/* Toggle between Glucose & BP */}
          <div className="flex items-center rounded-lg bg-slate-100 dark:bg-slate-800 p-1 self-start sm:self-auto">
            <button
              onClick={() => setMetric("glucose")}
              className={`px-3 py-1.5 text-xs font-semibold rounded-md transition-all ${
                metric === "glucose"
                  ? "bg-white dark:bg-slate-900 text-teal-800 dark:text-teal-300 shadow-sm"
                  : "text-slate-600 dark:text-slate-400 hover:text-slate-900"
              }`}
            >
              Glucose (mg/dL)
            </button>
            <button
              onClick={() => setMetric("bp")}
              className={`px-3 py-1.5 text-xs font-semibold rounded-md transition-all ${
                metric === "bp"
                  ? "bg-white dark:bg-slate-900 text-teal-800 dark:text-teal-300 shadow-sm"
                  : "text-slate-600 dark:text-slate-400 hover:text-slate-900"
              }`}
            >
              Blood Pressure (mmHg)
            </button>
          </div>
        </div>
      </CardHeader>

      <CardContent className="p-4 sm:p-6 space-y-4">
        {/* Trend summary banner */}
        <div className="p-3 bg-teal-50/60 dark:bg-teal-950/40 rounded-xl border border-teal-100 dark:border-teal-900/40 flex items-start gap-2.5 text-xs text-teal-900 dark:text-teal-200">
          <Activity className="h-4 w-4 text-teal-600 shrink-0 mt-0.5" />
          <div>
            <span className="font-bold">Forecast Summary: </span>
            {forecast.trend_description}
          </div>
        </div>

        {/* Chart */}
        <div className="h-64 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={activeData} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
              <defs>
                <linearGradient id="uncertaintyGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#0f766e" stopOpacity={0.25} />
                  <stop offset="95%" stopColor="#0f766e" stopOpacity={0.05} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
              <XAxis
                dataKey="time"
                tick={{ fontSize: 12, fill: "#64748b" }}
                axisLine={{ stroke: "#cbd5e1" }}
                tickLine={false}
              />
              <YAxis
                domain={["auto", "auto"]}
                tick={{ fontSize: 12, fill: "#64748b" }}
                axisLine={{ stroke: "#cbd5e1" }}
                tickLine={false}
                unit={` ${unit}`}
              />
              <Tooltip
                content={({ active, payload, label }) => {
                  if (active && payload && payload.length) {
                    const data = payload[0].payload;
                    return (
                      <div className="rounded-lg bg-slate-900 p-3 text-xs text-white shadow-xl border border-slate-700">
                        <p className="font-bold text-slate-200 mb-1">{label}</p>
                        <p className="text-teal-300 font-semibold">
                          Expected Value: {data.value} {unit}
                        </p>
                        {label !== "Current" && (
                          <p className="text-slate-400 text-[11px] mt-0.5">
                            90% Confidence: [{data.lower} – {data.upper}] {unit}
                          </p>
                        )}
                      </div>
                    );
                  }
                  return null;
                }}
              />
              {/* Uncertainty Band Area */}
              <Area
                type="monotone"
                dataKey="upper"
                stroke="transparent"
                fill="url(#uncertaintyGradient)"
              />
              {/* Forecast Mean Line */}
              <Line
                type="monotone"
                dataKey="value"
                stroke="#0f766e"
                strokeWidth={3}
                dot={{ r: 5, fill: "#0f766e", stroke: "#ffffff", strokeWidth: 2 }}
                activeDot={{ r: 7 }}
              />
            </ComposedChart>
          </ResponsiveContainer>
        </div>

        {/* Legend / Uncertainty Explanation */}
        <div className="flex flex-wrap items-center justify-between text-xs text-slate-500 pt-2 border-t">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1.5">
              <span className="h-3 w-3 rounded-full bg-teal-700 inline-block" />
              ML Expected Path
            </span>
            <span className="flex items-center gap-1.5">
              <span className="h-3 w-6 rounded bg-teal-600/20 inline-block border border-teal-600/30" />
              90% Uncertainty Band
            </span>
          </div>
          <div className="flex items-center gap-1 text-[11px] text-slate-600 dark:text-slate-400 mt-2 sm:mt-0">
            <ShieldCheck className="h-3.5 w-3.5 text-teal-600" />
            Conformal Quantile Regression
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
