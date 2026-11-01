"""Main FastAPI application entrypoint for Sanjivani AI."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from src.api.middleware import SecurityAndCorrelationMiddleware, limiter
from src.api.v1.router import api_router
from src.core.audit import setup_structured_logging
from src.core.config import settings
from src.core.database import init_db
from src.ml.registry import model_registry

logger = setup_structured_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for application startup and graceful shutdown."""
    logger.info("Initializing Sanjivani AI Backend & Database tables...")
    await init_db()

    logger.info("Loading / Bootstrapping ML models into memory...")
    try:
        model_registry.load_or_train()
        logger.info("ML Models loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load ML models during startup: {e}")

    yield

    logger.info("Sanjivani AI service shutting down gracefully...")


app = FastAPI(
    title="Sanjivani AI Health Risk Screening Platform",
    description=(
        "Production-grade, explainable, and multilingual AI health risk screening platform for India. "
        "Strictly provides screening support and early cardiometabolic risk stratification—never definitive medical diagnosis. "
        "Complies with India's Digital Personal Data Protection (DPDP) Act 2023."
    ),
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Attach SlowAPI rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middlewares
app.add_middleware(SecurityAndCorrelationMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus Metrics ASGI App mounted at /metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Include master API v1 router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Root"])
async def root_health():
    """Root health probe for container orchestrators and load balancers."""
    return {
        "status": "UP",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
