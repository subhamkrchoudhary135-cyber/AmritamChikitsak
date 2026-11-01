"""Patient management API routes with DPDP Act encryption."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps import get_current_user, get_db
from src.core.audit import audit_logger
from src.core.crypto import pii_crypto
from src.core.security import UserRole
from src.db.models import Patient, User
from src.schemas.patient import PatientCreate, PatientResponse, PatientUpdate

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post("", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient_profile(
    payload: PatientCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new patient record with AES/Fernet encrypted PII fields."""
    patient = Patient(
        user_id=current_user.id if current_user.role == UserRole.PATIENT.value else None,
        full_name=payload.full_name,
        phone_number=payload.phone_number,
        abha_id=payload.abha_id,
        address=payload.address,
        age=payload.age,
        gender=payload.gender,
        preferred_language=payload.preferred_language,
        state_province=payload.state_province,
        phone_blind_index=pii_crypto.compute_blind_index(payload.phone_number),
    )
    db.add(patient)
    await db.commit()
    await db.refresh(patient)

    audit_logger.log_event(
        action="PATIENT_PROFILE_CREATED",
        user_id=current_user.id,
        role=current_user.role,
        resource_type="PATIENT",
        resource_id=patient.id,
    )

    return patient


@router.get("", response_model=list[PatientResponse])
async def list_patients(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List patients (Doctors/Admins see all; Patients see only their own linked profile)."""
    if current_user.role == UserRole.PATIENT.value:
        stmt = select(Patient).where(Patient.user_id == current_user.id)
    else:
        stmt = select(Patient).offset(skip).limit(limit)

    results = (await db.execute(stmt)).scalars().all()

    audit_logger.log_event(
        action="PATIENTS_LIST_ACCESSED",
        user_id=current_user.id,
        role=current_user.role,
        resource_type="PATIENT",
        resource_id=f"count_{len(results)}",
    )

    return results


@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient_by_id(
    patient_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve specific patient profile with authorization checks."""
    stmt = select(Patient).where(Patient.id == patient_id)
    patient = (await db.execute(stmt)).scalar_one_or_none()

    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    # Patient can only access their own profile
    if current_user.role == UserRole.PATIENT.value and patient.user_id != current_user.id:
        audit_logger.log_event(
            action="UNAUTHORIZED_PATIENT_ACCESS_ATTEMPT",
            user_id=current_user.id,
            role=current_user.role,
            resource_type="PATIENT",
            resource_id=patient_id,
            status="DENIED",
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to this patient profile"
        )

    return patient


@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient(
    patient_id: str,
    payload: PatientUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update patient demographics or contact info."""
    stmt = select(Patient).where(Patient.id == patient_id)
    patient = (await db.execute(stmt)).scalar_one_or_none()

    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    if current_user.role == UserRole.PATIENT.value and patient.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(patient, field, value)

    if payload.phone_number:
        patient.phone_blind_index = pii_crypto.compute_blind_index(payload.phone_number)

    await db.commit()
    await db.refresh(patient)

    audit_logger.log_event(
        action="PATIENT_PROFILE_UPDATED",
        user_id=current_user.id,
        role=current_user.role,
        resource_type="PATIENT",
        resource_id=patient_id,
    )

    return patient
