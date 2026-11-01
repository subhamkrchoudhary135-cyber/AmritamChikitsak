"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useI18n } from "@/lib/i18n/context";
import { api, ScreeningInput, ScreeningResponse } from "@/lib/api";
import { Storage } from "@/lib/storage";
import { UnitConverters } from "@/lib/utils";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Progress } from "@/components/ui/progress";
import { LabReportUploadModal } from "@/components/screening/LabReportUploadModal";
import { VoiceInputButton } from "@/components/shared/VoiceInputButton";
import {
  Activity,
  Heart,
  FileText,
  User,
  ShieldAlert,
  Sparkles,
  ArrowRight,
  ArrowLeft,
  CheckCircle2,
  AlertTriangle,
  UploadCloud,
  Scale,
  RotateCcw,
} from "lucide-react";

const TOTAL_STEPS = 4;

const DEFAULT_FORM: ScreeningInput = {
  age: 45,
  gender: "male",
  height_cm: 168,
  weight_kg: 72,
  bmi: 25.5,
  waist_circumference_cm: 88,
  systolic_bp: 128,
  diastolic_bp: 82,
  resting_heart_rate: 76,
  fasting_glucose: 110,
  hba1c: 5.9,
  total_cholesterol: 195,
  ldl_cholesterol: 118,
  hdl_cholesterol: 42,
  triglycerides: 165,
  physical_activity_hours_per_week: 2.0,
  smoking_status: "never",
  alcohol_consumption: "occasional",
  diet_type: "vegetarian",
  family_history_diabetes: true,
  family_history_heart_disease: false,
  chest_pain_present: false,
  shortness_of_breath_severe: false,
  stroke_signs_fast: false,
  symptoms_free_text: "",
  preferred_language: "en",
};

