"use client";

import React, { useState, useEffect } from "react";
import { Mic, MicOff } from "lucide-react";
import { useI18n } from "@/lib/i18n/context";

interface VoiceInputButtonProps {
  onResult: (text: string) => void;
  className?: string;
  fieldLabel?: string;
}

export function VoiceInputButton({ onResult, className, fieldLabel }: VoiceInputButtonProps) {
  const { speechLanguage, t } = useI18n();
  const [isListening, setIsListening] = useState(false);
  const [isSupported, setIsSupported] = useState(true);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const hasSpeech = "webkitSpeechRecognition" in window || "SpeechRecognition" in window;
      setIsSupported(hasSpeech);
    }
  }, []);

  const startListening = () => {
    if (typeof window === "undefined") return;

    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Speech recognition is not supported in this browser. Please use Chrome or Edge.");
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognition.lang = speechLanguage;
      recognition.interimResults = false;
      recognition.maxAlternatives = 1;

      recognition.onstart = () => {
        setIsListening(true);
      };

      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        // Clean speech text (e.g. extract numbers or words)
        onResult(transcript.trim());
        setIsListening(false);
      };

      recognition.onerror = (event: any) => {
        console.warn("Speech recognition error:", event.error);
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognition.start();
    } catch (e) {
      console.error("Speech recognition initialization failed:", e);
      setIsListening(false);
    }
  };

  if (!isSupported) return null;

  return (
    <button
      type="button"
      onClick={startListening}
      disabled={isListening}
      aria-label={`Voice input for ${fieldLabel || "field"}`}
      title={isListening ? t("form.listening") : t("form.voice_input")}
      className={`relative inline-flex items-center justify-center w-10 h-10 rounded-xl border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-200 hover:bg-teal-50 dark:hover:bg-teal-950/80 hover:text-teal-700 transition active:scale-95 ${
        isListening ? "bg-red-50 text-red-600 border-red-300 ring-2 ring-red-400" : ""
      } ${className || ""}`}
    >
      {isListening ? (
        <>
          <span className="absolute -top-1 -right-1 flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75" />
            <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500" />
          </span>
          <Mic className="w-5 h-5 text-red-600 animate-pulse" />
        </>
      ) : (
        <Mic className="w-5 h-5" />
      )}
    </button>
  );
}
