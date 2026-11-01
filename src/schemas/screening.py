"""Screening inputs, outputs, risk levels, and prediction schemas."""

from datetime import datetime
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


class RiskLevel(StrEnum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ScreeningInput(BaseModel):
    """Clinical, biometric, and lifestyle inputs for screening."""

    # Demographics
    age: int = Field(..., ge=18, le=120, description="Age in completed years")
    gender: Literal["male", "female", "other"] = Field(..., description="Biological sex")

    # Anthropometric
    height_cm: float = Field(..., ge=90.0, le=250.0, description="Height in centimeters")
    weight_kg: float = Field(..., ge=25.0, le=300.0, description="Weight in kilograms")
    bmi: float | None = Field(
        None, ge=10.0, le=80.0, description="Calculated automatically if omitted"
    )
    waist_circumference_cm: float | None = Field(
        None, ge=40.0, le=200.0, description="Waist circumference in cm"
    )

    # Vitals
    systolic_bp: float = Field(..., ge=60.0, le=260.0, description="Systolic Blood Pressure (mmHg)")
    diastolic_bp: float = Field(
        ..., ge=40.0, le=160.0, description="Diastolic Blood Pressure (mmHg)"
    )
    resting_heart_rate: float | None = Field(
        72.0, ge=30.0, le=220.0, description="Resting heart rate (bpm)"
    )

    # Glycemic Parameters
    fasting_glucose: float = Field(
        ..., ge=40.0, le=500.0, description="Fasting blood glucose (mg/dL)"
    )
    hba1c: float | None = Field(None, ge=3.5, le=18.0, description="Glycated hemoglobin (%)")

    # Lipid Panel (mg/dL)
    total_cholesterol: float | None = Field(
        190.0, ge=70.0, le=600.0, description="Total cholesterol (mg/dL)"
    )
    ldl_cholesterol: float | None = Field(
        110.0, ge=20.0, le=400.0, description="LDL cholesterol (mg/dL)"
    )
    hdl_cholesterol: float | None = Field(
        48.0, ge=10.0, le=150.0, description="HDL cholesterol (mg/dL)"
    )
    triglycerides: float | None = Field(
        150.0, ge=30.0, le=1500.0, description="Triglycerides (mg/dL)"
    )

    # Lifestyle & Medical History
    physical_activity_hours_per_week: float = Field(
        2.5, ge=0.0, le=40.0, description="Moderate to vigorous activity"
    )
    smoking_status: Literal["never", "former", "current"] = Field("never")
    alcohol_consumption: Literal["none", "occasional", "regular"] = Field("none")
    diet_type: Literal["vegetarian", "non_vegetarian", "vegan", "other"] = Field("vegetarian")
    family_history_diabetes: bool = Field(False, description="First-degree relative with diabetes")
    family_history_heart_disease: bool = Field(
        False, description="First-degree relative with early CAD"
    )

    # Acute Emergency Symptom Checklist (Triaged for Red Flags)
    chest_pain_present: bool = Field(False, description="Crushing/radiating chest pain or pressure")
    shortness_of_breath_severe: bool = Field(False, description="Acute sudden dyspnea at rest")
    stroke_signs_fast: bool = Field(
        False, description="Facial drooping, arm weakness, slurred speech"
    )
    symptoms_free_text: str | None = Field(None, description="Free text clinical description")

    # Language preference
    preferred_language: Literal["en", "hi", "pa"] = Field("en")

    @model_validator(mode="after")
    def compute_bmi_if_missing(self) -> "ScreeningInput":
        if self.bmi is None:
            height_m = self.height_cm / 100.0
            computed = self.weight_kg / (height_m * height_m)
            self.bmi = round(computed, 2)
        return self


class ConditionRiskResult(BaseModel):
    """Detailed risk assessment for a specific condition (e.g. Diabetes, Heart Disease, Hypertension)."""

    condition_name: str
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Raw ensemble score")
    calibrated_probability: float = Field(..., ge=0.0, le=1.0, description="Calibrated probability")
    risk_level: RiskLevel
    decision_threshold: float = Field(..., description="Recall-prioritized threshold")
    is_screened_positive: bool = Field(
        ..., description="True if calibrated probability >= decision_threshold"
    )
    confidence_interval: tuple[float, float] = Field(..., description="95% confidence interval")
    clinical_guideline_category: str = Field(
        ..., description="e.g. Pre-diabetes (ICMR) or Stage 1 HTN"
    )


class ProgressionForecast(BaseModel):
    """3-6 month biomarker trajectory forecasts and continuous metabolic risk."""

    forecasted_glucose_3m: float = Field(
        ..., description="Estimated fasting glucose in 3 months (mg/dL)"
    )
    forecasted_glucose_6m: float = Field(
        ..., description="Estimated fasting glucose in 6 months (mg/dL)"
    )
    forecasted_systolic_bp_3m: float = Field(..., description="Estimated SBP in 3 months (mmHg)")
    forecasted_systolic_bp_6m: float = Field(..., description="Estimated SBP in 6 months (mmHg)")
    continuous_risk_score_100: float = Field(
        ..., ge=0.0, le=100.0, description="Composite cardiometabolic index"
    )
    glucose_prediction_interval_6m: tuple[float, float] = Field(
        ..., description="Quantile/conformal interval"
    )
    bp_prediction_interval_6m: tuple[float, float] = Field(
        ..., description="Quantile/conformal interval"
    )
    trend_description: str


class ClusteringResult(BaseModel):
    """Patient segmentation into phenotype/lifestyle risk groups."""

    cluster_id: int
    cluster_label: str  # e.g., "High BMI + Low Physical Activity"
    cluster_description: str
    is_anomaly: bool = Field(..., description="Flagged by Isolation Forest / One-Class SVM")
    anomaly_score: float
    pca_coordinates: list[float] = Field(
        default_factory=list, description="2D PCA projection for visual plotting"
    )
    lifestyle_priorities: list[str]


class ShapFactor(BaseModel):
    """Individual SHAP feature explanation factor."""

    feature: str
    feature_name_friendly: str
    patient_value: Any
    impact_score: float = Field(..., description="Absolute SHAP value magnitude")
    direction: Literal["increases_risk", "decreases_risk", "neutral"]
    clinical_reference: str
    actionable_advice: str


class MultilingualExplanation(BaseModel):
    """Plain-language patient guidance at Class 8 reading level."""

    language: Literal["en", "hi", "pa"]
    language_name: str
    headline: str
    summary_overview: str
    top_factors_plain_text: list[str]
    actionable_steps: list[str]
    reading_level: str = "Class 8"


class EmergencyAlert(BaseModel):
    """Emergency red-flag notification."""

    is_emergency: bool
    emergency_triggers: list[str]
    triage_instruction: str
    emergency_helpline_india: str = "112 / 108"


class ScreeningResponse(BaseModel):
    """Complete Sanjivani AI screening report response."""

    screening_id: str
    patient_id: str
    created_at: datetime
    input_biometrics: ScreeningInput
    conditions: dict[str, ConditionRiskResult]
    progression_forecast: ProgressionForecast
    phenotype: ClusteringResult
    top_shap_factors: list[ShapFactor]
    multilingual_explanations: dict[str, MultilingualExplanation]
    emergency_alert: EmergencyAlert
    clinical_disclaimer: str

    class Config:
        from_attributes = True
