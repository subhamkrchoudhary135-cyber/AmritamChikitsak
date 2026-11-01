import * as React from "react";
import { cn } from "@/lib/utils";

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "secondary" | "destructive" | "outline" | "low" | "moderate" | "high" | "critical";
}

export function Badge({ className, variant = "default", ...props }: BadgeProps) {
  const variantStyles = {
    default: "bg-teal-100 text-teal-800 dark:bg-teal-900/60 dark:text-teal-300 border-teal-200 dark:border-teal-800",
    secondary: "bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-300 border-slate-200",
    destructive: "bg-red-100 text-red-800 dark:bg-red-900/60 dark:text-red-300 border-red-200",
    outline: "text-foreground border border-slate-300 dark:border-slate-700",
    low: "bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border-emerald-300",
    moderate: "bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 border-amber-300",
    high: "bg-orange-100 text-orange-800 dark:bg-orange-950 dark:text-orange-300 border-orange-300",
    critical: "bg-red-100 text-red-900 dark:bg-red-950 dark:text-red-300 border-red-300 animate-pulse",
  }[variant];

  return (
    <div
      className={cn(
        "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold tracking-wide transition-colors",
        variantStyles,
        className
      )}
      {...props}
    />
  );
}
