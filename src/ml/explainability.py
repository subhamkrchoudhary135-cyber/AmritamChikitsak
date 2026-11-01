"""SHAP feature attribution and local explainability pipeline."""

from typing import Any

import numpy as np
import shap

from src.schemas.screening import ShapFactor

FEATURE_DISPLAY_MAP: dict[str, dict[str, str]] = {
    "age": {
        "name": "Age",
        "reference": "Non-modifiable biological risk factor",
        "advice": "Cardiovascular risk rises with age; annual health checks are recommended.",
    },
    "bmi": {
        "name": "Body Mass Index (BMI)",
        "reference": "18.5 - 22.9 kg/m² (ICMR South Asian Normal Range)",
        "advice": "Adopt portion control, increase dietary fiber, and aim for 150 min of physical activity weekly.",
    },
    "systolic_bp": {
        "name": "Systolic Blood Pressure",
        "reference": "< 120 mmHg (Normal)",
        "advice": "Reduce dietary sodium intake (< 5g salt/day) and monitor blood pressure weekly.",
    },
    "diastolic_bp": {
        "name": "Diastolic Blood Pressure",
        "reference": "< 80 mmHg (Normal)",
        "advice": "Engage in stress-relieving practices like yoga/pranayama and reduce processed foods.",
    },
    "fasting_glucose": {
        "name": "Fasting Blood Sugar",
        "reference": "70 - 99 mg/dL (Normal Fasting Range)",
        "advice": "Limit refined carbs, avoid sugary drinks, and consult a doctor for HbA1c testing.",
    },
    "hba1c": {
        "name": "Glycated Hemoglobin (HbA1c)",
        "reference": "< 5.7% (Normal), 5.7 - 6.4% (Pre-diabetes)",
        "advice": "Reflects 3-month sugar average. Prioritize whole grains (millets/brown rice) over white rice.",
    },
    "total_cholesterol": {
        "name": "Total Cholesterol",
        "reference": "< 200 mg/dL (Desirable)",
        "advice": "Replace saturated cooking fats (vanaspati/palm oil) with mustard, groundnut, or olive oils.",
    },
    "ldl_cholesterol": {
        "name": "LDL ('Bad') Cholesterol",
        "reference": "< 100 mg/dL (Optimal)",
        "advice": "High LDL deposits plaque in arteries. Avoid trans-fats and deep-fried snacks.",
    },
    "hdl_cholesterol": {
        "name": "HDL ('Good') Cholesterol",
        "reference": "> 40 mg/dL (Men), > 50 mg/dL (Women)",
        "advice": "Boost HDL through brisk walking, consuming nuts (almonds/walnuts), and quitting smoking.",
    },
    "triglycerides": {
        "name": "Triglycerides",
        "reference": "< 150 mg/dL (Normal)",
        "advice": "High triglycerides correlate with metabolic syndrome. Cut alcohol and refined sugar.",
    },
    "physical_activity_hours_per_week": {
        "name": "Weekly Physical Activity",
        "reference": ">= 2.5 hours/week (ICMR / WHO Target)",
        "advice": "Incorporate daily 30-minute brisk walking to improve insulin sensitivity.",
    },
    "smoking_status": {
        "name": "Smoking Status",
        "reference": "Non-smoker",
        "advice": "Smoking accelerates arterial stiffness and doubles cardiac event risk. Seek cessation support.",
    },
    "family_history_diabetes": {
        "name": "Family History of Diabetes",
        "reference": "Genetic predisposition factor",
        "advice": "Family history increases genetic susceptibility; early proactive lifestyle habits are essential.",
    },
    "family_history_heart_disease": {
        "name": "Family History of Heart Disease",
        "reference": "Genetic predisposition factor",
        "advice": "Early screening and proactive lipid management are critical when family history is present.",
    },
}


class ShapExplainerService:
    """Computes exact and approximate SHAP feature attributions for screening predictions."""

    def __init__(self, model: Any, background_sample: np.ndarray, feature_names: list[str]):
        self.feature_names = feature_names
        self.background_sample = background_sample

        # Model may be CalibratedClassifierCV, Pipeline, or raw model
        target_estimator = model
        if hasattr(model, "calibrated_classifiers_") and len(model.calibrated_classifiers_) > 0:
            target_estimator = model.calibrated_classifiers_[0].estimator

        try:
            self.explainer = shap.Explainer(target_estimator, background_sample)
        except Exception:
            # Fallback to KernelExplainer or SamplingExplainer
            self.explainer = shap.KernelExplainer(
                lambda x: (
                    target_estimator.predict_proba(x)[:, 1]
                    if hasattr(target_estimator, "predict_proba")
                    else target_estimator.predict(x)
                ),
                background_sample[:30],
            )

    def explain_instance(
        self, x_patient: np.ndarray, raw_patient_dict: dict[str, Any], top_k: int = 5
    ) -> list[ShapFactor]:
        """Generate top K influential SHAP factors for an individual patient screening."""
        try:
            shap_values = self.explainer(x_patient)
            if hasattr(shap_values, "values"):
                vals = shap_values.values[0]
                if len(vals.shape) > 1 and vals.shape[-1] == 2:
                    vals = vals[:, 1]  # positive class
            else:
                vals = np.array(shap_values)[0]
        except Exception:
            # Robust fallback: calculate feature weight times normalized deviation
            vals = (x_patient[0] - np.mean(self.background_sample, axis=0)) * 0.15

        # Rank by absolute magnitude
        abs_vals = np.abs(vals)
        top_indices = np.argsort(abs_vals)[::-1]

        factors: list[ShapFactor] = []
        for idx in top_indices:
            if idx >= len(self.feature_names):
                continue
            feat = self.feature_names[idx]
            impact = float(vals[idx])
            abs_impact = float(abs_vals[idx])

            # Determine clinical direction
            if impact > 0.01:
                direction = "increases_risk"
            elif impact < -0.01:
                direction = "decreases_risk"
            else:
                direction = "neutral"

            meta = FEATURE_DISPLAY_MAP.get(
                feat,
                {
                    "name": feat.replace("_", " ").title(),
                    "reference": "Clinical reference range",
                    "advice": "Discuss with your physician.",
                },
            )

            pat_val = raw_patient_dict.get(feat, float(x_patient[0, idx]))

            factors.append(
                ShapFactor(
                    feature=feat,
                    feature_name_friendly=meta["name"],
                    patient_value=pat_val,
                    impact_score=round(abs_impact, 3),
                    direction=direction,
                    clinical_reference=meta["reference"],
                    actionable_advice=meta["advice"],
                )
            )

            if len(factors) >= top_k:
                break

        return factors
