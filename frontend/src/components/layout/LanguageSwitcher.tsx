"use client";

import React, { useState } from "react";
import { Globe, Check } from "lucide-react";
import { useI18n, Locale } from "@/lib/i18n/context";

export function LanguageSwitcher() {
  const { locale, setLocale, t } = useI18n();
  const [isOpen, setIsOpen] = useState(false);

  const languages: { code: Locale; label: string; native: string }[] = [
    { code: "en", label: "English", native: "English" },
    { code: "hi", label: "Hindi", native: "हिन्दी" },
    { code: "pa", label: "Punjabi", native: "ਪੰਜਾਬੀ" },
  ];

  const current = languages.find((l) => l.code === locale) || languages[0];

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="inline-flex items-center gap-2 h-10 px-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-sm font-semibold text-slate-800 dark:text-slate-100 hover:bg-slate-50 dark:hover:bg-slate-800 transition active:scale-95 shadow-sm"
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        aria-label="Select preferred language"
      >
        <Globe className="w-4 h-4 text-teal-600 dark:text-teal-400" />
        <span>{current.native}</span>
      </button>

      {isOpen && (
        <>
          <div
            className="fixed inset-0 z-40"
            onClick={() => setIsOpen(false)}
          />
          <ul
            role="listbox"
            className="absolute right-0 mt-2 w-44 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-xl z-50 py-1.5 overflow-hidden animate-in fade-in-50 zoom-in-95"
          >
            {languages.map((lang) => (
              <li
                key={lang.code}
                role="option"
                aria-selected={locale === lang.code}
                onClick={() => {
                  setLocale(lang.code);
                  setIsOpen(false);
                }}
                className={`flex items-center justify-between px-4 py-2.5 text-sm cursor-pointer transition-colors ${
                  locale === lang.code
                    ? "bg-teal-50 dark:bg-teal-950/80 font-bold text-teal-800 dark:text-teal-300"
                    : "text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800"
                }`}
              >
                <div>
                  <span className="block">{lang.native}</span>
                  <span className="text-xs text-slate-400 font-normal">{lang.label}</span>
                </div>
                {locale === lang.code && <Check className="w-4 h-4 text-teal-600" />}
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}
