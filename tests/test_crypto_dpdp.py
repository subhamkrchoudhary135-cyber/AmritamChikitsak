"""Tests for DPDP Act field-level encryption and blind indexing."""

from src.core.crypto import pii_crypto


def test_pii_encryption_and_decryption():
    plaintext = "Rajesh Kumar Sharma"
    encrypted = pii_crypto.encrypt(plaintext)

    assert encrypted is not None
    assert encrypted != plaintext
    assert len(encrypted) > len(plaintext)

    decrypted = pii_crypto.decrypt(encrypted)
    assert decrypted == plaintext


def test_encryption_handles_none():
    assert pii_crypto.encrypt(None) is None
    assert pii_crypto.decrypt(None) is None
    assert pii_crypto.compute_blind_index(None) is None


def test_blind_indexing_deterministic():
    phone_1 = "+919876543210"
    phone_2 = "+919876543210 "  # with whitespace

    hash_1 = pii_crypto.compute_blind_index(phone_1)
    hash_2 = pii_crypto.compute_blind_index(phone_2)

    assert hash_1 == hash_2
    assert len(hash_1) == 64  # SHA256 hex length
    assert hash_1 != phone_1


def test_mask_identifier():
    masked_phone = pii_crypto.mask_identifier("+919876543210")
    assert masked_phone.startswith("+91")
    assert masked_phone.endswith("10")
    assert "*" in masked_phone
