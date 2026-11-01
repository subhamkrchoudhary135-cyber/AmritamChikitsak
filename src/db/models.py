"""SQLAlchemy 2.0 ORM Models for Sanjivani AI.

Implements DPDP Act 2023 compliant field encryption, audit logging,
patient management, longitudinal screenings, consent tracking, and model registry records.
"""

import uuid
from datetime import UTC, datetime
from typing import Any, Optional

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.crypto import EncryptedString
from src.core.database import Base, TimestampMixin


class User(Base, TimestampMixin):
    """System user supporting RBAC (patient, doctor, admin)."""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default="patient", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationship to Patient record
    patient_profile: Mapped[Optional["Patient"]] = relationship(
        "Patient", back_populates="user", uselist=False
    )


class Patient(Base, TimestampMixin):
    """Patient entity with DPDP Act 2023 encrypted PII and blind indexing."""

    __tablename__ = "patients"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    # Encrypted PII Fields (Stored as ciphertext in DB, decrypted automatically on load)
    full_name: Mapped[str] = mapped_column(EncryptedString(512), nullable=False)
    phone_number: Mapped[str] = mapped_column(EncryptedString(512), nullable=False)
    abha_id: Mapped[str | None] = mapped_column(
        EncryptedString(512), nullable=True
    )  # Ayushman Bharat Health Account
    address: Mapped[str | None] = mapped_column(EncryptedString(1024), nullable=True)

    # Blind Indexes (HMAC-SHA256) for searching without decrypting all database rows
    phone_blind_index: Mapped[str | None] = mapped_column(String(64), index=True, nullable=True)
    email_blind_index: Mapped[str | None] = mapped_column(String(64), index=True, nullable=True)

    # Clinical & Demographic parameters (Non-PII, used in risk stratifications)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)  # male, female, other
    preferred_language: Mapped[str] = mapped_column(
        String(10), default="en", nullable=False
    )  # en, hi, pa
    state_province: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )  # Geographic region in India

    # Relationships
    user: Mapped[Optional["User"]] = relationship("User", back_populates="patient_profile")
    screenings: Mapped[list["Screening"]] = relationship(
        "Screening", back_populates="patient", cascade="all, delete-orphan"
    )
    consents: Mapped[list["Consent"]] = relationship(
        "Consent", back_populates="patient", cascade="all, delete-orphan"
    )


class Consent(Base, TimestampMixin):
    """DPDP Act 2023 Compliant Consent Record."""

    __tablename__ = "consents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True
    )
    consent_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # e.g., "RISK_SCREENING", "DATA_STORAGE", "AI_ANALYSIS"
    is_granted: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    purpose_description: Mapped[str] = mapped_column(Text, nullable=False)
    consent_version: Mapped[str] = mapped_column(String(20), default="1.0", nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    client_ip: Mapped[str | None] = mapped_column(String(45), nullable=True)

    patient: Mapped["Patient"] = relationship("Patient", back_populates="consents")


class Screening(Base, TimestampMixin):
    """Health risk screening record with ML classifications, forecasts, clusters, and SHAP factors."""

    __tablename__ = "screenings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True
    )
    screening_type: Mapped[str] = mapped_column(String(50), default="comprehensive", nullable=False)

    # Input biometrics (JSON dict)
    input_biometrics: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    # Multi-condition Classification (Diabetes, Heart Disease, Hypertension)
    classification_results: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    # Regression Forecast (3-6 month Glucose/BMI/BP + continuous risk score + prediction intervals)
    regression_forecast: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    # Phenotyping & Clustering (Cluster label, ID, anomaly flag, PCA/UMAP coordinates)
    clustering_phenotype: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    # Explainability (Top 5 SHAP factors with impact and direction)
    explainability_shap: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    # Multilingual plain-language explanations (English, Hindi, Punjabi at Class 8 level)
    multilingual_explanations: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    # Guardrails & Safety
    is_emergency_red_flag: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    red_flag_details: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    clinical_disclaimer: Mapped[str] = mapped_column(Text, nullable=False)

    patient: Mapped["Patient"] = relationship("Patient", back_populates="screenings")


class AuditLog(Base):
    """DPDP Act Audit Log capturing all sensitive accesses without storing raw PII."""

    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False, index=True
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False)
    resource_id: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # SUCCESS, DENIED, FAILED
    client_ip: Mapped[str] = mapped_column(String(45), nullable=False)
    metadata_json: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


class ModelVersionRecord(Base, TimestampMixin):
    """Model registry table tracking loaded ML models, metrics, and fairlearn stats."""

    __tablename__ = "model_versions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    model_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    condition: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # diabetes, heart_disease, hypertension, etc.
    algorithm: Mapped[str] = mapped_column(String(50), nullable=False)
    version_tag: Mapped[str] = mapped_column(String(20), nullable=False)
    metrics: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False
    )  # ROC-AUC, Recall, Brier, etc.
    fairness_metrics: Mapped[dict[str, Any] | None] = mapped_column(
        JSON, nullable=True
    )  # Fairlearn demographic parity, equalized odds
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    model_artifact_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
