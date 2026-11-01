"""Master API Router for v1 endpoints."""

from fastapi import APIRouter
from src.api.v1.auth import router as auth_router
from src.api.v1.chat import router as chat_router
from src.api.v1.consent import router as consent_router
from src.api.v1.health import router as health_router
from src.api.v1.history import router as history_router
from src.api.v1.models_meta import router as models_router
from src.api.v1.patients import router as patients_router
from src.api.v1.reports import router as reports_router
from src.api.v1.screenings import router as screenings_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(patients_router)
api_router.include_router(screenings_router)
api_router.include_router(history_router)
api_router.include_router(chat_router)
api_router.include_router(reports_router)
api_router.include_router(consent_router)
api_router.include_router(models_router)
