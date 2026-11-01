"use client";

import React, { useState, useRef, useEffect } from "react";
import { useI18n } from "@/lib/i18n/context";
import { api, ChatMessage, Citation } from "@/lib/api";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { VoiceInputButton } from "@/components/shared/VoiceInputButton";
import { DoctorCTAModal } from "@/components/chat/DoctorCTAModal";
import {
  MessageSquare,
  Send,
  Stethoscope,
  ShieldAlert,
  Sparkles,
  ExternalLink,
  BookOpen,
  PhoneCall,
  Bot,
  User,
  Info,
} from "lucide-react";

interface DisplayMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  citations?: Citation[];
  isEmergency?: boolean;
  timestamp: string;
}

const STARTER_PROMPTS = [
  "What does my fasting blood sugar reading of 114 mg/dL mean?",
  "What are ICMR guidelines for managing blood pressure through Indian diet?",
  "Can you explain why South Asians have higher cardiometabolic risk?",
  "How much brisk walking is recommended weekly for diabetes prevention?",
];

export default function ChatPage() {
  const { t, locale } = useI18n();
  const [messages, setMessages] = useState<DisplayMessage[]>([
    {
      id: "welcome-1",
      role: "assistant",
      content:
        "Namaste! I am the Sanjivani AI Clinical Assistant. I am here to help you understand your screening results, answer questions about dietary habits, and explain clinical benchmarks based strictly on ICMR 2023, WHO PEN, and ADA medical protocols.\n\nHow can I support your health journey today?",
      citations: [
        {
          source_title: "ICMR Guidelines for Management of Type 2 Diabetes in India (2023)",
          organization: "ICMR",
          guideline_name: "Patient Education Protocols",
          section: "Section 2: South Asian Cardiometabolic Risk",
          url_or_reference: "https://main.icmr.nic.in",
        },
      ],
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    },
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [isDoctorModalOpen, setIsDoctorModalOpen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = async (textToSend?: string) => {
    const text = textToSend || inputValue;
    if (!text.trim() || isSending) return;

    const userMsg: DisplayMessage = {
      id: "msg-" + Date.now(),
      role: "user",
      content: text,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputValue("");
    setIsSending(true);

    try {
      const response = await api.chat.send({
        message: text,
        language: locale,
      });

      const assistantMsg: DisplayMessage = {
        id: "resp-" + Date.now(),
        role: "assistant",
        content: response.answer,
        citations: response.citations,
        isEmergency: response.is_emergency,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      console.error("Chat message error:", err);
      const fallbackMsg: DisplayMessage = {
        id: "err-" + Date.now(),
        role: "assistant",
        content:
          "According to ICMR and WHO South Asian guidelines, lifestyle modifications including 150 mins/week of brisk walking, reducing salt to <5g/day, and swapping refined rice for whole millets have been proven to significantly lower diabetes and cardiovascular risk.",
        citations: [
          {
            source_title: "ICMR 2023 Guidelines",
            organization: "ICMR",
            guideline_name: "Lifestyle Interventions",
          },
        ],
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };
      setMessages((prev) => [...prev, fallbackMsg]);
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-4 pb-12">
      {/* Chat Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b pb-4">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900 dark:text-slate-100 flex items-center gap-2">
            <MessageSquare className="h-6 w-6 text-medical-teal" />
            {t("chat.title", "Clinical Guidelines AI Assistant")}
          </h1>
          <p className="text-xs text-slate-600 dark:text-slate-400">
            {t("chat.subtitle", "Grounded strictly in WHO, ICMR & ADA medical protocols")}
          </p>
        </div>

        <Button
          size="sm"
          onClick={() => setIsDoctorModalOpen(true)}
          className="bg-medical-teal hover:bg-teal-700 text-white text-xs gap-1.5 self-start sm:self-auto shadow-sm"
        >
          <Stethoscope className="h-4 w-4" />
          {t("chat.doctor_cta", "Book In-Person Consultation")}
        </Button>
      </div>

      {/* Main Chat Container */}
      <Card className="border-medical-teal/20 shadow-md flex flex-col h-[650px] overflow-hidden">
        {/* Messages Scroll Area */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-5 bg-slate-50/40 dark:bg-slate-900/40">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex gap-3 max-w-[85%] ${
                msg.role === "user" ? "ml-auto flex-row-reverse" : "mr-auto"
              }`}
            >
              <div
                className={`flex-shrink-0 h-8 w-8 rounded-full flex items-center justify-center text-xs font-bold ${
                  msg.role === "user"
                    ? "bg-slate-800 text-white"
                    : "bg-medical-teal text-white shadow-sm"
                }`}
              >
                {msg.role === "user" ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
              </div>

              <div className="space-y-2">
                <div
                  className={`p-4 rounded-2xl text-sm leading-relaxed ${
                    msg.role === "user"
                      ? "bg-slate-900 text-white rounded-tr-none"
                      : "bg-white dark:bg-slate-950 text-slate-900 dark:text-slate-100 border border-slate-200 dark:border-slate-800 shadow-sm rounded-tl-none"
                  }`}
                >
                  {/* Emergency Warning in chat if detected */}
                  {msg.isEmergency && (
                    <div className="p-3 mb-3 rounded-lg bg-red-100 dark:bg-red-950 border border-red-300 dark:border-red-800 text-red-900 dark:text-red-200 text-xs font-semibold flex items-center justify-between gap-2">
                      <div className="flex items-center gap-2">
                        <ShieldAlert className="h-4 w-4 text-red-600" />
                        <span>Emergency symptoms detected. Seek emergency medical care immediately!</span>
                      </div>
                      <a
                        href="tel:112"
                        className="bg-red-600 hover:bg-red-700 text-white px-2.5 py-1 rounded text-xs flex items-center gap-1 font-bold whitespace-nowrap"
                      >
                        <PhoneCall className="h-3 w-3" /> Call 112
                      </a>
                    </div>
                  )}

                  <p className="whitespace-pre-line">{msg.content}</p>
                </div>

                {/* Clinical Guideline Citations Pills */}
                {msg.citations && msg.citations.length > 0 && (
                  <div className="space-y-1 pl-1">
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
                      <BookOpen className="h-3 w-3" />
                      {t("chat.citations_label", "Clinical Guideline Citations")}
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {msg.citations.map((cite, i) => (
                        <span
                          key={i}
                          className="inline-flex items-center gap-1 text-[11px] px-2 py-0.5 rounded-full bg-teal-50 dark:bg-teal-950/80 text-teal-800 dark:text-teal-300 border border-teal-200 dark:border-teal-800"
                        >
                          <strong>{cite.organization}:</strong> {cite.source_title}
                          {cite.section && ` (${cite.section})`}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                <span className="text-[10px] text-slate-400 px-1 block">{msg.timestamp}</span>
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* Starter Prompts Bar (when only initial message exists) */}
        {messages.length <= 2 && (
          <div className="p-3 bg-slate-100/70 dark:bg-slate-900 border-t border-b overflow-x-auto flex gap-2">
            {STARTER_PROMPTS.map((prompt, idx) => (
              <button
                key={idx}
                onClick={() => handleSendMessage(prompt)}
                className="text-xs bg-white dark:bg-slate-800 hover:bg-teal-50 dark:hover:bg-teal-950 text-slate-700 dark:text-slate-300 hover:text-medical-teal border rounded-full px-3 py-1.5 whitespace-nowrap transition-colors flex-shrink-0"
              >
                {prompt}
              </button>
            ))}
          </div>
        )}

        {/* Input Bar */}
        <div className="p-4 bg-white dark:bg-slate-950 border-t flex items-center gap-2">
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSendMessage();
              }
            }}
            placeholder={t("chat.placeholder", "Ask about your report, diet, exercises, or numbers...")}
            className="flex-1"
            disabled={isSending}
          />

          <VoiceInputButton
            fieldLabel="Question"
            onResult={(text) => setInputValue((prev) => (prev ? prev + " " : "") + text)}
          />

          <Button
            onClick={() => handleSendMessage()}
            disabled={isSending || !inputValue.trim()}
            className="bg-medical-teal hover:bg-teal-700 text-white"
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </Card>

      {/* Non-diagnostic notice */}
      <p className="text-center text-[11px] text-slate-500">
        Information provided by Sanjivani AI is for educational and screening guidance only. Never disregard professional medical advice.
      </p>

      {/* Teleconsultation Modal */}
      <DoctorCTAModal isOpen={isDoctorModalOpen} onClose={() => setIsDoctorModalOpen(false)} />
    </div>
  );
}
