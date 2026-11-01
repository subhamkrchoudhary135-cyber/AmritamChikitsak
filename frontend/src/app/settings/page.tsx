"use client";

import React, { useState } from "react";
import { useI18n, Locale } from "@/lib/i18n/context";
import { api } from "@/lib/api";
import { Storage } from "@/lib/storage";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Settings as SettingsIcon,
  Shield,
  Download,
  Trash2,
  CheckCircle2,
  Globe,
  AlertTriangle,
  Lock,
} from "lucide-react";

export default function SettingsPage() {
  const { t, locale, setLocale } = useI18n();
  const [consentScreening, setConsentScreening] = useState(true);
  const [consentTimeline, setConsentTimeline] = useState(true);
  const [consentResearch, setConsentResearch] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [statusMessage, setStatusMessage] = useState<{ type: "success" | "error"; text: string } | null>(
    null
  );

  const handleExportData = async () => {
    setIsExporting(true);
    setStatusMessage(null);
    try {
      const history = await api.history.get("demo-pat-001");
      const blob = new Blob([JSON.stringify(history, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `sanjivani-health-records-${new Date().toISOString().slice(0, 10)}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setStatusMessage({ type: "success", text: "Health data successfully exported in JSON format." });
    } catch (e: any) {
      setStatusMessage({ type: "error", text: "Export failed: " + (e.message || "Unknown error") });
    } finally {
      setIsExporting(false);
    }
  };

  const handleDeleteData = async () => {
    const confirmed = window.confirm(
      "Are you absolutely sure? This will permanently erase all your health biometrics, screenings, and consent tokens pursuant to DPDP Act 2023 Sec. 12."
    );
    if (!confirmed) return;

    setIsDeleting(true);
    setStatusMessage(null);
    try {
      await api.consent.deleteData({
        patient_id: "demo-pat-001",
        confirmation: true,
        reason: "User requested Right to Erasure",
      });
      Storage.clearDraft();
      Storage.removeToken();
      if (typeof window !== "undefined") {
        localStorage.removeItem("sanjivani_last_result");
      }
      setStatusMessage({
        type: "success",
        text: "Right to Erasure honored: All your personal health records have been permanently purged.",
      });
    } catch (e: any) {
      setStatusMessage({ type: "error", text: "Deletion failed: " + (e.message || "Unknown error") });
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-8 pb-16">
      {/* Header */}
      <div className="border-b pb-6">
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-slate-100 flex items-center gap-2">
          <SettingsIcon className="h-7 w-7 text-medical-teal" />
          {t("settings.title", "Privacy & Account Settings")}
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
          Manage your personal data rights, language preferences, and DPDP Act 2023 consents.
        </p>
      </div>

      {/* Status Alert */}
      {statusMessage && (
        <div
          className={`p-4 rounded-xl border text-sm flex items-center gap-3 ${
            statusMessage.type === "success"
              ? "bg-emerald-50 text-emerald-800 border-emerald-200 dark:bg-emerald-950 dark:text-emerald-200 dark:border-emerald-800"
              : "bg-red-50 text-red-800 border-red-200 dark:bg-red-950 dark:text-red-200 dark:border-red-800"
          }`}
        >
          {statusMessage.type === "success" ? (
            <CheckCircle2 className="h-5 w-5 text-emerald-600 flex-shrink-0" />
          ) : (
            <AlertTriangle className="h-5 w-5 text-red-600 flex-shrink-0" />
          )}
          <span>{statusMessage.text}</span>
        </div>
      )}

      {/* Language Preference Card */}
      <Card className="border-slate-200 dark:border-slate-800 shadow-sm">
        <CardHeader className="pb-4 border-b">
          <CardTitle className="text-lg flex items-center gap-2">
            <Globe className="h-5 w-5 text-medical-teal" />
            Language Preference
          </CardTitle>
          <CardDescription>
            Select your preferred interface language. Explanations and voice prompts adapt automatically.
          </CardDescription>
        </CardHeader>
        <CardContent className="p-6">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {[
              { code: "en" as Locale, label: "English", desc: "English (India)" },
              { code: "hi" as Locale, label: "हिन्दी", desc: "Hindi (हिन्दी)" },
              { code: "pa" as Locale, label: "ਪੰਜਾਬੀ", desc: "Punjabi (ਪੰਜਾਬੀ)" },
            ].map((item) => (
              <button
                key={item.code}
                type="button"
                onClick={() => setLocale(item.code)}
                className={`p-4 rounded-xl border text-left transition-all ${
                  locale === item.code
                    ? "border-medical-teal bg-teal-50/60 dark:bg-teal-950/40 ring-2 ring-medical-teal/30 font-semibold"
                    : "border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-900"
                }`}
              >
                <p className="text-base font-bold text-slate-900 dark:text-slate-100">{item.label}</p>
                <p className="text-xs text-slate-500 mt-0.5">{item.desc}</p>
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* DPDP Act 2023 Consent Management */}
      <Card className="border-medical-teal/20 shadow-sm">
        <CardHeader className="pb-4 border-b">
          <div className="flex items-center gap-2">
            <Shield className="h-5 w-5 text-medical-teal" />
            <div>
              <CardTitle className="text-lg">DPDP Act 2023 Consent Management</CardTitle>
              <CardDescription>
                Under India's Digital Personal Data Protection Act, you maintain granular control over your health information.
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="p-6 space-y-5">
          <div className="flex items-start justify-between gap-4">
            <div className="space-y-0.5">
              <p className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                AI Health Risk Screening Consent
              </p>
              <p className="text-xs text-slate-500">
                Process health biometrics for calculating cardiometabolic risk scores.
              </p>
            </div>
            <input
              type="checkbox"
              className="mt-1 h-5 w-5 rounded border-slate-300 text-medical-teal focus:ring-medical-teal"
              checked={consentScreening}
              onChange={(e) => setConsentScreening(e.target.checked)}
            />
          </div>

          <div className="flex items-start justify-between gap-4 pt-3 border-t">
            <div className="space-y-0.5">
              <p className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                Longitudinal Health Record Timeline
              </p>
              <p className="text-xs text-slate-500">
                Save multi-month historical screenings to compute progression trajectories.
              </p>
            </div>
            <input
              type="checkbox"
              className="mt-1 h-5 w-5 rounded border-slate-300 text-medical-teal focus:ring-medical-teal"
              checked={consentTimeline}
              onChange={(e) => setConsentTimeline(e.target.checked)}
            />
          </div>

          <div className="flex items-start justify-between gap-4 pt-3 border-t">
            <div className="space-y-0.5">
              <p className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                Anonymized Research Contribution (Optional)
              </p>
              <p className="text-xs text-slate-500">
                Help advance South Asian metabolic research using strictly de-identified datasets.
              </p>
            </div>
            <input
              type="checkbox"
              className="mt-1 h-5 w-5 rounded border-slate-300 text-medical-teal focus:ring-medical-teal"
              checked={consentResearch}
              onChange={(e) => setConsentResearch(e.target.checked)}
            />
          </div>
        </CardContent>
      </Card>

      {/* Data Export & Right to Erasure */}
      <Card className="border-slate-200 dark:border-slate-800 shadow-sm">
        <CardHeader className="pb-4 border-b">
          <CardTitle className="text-lg flex items-center gap-2">
            <Lock className="h-5 w-5 text-medical-teal" />
            Data Portability & Erasure
          </CardTitle>
          <CardDescription>
            Exercise your statutory rights under the Digital Personal Data Protection Act 2023.
          </CardDescription>
        </CardHeader>

        <CardContent className="p-6 space-y-6">
          {/* Export Data */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="space-y-1">
              <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                {t("settings.export_title", "Export My Health Data")}
              </h3>
              <p className="text-xs text-slate-500">
                {t("settings.export_desc", "Download all your screening records in open JSON format.")}
              </p>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={handleExportData}
              disabled={isExporting}
              className="text-xs gap-1.5 self-start sm:self-auto"
            >
              <Download className="h-4 w-4" />
              {isExporting ? "Exporting..." : t("settings.btn_export", "Export Data (JSON)")}
            </Button>
          </div>

          {/* Delete Account */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pt-4 border-t">
            <div className="space-y-1">
              <h3 className="text-sm font-semibold text-red-600 flex items-center gap-1.5">
                <AlertTriangle className="h-4 w-4" />
                {t("settings.delete_title", "Right to Erasure (DPDP Act Sec. 12)")}
              </h3>
              <p className="text-xs text-slate-500">
                {t(
                  "settings.delete_desc",
                  "Permanently purge all your personal identity, biometric screenings, and consent records."
                )}
              </p>
            </div>
            <Button
              variant="destructive"
              size="sm"
              onClick={handleDeleteData}
              disabled={isDeleting}
              className="text-xs gap-1.5 self-start sm:self-auto"
            >
              <Trash2 className="h-4 w-4" />
              {isDeleting ? "Erasing..." : t("settings.btn_delete", "Permanently Delete My Data")}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
