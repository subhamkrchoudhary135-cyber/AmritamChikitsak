"use client";

import React from "react";
import { ClusteringResult } from "@/lib/api";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Users, Sparkles, CheckCircle, ShieldAlert } from "lucide-react";

interface ClusterCardProps {
  cluster: ClusteringResult;
}

export function ClusterCard({ cluster }: ClusterCardProps) {
  if (!cluster) return null;

  return (
    <Card className="border-sky-200 dark:border-sky-900 bg-gradient-to-br from-sky-50/40 via-white to-teal-50/30 dark:from-slate-900 dark:via-slate-900 dark:to-slate-800 shadow-sm overflow-hidden">
      <CardHeader className="border-b border-sky-100 dark:border-slate-800 pb-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="p-2 bg-sky-100 dark:bg-sky-950 text-sky-700 dark:text-sky-300 rounded-lg">
              <Users className="h-5 w-5" />
            </div>
            <div>
              <CardTitle className="text-lg font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
                People Like You
                <span className="text-xs font-normal px-2.5 py-0.5 rounded-full bg-sky-100 dark:bg-sky-900 text-sky-800 dark:text-sky-200">
                  Cohort #{cluster.cluster_id + 1}
                </span>
              </CardTitle>
              <CardDescription className="text-xs text-slate-600 dark:text-slate-400">
                Unsupervised patient phenotype segmentation based on Indian cardiometabolic patterns.
              </CardDescription>
            </div>
          </div>
        </div>
      </CardHeader>

      <CardContent className="p-4 sm:p-6 space-y-4">
        <div className="p-3.5 bg-white dark:bg-slate-800/80 rounded-xl border border-sky-100 dark:border-slate-700 shadow-sm">
          <h4 className="text-sm font-bold text-sky-900 dark:text-sky-200 flex items-center gap-2">
            <Sparkles className="h-4 w-4 text-sky-600" />
            Segment: {cluster.cluster_label}
          </h4>
          <p className="text-xs text-slate-600 dark:text-slate-300 mt-1 leading-relaxed">
            {cluster.cluster_description}
          </p>
        </div>

        {cluster.is_anomaly && (
          <div className="p-3 bg-amber-50 dark:bg-amber-950/60 rounded-xl border border-amber-200 dark:border-amber-800 flex items-start gap-2.5 text-xs text-amber-800 dark:text-amber-300">
            <ShieldAlert className="h-5 w-5 text-amber-600 shrink-0 mt-0.5" />
            <div>
              <span className="font-bold">Unusual Pattern Detected: </span>
              Your vitals deviate slightly from typical standard cluster profiles (Anomaly Score: {cluster.anomaly_score.toFixed(2)}). A clinician review is advised to verify test numbers.
            </div>
          </div>
        )}

        <div>
          <h5 className="text-xs font-bold uppercase tracking-wider text-slate-600 dark:text-slate-400 mb-2.5 flex items-center gap-1.5">
            <CheckCircle className="h-4 w-4 text-teal-600" />
            ICMR & WHO Guideline Priorities for Your Group:
          </h5>
          <ul className="space-y-2">
            {cluster.lifestyle_priorities.map((item, idx) => (
              <li
                key={idx}
                className="flex items-start gap-2.5 text-xs text-slate-700 dark:text-slate-300 bg-slate-50/80 dark:bg-slate-800/40 p-2.5 rounded-lg border border-slate-100 dark:border-slate-800"
              >
                <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-teal-100 dark:bg-teal-900/60 text-teal-700 dark:text-teal-300 text-[10px] font-bold">
                  {idx + 1}
                </span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>
      </CardContent>
    </Card>
  );
}
