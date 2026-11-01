"""Tests for Patients CRUD API endpoints and DPDP encryption."""

import pytest
from httpx import AsyncClient
from src.db.models import User


@pytest.mark.asyncio
async def test_patients_crud_and_rbac(
    client: AsyncClient,
    test_patient_user: User,
    test_doctor_user: User,
    patient_headers: dict,
    doctor_headers: dict,
):
    # 1. Create patient via API
    payload = {
        "full_name": "Amanpreet Kaur",
        "phone_number": "+919876543219",
        "abha_id": "91-9999-8888-7777",
        "age": 38,
        "gender": "female",
        "preferred_language": "pa",
        "state_province": "Punjab",
    }
    resp = await client.post("/api/v1/patients", json=payload, headers=patient_headers)
    assert resp.status_code == 201
    created = resp.json()
    patient_id = created["id"]
    assert created["full_name"] == "Amanpreet Kaur"

    # 2. List patients
    list_resp = await client.get("/api/v1/patients", headers=patient_headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 1

    # Doctor lists all patients
    doc_list_resp = await client.get("/api/v1/patients", headers=doctor_headers)
    assert doc_list_resp.status_code == 200
    assert len(doc_list_resp.json()) >= 1

    # 3. Get single patient
    get_resp = await client.get(f"/api/v1/patients/{patient_id}", headers=patient_headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == patient_id

    # 4. Update patient
    update_resp = await client.put(
        f"/api/v1/patients/{patient_id}",
        json={"age": 39, "preferred_language": "pa"},
        headers=patient_headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["age"] == 39
