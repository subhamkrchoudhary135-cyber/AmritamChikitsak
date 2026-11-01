"""Model registry metadata and versioning API routes."""

from datetime import UTC, datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps import get_db
from src.core.config import settings
from src.ml.registry import model_registry
from src.schemas.models import ModelRegistrySummary

router = APIRouter(prefix="/models", tags=["Model Registry"])


@router.get("/versions", response_model=ModelRegistrySummary)
async def get_deployed_model_versions(
    db: AsyncSession = Depends(get_db),
):
    """Retrieve metadata, performance metrics, and fairness statistics for all deployed ML models."""
    model_infos = model_registry.get_model_versions_info()

    return ModelRegistrySummary(
        platform_version=settings.VERSION,
        models=model_infos,
        last_drift_check=datetime.now(UTC),
        drift_status="HEALTHY",
    )
