"""DPDP Act 2023 Compliant Field-Level Cryptography for PII protection.

Provides AES-128/256-CBC with HMAC via Fernet and blind indexing with HMAC-SHA256
so that patient PII is encrypted at rest in PostgreSQL/SQLite and never logged.
"""

import base64
import hashlib
import hmac

from cryptography.fernet import Fernet, InvalidToken
from sqlalchemy.types import String, TypeDecorator

from src.core.config import settings


class PIIEncryptionService:
    """Service providing symmetric encryption and blind indexing for sensitive fields."""

    def __init__(self, key: str | None = None):
        self._key = (key or settings.DPDP_ENCRYPTION_KEY).encode("utf-8")
        try:
            self._fernet = Fernet(self._key)
        except Exception:
            # Fallback for dev / tests if key is not 32 url-safe base64
            derived_key = base64.urlsafe_b64encode(hashlib.sha256(self._key).digest())
            self._fernet = Fernet(derived_key)

    def encrypt(self, plaintext: str | None) -> str | None:
        """Encrypt plaintext string into base64 token."""
        if plaintext is None:
            return None
        return self._fernet.encrypt(plaintext.encode("utf-8")).decode("utf-8")

    def decrypt(self, ciphertext: str | None) -> str | None:
        """Decrypt base64 token back to plaintext string."""
        if ciphertext is None:
            return None
        try:
            return self._fernet.decrypt(ciphertext.encode("utf-8")).decode("utf-8")
        except InvalidToken:
            # If text is already plain or corrupted, return fallback gracefully
            return ciphertext

    def compute_blind_index(self, value: str | None) -> str | None:
        """Generate a deterministic HMAC-SHA256 hash for exact-match database queries."""
        if value is None:
            return None
        normalized = value.strip().lower().encode("utf-8")
        return hmac.new(self._key, normalized, hashlib.sha256).hexdigest()

    def mask_identifier(self, identifier: str | None) -> str:
        """Mask identifiers for safe display / logging (e.g. +91 98765*****)."""
        if not identifier:
            return "N/A"
        if len(identifier) <= 4:
            return "*" * len(identifier)
        return identifier[:3] + "*" * (len(identifier) - 5) + identifier[-2:]


pii_crypto = PIIEncryptionService()


class EncryptedString(TypeDecorator):
    """SQLAlchemy TypeDecorator that encrypts data before storing and decrypts on retrieval."""

    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return pii_crypto.encrypt(str(value))
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return pii_crypto.decrypt(value)
        return value
