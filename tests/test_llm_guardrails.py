"""Tests for Clinical Guardrails, Emergency Detection, and Multilingual explanations."""

from src.llm.explainer import generate_multilingual_explanation
from src.llm.guardrails import STATUTORY_DISCLAIMER, ClinicalGuardrails
from src.schemas.screening import (
    ConditionRiskResult,
    RiskLevel,
    ScreeningInput,
    ShapFactor,
)


def test_emergency_red_flags_detection():
    # Normal input
    normal_input = ScreeningInput(
        age=35,
        gender="male",
        height_cm=170,
        weight_kg=70,
        systolic_bp=120,
        diastolic_bp=80,
        fasting_glucose=90,
    )
    alert = ClinicalGuardrails.detect_emergency_red_flags(normal_input)
    assert alert.is_emergency is False

    # Chest pain emergency input
    emergency_input = ScreeningInput(
        age=55,
        gender="male",
        height_cm=170,
        weight_kg=85,
        systolic_bp=195,  # Hypertensive crisis
        diastolic_bp=125,
        fasting_glucose=140,
        chest_pain_present=True,
    )
    alert_em = ClinicalGuardrails.detect_emergency_red_flags(emergency_input)
    assert alert_em.is_emergency is True
    assert len(alert_em.emergency_triggers) >= 2
    assert "112" in alert_em.triage_instruction or "108" in alert_em.triage_instruction


def test_prescription_and_diagnosis_refusal():
    # Attempting to ask for prescription
    blocked, msg = ClinicalGuardrails.sanitize_and_check_query(
        "Please prescribe me Metformin 500mg dose"
    )
    assert blocked is True
    assert "NON-DIAGNOSTIC BOUNDARY" in msg

    # Safe general query
    blocked_safe, _ = ClinicalGuardrails.sanitize_and_check_query(
        "What are ICMR guidelines for diabetes screening?"
    )
    assert blocked_safe is False


def test_statutory_disclaimer_appended():
    text = "Your blood sugar is currently well managed."
    guarded = ClinicalGuardrails.append_disclaimer(text)
    assert STATUTORY_DISCLAIMER in guarded


def test_multilingual_explanation_generation():
    patient_input = ScreeningInput(
        age=50,
        gender="male",
        height_cm=165,
        weight_kg=80,
        systolic_bp=135,
        diastolic_bp=85,
        fasting_glucose=120,
    )
    conditions = {
        "diabetes": ConditionRiskResult(
            condition_name="Type 2 Diabetes",
            risk_score=0.65,
            calibrated_probability=0.65,
            risk_level=RiskLevel.HIGH,
            decision_threshold=0.35,
            is_screened_positive=True,
            confidence_interval=(0.55, 0.75),
            clinical_guideline_category="Pre-diabetes",
        )
    }
    factors = [
        ShapFactor(
            feature="fasting_glucose",
            feature_name_friendly="Fasting Blood Sugar",
            patient_value=120,
            impact_score=0.25,
            direction="increases_risk",
            clinical_reference="70-99 mg/dL",
            actionable_advice="Limit refined carbs.",
        )
    ]

    explanations = generate_multilingual_explanation(patient_input, conditions, factors)

    assert "en" in explanations
    assert "hi" in explanations
    assert "pa" in explanations

    assert explanations["en"].reading_level == "Class 8"
    assert "जोखिम" in explanations["hi"].headline or "स्वास्थ्य" in explanations["hi"].headline
    assert "ਸਿਹਤ" in explanations["pa"].headline or "ਖ਼ਤਰਾ" in explanations["pa"].headline
