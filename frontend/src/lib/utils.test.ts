import { describe, it, expect } from "vitest";
import { cn, UnitConverters } from "./utils";

describe("Frontend Utilities & Unit Converters", () => {
  it("cn correctly merges tailwind classes", () => {
    const result = cn("p-4", "text-red-500", { "font-bold": true, "italic": false });
    expect(result).toContain("p-4");
    expect(result).toContain("text-red-500");
    expect(result).toContain("font-bold");
    expect(result).not.toContain("italic");
  });

  it("calculates BMI correctly", () => {
    // 70 kg, 175 cm -> 70 / (1.75 * 1.75) = 22.86 -> 22.9
    const bmi = UnitConverters.calculateBmi(70, 175);
    expect(bmi).toBeCloseTo(22.9, 1);
  });

  it("handles invalid height for BMI calculation", () => {
    expect(UnitConverters.calculateBmi(70, 0)).toBe(0);
    expect(UnitConverters.calculateBmi(70, -10)).toBe(0);
  });

  it("converts blood glucose between mg/dL and mmol/L", () => {
    const mmol = UnitConverters.mgDlToMmolL(90);
    expect(mmol).toBe(5);

    const mgdl = UnitConverters.mmolLToMgDl(5);
    expect(mgdl).toBe(90);
  });

  it("converts height and weight correctly", () => {
    const { feet, inches } = UnitConverters.cmToFeetInches(175);
    expect(feet).toBe(5);
    expect(inches).toBe(9);

    const cm = UnitConverters.feetInchesToCm(5, 9);
    expect(cm).toBe(175);

    const lbs = UnitConverters.kgToLbs(70);
    expect(lbs).toBeCloseTo(154.3, 1);

    const kg = UnitConverters.lbsToKg(154.3);
    expect(kg).toBeCloseTo(70, 0);
  });
});