export default function ScreeningPage() {
  const router = useRouter();
  const { t, locale } = useI18n();
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState<ScreeningInput>(DEFAULT_FORM);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isOcrOpen, setIsOcrOpen] = useState(false);
  const [glucoseUnit, setGlucoseUnit] = useState<"mg/dl" | "mmol/l">("mg/dl");
  const [weightUnit, setWeightUnit] = useState<"kg" | "lbs">("kg");

  // Load saved draft or initialize
  useEffect(() => {
    const savedDraft = Storage.getDraft<ScreeningInput>();
    if (savedDraft) {
      setFormData(savedDraft);
    }
  }, []);

  // Update BMI whenever height or weight changes
  useEffect(() => {
    if (formData.height_cm > 0 && formData.weight_kg > 0) {
      const computedBmi = UnitConverters.calculateBmi(formData.weight_kg, formData.height_cm);
      setFormData((prev) => ({ ...prev, bmi: computedBmi }));
    }
  }, [formData.height_cm, formData.weight_kg]);

  // Sync draft to storage on change
  const updateField = <K extends keyof ScreeningInput>(field: K, value: ScreeningInput[K]) => {
    setFormData((prev) => {
      const updated = { ...prev, [field]: value };
      Storage.saveDraft(updated);
      return updated;
    });
  };

  const handleNext = () => {
    setErrorMessage(null);
    if (step < TOTAL_STEPS) {
      setStep((s) => s + 1);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  const handleBack = () => {
    setErrorMessage(null);
    if (step > 1) {
      setStep((s) => s - 1);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  const handleApplyOcrValues = (extracted: any) => {
    setFormData((prev) => {
      const updated = {
        ...prev,
        fasting_glucose: extracted.fasting_glucose ?? prev.fasting_glucose,
        hba1c: extracted.hba1c ?? prev.hba1c,
        systolic_bp: extracted.systolic_bp ?? prev.systolic_bp,
        diastolic_bp: extracted.diastolic_bp ?? prev.diastolic_bp,
        total_cholesterol: extracted.total_cholesterol ?? prev.total_cholesterol,
        triglycerides: extracted.triglycerides ?? prev.triglycerides,
      };
      Storage.saveDraft(updated);
      return updated;
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setErrorMessage(null);

    try {
      const payload: ScreeningInput = {
        ...formData,
        preferred_language: locale as "en" | "hi" | "pa",
      };

      const result: ScreeningResponse = await api.screenings.submit(payload);

      // Save latest result in localStorage for instant rendering on results page
      if (typeof window !== "undefined") {
        localStorage.setItem("sanjivani_last_result", JSON.stringify(result));
      }

      // Clear draft on successful completion
      Storage.clearDraft();

      // Navigate to results page
      router.push(`/results?id=${result.screening_id}`);
    } catch (err: any) {
      console.error("Screening submission failed:", err);
      setErrorMessage(
        err.message || "Failed to analyze risk. Please check your network connection and try again."
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  const progressPercent = (step / TOTAL_STEPS) * 100;

  return (
    <div className="max-w-3xl mx-auto space-y-6 pb-12">
      {/* Title & Progress Header */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-slate-100 flex items-center gap-2">
              <Activity className="h-7 w-7 text-medical-teal" />
              {t("nav.screen", "AI Health Risk Screening")}
            </h1>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Validated on ICMR 2023 & WHO SEAR South Asian cardiometabolic criteria.
            </p>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              setFormData(DEFAULT_FORM);
              Storage.clearDraft();
            }}
            className="text-xs text-slate-500 hover:text-slate-700"
          >
            <RotateCcw className="h-3.5 w-3.5 mr-1" />
            Reset Form
          </Button>
        </div>

        {/* Step Progress Bar */}
        <div className="space-y-1.5">
          <div className="flex justify-between text-xs font-semibold text-slate-500">
            <span>
              Step {step} of {TOTAL_STEPS}:{" "}
              {step === 1 && t("form.step_demographics", "Demographics & Body Measurements")}
              {step === 2 && t("form.step_vitals", "Blood Pressure & Vitals")}
              {step === 3 && t("form.step_glycemic", "Blood Sugar & Lipid Profile")}
              {step === 4 && t("form.step_lifestyle", "Lifestyle & Clinical Symptoms")}
            </span>
            <span>{Math.round(progressPercent)}% completed</span>
          </div>
          <Progress value={progressPercent} className="h-2" />
        </div>
      </div>

      {/* Error Banner */}
      {errorMessage && (
        <div className="p-4 rounded-xl bg-red-50 dark:bg-red-950/60 border border-red-200 dark:border-red-800 text-red-800 dark:text-red-200 text-sm flex items-start gap-3">
          <AlertTriangle className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
          <div>
            <p className="font-semibold">Unable to complete screening</p>
            <p>{errorMessage}</p>
          </div>
        </div>
      )}

      {/* Form Card */}
      <Card className="border-medical-teal/20 shadow-md overflow-hidden">
        <form onSubmit={handleSubmit}>
          {/* STEP 1: Demographics & Anthropometrics */}
          {step === 1 && (
            <div className="p-6 space-y-6">
              <CardHeader className="p-0 pb-4 border-b">
                <CardTitle className="text-lg flex items-center gap-2">
                  <User className="h-5 w-5 text-medical-teal" />
                  Step 1: {t("form.step_demographics", "Demographics & Body Measurements")}
                </CardTitle>
                <CardDescription>
                  Indian cut-offs apply (e.g. BMI ≥ 23 kg/m² indicates overweight for South Asians).
                </CardDescription>
              </CardHeader>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-5 pt-2">
                {/* Age */}
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                    {t("form.age", "Age (years)")} *
                  </label>
                  <Input
                    type="number"
                    min={18}
                    max={120}
                    required
                    value={formData.age}
                    onChange={(e) => updateField("age", Number(e.target.value))}
                  />
                  <span className="text-xs text-slate-500">Target cohort: 18 - 85 years</span>
                </div>

                {/* Biological Sex */}
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                    {t("form.gender", "Biological Sex")} *
                  </label>
                  <select
                    className="w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm focus:border-medical-teal focus:outline-none focus:ring-1 focus:ring-medical-teal dark:border-slate-800 dark:bg-slate-950 dark:text-slate-100"
                    value={formData.gender}
                    onChange={(e) => updateField("gender", e.target.value as any)}
                  >
                    <option value="male">{t("form.male", "Male")}</option>
                    <option value="female">{t("form.female", "Female")}</option>
                    <option value="other">{t("form.other", "Other")}</option>
                  </select>
                </div>

                {/* Height */}
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                      {t("form.height", "Height (cm)")} *
                    </label>
                    <span className="text-xs text-slate-500">
                      ≈ {UnitConverters.cmToFeetInches(formData.height_cm).feet} ft{" "}
                      {UnitConverters.cmToFeetInches(formData.height_cm).inches} in
                    </span>
                  </div>
                  <Input
                    type="number"
                    min={100}
                    max={250}
                    required
                    value={formData.height_cm}
                    onChange={(e) => updateField("height_cm", Number(e.target.value))}
                  />
                </div>

                {/* Weight */}
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                      {t("form.weight", "Weight")} ({weightUnit}) *
                    </label>
                    <button
                      type="button"
                      onClick={() => setWeightUnit(weightUnit === "kg" ? "lbs" : "kg")}
                      className="text-xs text-medical-teal hover:underline font-medium"
                    >
                      Switch to {weightUnit === "kg" ? "lbs" : "kg"}
                    </button>
                  </div>
                  <Input
                    type="number"
                    min={30}
                    max={250}
                    required
                    value={
                      weightUnit === "kg"
                        ? formData.weight_kg
                        : UnitConverters.kgToLbs(formData.weight_kg)
                    }
                    onChange={(e) => {
                      const val = Number(e.target.value);
                      updateField("weight_kg", weightUnit === "kg" ? val : UnitConverters.lbsToKg(val));
                    }}
                  />
                </div>

                {/* Waist Circumference */}
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                    Waist Circumference (cm)
                  </label>
                  <Input
                    type="number"
                    min={50}
                    max={180}
                    value={formData.waist_circumference_cm || ""}
                    placeholder="e.g. 88 cm"
                    onChange={(e) => updateField("waist_circumference_cm", Number(e.target.value))}
                  />
                  <span className="text-xs text-slate-500">
                    ICMR cut-off: &gt;90cm (Men), &gt;80cm (Women) indicates central adiposity
                  </span>
                </div>

                {/* Live Computed BMI Card */}
                <div className="space-y-2 flex flex-col justify-end">
                  <div className="p-3.5 rounded-lg bg-teal-50 dark:bg-teal-950/40 border border-teal-200 dark:border-teal-800 flex items-center justify-between">
                    <div>
                      <p className="text-xs font-semibold text-teal-800 dark:text-teal-300">
                        Computed Body Mass Index (BMI)
                      </p>
                      <p className="text-xs text-teal-600 dark:text-teal-400">
                        {formData.bmi && formData.bmi < 18.5
                          ? "Underweight (< 18.5)"
                          : formData.bmi && formData.bmi < 23
                          ? "Healthy / Normal (18.5 - 22.9)"
                          : formData.bmi && formData.bmi < 27.5
                          ? "Overweight (23.0 - 27.4)"
                          : "Obese (≥ 27.5)"}
                      </p>
                    </div>
                    <div className="text-right">
                      <span className="text-2xl font-black text-teal-900 dark:text-teal-100">
                        {formData.bmi || "--"}
                      </span>
                      <span className="text-xs text-teal-700 dark:text-teal-300 block">kg/m²</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* STEP 2: Blood Pressure & Vitals */}
          {step === 2 && (
            <div className="p-6 space-y-6">
              <CardHeader className="p-0 pb-4 border-b">
                <CardTitle className="text-lg flex items-center gap-2">
                  <Heart className="h-5 w-5 text-medical-teal" />
                  Step 2: {t("form.step_vitals", "Blood Pressure & Vitals")}
                </CardTitle>
                <CardDescription>
                  Accurate blood pressure measurement is essential for stroke and infarction screening.
                </CardDescription>
              </CardHeader>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-5 pt-2">
                {/* Systolic BP */}
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                      {t("form.systolic_bp", "Systolic Blood Pressure (mmHg)")} *
                    </label>
                    <VoiceInputButton
                      fieldLabel="Systolic BP"
                      onResult={(val) => {
                        const num = parseInt(val.replace(/\D/g, ""), 10);
                        if (!isNaN(num)) updateField("systolic_bp", num);
                      }}
                    />
                  </div>
                  <Input
                    type="number"
                    min={70}
                    max={260}
                    required
                    value={formData.systolic_bp}
                    onChange={(e) => updateField("systolic_bp", Number(e.target.value))}
                  />
                  <span className="text-xs text-slate-500">
                    Normal: &lt;120 mmHg | Stage 1: 130-139 | Crisis: ≥180
                  </span>
                </div>

                {/* Diastolic BP */}
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                      {t("form.diastolic_bp", "Diastolic Blood Pressure (mmHg)")} *
                    </label>
                    <VoiceInputButton
                      fieldLabel="Diastolic BP"
                      onResult={(val) => {
                        const num = parseInt(val.replace(/\D/g, ""), 10);
                        if (!isNaN(num)) updateField("diastolic_bp", num);
                      }}
                    />
                  </div>
                  <Input
                    type="number"
                    min={40}
                    max={160}
                    required
                    value={formData.diastolic_bp}
                    onChange={(e) => updateField("diastolic_bp", Number(e.target.value))}
                  />
                  <span className="text-xs text-slate-500">
                    Normal: &lt;80 mmHg | Stage 1: 80-89 | Crisis: ≥120
                  </span>
                </div>

                {/* Resting Heart Rate */}
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                    {t("form.heart_rate", "Resting Heart Rate (bpm)")}
                  </label>
                  <Input
                    type="number"
                    min={40}
                    max={200}
                    value={formData.resting_heart_rate || ""}
                    placeholder="e.g. 72 bpm"
                    onChange={(e) => updateField("resting_heart_rate", Number(e.target.value))}
                  />
                  <span className="text-xs text-slate-500">Healthy resting range: 60 - 100 bpm</span>
                </div>

                {/* BP Classification Guide Card */}
                <div className="p-3.5 rounded-lg bg-slate-50 dark:bg-slate-900 border text-xs space-y-1 flex flex-col justify-center">
                  <p className="font-semibold text-slate-700 dark:text-slate-200">
                    Current Reading Classification:
                  </p>
                  <p
                    className={
                      formData.systolic_bp >= 140 || formData.diastolic_bp >= 90
                        ? "text-orange-600 font-bold"
                        : formData.systolic_bp >= 130 || formData.diastolic_bp >= 80
                        ? "text-amber-600 font-bold"
                        : "text-emerald-600 font-bold"
                    }
                  >
                    {formData.systolic_bp >= 180 || formData.diastolic_bp >= 120
                      ? "⚠️ Hypertensive Crisis (Seek Emergency Care)"
                      : formData.systolic_bp >= 140 || formData.diastolic_bp >= 90
                      ? "Stage 2 Hypertension (ICMR Protocol)"
                      : formData.systolic_bp >= 130 || formData.diastolic_bp >= 80
                      ? "Stage 1 Hypertension"
                      : "Normotensive / Healthy"}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* STEP 3: Blood Sugar & Lipid Profile */}
          {step === 3 && (
            <div className="p-6 space-y-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b pb-4">
                <div>
                  <CardTitle className="text-lg flex items-center gap-2">
                    <FileText className="h-5 w-5 text-medical-teal" />
                    Step 3: {t("form.step_glycemic", "Blood Sugar & Lipid Profile")}
                  </CardTitle>
                  <CardDescription>
                    Enter your recent lab values or use our AI OCR reader to extract values automatically.
                  </CardDescription>
                </div>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setIsOcrOpen(true)}
                  className="bg-medical-teal/10 hover:bg-medical-teal/20 text-medical-teal border-medical-teal/30 text-xs font-semibold gap-1.5 self-start sm:self-auto"
                >
                  <UploadCloud className="h-4 w-4" />
                  {t("form.upload_lab", "Upload Lab PDF/Photo")}
                </Button>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-5 pt-2">
                {/* Fasting Glucose */}
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                      {t("form.fasting_glucose", "Fasting Blood Sugar")} ({glucoseUnit}) *
                    </label>
                    <button
                      type="button"
                      onClick={() => setGlucoseUnit(glucoseUnit === "mg/dl" ? "mmol/l" : "mg/dl")}
                      className="text-xs text-medical-teal hover:underline font-medium"
                    >
                      Switch to {glucoseUnit === "mg/dl" ? "mmol/L" : "mg/dL"}
                    </button>
                  </div>
                  <Input
                    type="number"
                    step={glucoseUnit === "mmol/l" ? "0.1" : "1"}
                    min={40}
                    max={500}
                    required
                    value={
                      glucoseUnit === "mg/dl"
                        ? formData.fasting_glucose
                        : UnitConverters.mgDlToMmolL(formData.fasting_glucose)
                    }
                    onChange={(e) => {
                      const val = Number(e.target.value);
                      updateField(
                        "fasting_glucose",
                        glucoseUnit === "mg/dl" ? val : UnitConverters.mmolLToMgDl(val)
                      );
                    }}
                  />
                  <span className="text-xs text-slate-500">
                    Normal: 70 - 99 mg/dL | Pre-diabetes: 100 - 125 | Diabetes: ≥126
                  </span>
                </div>

                {/* HbA1c */}
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                    {t("form.hba1c", "HbA1c (% - 3 Month Average)")}
                  </label>
                  <Input
                    type="number"
                    step="0.1"
                    min={4.0}
                    max={16.0}
                    value={formData.hba1c || ""}
                    placeholder="e.g. 5.9%"
                    onChange={(e) => updateField("hba1c", Number(e.target.value))}
                  />
                  <span className="text-xs text-slate-500">
                    Normal: &lt;5.7% | Pre-diabetes: 5.7 - 6.4% | Diabetes: ≥6.5%
                  </span>
                </div>

                {/* Total Cholesterol */}
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                    {t("form.cholesterol", "Total Cholesterol (mg/dL)")}
                  </label>
                  <Input
                    type="number"
                    min={80}
                    max={400}
                    value={formData.total_cholesterol || ""}
                    placeholder="e.g. 195"
                    onChange={(e) => updateField("total_cholesterol", Number(e.target.value))}
                  />
                  <span className="text-xs text-slate-500">Desirable: &lt;200 mg/dL</span>
                </div>

                {/* Triglycerides */}
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                    {t("form.triglycerides", "Triglycerides (mg/dL)")}
                  </label>
                  <Input
                    type="number"
                    min={40}
                    max={600}
                    value={formData.triglycerides || ""}
                    placeholder="e.g. 165"
                    onChange={(e) => updateField("triglycerides", Number(e.target.value))}
                  />
                  <span className="text-xs text-slate-500">Normal: &lt;150 mg/dL</span>
                </div>
              </div>
            </div>
          )}

          {/* STEP 4: Lifestyle, Family History & Emergency Check */}
          {step === 4 && (
            <div className="p-6 space-y-6">
              <CardHeader className="p-0 pb-4 border-b">
                <CardTitle className="text-lg flex items-center gap-2">
                  <Sparkles className="h-5 w-5 text-medical-teal" />
                  Step 4: {t("form.step_lifestyle", "Lifestyle, Family History & Symptom Check")}
                </CardTitle>
                <CardDescription>
                  Identifies behavioral drivers and checks for acute red-flag symptoms.
                </CardDescription>
              </CardHeader>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-5 pt-2">
                {/* Physical Activity */}
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                    {t("form.activity", "Physical Activity (hours/week)")} *
                  </label>
                  <Input
                    type="number"
                    step="0.5"
                    min={0}
                    max={40}
                    required
                    value={formData.physical_activity_hours_per_week}
                    onChange={(e) =>
                      updateField("physical_activity_hours_per_week", Number(e.target.value))
                    }
                  />
                  <span className="text-xs text-slate-500">
                    ICMR/WHO target: ≥ 2.5 hours/week of moderate exercise
                  </span>
                </div>

                {/* Diet Type */}
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                    {t("form.diet", "Diet Type")}
                  </label>
                  <select
                    className="w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm focus:border-medical-teal focus:outline-none focus:ring-1 focus:ring-medical-teal dark:border-slate-800 dark:bg-slate-950 dark:text-slate-100"
                    value={formData.diet_type}
                    onChange={(e) => updateField("diet_type", e.target.value as any)}
                  >
                    <option value="vegetarian">Vegetarian</option>
                    <option value="non_vegetarian">Non-Vegetarian</option>
                    <option value="vegan">Vegan</option>
                    <option value="other">Other</option>
                  </select>
                </div>

                {/* Smoking Habit */}
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                    {t("form.smoking", "Smoking Habit")}
                  </label>
                  <select
                    className="w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm focus:border-medical-teal focus:outline-none focus:ring-1 focus:ring-medical-teal dark:border-slate-800 dark:bg-slate-950 dark:text-slate-100"
                    value={formData.smoking_status}
                    onChange={(e) => updateField("smoking_status", e.target.value as any)}
                  >
                    <option value="never">Never Smoked</option>
                    <option value="former">Former Smoker</option>
                    <option value="current">Current Smoker</option>
                  </select>
                </div>

                {/* Family History */}
                <div className="space-y-3 flex flex-col justify-center">
                  <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                    Family Medical History
                  </label>
                  <label className="flex items-center gap-2 text-sm cursor-pointer">
                    <input
                      type="checkbox"
                      className="rounded border-slate-300 text-medical-teal focus:ring-medical-teal"
                      checked={formData.family_history_diabetes}
                      onChange={(e) => updateField("family_history_diabetes", e.target.checked)}
                    />
                    <span>{t("form.family_diabetes", "First-degree relative with Diabetes")}</span>
                  </label>
                  <label className="flex items-center gap-2 text-sm cursor-pointer">
                    <input
                      type="checkbox"
                      className="rounded border-slate-300 text-medical-teal focus:ring-medical-teal"
                      checked={formData.family_history_heart_disease}
                      onChange={(e) => updateField("family_history_heart_disease", e.target.checked)}
                    />
                    <span>{t("form.family_heart", "First-degree relative with Heart Disease")}</span>
                  </label>
                </div>
              </div>

              {/* Acute Emergency Symptom Screen */}
              <div className="p-4 rounded-xl bg-amber-50/70 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800 space-y-3">
                <div className="flex items-center gap-2 text-amber-900 dark:text-amber-200 font-semibold text-sm">
                  <ShieldAlert className="h-5 w-5 text-amber-600" />
                  <span>Clinical Red-Flag Screening (Immediate Triage)</span>
                </div>
                <p className="text-xs text-amber-800 dark:text-amber-300">
                  Are you currently experiencing any of the following acute warning signs?
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                  <label className="flex items-center gap-2 text-xs bg-white dark:bg-slate-900 p-2.5 rounded-lg border cursor-pointer">
                    <input
                      type="checkbox"
                      className="rounded text-red-600 focus:ring-red-500"
                      checked={formData.chest_pain_present}
                      onChange={(e) => updateField("chest_pain_present", e.target.checked)}
                    />
                    <span>Chest pain / pressure</span>
                  </label>
                  <label className="flex items-center gap-2 text-xs bg-white dark:bg-slate-900 p-2.5 rounded-lg border cursor-pointer">
                    <input
                      type="checkbox"
                      className="rounded text-red-600 focus:ring-red-500"
                      checked={formData.shortness_of_breath_severe}
                      onChange={(e) => updateField("shortness_of_breath_severe", e.target.checked)}
                    />
                    <span>Severe breathlessness</span>
                  </label>
                  <label className="flex items-center gap-2 text-xs bg-white dark:bg-slate-900 p-2.5 rounded-lg border cursor-pointer">
                    <input
                      type="checkbox"
                      className="rounded text-red-600 focus:ring-red-500"
                      checked={formData.stroke_signs_fast}
                      onChange={(e) => updateField("stroke_signs_fast", e.target.checked)}
                    />
                    <span>FAST stroke signs (face/arm/speech)</span>
                  </label>
                </div>
              </div>

              {/* Free Text / Voice Symptom Notes */}
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                    Additional Symptoms or Health Observations (Optional)
                  </label>
                  <VoiceInputButton
                    fieldLabel="Symptoms"
                    onResult={(text) =>
                      updateField(
                        "symptoms_free_text",
                        (formData.symptoms_free_text ? formData.symptoms_free_text + " " : "") + text
                      )
                    }
                  />
                </div>
                <textarea
                  rows={2}
                  value={formData.symptoms_free_text || ""}
                  onChange={(e) => updateField("symptoms_free_text", e.target.value)}
                  placeholder="e.g. Mild dizziness when standing up quickly, occasional morning fatigue..."
                  className="w-full rounded-md border border-slate-300 bg-white p-3 text-sm text-slate-900 shadow-sm focus:border-medical-teal focus:outline-none focus:ring-1 focus:ring-medical-teal dark:border-slate-800 dark:bg-slate-950 dark:text-slate-100"
                />
              </div>
            </div>
          )}

          {/* Card Footer with Navigation Buttons */}
          <div className="p-4 sm:p-6 bg-slate-50 dark:bg-slate-900/50 border-t flex items-center justify-between">
            {step > 1 ? (
              <Button type="button" variant="outline" onClick={handleBack} disabled={isSubmitting}>
                <ArrowLeft className="h-4 w-4 mr-1.5" />
                {t("form.btn_back", "Back")}
              </Button>
            ) : (
              <div />
            )}

            {step < TOTAL_STEPS ? (
              <Button type="button" onClick={handleNext} className="bg-medical-teal hover:bg-teal-700">
                {t("form.btn_next", "Next Step")}
                <ArrowRight className="h-4 w-4 ml-1.5" />
              </Button>
            ) : (
              <Button
                type="submit"
                disabled={isSubmitting}
                className="bg-medical-teal hover:bg-teal-700 text-white font-semibold shadow-lg shadow-teal-700/20"
              >
                {isSubmitting ? (
                  <span className="flex items-center gap-2">
                    <span className="h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    Computing Risk with AI...
                  </span>
                ) : (
                  <span className="flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4" />
                    {t("form.btn_submit", "Analyze My Health Risk")}
                  </span>
                )}
              </Button>
            )}
          </div>
        </form>
      </Card>

      {/* OCR Modal */}
      <LabReportUploadModal
        isOpen={isOcrOpen}
        onClose={() => setIsOcrOpen(false)}
        onApplyValues={handleApplyOcrValues}
      />
    </div>
  );
}
