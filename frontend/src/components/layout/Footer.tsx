"use client";

import React from "react";
import { ShieldCheck, HeartPulse, ExternalLink } from "lucide-react";
import { useI18n } from "@/lib/i18n/context";

export function Footer() {
  const { t } = useI18n();

  return (
    <footer className="border-t border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 py-10 px-4 sm:px-6 transition-colors">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Statutory Clinical Non-Diagnostic Disclaimer Box */}
        <div className="rounded-2xl border-2 border-red-200 dark:border-red-950/80 bg-red-50/70 dark:bg-red-950/30 p-4 sm:p-5 text-red-900 dark:text-red-200 text-xs sm:text-sm leading-relaxed">
          <p className="font-bold flex items-center gap-1.5 mb-1 text-red-700 dark:text-red-400">
            <HeartPulse className="w-4 h-4 flex-shrink-0" />
            <span>MANDATORY STATUTORY MEDICAL NOTICE:</span>
          </p>
          <p>
            Sanjivani AI is an artificial intelligence health risk screening support platform designed for early cardiometabolic stratification. 
            It is <strong>NEVER a medical diagnosis, clinical prescription, or drug dosing recommendation</strong>. 
            Always consult a qualified, registered medical practitioner for definitive clinical evaluation, diagnosis, and prescription medications. 
            In case of acute chest discomfort, radiating pain, breathlessness, or stroke signs, immediately contact emergency services (<strong>112 / 108</strong> in India).
          </p>
        </div>

        {/* Accreditation and DPDP Compliance */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500 dark:text-slate-400">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-teal-600 dark:text-teal-400" />
            <span>DPDP Act 2023 Compliant • AES-256 Encrypted PII • Zero Tracking Logs</span>
          </div>
          <div>
            <span>Clinical protocols grounded in ICMR (2023), WHO SEAR & ADA (2024) Guidelines</span>
          </div>
        </div>

        <div className="text-center text-xs text-slate-400 dark:text-slate-600 pt-2 border-t border-slate-200 dark:border-slate-800">
          &copy; {new Date().getFullYear()} Sanjivani AI Health Informatics Platform. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
