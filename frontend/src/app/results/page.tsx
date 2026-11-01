"use client";

import React, { useState, useEffect, Suspense } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useI18n } from "@/lib/i18n/context";
import { api, ScreeningResponse, RiskLevel } from "@/lib/api";
import { RiskGauge } from "@/components/results/RiskGauge";
import { ShapBarChart } from "@/components/results/ShapBarChart";
import { ForecastChart } from "@/components/results/ForecastChart";
import { ClusterCard } from "@/components/results/ClusterCard";
import { DoctorCTAModal } from "@/components/chat/DoctorCTAModal";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Activity,
  FileDown,
  MessageSquare,
  Stethoscope,
  AlertTriangle,
  CheckCircle2,
  Calendar,
  Share2,
  RotateCcw,
  Sparkles,
  ArrowRight,
  ShieldAlert,
} from "lucide-react";

// Fallback baseline assessment if user navigates directly without screening ID
const DEMO_ASSESSMENT: ScreeningResponse = {
  screening_id: "scr-demo-99",
  patient_id: "pat-local-01",
  created_at: new Date().toISOString(),
  input_biometrics: {
    age: 48,
    gender: "male",
    height_cm: 168,
    weight_kg: 74,
    bmi: 26.2,
    systolic_bp: 136,
    diastolic_bp: 86,
    fasting_glucose: 114,
    hba1c: 6.0,
    physical_activity_hours_per_week: 1.5,
    smoking_status: "never",
    alcohol_consumption: "occasional",
    diet_type: "vegetarian",
    family_history_diabetes: true,
    family_history_heart_disease: false,
    preferred_language: "en",
  },
  conditions: {
    diabetes: {
      condition_name: "Type 2 Diabetes",
      risk_score: 0.64,
      calibrated_probability: 0.64,
      risk_level: "HIGH",
      decision_threshold: 0.35,
      is_screened_positive: true,
      confidence_interval: [0.52, 0.76],
      clinical_guideline_category: "Impaired Fasting Glucose (ICMR 2023 Criteria)",
    },
    heart_disease: {
      condition_name: "Coronary Heart Disease",
      risk_score: 0.42,
      calibrated_probability: 0.42,
      risk_level: "MODERATE",
      decision_threshold: 0.32,
      is_screened_positive: true,
      confidence_interval: [0.31, 0.55],
      clinical_guideline_category: "WHO SEAR Cardiovascular Risk Chart",
    },
    hypertension: {
      condition_name: "Hypertension",
      risk_score: 0.72,
      calibrated_probability: 0.72,
      risk_level: "HIGH",
      decision_threshold: 0.38,
      is_screened_positive: true,
      confidence_interval: [0.61, 0.83],
      clinical_guideline_category: "Stage 1 Hypertension (ICMR Protocol)",
    },
  },
  progression_forecast: {
    forecasted_glucose_3m: 117.2,
    forecasted_glucose_6m: 120.5,
    forecasted_systolic_bp_3m: 138.0,
    forecasted_systolic_bp_6m: 140.1,
    continuous_risk_score_100: 64,
    glucose_prediction_interval_6m: [115.0, 126.0],
    bp_prediction_interval_6m: [134.0, 146.5],
    trend_description: "Upward fasting glucose slope over 6 months without lifestyle modifications.",
  },
  phenotype: {
    cluster_id: 0,
    cluster_label: "Elevated BMI & Low Physical Activity",
    cluster_description: "Cohort Segment 0: Metabolic risk with sedentary habits",
    is_anomaly: false,
    anomaly_score: 0.12,
    pca_coordinates: [1.25, -0.45],
    lifestyle_priorities: [
      "Target 150 minutes of brisk walking weekly (30 mins x 5 days)",
      "Replace white rice with millets (bajra, jowar, ragi)",
      "Restrict dietary salt to < 5g per day",
    ],
  },
  top_shap_factors: [
    {
      feature: "fasting_glucose",
      feature_name_friendly: "Fasting Blood Sugar",
      patient_value: 114,
      impact_score: 0.34,
      direction: "increases_risk",
      clinical_reference: "70 - 99 mg/dL (Normal Fasting Range)",
      actionable_advice: "Avoid sugary tea and refined carbohydrates; consult doctor for HbA1c test.",
    },
    {
      feature: "systolic_bp",
      feature_name_friendly: "Systolic Blood Pressure",
      patient_value: 136,
      impact_score: 0.28,
      direction: "increases_risk",
      clinical_reference: "< 120 mmHg (Normal)",
      actionable_advice: "Cut table salt and pickles; practice pranayama or deep breathing daily.",
    },
    {
      feature: "bmi",
      feature_name_friendly: "Body Mass Index",
      patient_value: 26.2,
      impact_score: 0.21,
      direction: "increases_risk",
      clinical_reference: "18.5 - 22.9 kg/m² (ICMR Asian Indian Cut-off)",
      actionable_advice: "Aim for a 5-7% weight reduction through mindful portion control.",
    },
    {
      feature: "physical_activity_hours_per_week",
      feature_name_friendly: "Physical Activity",
      patient_value: 1.5,
      impact_score: 0.17,
      direction: "increases_risk",
      clinical_reference: ">= 2.5 hrs/week (ICMR / WHO Target)",
      actionable_advice: "Incorporate morning walks or cycling into your routine.",
    },
    {
      feature: "family_history_diabetes",
      feature_name_friendly: "Family History of Diabetes",
      patient_value: "Yes",
      impact_score: 0.14,
      direction: "increases_risk",
      clinical_reference: "Genetic Predisposition",
      actionable_advice: "Early lifestyle habits prevent expression of genetic risk.",
    },
  ],
  multilingual_explanations: {
    en: {
      language: "en",
      language_name: "English",
      headline: "Your Health Screening Summary: Actionable Prevention Plan",
      summary_overview:
        "This screening indicates your risk for diabetes or blood pressure strain is elevated. This is not a disease diagnosis, but an early chance to reverse the trend with daily habit changes.",
      top_factors_plain_text: [
        "Fasting Blood Sugar is higher than ideal (114 mg/dL).",
        "Systolic Blood Pressure indicates moderate vascular strain (136 mmHg).",
        "BMI is above the recommended Asian Indian threshold of 23.",
      ],
      actionable_steps: [
        "Walk briskly for 30 minutes every day.",
        "Cut sugar in tea and reduce fried snacks.",
        "Eat more whole pulses, green vegetables, and millets.",
        "Consult a doctor for formal clinical tests.",
      ],
      reading_level: "Class 8",
    },
    hi: {
      language: "hi",
      language_name: "हिन्दी",
      headline: "आपकी स्वास्थ्य जांच रिपोर्ट: समय रहते संभलने का अवसर",
      summary_overview:
        "इस जांच से पता चलता है कि शुगर और रक्तचाप (BP) का जोखिम बढ़ा हुआ है। यह कोई बीमारी का पक्का फैसला नहीं है, बल्कि जीवनशैली सुधारने का एक संकेत है।",
      top_factors_plain_text: [
        "खाली पेट शुगर का स्तर सामान्य से अधिक है।",
        "रक्तचाप (BP) में हल्का तनाव देखा गया है।",
        "भारतीय मानकों (BMI 23) के अनुसार वजन थोड़ा अधिक है।",
      ],
      actionable_steps: [
        "रोजाना 30 मिनट तेज कदमों से चलें।",
        "मीठी चाय और तली-भुनी चीजों से परहेज करें।",
        "भोजन में ज्वार, बाजरा, दालें और हरी सब्जियां बढ़ाएं।",
        "नजदीकी डॉक्टर से मिलकर सलाह लें।",
      ],
      reading_level: "Class 8",
    },
    pa: {
      language: "pa",
      language_name: "ਪੰਜਾਬੀ",
      headline: "ਤੁਹਾਡੀ ਸਿਹਤ ਜਾਂਚ ਰਿਪੋਰਟ: ਤੰਦਰੁਸਤੀ ਵੱਲ ਕਦਮ",
      summary_overview:
        "ਇਸ ਜਾਂਚ ਤੋਂ ਪਤਾ ਲੱਗਦਾ ਹੈ ਕਿ ਸ਼ੂਗਰ ਅਤੇ ਬਲੱਡ ਪ੍ਰੈਸ਼ਰ ਦਾ ਖ਼ਤਰਾ ਵਧਿਆ ਹੋਇਆ ਹੈ। ਇਹ ਕੋਈ ਬਿਮਾਰੀ ਨਹੀਂ ਹੈ, ਸਗੋਂ ਜੀਵਨ ਸ਼ੈਲੀ ਬਦਲਣ ਦੀ ਚੇਤਾਵਨੀ ਹੈ।",
      top_factors_plain_text: [
        "ਖਾਲੀ ਪੇਟ ਸ਼ੂਗਰ ਆਮ ਨਾਲੋਂ ਵੱਧ ਹੈ।",
        "ਬਲੱਡ ਪ੍ਰੈਸ਼ਰ ਵਿੱਚ ਵਾਧਾ ਦਰਜ ਕੀਤਾ ਗਿਆ ਹੈ।",
        "ਭਾਰਤ ਦੇ ਮਾਪਦੰਡਾਂ ਅਨੁਸਾਰ ਭਾਰ ਥੋੜ੍ਹਾ ਜ਼ਿਆਦਾ ਹੈ।",
      ],
      actionable_steps: [
        "ਹਰ ਰੋਜ਼ ਘੱਟੋ-ਘੱਟ 30 ਮਿੰਟ ਤੇਜ਼ ਸੈਰ ਕਰੋ।",
        "ਮਿੱਠੀ ਚਾਹ ਅਤੇ ਤਲੀਆਂ ਚੀਜ਼ਾਂ ਤੋਂ ਪਰਹੇਜ਼ ਰੱਖੋ।",
        "ਰੋਟੀ ਵਿੱਚ ਜਵਾਰ, ਬਾਜਰਾ ਅਤੇ ਮੱਕੀ ਸ਼ਾਮਲ ਕਰੋ।",
        "ਡਾਕਟਰ ਨੂੰ ਮਿਲ ਕੇ ਆਪਣੀ ਰੁਟੀਨ ਜਾਂਚ ਕਰਵਾਓ।",
      ],
      reading_level: "Class 8",
    },
  },
  emergency_alert: {
    is_emergency: false,
    emergency_triggers: [],
    triage_instruction: "No acute emergency red flags identified.",
    emergency_helpline_india: "112 / 108",
  },
  clinical_disclaimer:
    "DISCLAIMER: Sanjivani AI is an AI-powered screening support tool and NOT a diagnostic medical device. Consult a qualified medical practitioner.",
};

