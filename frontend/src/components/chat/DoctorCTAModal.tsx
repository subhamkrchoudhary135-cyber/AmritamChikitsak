"use client";

import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Stethoscope, X, CheckCircle2, Phone, Calendar, MapPin, Building2 } from "lucide-react";

interface DoctorCTAModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export function DoctorCTAModal({ isOpen, onClose }: DoctorCTAModalProps) {
  const [submitted, setSubmitted] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    phone: "",
    mode: "teleconsult",
    preferredTime: "morning",
    location: "",
  });

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
  };

  const handleResetAndClose = () => {
    setSubmitted(false);
    onClose();
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm animate-in fade-in duration-200"
      role="dialog"
      aria-modal="true"
      aria-labelledby="doctor-cta-title"
    >
      <div className="relative w-full max-w-lg">
        <Card className="border-teal-200 dark:border-slate-700 shadow-2xl bg-white dark:bg-slate-900 overflow-hidden">
          {/* Header */}
          <CardHeader className="bg-gradient-to-r from-medical-teal to-teal-800 text-white p-5">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="p-2 bg-white/20 rounded-lg">
                  <Stethoscope className="h-6 w-6 text-white" />
                </div>
                <div>
                  <CardTitle id="doctor-cta-title" className="text-lg font-bold text-white">
                    Connect With a Physician
                  </CardTitle>
                  <CardDescription className="text-teal-100 text-xs">
                    Ayushman Bharat Health Centres & Verified Teleconsultation
                  </CardDescription>
                </div>
              </div>
              <button
                onClick={handleResetAndClose}
                className="rounded-full p-1.5 text-white/80 hover:bg-white/20 transition-colors"
                aria-label="Close dialog"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
          </CardHeader>

          <CardContent className="p-6">
            {submitted ? (
              <div className="text-center py-6 space-y-4">
                <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400">
                  <CheckCircle2 className="h-8 w-8" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100">
                    Consultation Request Registered
                  </h3>
                  <p className="text-xs text-slate-600 dark:text-slate-400 mt-1 max-w-sm mx-auto">
                    A duty medical officer or eSanjeevani teleconsultation coordinator will contact you at{" "}
                    <strong>{formData.phone || "+91 XXXXXXXXXX"}</strong> within 2 hours.
                  </p>
                </div>

                <div className="p-3.5 bg-slate-50 dark:bg-slate-800 rounded-xl text-left text-xs space-y-1.5 border">
                  <div className="font-semibold text-slate-700 dark:text-slate-200">
                    Government of India eSanjeevani OPD:
                  </div>
                  <div className="text-slate-500">
                    Free national telemedicine service open Mon-Sat (9:00 AM – 5:00 PM).
                  </div>
                  <div className="text-teal-700 dark:text-teal-400 font-medium">
                    National Helpline: 1075 or esanjeevaniopd.in
                  </div>
                </div>

                <Button onClick={handleResetAndClose} className="w-full">
                  Close & Return to Chat
                </Button>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4">
                <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                  Sanjivani AI screening scores provide early guidance. We strongly recommend having an MBBS/MD doctor review your blood reports and clinical history.
                </p>

                <div className="space-y-3">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                      Patient Name
                    </label>
                    <input
                      required
                      type="text"
                      placeholder="e.g. Gurpreet Singh"
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3 py-2 text-sm text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-medical-teal min-h-[44px]"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                      Mobile Number (+91)
                    </label>
                    <div className="relative">
                      <Phone className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
                      <input
                        required
                        type="tel"
                        pattern="[0-9]{10}"
                        placeholder="10-digit mobile number"
                        value={formData.phone}
                        onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                        className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 pl-9 pr-3 py-2 text-sm text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-medical-teal min-h-[44px]"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                        Mode
                      </label>
                      <select
                        value={formData.mode}
                        onChange={(e) => setFormData({ ...formData, mode: e.target.value })}
                        className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3 py-2 text-xs text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-medical-teal min-h-[44px]"
                      >
                        <option value="teleconsult">Video / Teleconsultation</option>
                        <option value="phc">Visit Nearest PHC / Clinic</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                        Preferred Time
                      </label>
                      <select
                        value={formData.preferredTime}
                        onChange={(e) => setFormData({ ...formData, preferredTime: e.target.value })}
                        className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3 py-2 text-xs text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-medical-teal min-h-[44px]"
                      >
                        <option value="morning">Morning (9 AM - 12 PM)</option>
                        <option value="afternoon">Afternoon (12 PM - 4 PM)</option>
                        <option value="evening">Evening (4 PM - 8 PM)</option>
                      </select>
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                      City or PIN Code
                    </label>
                    <div className="relative">
                      <MapPin className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
                      <input
                        type="text"
                        placeholder="e.g. Ludhiana, 141001"
                        value={formData.location}
                        onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                        className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 pl-9 pr-3 py-2 text-sm text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-medical-teal min-h-[44px]"
                      />
                    </div>
                  </div>
                </div>

                <div className="pt-2">
                  <Button type="submit" className="w-full min-h-[48px] text-sm font-bold bg-medical-teal hover:bg-teal-700">
                    Confirm Consultation Request
                  </Button>
                </div>
              </form>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
