"""Model metadata, versioning, and drift monitoring schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ModelVersionInfo(BaseModel):
    """Metadata describing a trained ML model."""

    condition: str
    algorithm: str
    version_tag: str
    metrics: dict[str, float] = Field(..., description="ROC-AUC, PR-AUC, Recall, F1, Brier, etc.")
    fairness_metrics: dict[str, Any] | None = Field(
        None, description="Demographic parity & equalized odds"
    )
    decision_threshold: float
    trained_at: datetime
    is_active: bool = True


class ModelRegistrySummary(BaseModel):
    """Summary of all deployed models in the Sanjivani AI platform."""

    platform_version: str
    models: list[ModelVersionInfo]
    last_drift_check: datetime | None = None
    drift_status: str = "HEALTHY"
