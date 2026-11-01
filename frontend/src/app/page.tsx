"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Activity,
  ShieldCheck,
  BrainCircuit,
  Languages,
  Clock,
  ArrowRight,
  HeartPulse,
  Stethoscope,
  CheckCircle2,
  AlertTriangle,
  FileText,
} from "lucide-react";
import { useI18n } from "@/lib/i18n/context";

export default function HomePage() {
  const { t } = useI18n();
  const router = useRouter();

  const [consentScreening, setConsentScreening] = useState(true);
  const [consentStorage, setConsentStorage] = useState(true);
  const [consentResearch, setConsentResearch] = useState(false);

  const handleStartScreening = () => {
    if (!consentScreening) {
      alert("Please consent to risk screening to proceed.");
      return;
    }
    router.push("/screen");
  };

  return (
    <div className="space-y-12 py-4">
      {/* Hero Section */}
      <section className="text-center max-w-4xl mx-auto space-y-6 pt-4">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-teal-100 dark:bg-teal-950/80 text-teal-800 dark:text-teal-300 text-xs sm:text-sm font-semibold border border-teal-200 dark:border-teal-800">
          <Activity className="w-4 h-4 text-teal-600" />
          <span>ICMR & WHO Guideline Aligned Screening Platform</span>
        </div>

        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-slate-900 dark:text-white leading-tight">
          Early Health Risk Screening for{" "}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-teal-600 to-emerald-600">
            Indian Adults
          </span>
        </h1>

        <p className="text-lg sm:text-xl text-slate-600 dark:text-slate-300 max-w-2xl mx-auto leading-relaxed">
          Screen your risk for Type 2 Diabetes, Heart Disease, and Hypertension in under 3 minutes with explainable AI, multilingual voice support, and longitudinal trajectory forecasts.
        </p>

        {/* Primary CTA Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
          <button
            onClick={handleStartScreening}
            className="w-full sm:w-auto px-8 py-4 rounded-xl bg-teal-700 hover:bg-teal-800 text-white font-bold text-base shadow-lg shadow-teal-700/25 transition active:scale-95 flex items-center justify-center gap-2"
          >
            <span>Start Free Health Screening</span>
            <ArrowRight className="w-5 h-5" />
          </button>

          <Link
            href="/chat"
            className="w-full sm:w-auto px-6 py-4 rounded-xl border border-slate-300 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 font-semibold text-slate-800 dark:text-slate-200 text-base transition flex items-center justify-center gap-2"
          >
            <BrainCircuit className="w-5 h-5 text-teal-600" />
            <span>Ask AI Health Assistant</span>
          </Link>
        </div>
      </section>

      {/* DPDP Act 2023 Consent & Trust Card */}
      <section className="max-w-3xl mx-auto rounded-2xl border border-teal-200 dark:border-teal-900/60 bg-gradient-to-b from-teal-50/50 to-white dark:from-teal-950/30 dark:to-slate-900 p-6 sm:p-8 shadow-sm space-y-6">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-xl bg-teal-700 text-white flex items-center justify-center shrink-0 shadow-md">
            <ShieldCheck className="w-7 h-7" />
          </div>
          <div className="space-y-1">
            <h2 className="text-xl font-bold text-slate-900 dark:text-white">
              {t("onboarding.dpdp_title", "DPDP Act 2023 Transparent Data Consent")}
            </h2>
            <p className="text-sm text-slate-600 dark:text-slate-300">
              {t(
                "onboarding.dpdp_body",
                "Under India's Digital Personal Data Protection Act 2023, your personal health information is protected. We encrypt your identity with AES-256 and never share your data without explicit permission."
              )}
            </p>
          </div>
        </div>

        <div className="space-y-3 pt-2">
          <label className="flex items-start gap-3 p-3 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/80 cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-800/50 transition">
            <input
              type="checkbox"
              checked={consentScreening}
              onChange={(e) => setConsentScreening(e.target.checked)}
              className="mt-1 w-4 h-4 text-teal-600 rounded border-slate-300 focus:ring-teal-500"
            />
            <span className="text-sm font-medium text-slate-800 dark:text-slate-200">
              {t(
                "onboarding.consent_screening",
                "I consent to processing my health biometrics for AI risk screening and 3-6 month forecasting."
              )}{" "}
              <span className="text-xs font-bold text-teal-700 dark:text-teal-400">(Required)</span>
            </span>
          </label>

          <label className="flex items-start gap-3 p-3 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/80 cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-800/50 transition">
            <input
              type="checkbox"
              checked={consentStorage}
              onChange={(e) => setConsentStorage(e.target.checked)}
              className="mt-1 w-4 h-4 text-teal-600 rounded border-slate-300 focus:ring-teal-500"
            />
            <span className="text-sm font-medium text-slate-800 dark:text-slate-200">
              {t(
                "onboarding.consent_storage",
                "I consent to securely storing my encrypted health check timeline."
              )}
            </span>
          </label>

          <label className="flex items-start gap-3 p-3 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/80 cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-800/50 transition">
            <input
              type="checkbox"
              checked={consentResearch}
              onChange={(e) => setConsentResearch(e.target.checked)}
              className="mt-1 w-4 h-4 text-teal-600 rounded border-slate-300 focus:ring-teal-500"
            />
            <span className="text-sm font-medium text-slate-800 dark:text-slate-200">
              {t(
                "onboarding.consent_anonymous_research",
                "I consent to anonymized, de-identified data use for advancing Indian health research (Optional)."
              )}
            </span>
          </label>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-2 border-t border-slate-200 dark:border-slate-800">
          <span className="text-xs text-slate-500 dark:text-slate-400">
            You can revoke consent or exercise your Right to Erasure anytime in Settings.
          </span>
          <button
            onClick={handleStartScreening}
            className="w-full sm:w-auto px-6 py-2.5 rounded-xl bg-teal-700 hover:bg-teal-800 text-white font-semibold text-sm transition"
          >
            {t("onboarding.cta_agree", "Agree & Proceed")}
          </button>
        </div>
      </section>

      {/* Feature Value Cards */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto">
        <div className="p-6 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 space-y-3">
          <div className="w-10 h-10 rounded-xl bg-amber-100 dark:bg-amber-950/80 text-amber-700 dark:text-amber-300 flex items-center justify-center">
            <Languages className="w-5 h-5" />
          </div>
          <h3 className="text-lg font-bold text-slate-900 dark:text-white">
            Multilingual in 3 Languages
          </h3>
          <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
            Accessible in English, हिन्दी (Hindi), and ਪੰਜਾਬੀ (Punjabi) with voice input and Class 8 reading level explanations tailored for rural and urban India.
          </p>
        </div>

        <div className="p-6 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 space-y-3">
          <div className="w-10 h-10 rounded-xl bg-teal-100 dark:bg-teal-950/80 text-teal-700 dark:text-teal-300 flex items-center justify-center">
            <BrainCircuit className="w-5 h-5" />
          </div>
          <h3 className="text-lg font-bold text-slate-900 dark:text-white">
            Explainable AI (SHAP)
          </h3>
          <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
            Never a black box. See the exact top 5 physiological factors driving your risk score, with actionable lifestyle modifications based on ICMR guidelines.
          </p>
        </div>

        <div className="p-6 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 space-y-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-100 dark:bg-emerald-950/80 text-emerald-700 dark:text-emerald-300 flex items-center justify-center">
            <Clock className="w-5 h-5" />
          </div>
          <h3 className="text-lg font-bold text-slate-900 dark:text-white">
            6-Month Progression Forecast
          </h3>
          <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
            Conformal prediction models project your blood sugar and blood pressure trajectories over 180 days with rigorous 90% statistical confidence bands.
          </p>
        </div>
      </section>

      {/* Statutory Clinical Notice */}
      <section className="max-w-4xl mx-auto p-4 rounded-xl border border-amber-300/80 dark:border-amber-900/60 bg-amber-50/60 dark:bg-amber-950/30 flex items-start gap-3">
        <AlertTriangle className="w-5 h-5 text-amber-700 dark:text-amber-400 shrink-0 mt-0.5" />
        <p className="text-xs sm:text-sm text-amber-900 dark:text-amber-200 leading-relaxed">
          <strong>Non-Diagnostic Disclaimer:</strong> Sanjivani AI is an artificial intelligence-powered risk screening support platform and does NOT provide a definitive medical diagnosis, prescribe pharmaceutical dosages, or replace evaluation by a licensed physician. If you experience acute symptoms like chest pain or shortness of breath, please dial <strong>112</strong> or <strong>108</strong> immediately.
        </p>
      </section>
    </div>
  );
}
