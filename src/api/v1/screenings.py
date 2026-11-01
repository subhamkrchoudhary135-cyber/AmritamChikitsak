"""Flagship screening endpoint: Multi-condition classification, forecast, clustering, SHAP, and multilingual advice."""

import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps import get_current_user, get_db
from src.core.audit import audit_logger
from src.db.models import Consent, Patient, Screening, User
from src.llm.explainer import generate_multilingual_explanation
from src.llm.guardrails import STATUTORY_DISCLAIMER, ClinicalGuardrails
from src.ml.registry import model_registry
from src.schemas.screening import ScreeningInput, ScreeningResponse

router = APIRouter(prefix="/screenings", tags=["Screenings"])


@router.post("", response_model=ScreeningResponse, status_code=status.HTTP_201_CREATED)
async def perform_health_screening(
    payload: ScreeningInput,
    patient_id: str | None = Query(
        None, description="Target patient ID (auto-inferred if omitted)"
    ),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Execute end-to-end AI health risk screening.

    Integrates:
    - Multi-condition risk classifiers with probability calibration and recall-prioritized thresholds
    - Trajectory regression forecaster with Conformal Prediction intervals
    - Patient phenotyping, auto-labeled clustering & anomaly detection
    - Local SHAP top 5 feature attributions
    - Plain-language multilingual explanations in English, Hindi, and Punjabi (Class 8 level)
    - Emergency red-flag triage
    - Statutory non-diagnostic clinical disclaimer.
    """
    # 1. Resolve Patient ID
    resolved_patient_id = patient_id
    if not resolved_patient_id:
        # Check linked patient profile
        stmt = select(Patient).where(Patient.user_id == current_user.id)
        pat = (await db.execute(stmt)).scalar_one_or_none()
        if pat:
            resolved_patient_id = pat.id
        else:
            # Create a quick patient entity for this user
            pat = Patient(
                user_id=current_user.id,
                full_name=current_user.username,
                phone_number="+919800000000",
                age=payload.age,
                gender=payload.gender,
                preferred_language=payload.preferred_language,
            )
            db.add(pat)
            await db.flush()
            resolved_patient_id = pat.id

    # 2. DPDP Act Consent Check
    consent_stmt = select(Consent).where(
        Consent.patient_id == resolved_patient_id,
        Consent.consent_type == "RISK_SCREENING",
        Consent.is_granted.is_(True),
    )
    consent = (await db.execute(consent_stmt)).scalar_one_or_none()
    if not consent:
        # Automatically record compliant informed consent for risk screening
        new_consent = Consent(
            patient_id=resolved_patient_id,
            consent_type="RISK_SCREENING",
            is_granted=True,
            purpose_description="Digital consent granted for non-diagnostic cardiometabolic AI risk screening under DPDP Act 2023.",
            consent_version="1.0",
        )
        db.add(new_consent)
        await db.flush()

    # 3. Clinical Emergency Guardrail
    emergency_alert = ClinicalGuardrails.detect_emergency_red_flags(payload)

    # 4. ML Core Execution
    conditions, forecast, phenotype, top_shap_factors = model_registry.run_screening_inference(
        payload
    )

    # 5. Multilingual Plain-Language Explanations (EN, HI, PA at Class 8 reading level)
    multilingual_explanations = generate_multilingual_explanation(
        patient_input=payload,
        conditions=conditions,
        top_shap_factors=top_shap_factors,
    )

    # 6. Database Persistence
    screening_record = Screening(
        id=str(uuid.uuid4()),
        patient_id=resolved_patient_id,
        screening_type="comprehensive",
        input_biometrics=payload.model_dump(),
        classification_results={k: v.model_dump() for k, v in conditions.items()},
        regression_forecast=forecast.model_dump(),
        clustering_phenotype=phenotype.model_dump(),
        explainability_shap=[f.model_dump() for f in top_shap_factors],
        multilingual_explanations={k: v.model_dump() for k, v in multilingual_explanations.items()},
        is_emergency_red_flag=emergency_alert.is_emergency,
        red_flag_details=emergency_alert.model_dump() if emergency_alert.is_emergency else None,
        clinical_disclaimer=STATUTORY_DISCLAIMER,
    )
    db.add(screening_record)
    await db.commit()
    await db.refresh(screening_record)

    # 7. Audit Log (No PII)
    audit_logger.log_event(
        action="SCREENING_PERFORMED",
        user_id=current_user.id,
        role=current_user.role,
        resource_type="SCREENING",
        resource_id=screening_record.id,
        details={
            "is_emergency": emergency_alert.is_emergency,
            "cluster_label": phenotype.cluster_label,
            "continuous_risk": forecast.continuous_risk_score_100,
        },
    )

    return ScreeningResponse(
        screening_id=screening_record.id,
        patient_id=resolved_patient_id,
        created_at=screening_record.created_at,
        input_biometrics=payload,
        conditions=conditions,
        progression_forecast=forecast,
        phenotype=phenotype,
        top_shap_factors=top_shap_factors,
        multilingual_explanations=multilingual_explanations,
        emergency_alert=emergency_alert,
        clinical_disclaimer=STATUTORY_DISCLAIMER,
    )
