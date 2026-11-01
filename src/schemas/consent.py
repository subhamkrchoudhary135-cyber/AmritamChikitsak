"""Consent and DPDP Act schemas."""

from datetime import datetime

from pydantic import BaseModel, Field


class ConsentGrantRequest(BaseModel):
    """Payload to record informed consent under India DPDP Act 2023."""

    patient_id: str
    consent_type: str = Field(
        "RISK_SCREENING",
        description="e.g. RISK_SCREENING, LIFESTYLE_ANALYTICS, ANONYMIZED_RESEARCH",
    )
    purpose_description: str = Field(
        "Consent to process health biometrics for non-diagnostic risk screening and trend forecasting under India DPDP Act 2023.",
        min_length=10,
    )
    consent_version: str = "1.0"


class ConsentResponse(BaseModel):
    """Consent status response."""

    id: str
    patient_id: str
    consent_type: str
    is_granted: bool
    purpose_description: str
    consent_version: str
    created_at: datetime
    revoked_at: datetime | None = None

    class Config:
        from_attributes = True


class DataDeletionRequest(BaseModel):
    """Payload to exercise Right to Erasure / Right to be Forgotten under DPDP Act 2023."""

    patient_id: str
    confirmation: bool = Field(..., description="Must explicitly confirm data erasure")
    reason: str | None = Field(None, max_length=500)
