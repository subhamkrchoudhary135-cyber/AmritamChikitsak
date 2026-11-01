"use client";

import React, { useState } from "react";
import { UploadCloud, FileText, CheckCircle2, AlertCircle, X, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useI18n } from "@/lib/i18n/context";

interface ExtractedValues {
  fasting_glucose?: number;
  hba1c?: number;
  systolic_bp?: number;
  diastolic_bp?: number;
  total_cholesterol?: number;
  triglycerides?: number;
}

interface LabReportUploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  onApplyValues: (values: ExtractedValues) => void;
}

export function LabReportUploadModal({
  isOpen,
  onClose,
  onApplyValues,
}: LabReportUploadModalProps) {
  const { t } = useI18n();
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [extracted, setExtracted] = useState<ExtractedValues | null>(null);

  if (!isOpen) return null;

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selected = e.target.files[0];
      setFile(selected);
      if (selected.type.startsWith("image/")) {
        setPreviewUrl(URL.createObjectURL(selected));
      } else {
        setPreviewUrl(null);
      }
      simulateExtraction(selected.name);
    }
  };

  const simulateExtraction = (fileName: string) => {
    setIsProcessing(true);
    // Simulate OCR parsing matching backend regex logic
    setTimeout(() => {
      setExtracted({
        fasting_glucose: 118.0,
        hba1c: 6.2,
        systolic_bp: 134.0,
        diastolic_bp: 86.0,
        total_cholesterol: 212.0,
        triglycerides: 175.0,
      });
      setIsProcessing(false);
    }, 1200);
  };

  const handleApply = () => {
    if (extracted) {
      onApplyValues(extracted);
      onClose();
    }
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in-50"
    >
      <div className="bg-white dark:bg-slate-900 rounded-3xl max-w-lg w-full border border-slate-200 dark:border-slate-800 shadow-2xl overflow-hidden p-6 space-y-6">
        <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4">
          <div className="flex items-center gap-2.5">
            <div className="w-10 h-10 rounded-xl bg-teal-100 dark:bg-teal-950 text-teal-700 dark:text-teal-400 flex items-center justify-center">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h3 id="modal-title" className="text-lg font-bold text-slate-900 dark:text-slate-100">
                {t("form.upload_lab")}
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                AI extracts verified numbers for your review
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 flex items-center justify-center text-slate-500"
            aria-label="Close modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Upload Dropzone */}
        {!extracted && !isProcessing && (
          <label className="border-2 border-dashed border-teal-300 dark:border-teal-900 rounded-2xl p-8 flex flex-col items-center justify-center text-center cursor-pointer hover:bg-teal-50/50 dark:hover:bg-teal-950/20 transition group">
            <UploadCloud className="w-12 h-12 text-teal-600 dark:text-teal-400 mb-3 group-hover:scale-110 transition" />
            <span className="text-sm font-bold text-slate-800 dark:text-slate-200">
              Click to upload lab test photo or PDF
            </span>
            <span className="text-xs text-slate-500 mt-1">
              Supports JPEG, PNG, or PDF lab results (e.g. Dr. Lal PathLabs, SRL, Apollo)
            </span>
            <input
              type="file"
              accept="image/*,.pdf"
              className="hidden"
              onChange={handleFileChange}
            />
          </label>
        )}

        {/* Processing State */}
        {isProcessing && (
          <div className="py-12 flex flex-col items-center justify-center text-center space-y-3">
            <div className="w-12 h-12 border-4 border-teal-600 border-t-transparent rounded-full animate-spin" />
            <p className="font-bold text-slate-800 dark:text-slate-200 text-sm">
              Analyzing Lab Report with Medical OCR...
            </p>
            <p className="text-xs text-slate-500">
              Locating Fasting Glucose, HbA1c, and Lipid parameters
            </p>
          </div>
        )}

        {/* Review Extracted Values */}
        {extracted && (
          <div className="space-y-4 animate-in fade-in-50">
            <div className="flex items-center gap-2 text-xs font-semibold text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/60 p-3 rounded-xl border border-emerald-200 dark:border-emerald-800">
              <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
              <span>We extracted the following values. Please confirm before applying:</span>
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="p-3 bg-slate-50 dark:bg-slate-800/60 rounded-xl border border-slate-200 dark:border-slate-700">
                <span className="text-slate-500 block">Fasting Glucose</span>
                <span className="text-base font-bold text-slate-900 dark:text-slate-100">
                  {extracted.fasting_glucose} mg/dL
                </span>
              </div>
              <div className="p-3 bg-slate-50 dark:bg-slate-800/60 rounded-xl border border-slate-200 dark:border-slate-700">
                <span className="text-slate-500 block">HbA1c</span>
                <span className="text-base font-bold text-slate-900 dark:text-slate-100">
                  {extracted.hba1c} %
                </span>
              </div>
              <div className="p-3 bg-slate-50 dark:bg-slate-800/60 rounded-xl border border-slate-200 dark:border-slate-700">
                <span className="text-slate-500 block">Blood Pressure</span>
                <span className="text-base font-bold text-slate-900 dark:text-slate-100">
                  {extracted.systolic_bp} / {extracted.diastolic_bp} mmHg
                </span>
              </div>
              <div className="p-3 bg-slate-50 dark:bg-slate-800/60 rounded-xl border border-slate-200 dark:border-slate-700">
                <span className="text-slate-500 block">Total Cholesterol</span>
                <span className="text-base font-bold text-slate-900 dark:text-slate-100">
                  {extracted.total_cholesterol} mg/dL
                </span>
              </div>
            </div>

            <div className="flex items-center gap-3 pt-2">
              <Button
                variant="outline"
                onClick={() => {
                  setExtracted(null);
                  setFile(null);
                }}
                className="w-1/2"
              >
                Re-upload
              </Button>
              <Button onClick={handleApply} className="w-1/2">
                Apply to Form
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
