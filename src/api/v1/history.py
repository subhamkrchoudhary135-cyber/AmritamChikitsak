"""Longitudinal screening history API routes."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps import get_current_user, get_db
from src.core.audit import audit_logger
from src.core.security import UserRole
from src.db.models import Patient, Screening, User

router = APIRouter(prefix="/history", tags=["History"])


@router.get("/{patient_id}")
async def get_patient_screening_history(
    patient_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, Any]:
    """Retrieve longitudinal cardiometabolic trajectory and screening history."""
    # Verify patient existence
    stmt_pat = select(Patient).where(Patient.id == patient_id)
    patient = (await db.execute(stmt_pat)).scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    # Patient role authorization
    if current_user.role == UserRole.PATIENT.value and patient.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    # Fetch longitudinal screenings ordered chronologically
    stmt = (
        select(Screening)
        .where(Screening.patient_id == patient_id)
        .order_by(desc(Screening.created_at))
    )
    records = (await db.execute(stmt)).scalars().all()

    # Build longitudinal trajectory timeline
    timeline = []
    for s in records:
        bio = s.input_biometrics
        fore = s.regression_forecast
        pheno = s.clustering_phenotype
        conds = s.classification_results

        timeline.append(
            {
                "screening_id": s.id,
                "date": s.created_at.isoformat(),
                "systolic_bp": bio.get("systolic_bp"),
                "diastolic_bp": bio.get("diastolic_bp"),
                "fasting_glucose": bio.get("fasting_glucose"),
                "hba1c": bio.get("hba1c"),
                "bmi": bio.get("bmi"),
                "continuous_risk_score": fore.get("continuous_risk_score_100"),
                "cluster_label": pheno.get("cluster_label"),
                "conditions_summary": {k: v.get("risk_level") for k, v in conds.items()},
            }
        )

    audit_logger.log_event(
        action="LONGITUDINAL_HISTORY_ACCESSED",
        user_id=current_user.id,
        role=current_user.role,
        resource_type="SCREENING_HISTORY",
        resource_id=patient_id,
        details={"record_count": len(timeline)},
    )

    return {
        "patient_id": patient_id,
        "total_screenings": len(timeline),
        "timeline": timeline,
    }
