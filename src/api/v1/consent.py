"""DPDP Act 2023 Consent Management and Data Erasure endpoints."""

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps import get_current_user, get_db
from src.core.audit import audit_logger
from src.core.security import UserRole
from src.db.models import Consent, Patient, Screening, User
from src.schemas.consent import ConsentGrantRequest, ConsentResponse, DataDeletionRequest

router = APIRouter(tags=["DPDP Act & Consent"])


@router.post("/consent", response_model=ConsentResponse, status_code=status.HTTP_201_CREATED)
async def record_patient_consent(
    payload: ConsentGrantRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Record informed digital consent under India's DPDP Act 2023."""
    # Verify patient ownership
    stmt = select(Patient).where(Patient.id == payload.patient_id)
    patient = (await db.execute(stmt)).scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    if current_user.role == UserRole.PATIENT.value and patient.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    consent = Consent(
        patient_id=payload.patient_id,
        consent_type=payload.consent_type,
        is_granted=True,
        purpose_description=payload.purpose_description,
        consent_version=payload.consent_version,
    )
    db.add(consent)
    await db.commit()
    await db.refresh(consent)

    audit_logger.log_event(
        action="CONSENT_RECORDED",
        user_id=current_user.id,
        role=current_user.role,
        resource_type="CONSENT",
        resource_id=consent.id,
        details={"consent_type": payload.consent_type, "version": payload.consent_version},
    )

    return consent


@router.post("/consent/{consent_id}/revoke", response_model=ConsentResponse)
async def revoke_patient_consent(
    consent_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Revoke a previously granted consent under DPDP Act 2023."""
    stmt = select(Consent).where(Consent.id == consent_id)
    consent = (await db.execute(stmt)).scalar_one_or_none()
    if not consent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Consent record not found"
        )

    consent.is_granted = False
    consent.revoked_at = datetime.now(UTC)
    await db.commit()
    await db.refresh(consent)

    audit_logger.log_event(
        action="CONSENT_REVOKED",
        user_id=current_user.id,
        role=current_user.role,
        resource_type="CONSENT",
        resource_id=consent.id,
    )

    return consent


@router.post("/data/delete", status_code=status.HTTP_200_OK)
async def exercise_right_to_erasure(
    payload: DataDeletionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Exercise 'Right to Erasure' under Section 12 of India DPDP Act 2023.

    Permanently purges patient PII, screenings, and consent records.
    """
    if not payload.confirmation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Explicit confirmation is required to execute irreversible data erasure",
        )

    stmt = select(Patient).where(Patient.id == payload.patient_id)
    patient = (await db.execute(stmt)).scalar_one_or_none()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient record not found"
        )

    if current_user.role == UserRole.PATIENT.value and patient.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    # Cascade delete screenings and consents
    await db.execute(delete(Screening).where(Screening.patient_id == payload.patient_id))
    await db.execute(delete(Consent).where(Consent.patient_id == payload.patient_id))
    await db.delete(patient)
    await db.commit()

    audit_logger.log_event(
        action="DPDP_RIGHT_TO_ERASURE_EXECUTED",
        user_id=current_user.id,
        role=current_user.role,
        resource_type="PATIENT_DATA",
        resource_id=payload.patient_id,
        status="SUCCESS",
        details={"reason": payload.reason or "Patient request"},
    )

    return {
        "status": "SUCCESS",
        "message": "All patient personal data, screenings, and consent records have been irreversibly purged under DPDP Act 2023.",
        "erased_patient_id": payload.patient_id,
    }
