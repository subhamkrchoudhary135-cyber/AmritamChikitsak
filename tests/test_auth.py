"""Tests for Authentication, JWT tokens, and User lifecycle."""

import pytest
from httpx import AsyncClient
from src.core.security import (
    UserRole,
    create_access_token,
    decode_token,
    get_password_hash,
    verify_password,
)


def test_password_hashing():
    pw = "SuperSecurePassword123!"
    hashed = get_password_hash(pw)

    assert hashed != pw
    assert verify_password(pw, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False


def test_jwt_token_flow():
    user_id = "test-user-uuid-1234"
    token = create_access_token(subject=user_id, role=UserRole.PATIENT)

    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == user_id
    assert payload["role"] == "patient"
    assert payload["type"] == "access"


@pytest.mark.asyncio
async def test_register_and_login_api(client: AsyncClient):
    # 1. Register new patient
    register_payload = {
        "email": "sunita.devi@example.com",
        "username": "sunita_devi",
        "password": "Password789!",
        "role": "patient",
        "full_name": "Sunita Devi",
        "phone_number": "+919812345678",
        "age": 42,
        "gender": "female",
        "preferred_language": "hi",
    }
    resp = await client.post("/api/v1/auth/register", json=register_payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "sunita.devi@example.com"
    assert data["username"] == "sunita_devi"

    # 2. Login
    login_resp = await client.post(
        "/api/v1/auth/login",
        data={"username": "sunita_devi", "password": "Password789!"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_resp.status_code == 200
    token_data = login_resp.json()
    assert "access_token" in token_data
    assert "refresh_token" in token_data

    # 3. Access /auth/me
    auth_header = {"Authorization": f"Bearer {token_data['access_token']}"}
    me_resp = await client.get("/api/v1/auth/me", headers=auth_header)
    assert me_resp.status_code == 200
    assert me_resp.json()["username"] == "sunita_devi"

    # 4. Refresh token
    refresh_resp = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": token_data["refresh_token"]},
    )
    assert refresh_resp.status_code == 200
    assert "access_token" in refresh_resp.json()
