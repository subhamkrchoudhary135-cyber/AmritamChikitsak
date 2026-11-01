"""Lab Report Parser: regex and OCR extraction of clinical biometrics into structured Pydantic models."""

import re
from typing import Any


class LabReportTextExtractor:
    """Extracts biomarker values from clinical notes or OCR text strings."""

    @staticmethod
    def extract_biometrics_from_text(raw_text: str) -> dict[str, Any]:
        """Parse unstructured clinical or lab report text into a normalized dictionary."""
        extracted: dict[str, Any] = {}
        text = raw_text.replace("\n", " ").lower()

        # Age (e.g., "age: 45", "45 yo", "45 yrs")
        age_match = re.search(r"\b(?:age|years?\s*old|yrs?)[:\s]*([0-9]{2})\b", text)
        if age_match:
            extracted["age"] = int(age_match.group(1))

        # Gender
        if re.search(r"\b(?:female|woman|f)\b", text):
            extracted["gender"] = "female"
        elif re.search(r"\b(?:male|man|m)\b", text):
            extracted["gender"] = "male"

        # Blood Pressure (e.g., "130/85", "bp: 120 / 80 mmHg")
        bp_match = re.search(r"\b([0-9]{2,3})\s*/\s*([0-9]{2,3})\s*(?:mmhg)?\b", text)
        if bp_match:
            extracted["systolic_bp"] = float(bp_match.group(1))
            extracted["diastolic_bp"] = float(bp_match.group(2))

        # Fasting Blood Glucose (e.g., "fbs: 110 mg/dl", "fbs (fasting blood sugar): 122.5")
        glucose_match = re.search(
            r"\b(?:fbs|fasting\s*glucose|fasting\s*sugar|fbg)(?:\s*\([^)]*\))?[:\s]*([0-9]{2,3}(?:\.[0-9]+)?)\b",
            text,
        )
        if glucose_match:
            extracted["fasting_glucose"] = float(glucose_match.group(1))

        # HbA1c (e.g., "hba1c: 6.8%", "glycated hemoglobin 7.1")
        hba1c_match = re.search(
            r"\b(?:hba1c|glycated\s*h(?:a)?emoglobin)[:\s]*([0-9]{1,2}(?:\.[0-9]+)?)\s*%?\b",
            text,
        )
        if hba1c_match:
            extracted["hba1c"] = float(hba1c_match.group(1))

        # Total Cholesterol (e.g., "total cholesterol: 210", "cholesterol: 195 mg/dl")
        chol_match = re.search(
            r"\b(?:total\s*cholesterol|cholesterol)[:\s]*([0-9]{2,3}(?:\.[0-9]+)?)\s*(?:mg/dl)?\b",
            text,
        )
        if chol_match:
            extracted["total_cholesterol"] = float(chol_match.group(1))

        # Triglycerides
        tg_match = re.search(
            r"\b(?:triglycerides|tg)[:\s]*([0-9]{2,4}(?:\.[0-9]+)?)\s*(?:mg/dl)?\b",
            text,
        )
        if tg_match:
            extracted["triglycerides"] = float(tg_match.group(1))

        # Height & Weight
        height_match = re.search(
            r"\b(?:height|ht)[:\s]*([0-9]{2,3}(?:\.[0-9]+)?)\s*(?:cm)?\b", text
        )
        if height_match:
            extracted["height_cm"] = float(height_match.group(1))

        weight_match = re.search(
            r"\b(?:weight|wt)[:\s]*([0-9]{2,3}(?:\.[0-9]+)?)\s*(?:kg)?\b", text
        )
        if weight_match:
            extracted["weight_kg"] = float(weight_match.group(1))

        # BMI
        bmi_match = re.search(r"\b(?:bmi)[:\s]*([0-9]{2}(?:\.[0-9]+)?)\b", text)
        if bmi_match:
            extracted["bmi"] = float(bmi_match.group(1))

        return extracted
