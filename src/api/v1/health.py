"""Health check and readiness API endpoints."""

from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps import get_db
from src.core.config import settings
from src.ml.registry import model_registry

router = APIRouter(tags=["Health"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check(
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Liveness and readiness health check probe."""
    # 1. Test Database connection
    db_status = "HEALTHY"
    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"UNHEALTHY: {str(e)}"

    # 2. Test ML Engine
    ml_status = "LOADED" if model_registry.is_loaded else "STANDBY"

    return {
        "status": "UP",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "database": db_status,
        "ml_engine": ml_status,
    }
