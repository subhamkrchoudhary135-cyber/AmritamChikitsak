/**
 * Offline Draft Storage & PWA Synchronization Manager
 * Saves screening draft progress locally and syncs when back online.
 */

const STORAGE_KEYS = {
  SCREENING_DRAFT: "sanjivani_screening_draft",
  USER_LOCALE: "sanjivani_user_locale",
  AUTH_TOKEN: "sanjivani_auth_token",
  OFFLINE_QUEUE: "sanjivani_offline_queue",
  THEME: "sanjivani_theme",
};

export const Storage = {
  saveDraft: (data: unknown) => {
    if (typeof window === "undefined") return;
    try {
      localStorage.setItem(STORAGE_KEYS.SCREENING_DRAFT, JSON.stringify(data));
    } catch (e) {
      console.warn("Storage quota exceeded or disabled", e);
    }
  },

  getDraft: <T>(): T | null => {
    if (typeof window === "undefined") return null;
    try {
      const item = localStorage.getItem(STORAGE_KEYS.SCREENING_DRAFT);
      return item ? JSON.parse(item) : null;
    } catch {
      return null;
    }
  },

  clearDraft: () => {
    if (typeof window === "undefined") return;
    localStorage.removeItem(STORAGE_KEYS.SCREENING_DRAFT);
  },

  getLocale: (fallback: string = "en"): string => {
    if (typeof window === "undefined") return fallback;
    return localStorage.getItem(STORAGE_KEYS.USER_LOCALE) || fallback;
  },

  setLocale: (locale: string) => {
    if (typeof window === "undefined") return;
    localStorage.setItem(STORAGE_KEYS.USER_LOCALE, locale);
  },

  getToken: (): string | null => {
    if (typeof window === "undefined") return null;
    return localStorage.getItem(STORAGE_KEYS.AUTH_TOKEN);
  },

  setToken: (token: string) => {
    if (typeof window === "undefined") return;
    localStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, token);
  },

  removeToken: () => {
    if (typeof window === "undefined") return;
    localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN);
  },
};
