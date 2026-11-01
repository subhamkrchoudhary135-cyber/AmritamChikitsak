"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useI18n } from "@/lib/i18n/context";
import { api, PatientResponse } from "@/lib/api";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Stethoscope,
  Search,
  Filter,
  UserCheck,
  FileDown,
  AlertTriangle,
  Users,
  Activity,
  ArrowRight,
  ShieldAlert,
} from "lucide-react";

export default function DoctorPortalPage() {
  const { t } = useI18n();
  const [patients, setPatients] = useState<PatientResponse[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedRisk, setSelectedRisk] = useState<string>("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadPatients() {
      try {
        const res = await api.patients.list();
        setPatients(res);
      } catch (e) {
        console.warn("Failed to fetch patients, fallback mock loaded", e);
      } finally {
        setLoading(false);
      }
    }
    loadPatients();
  }, []);

  const filteredPatients = patients.filter((p) => {
    const matchesSearch =
      p.full_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (p.abha_id && p.abha_id.includes(searchQuery)) ||
      p.phone_number.includes(searchQuery);
    return matchesSearch;
  });

  return (
    <div className="space-y-8 pb-16">
      {/* Clinician Portal Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b pb-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-medical-teal mb-1">
            <span className="px-2.5 py-0.5 rounded-full bg-teal-50 dark:bg-teal-950/60 border border-teal-200 dark:border-teal-800">
              Provider Dashboard
            </span>
            <span className="text-slate-500">Dr. Ananya Verma, MD (Internal Medicine)</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-slate-100 flex items-center gap-2">
            <Stethoscope className="h-7 w-7 text-medical-teal" />
            {t("nav.doctor", "Clinician Triage & EHR Portal")}
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
            Triaged patient records stratified by ICMR 2023 and WHO cardiometabolic risk algorithms.
          </p>
        </div>

        <Link href="/screen">
          <Button className="bg-medical-teal hover:bg-teal-700 text-white text-xs font-semibold gap-1.5 shadow-sm">
            <Activity className="h-4 w-4" />
            Initiate Clinical Screening
          </Button>
        </Link>
      </div>

      {/* Overview Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <Card className="border-medical-teal/20">
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 font-medium">Total Screened</p>
              <p className="text-2xl font-black text-slate-900 dark:text-slate-100">142</p>
            </div>
            <div className="p-2.5 bg-teal-50 dark:bg-teal-950 rounded-xl text-medical-teal">
              <Users className="h-5 w-5" />
            </div>
          </CardContent>
        </Card>

        <Card className="border-red-200 dark:border-red-900 bg-red-50/20">
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-red-600 font-medium">Critical Red Flags</p>
              <p className="text-2xl font-black text-red-700 dark:text-red-400">3</p>
            </div>
            <div className="p-2.5 bg-red-100 dark:bg-red-950 rounded-xl text-red-600">
              <ShieldAlert className="h-5 w-5" />
            </div>
          </CardContent>
        </Card>

        <Card className="border-orange-200 dark:border-orange-900 bg-orange-50/20">
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-orange-600 font-medium">Elevated Risk Triage</p>
              <p className="text-2xl font-black text-orange-700 dark:text-orange-400">28</p>
            </div>
            <div className="p-2.5 bg-orange-100 dark:bg-orange-950 rounded-xl text-orange-600">
              <AlertTriangle className="h-5 w-5" />
            </div>
          </CardContent>
        </Card>

        <Card className="border-emerald-200 dark:border-emerald-900 bg-emerald-50/20">
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-emerald-600 font-medium">Controlled / Normal</p>
              <p className="text-2xl font-black text-emerald-700 dark:text-emerald-400">111</p>
            </div>
            <div className="p-2.5 bg-emerald-100 dark:bg-emerald-950 rounded-xl text-emerald-600">
              <UserCheck className="h-5 w-5" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Patient Search and Filters */}
      <div className="flex flex-col sm:flex-row items-center gap-3">
        <div className="relative flex-1 w-full">
          <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
          <Input
            placeholder="Search by patient name, ABHA ID (e.g. 91-1234), or phone number..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-9 text-sm"
          />
        </div>
      </div>

      {/* Patient Triage Table */}
      <Card className="border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 dark:bg-slate-900/60 border-b text-xs font-semibold text-slate-500 uppercase tracking-wider">
              <tr>
                <th className="px-6 py-3.5">Patient Details</th>
                <th className="px-6 py-3.5">ABHA ID / Contact</th>
                <th className="px-6 py-3.5">Demographics</th>
                <th className="px-6 py-3.5">Language</th>
                <th className="px-6 py-3.5">Triage Status</th>
                <th className="px-6 py-3.5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
              {filteredPatients.map((patient, idx) => (
                <tr
                  key={patient.id}
                  className="hover:bg-slate-50/50 dark:hover:bg-slate-900/50 transition-colors"
                >
                  <td className="px-6 py-4">
                    <div className="font-semibold text-slate-900 dark:text-slate-100">
                      {patient.full_name}
                    </div>
                    <div className="text-xs text-slate-500">ID: {patient.id}</div>
                  </td>

                  <td className="px-6 py-4">
                    <div className="text-xs font-mono text-slate-700 dark:text-slate-300">
                      {patient.abha_id || "Unlinked"}
                    </div>
                    <div className="text-xs text-slate-500">{patient.phone_number}</div>
                  </td>

                  <td className="px-6 py-4 text-xs text-slate-600 dark:text-slate-400">
                    {patient.age} yrs • {patient.gender} • {patient.state_province || "India"}
                  </td>

                  <td className="px-6 py-4">
                    <span className="text-xs px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 font-medium uppercase">
                      {patient.preferred_language}
                    </span>
                  </td>

                  <td className="px-6 py-4">
                    {idx === 0 ? (
                      <span className="inline-flex items-center gap-1 text-xs px-2.5 py-0.5 rounded-full bg-orange-100 text-orange-800 font-semibold">
                        <AlertTriangle className="h-3 w-3" /> Elevated Triage
                      </span>
                    ) : idx === 1 ? (
                      <span className="inline-flex items-center gap-1 text-xs px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-800 font-semibold">
                        Moderate Risk
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 text-xs px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 font-semibold">
                        Normotensive
                      </span>
                    )}
                  </td>

                  <td className="px-6 py-4 text-right">
                    <div className="flex items-center justify-end gap-2">
                      <Link href={`/results?id=scr-demo-99`}>
                        <Button variant="ghost" size="sm" className="text-xs text-medical-teal hover:text-teal-700">
                          View Results <ArrowRight className="h-3.5 w-3.5 ml-1" />
                        </Button>
                      </Link>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
