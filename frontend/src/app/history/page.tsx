"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useI18n } from "@/lib/i18n/context";
import { api } from "@/lib/api";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  History as HistoryIcon,
  Activity,
  Calendar,
  TrendingDown,
  TrendingUp,
  Plus,
  ArrowRight,
  ShieldCheck,
  FileText,
  Clock,
} from "lucide-react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from "recharts";

interface HistoryRecord {
  screening_id: string;
  date: string;
  systolic_bp: number;
  diastolic_bp: number;
  fasting_glucose: number;
  hba1c: number;
  bmi: number;
  continuous_risk_score: number;
  cluster_label: string;
  conditions_summary: {
    diabetes: string;
    heart_disease: string;
    hypertension: string;
  };
}

export default function HistoryPage() {
  const { t } = useI18n();
  const [loading, setLoading] = useState(true);
  const [historyData, setHistoryData] = useState<HistoryRecord[]>([]);

  useEffect(() => {
    async function loadHistory() {
      try {
        const res = await api.history.get("demo-pat-001");
        if (res && res.timeline) {
          setHistoryData(res.timeline);
        }
      } catch (e) {
        console.warn("Failed to fetch history, using default local timeline", e);
      } finally {
        setLoading(false);
      }
    }
    loadHistory();
  }, []);

  // Format chart data (chronological order)
  const chartData = [...historyData]
    .reverse()
    .map((item) => ({
      date: new Date(item.date).toLocaleDateString("en-IN", { month: "short", day: "numeric" }),
      glucose: item.fasting_glucose,
      systolicBp: item.systolic_bp,
      riskScore: item.continuous_risk_score,
    }));

  return (
    <div className="space-y-8 pb-16">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b pb-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-medical-teal mb-1">
            <span className="px-2.5 py-0.5 rounded-full bg-teal-50 dark:bg-teal-950/60 border border-teal-200 dark:border-teal-800">
              Longitudinal EHR
            </span>
            <span className="text-slate-500">Patient: Rajesh Kumar Sharma (ABHA: 91-1234-****)</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-slate-100 flex items-center gap-2">
            <HistoryIcon className="h-7 w-7 text-medical-teal" />
            {t("nav.history", "Longitudinal Health Records")}
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
            Track multi-month trajectory of cardiometabolic biomarkers and risk reduction.
          </p>
        </div>

        <Link href="/screen">
          <Button className="bg-medical-teal hover:bg-teal-700 text-white text-xs font-semibold gap-1.5 shadow-sm">
            <Plus className="h-4 w-4" />
            New Screening Check
          </Button>
        </Link>
      </div>

      {/* Trajectory Trend Chart */}
      <Card className="border-medical-teal/20 shadow-sm overflow-hidden">
        <CardHeader className="bg-slate-50/60 dark:bg-slate-900/40 border-b pb-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="p-2 bg-medical-teal/10 text-medical-teal rounded-lg">
                <Activity className="h-5 w-5" />
              </div>
              <div>
                <CardTitle className="text-lg font-bold text-slate-900 dark:text-slate-100">
                  Biomarker Trajectory & Risk Score Trend
                </CardTitle>
                <CardDescription className="text-xs">
                  Historical measurements over the past 6 months
                </CardDescription>
              </div>
            </div>
            <span className="hidden sm:inline-flex items-center gap-1.5 text-xs text-emerald-600 font-semibold bg-emerald-50 dark:bg-emerald-950 px-2.5 py-1 rounded-full border border-emerald-200 dark:border-emerald-800">
              <TrendingDown className="h-3.5 w-3.5" />
              Risk Reduced by 25%
            </span>
          </div>
        </CardHeader>

        <CardContent className="p-4 sm:p-6">
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="date" stroke="#64748b" fontSize={12} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={12} tickLine={false} domain={[40, 160]} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#0f172a",
                    border: "none",
                    borderRadius: "8px",
                    color: "#fff",
                    fontSize: "12px",
                  }}
                />
                <Legend wrapperStyle={{ fontSize: "12px", paddingTop: "10px" }} />
                <Line
                  type="monotone"
                  dataKey="glucose"
                  name="Fasting Glucose (mg/dL)"
                  stroke="#0f766e"
                  strokeWidth={2.5}
                  dot={{ r: 4, fill: "#0f766e" }}
                />
                <Line
                  type="monotone"
                  dataKey="systolicBp"
                  name="Systolic BP (mmHg)"
                  stroke="#3b82f6"
                  strokeWidth={2.5}
                  dot={{ r: 4, fill: "#3b82f6" }}
                />
                <Line
                  type="monotone"
                  dataKey="riskScore"
                  name="Continuous Risk (0-100)"
                  stroke="#f97316"
                  strokeWidth={2}
                  strokeDasharray="4 4"
                  dot={{ r: 3, fill: "#f97316" }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* Timeline List */}
      <div className="space-y-4">
        <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
          <Clock className="h-5 w-5 text-medical-teal" />
          Past Screening Records
        </h2>

        <div className="space-y-4">
          {historyData.map((record) => (
            <Card
              key={record.screening_id}
              className="border-slate-200 dark:border-slate-800 hover:border-medical-teal/40 transition-colors shadow-sm"
            >
              <CardContent className="p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <div className="space-y-1.5">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-sm text-slate-900 dark:text-slate-100">
                      {new Date(record.date).toLocaleDateString("en-IN", {
                        year: "numeric",
                        month: "long",
                        day: "numeric",
                      })}
                    </span>
                    <span className="text-xs px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400">
                      ID: {record.screening_id}
                    </span>
                  </div>

                  <p className="text-xs text-slate-500">
                    Cohort Phenotype: <span className="text-slate-700 dark:text-slate-300 font-medium">{record.cluster_label}</span>
                  </p>

                  <div className="flex flex-wrap items-center gap-3 pt-1 text-xs">
                    <span className="text-slate-600 dark:text-slate-400">
                      Glucose: <strong className="text-slate-900 dark:text-slate-100">{record.fasting_glucose} mg/dL</strong>
                    </span>
                    <span className="text-slate-300 dark:text-slate-700">•</span>
                    <span className="text-slate-600 dark:text-slate-400">
                      BP: <strong className="text-slate-900 dark:text-slate-100">{record.systolic_bp}/{record.diastolic_bp} mmHg</strong>
                    </span>
                    <span className="text-slate-300 dark:text-slate-700">•</span>
                    <span className="text-slate-600 dark:text-slate-400">
                      HbA1c: <strong className="text-slate-900 dark:text-slate-100">{record.hba1c}%</strong>
                    </span>
                    <span className="text-slate-300 dark:text-slate-700">•</span>
                    <span className="text-slate-600 dark:text-slate-400">
                      BMI: <strong className="text-slate-900 dark:text-slate-100">{record.bmi}</strong>
                    </span>
                  </div>
                </div>

                <div className="flex sm:flex-col items-center sm:items-end justify-between w-full sm:w-auto gap-2 pt-2 sm:pt-0 border-t sm:border-0">
                  <div className="text-left sm:text-right">
                    <span className="text-xs text-slate-500 block">Overall Risk Index</span>
                    <span
                      className={`text-lg font-black ${
                        record.continuous_risk_score > 65
                          ? "text-orange-600"
                          : record.continuous_risk_score > 40
                          ? "text-amber-600"
                          : "text-emerald-600"
                      }`}
                    >
                      {record.continuous_risk_score}/100
                    </span>
                  </div>

                  <Link href={`/results?id=${record.screening_id}`}>
                    <Button variant="ghost" size="sm" className="text-xs text-medical-teal hover:text-teal-700 p-0 sm:px-2">
                      View Full Analysis <ArrowRight className="h-3.5 w-3.5 ml-1" />
                    </Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