function ResultsContent() {
  const searchParams = useSearchParams();
  const { t, locale } = useI18n();
  const [data, setData] = useState<ScreeningResponse>(DEMO_ASSESSMENT);
  const [isDoctorModalOpen, setIsDoctorModalOpen] = useState(false);

  useEffect(() => {
    // Attempt to load from localStorage first (populated by /screen)
    if (typeof window !== "undefined") {
      const stored = localStorage.getItem("sanjivani_last_result");
      if (stored) {
        try {
          setData(JSON.parse(stored));
        } catch (e) {
          console.warn("Could not parse cached screening result", e);
        }
      }
    }
  }, []);

  const explanation =
    data.multilingual_explanations[locale as "en" | "hi" | "pa"] ||
    data.multilingual_explanations.en;

  const handleDownloadPdf = () => {
    const pdfUrl = api.reports.getPdfUrl(data.screening_id, locale);
    window.open(pdfUrl, "_blank");
  };

  return (
    <div className="space-y-8 pb-16">
      {/* Top Banner & Quick Actions */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b pb-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-medical-teal mb-1">
            <span className="px-2.5 py-0.5 rounded-full bg-teal-50 dark:bg-teal-950/60 border border-teal-200 dark:border-teal-800">
              ID: {data.screening_id}
            </span>
            <span className="flex items-center gap-1 text-slate-500">
              <Calendar className="h-3.5 w-3.5" />
              {new Date(data.created_at).toLocaleDateString()}
            </span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-slate-100">
            {t("results.title", "Your Health Risk Screening Assessment")}
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
            Risk stratification calibrated against ICMR-INDIAB & Framingham South Asian cohorts.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          <Button
            variant="outline"
            size="sm"
            onClick={handleDownloadPdf}
            className="text-xs font-semibold gap-1.5"
          >
            <FileDown className="h-4 w-4 text-medical-teal" />
            {t("results.btn_download_pdf", "Download PDF Report")}
          </Button>

          <Button
            size="sm"
            onClick={() => setIsDoctorModalOpen(true)}
            className="bg-medical-teal hover:bg-teal-700 text-white text-xs font-semibold gap-1.5 shadow-sm"
          >
            <Stethoscope className="h-4 w-4" />
            Book Doctor Teleconsult
          </Button>
        </div>
      </div>

      {/* Emergency Warning Banner if acute triggers identified */}
      {data.emergency_alert.is_emergency && (
        <div className="p-4 rounded-xl bg-red-600 text-white flex items-start gap-3 shadow-lg animate-pulse">
          <ShieldAlert className="h-6 w-6 flex-shrink-0" />
          <div className="space-y-1">
            <p className="font-bold text-base">EMERGENCY RED-FLAG ALERT</p>
            <p className="text-sm text-red-100">{data.emergency_alert.triage_instruction}</p>
            <p className="text-xs font-semibold bg-red-800/80 px-2.5 py-1 rounded inline-block mt-1">
              National Emergency Services: 112 / 108
            </p>
          </div>
        </div>
      )}

      {/* SECTION 1: Condition Risk Gauges */}
      <div className="space-y-3">
        <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
          <Activity className="h-5 w-5 text-medical-teal" />
          Cardiometabolic Risk Stratification
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {Object.entries(data.conditions).map(([key, cond]) => (
            <RiskGauge
              key={key}
              score={cond.risk_score}
              level={cond.risk_level}
              conditionName={cond.condition_name}
              threshold={cond.decision_threshold}
            />
          ))}
        </div>
      </div>

      {/* SECTION 2: Multilingual Class 8 Reading Summary */}
      <Card className="border-medical-teal/20 bg-gradient-to-br from-teal-50/40 via-white to-slate-50/30 dark:from-slate-900 dark:via-slate-900 dark:to-teal-950/20 shadow-sm">
        <CardHeader className="pb-3 border-b">
          <div className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-medical-teal" />
            <div>
              <CardTitle className="text-base sm:text-lg font-bold text-slate-900 dark:text-slate-100">
                {explanation.headline}
              </CardTitle>
              <CardDescription className="text-xs">
                Plain-language health interpretation (Reading Level: {explanation.reading_level})
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="p-5 sm:p-6 space-y-4">
          <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
            {explanation.summary_overview}
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
            <div className="p-4 rounded-lg bg-white dark:bg-slate-950 border space-y-2">
              <h3 className="text-xs font-bold text-slate-900 dark:text-slate-100 uppercase tracking-wider flex items-center gap-1.5">
                <AlertTriangle className="h-4 w-4 text-amber-500" />
                Key Observations
              </h3>
              <ul className="space-y-1.5 text-xs text-slate-600 dark:text-slate-400">
                {explanation.top_factors_plain_text.map((factor, i) => (
                  <li key={i} className="flex items-start gap-1.5">
                    <span className="text-medical-teal font-bold">•</span>
                    <span>{factor}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="p-4 rounded-lg bg-teal-50/70 dark:bg-teal-950/40 border border-teal-200 dark:border-teal-800 space-y-2">
              <h3 className="text-xs font-bold text-teal-900 dark:text-teal-200 uppercase tracking-wider flex items-center gap-1.5">
                <CheckCircle2 className="h-4 w-4 text-teal-600" />
                Daily Action Plan
              </h3>
              <ul className="space-y-1.5 text-xs text-teal-800 dark:text-teal-300">
                {explanation.actionable_steps.map((step, i) => (
                  <li key={i} className="flex items-start gap-1.5">
                    <span className="text-teal-600 font-bold">✓</span>
                    <span>{step}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* SECTION 3: SHAP Feature Importance & Phenotype Clustering */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <ShapBarChart factors={data.top_shap_factors} />
        </div>
        <div className="lg:col-span-1">
          <ClusterCard cluster={data.phenotype} />
        </div>
      </div>

      {/* SECTION 4: 3-6 Month Trajectory Forecast with Uncertainty */}
      <div className="space-y-3">
        <div>
          <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
            <Activity className="h-5 w-5 text-medical-teal" />
            {t("results.forecast_title", "3-6 Month Trajectory Forecast")}
          </h2>
          <p className="text-xs text-slate-500">
            {t(
              "results.forecast_subtitle",
              "With 90% Conformal Prediction uncertainty bounds calibrated on clinical trajectories"
            )}
          </p>
        </div>

        <ForecastChart
          forecast={data.progression_forecast}
          currentGlucose={data.input_biometrics.fasting_glucose}
          currentSystolicBp={data.input_biometrics.systolic_bp}
        />
      </div>

      {/* SECTION 5: Next Steps & Disclaimers */}
      <div className="p-6 rounded-2xl bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="space-y-1 text-center sm:text-left">
          <h3 className="text-base font-bold text-slate-900 dark:text-slate-100">
            Have questions about your report or numbers?
          </h3>
          <p className="text-xs text-slate-600 dark:text-slate-400">
            Our AI Doctor Assistant can explain terms, cite ICMR/WHO guidelines, or suggest regional diet alternatives.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Link href="/screen">
            <Button variant="outline" size="sm" className="text-xs">
              <RotateCcw className="h-3.5 w-3.5 mr-1" />
              New Screening
            </Button>
          </Link>
          <Link href="/chat">
            <Button size="sm" className="bg-medical-teal hover:bg-teal-700 text-white text-xs gap-1.5 shadow-sm">
              <MessageSquare className="h-3.5 w-3.5" />
              {t("results.btn_chat_assistant", "Ask AI Doctor Assistant")}
              <ArrowRight className="h-3.5 w-3.5" />
            </Button>
          </Link>
        </div>
      </div>

      {/* Teleconsultation Modal */}
      <DoctorCTAModal isOpen={isDoctorModalOpen} onClose={() => setIsDoctorModalOpen(false)} />
    </div>
  );
}

export default function ResultsPage() {
  return (
    <Suspense
      fallback={
        <div className="py-24 text-center space-y-3">
          <div className="h-8 w-8 border-3 border-medical-teal border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-sm text-slate-500">Loading screening assessment...</p>
        </div>
      }
    >
      <ResultsContent />
    </Suspense>
  );
}
