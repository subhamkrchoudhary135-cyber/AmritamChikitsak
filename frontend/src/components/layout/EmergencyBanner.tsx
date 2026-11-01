"use client";

import React from "react";
import { PhoneCall, AlertTriangle } from "lucide-react";
import { useI18n } from "@/lib/i18n/context";

export function EmergencyBanner() {
  const { t } = useI18n();

  return (
    <div
      role="region"
      aria-label="Emergency Medical Helpline"
      className="bg-red-700 text-white px-4 py-2 text-xs sm:text-sm font-semibold flex items-center justify-between shadow-md"
    >
      <div className="flex items-center gap-2 max-w-xl">
        <AlertTriangle className="w-4 h-4 text-amber-300 flex-shrink-0" />
        <span className="truncate">
          {t("disclaimer_banner")}
        </span>
      </div>
      <div className="flex items-center gap-2 flex-shrink-0">
        <a
          href="tel:112"
          className="inline-flex items-center gap-1.5 bg-white text-red-700 px-3 py-1 rounded-full text-xs font-bold hover:bg-red-50 transition active:scale-95"
          aria-label="Call emergency number 112"
        >
          <PhoneCall className="w-3.5 h-3.5" />
          <span>112 (All India)</span>
        </a>
        <a
          href="tel:108"
          className="hidden sm:inline-flex items-center gap-1.5 bg-red-800 text-white px-3 py-1 rounded-full text-xs font-bold hover:bg-red-900 transition active:scale-95"
          aria-label="Call ambulance number 108"
        >
          <span>108 (Ambulance)</span>
        </a>
      </div>
    </div>
  );
}
