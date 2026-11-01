"""Application configuration using Pydantic v2 Settings."""

from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # General
    PROJECT_NAME: str = "Sanjivani AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["development", "testing", "production"] = "development"
    DEBUG: bool = True

    # Security & Auth
    SECRET_KEY: str = "sanjivani-ai-super-secret-key-change-in-production-2026-secure"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # DPDP Act 2023 - Field-Level Encryption Key (Fernet 32 url-safe base64 encoded bytes)
    # Default is a valid 32-byte Fernet key for dev/test
    DPDP_ENCRYPTION_KEY: str = "tU_h7nL3w-u7-sR58vB0VfM6iWwJ9qK4h1b8yV6d0nQ="

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]

    # Database (PostgreSQL default, falls back to SQLite for tests/local dev)
    DATABASE_URL: str = "sqlite+aiosqlite:///./sanjivani_ai.db"
    SYNC_DATABASE_URL: str = "sqlite:///./sanjivani_ai.db"

    # Redis & Celery
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # MLflow & Models
    MLFLOW_TRACKING_URI: str = "file:./mlruns"
    MODEL_REGISTRY_DIR: str = "models_cache"
    CHROMA_PERSIST_DIRECTORY: str = "data/chroma_db"

    # LLM Settings
    LLM_PROVIDER: Literal["offline", "claude", "ollama"] = "offline"
    ANTHROPIC_API_KEY: str | None = None
    ANTHROPIC_MODEL: str = "claude-3-haiku-20240307"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3:8b"

    # Rate Limiting
    RATE_LIMIT_DEFAULT: str = "100/minute"
    RATE_LIMIT_SCREENING: str = "20/minute"

    # Tesseract OCR path (optional on windows)
    TESSERACT_CMD: str | None = None

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: any) -> list[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return ["*"]


settings = Settings()
