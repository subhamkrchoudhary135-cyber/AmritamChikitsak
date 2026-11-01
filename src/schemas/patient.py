"""Patient schemas with DPDP Act fields."""

from datetime import datetime

from pydantic import BaseModel, Field


class PatientCreate(BaseModel):
    """Payload to register or create a patient profile."""

    full_name: str = Field(..., min_length=2, max_length=100)
    phone_number: str = Field(..., pattern=r"^\+?[0-9]{10,15}$")
    abha_id: str | None = Field(
        None, description="Ayushman Bharat Health Account ID (e.g., 91-1234-5678-9012)"
    )
    address: str | None = None
    age: int = Field(..., ge=1, le=120)
    gender: str = Field(..., pattern="^(male|female|other)$")
    preferred_language: str = Field("en", pattern="^(en|hi|pa)$")
    state_province: str | None = Field(None, max_length=50)


class PatientUpdate(BaseModel):
    """Payload to update patient profile."""

    full_name: str | None = Field(None, min_length=2, max_length=100)
    phone_number: str | None = Field(None, pattern=r"^\+?[0-9]{10,15}$")
    abha_id: str | None = None
    address: str | None = None
    age: int | None = Field(None, ge=1, le=120)
    gender: str | None = Field(None, pattern="^(male|female|other)$")
    preferred_language: str | None = Field(None, pattern="^(en|hi|pa)$")
    state_province: str | None = None


class PatientResponse(BaseModel):
    """Safe patient profile response."""

    id: str
    user_id: str | None
    full_name: str
    phone_number: str
    abha_id: str | None = None
    address: str | None = None
    age: int
    gender: str
    preferred_language: str
    state_province: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
