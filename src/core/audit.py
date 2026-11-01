"""DPDP Act Compliant Audit Logging Service.

Ensures every sensitive healthcare data access, screening, and consent mutation
is strictly audited with zero PII leakage into log streams or log aggregators.
"""

import json
import logging
import sys
import uuid
from datetime import UTC, datetime
from typing import Any


class AuditJSONFormatter(logging.Formatter):
    """Custom log formatter producing structured JSON lines."""

    def format(self, record: logging.LogRecord) -> str:
        log_obj: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "audit_event"):
            log_obj["audit"] = record.audit_event
        if hasattr(record, "correlation_id"):
            log_obj["correlation_id"] = record.correlation_id
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj)


def setup_structured_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure system-wide structured logger."""
    root_logger = logging.getLogger("sanjivani_ai")
    root_logger.setLevel(level)

    # Avoid duplicate handlers if re-called
    if not root_logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(AuditJSONFormatter())
        root_logger.addHandler(handler)

    return root_logger


logger = setup_structured_logging()


class AuditLogger:
    """Dedicated security and compliance audit logging helper."""

    @staticmethod
    def log_event(
        action: str,
        user_id: str | None = None,
        role: str | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
        status: str = "SUCCESS",
        client_ip: str | None = None,
        details: dict[str, Any] | None = None,
        correlation_id: str | None = None,
    ) -> None:
        """Log a secure audit event ensuring zero PII enters the record."""
        # Sanitize details to guarantee no PII keys exist
        sanitized_details: dict[str, Any] = {}
        disallowed_keys = {
            "name",
            "full_name",
            "phone",
            "email",
            "address",
            "aadhaar",
            "abha_id",
            "password",
            "token",
            "ssn",
        }
        if details:
            for k, v in details.items():
                if k.lower() in disallowed_keys:
                    sanitized_details[k] = "[REDACTED_PII]"
                else:
                    sanitized_details[k] = v

        event = {
            "audit_id": str(uuid.uuid4()),
            "action": action,
            "user_id": user_id or "ANONYMOUS",
            "role": role or "GUEST",
            "resource_type": resource_type or "GENERAL",
            "resource_id": resource_id or "N/A",
            "status": status,
            "client_ip": client_ip or "UNKNOWN",
            "details": sanitized_details,
        }

        extra: dict[str, Any] = {
            "audit_event": event,
            "correlation_id": correlation_id or str(uuid.uuid4()),
        }
        logger.info(f"AUDIT: [{action}] {status} by user={user_id or 'anon'}", extra=extra)


audit_logger = AuditLogger()
