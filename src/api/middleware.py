"""API Middleware: Correlation IDs, structured logging without PII, and Rate Limiting."""

import time
import uuid

from fastapi import Request, Response
from slowapi import Limiter
from slowapi.util import get_remote_address
from src.core.audit import logger
from src.core.config import settings
from starlette.middleware.base import BaseHTTPMiddleware

# Global SlowAPI rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[settings.RATE_LIMIT_DEFAULT],
)


class SecurityAndCorrelationMiddleware(BaseHTTPMiddleware):
    """Injects correlation IDs, tracks request duration, and logs requests without PII."""

    async def dispatch(self, request: Request, call_next) -> Response:
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        request.state.correlation_id = correlation_id

        start_time = time.perf_counter()

        response: Response = await call_next(request)

        process_time = time.perf_counter() - start_time
        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["X-Process-Time-Sec"] = f"{process_time:.4f}"

        # Safe request log with zero body content (PII safety)
        logger.info(
            f"{request.method} {request.url.path} -> {response.status_code} ({process_time:.4f}s)",
            extra={"correlation_id": correlation_id},
        )

        return response
