import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Unit Conversion Utilities
export const UnitConverters = {
  // Height
  cmToFeetInches: (cm: number): { feet: number; inches: number } => {
    const totalInches = cm / 2.54;
    const feet = Math.floor(totalInches / 12);
    const inches = Math.round(totalInches % 12);
    return { feet, inches };
  },
  feetInchesToCm: (feet: number, inches: number): number => {
    return Math.round((feet * 12 + inches) * 2.54);
  },

  // Weight
  kgToLbs: (kg: number): number => {
    return Math.round(kg * 2.20462 * 10) / 10;
  },
  lbsToKg: (lbs: number): number => {
    return Math.round((lbs / 2.20462) * 10) / 10;
  },

  // Blood Glucose
  mgDlToMmolL: (mgDl: number): number => {
    return Math.round((mgDl / 18.0) * 10) / 10;
  },
  mmolLToMgDl: (mmolL: number): number => {
    return Math.round(mmolL * 18.0);
  },

  // Computed BMI
  calculateBmi: (weightKg: number, heightCm: number): number => {
    if (!heightCm || heightCm <= 0) return 0;
    const heightM = heightCm / 100;
    return Math.round((weightKg / (heightM * heightM)) * 10) / 10;
  },
};
