"""Clinical Guardrails: Emergency Red-Flag detection, Non-Diagnostic boundaries, and Disclaimers."""

from src.core.audit import audit_logger
from src.schemas.screening import EmergencyAlert, ScreeningInput

STATUTORY_DISCLAIMER: str = (
    "DISCLAIMER: Sanjivani AI is an AI-powered screening support tool and NOT a diagnostic medical device. "
    "This assessment does not establish a doctor-patient relationship, make a medical diagnosis, or recommend drug dosages. "
    "Always consult a qualified, registered medical practitioner for clinical evaluation and prescription."
)

EMERGENCY_KEYWORDS: list[str] = [
    "chest pain",
    "radiating pain",
    "arm pain",
    "jaw pain",
    "shortness of breath",
    "cannot breathe",
    "slurred speech",
    "facial droop",
    "face drooping",
    "loss of consciousness",
    "fainted",
    "stroke",
    "heart attack",
    "severe headache",
    "blurred vision",
    "sweating profusely",
]

PRESCRIPTION_DIAGNOSIS_KEYWORDS: list[str] = [
    "prescribe",
    "prescription",
    "what dose",
    "what dosage",
    "how many mg",
    "take medicine",
    "which drug",
    "diagnose me",
    "give me antibiotics",
    "metformin dose",
    "insulin units",
    "tell me what disease i have",
]


class ClinicalGuardrails:
    """Enforces non-diagnostic boundaries, detects acute emergencies, and filters inappropriate content."""

    @staticmethod
    def detect_emergency_red_flags(
        patient_input: ScreeningInput,
    ) -> EmergencyAlert:
        """Scan structured screening inputs and free-text symptoms for critical clinical emergencies."""
        triggers: list[str] = []

        # 1. Structural flags
        if patient_input.chest_pain_present:
            triggers.append("Reported acute chest pain / chest pressure")

        if patient_input.shortness_of_breath_severe:
            triggers.append("Severe sudden shortness of breath at rest")

        if patient_input.stroke_signs_fast:
            triggers.append(
                "Reported stroke warning signs (facial drooping / limb weakness / slurred speech)"
            )

        # 2. Extreme hemodynamic vitals (Hypertensive Emergency: SBP >= 180 or DBP >= 120)
        if patient_input.systolic_bp >= 180.0 or patient_input.diastolic_bp >= 120.0:
            triggers.append(
                f"Hypertensive Crisis range BP: {patient_input.systolic_bp}/{patient_input.diastolic_bp} mmHg"
            )

        # 3. Severe hypoglycemia / extreme hyperglycemia
        if patient_input.fasting_glucose < 50.0:
            triggers.append(
                f"Critical hypoglycemia danger: fasting blood glucose {patient_input.fasting_glucose} mg/dL"
            )
        elif patient_input.fasting_glucose >= 400.0:
            triggers.append(
                f"Hyperglycemic emergency threshold: blood glucose {patient_input.fasting_glucose} mg/dL"
            )

        # 4. Free-text symptoms scan
        if patient_input.symptoms_free_text:
            text_lower = patient_input.symptoms_free_text.lower()
            for kw in EMERGENCY_KEYWORDS:
                if kw in text_lower:
                    triggers.append(f"Symptom keyword detected: '{kw}'")

        is_emergency = len(triggers) > 0
        instruction = (
            "CRITICAL: SEEK IMMEDIATE EMERGENCY MEDICAL CARE NOW. Call 112 or 108 (India Emergency Services) "
            "or proceed to the nearest emergency department without delay."
            if is_emergency
            else "No acute emergency red flags identified during screening intake."
        )

        return EmergencyAlert(
            is_emergency=is_emergency,
            emergency_triggers=triggers,
            triage_instruction=instruction,
            emergency_helpline_india="112 / 108",
        )

    @staticmethod
    def sanitize_and_check_query(
        query: str,
        user_id: str | None = None,
    ) -> tuple[bool, str | None]:
        """Verify if a user query violates medical practice boundaries (e.g. asking for prescription).

        Returns: (is_blocked, rejection_message)
        """
        query_lower = query.lower()

        # Audit query attempt without PII
        audit_logger.log_event(
            action="CHAT_QUERY_GUARDRAIL_EVALUATED",
            user_id=user_id,
            details={"query_length": len(query)},
        )

        # Check for emergency signs in chat
        for kw in EMERGENCY_KEYWORDS:
            if kw in query_lower:
                return (
                    True,
                    "EMERGENCY RED FLAG DETECTED: You mentioned symptoms that could indicate an acute medical event. "
                    "Please do not wait for AI screening. Call 112 or 108 immediately or go to the nearest hospital emergency room.",
                )

        # Check for prescription/diagnosis requests
        for kw in PRESCRIPTION_DIAGNOSIS_KEYWORDS:
            if kw in query_lower:
                return (
                    True,
                    "NON-DIAGNOSTIC BOUNDARY: Sanjivani AI is an AI screening tool, not a doctor. I cannot provide definitive medical "
                    "diagnoses, prescribe medications, or recommend drug dosages. Please consult a registered medical practitioner "
                    "for prescription therapies.",
                )

        return False, None

    @staticmethod
    def append_disclaimer(response_text: str) -> str:
        """Ensure every clinical or conversational response ends with statutory disclaimer."""
        if STATUTORY_DISCLAIMER in response_text:
            return response_text
        return f"{response_text}\n\n---\n*{STATUTORY_DISCLAIMER}*"
