"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import en from "./en.json";
import hi from "./hi.json";
import pa from "./pa.json";
import { Storage } from "../storage";

export type Locale = "en" | "hi" | "pa";

const translations: Record<Locale, any> = { en, hi, pa };

interface I18nContextType {
  locale: Locale;
  setLocale: (loc: Locale) => void;
  t: (key: string, defaultVal?: string) => string;
  speechLanguage: string;
}

const I18nContext = createContext<I18nContextType | undefined>(undefined);

export function I18nProvider({ children }: { children: React.ReactNode }) {
  const [locale, setLocaleState] = useState<Locale>("en");

  useEffect(() => {
    const saved = Storage.getLocale("en") as Locale;
    if (saved && (saved === "en" || saved === "hi" || saved === "pa")) {
      setLocaleState(saved);
    }
  }, []);

  const setLocale = (loc: Locale) => {
    setLocaleState(loc);
    Storage.setLocale(loc);
  };

  const speechLanguage =
    locale === "hi" ? "hi-IN" : locale === "pa" ? "pa-IN" : "en-IN";

  const t = (path: string, defaultVal?: string): string => {
    const keys = path.split(".");
    let current = translations[locale];
    for (const k of keys) {
      if (current && typeof current === "object" && k in current) {
        current = current[k];
      } else {
        // Fallback to English
        let fallback = translations["en"];
        for (const fk of keys) {
          if (fallback && typeof fallback === "object" && fk in fallback) {
            fallback = fallback[fk];
          } else {
            return defaultVal || path;
          }
        }
        return typeof fallback === "string" ? fallback : defaultVal || path;
      }
    }
    return typeof current === "string" ? current : defaultVal || path;
  };

  return (
    <I18nContext.Provider value={{ locale, setLocale, t, speechLanguage }}>
      {children}
    </I18nContext.Provider>
  );
}

export function useI18n() {
  const context = useContext(I18nContext);
  if (!context) {
    throw new Error("useI18n must be used within an I18nProvider");
  }
  return context;
}
