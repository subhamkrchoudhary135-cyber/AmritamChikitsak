"""Tests for PDF Report generation with ReportLab."""

import pytest
from httpx import AsyncClient
from src.db.models import User


@pytest.mark.asyncio
async def test_generate_pdf_report(
    client: AsyncClient,
    test_patient_user: User,
    patient_headers: dict,
):
    # 1. Create a screening first
    screening_payload = {
        "age": 45,
        "gender": "male",
        "height_cm": 168.0,
        "weight_kg": 74.0,
        "systolic_bp": 130.0,
        "diastolic_bp": 84.0,
        "fasting_glucose": 110.0,
        "hba1c": 5.9,
    }
    screen_resp = await client.post(
        "/api/v1/screenings", json=screening_payload, headers=patient_headers
    )
    assert screen_resp.status_code == 201
    screening_id = screen_resp.json()["screening_id"]

    # 2. Request PDF report
    pdf_resp = await client.get(
        f"/api/v1/reports/pdf?screening_id={screening_id}&language=en",
        headers=patient_headers,
    )
    assert pdf_resp.status_code == 200
    assert pdf_resp.headers["content-type"] == "application/pdf"
    assert pdf_resp.content.startswith(b"%PDF")
