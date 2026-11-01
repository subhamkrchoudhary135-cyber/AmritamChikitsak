"""End-to-end API integration tests for Screenings, History, DPDP Consent, and Models."""

import pytest
from httpx import AsyncClient
from src.db.models import User


@pytest.mark.asyncio
async def test_screenings_and_history_api_flow(
    client: AsyncClient,
    test_patient_user: User,
    patient_headers: dict,
):
    # 1. Execute health screening
    screening_payload = {
        "age": 45,
        "gender": "male",
        "height_cm": 168.0,
        "weight_kg": 76.0,
        "systolic_bp": 136.0,
        "diastolic_bp": 86.0,
        "resting_heart_rate": 72.0,
        "fasting_glucose": 115.0,
        "hba1c": 6.2,
        "total_cholesterol": 210.0,
        "ldl_cholesterol": 125.0,
        "hdl_cholesterol": 45.0,
        "triglycerides": 180.0,
        "physical_activity_hours_per_week": 1.5,
        "smoking_status": "never",
        "alcohol_consumption": "none",
        "diet_type": "vegetarian",
        "family_history_diabetes": True,
        "family_history_heart_disease": False,
        "preferred_language": "hi",
    }

    resp = await client.post("/api/v1/screenings", json=screening_payload, headers=patient_headers)
    assert resp.status_code == 201
    data = resp.json()

    assert "screening_id" in data
    assert len(data["screening_id"]) > 0
    patient_id = data["patient_id"]

    # Verify classification results
    assert "diabetes" in data["conditions"]
    assert "heart_disease" in data["conditions"]
    assert "hypertension" in data["conditions"]

    # Verify regression forecast with conformal prediction intervals
    forecast = data["progression_forecast"]
    assert "forecasted_glucose_6m" in forecast
    assert "glucose_prediction_interval_6m" in forecast
    assert len(forecast["glucose_prediction_interval_6m"]) == 2

    # Verify phenotyping & SHAP
    assert "cluster_label" in data["phenotype"]
    assert len(data["top_shap_factors"]) == 5

    # Verify multilingual explanations (en, hi, pa)
    assert "en" in data["multilingual_explanations"]
    assert "hi" in data["multilingual_explanations"]
    assert "pa" in data["multilingual_explanations"]

    # 2. Retrieve history timeline
    hist_resp = await client.get(f"/api/v1/history/{patient_id}", headers=patient_headers)
    assert hist_resp.status_code == 200
    hist_data = hist_resp.json()
    assert hist_data["total_screenings"] >= 1
    assert len(hist_data["timeline"]) >= 1

    # 3. Model versions endpoint
    models_resp = await client.get("/api/v1/models/versions")
    assert models_resp.status_code == 200
    models_data = models_resp.json()
    assert len(models_data["models"]) >= 3
    assert models_data["drift_status"] == "HEALTHY"

    # 4. DPDP Right to Erasure / Data Deletion
    del_resp = await client.post(
        "/api/v1/data/delete",
        json={
            "patient_id": patient_id,
            "confirmation": True,
            "reason": "Patient requested erasure",
        },
        headers=patient_headers,
    )
    assert del_resp.status_code == 200
    assert del_resp.json()["status"] == "SUCCESS"


@pytest.mark.asyncio
async def test_health_and_metrics_endpoints(client: AsyncClient):
    # Health endpoint
    h_resp = await client.get("/health")
    assert h_resp.status_code == 200
    assert h_resp.json()["status"] == "UP"

    # Prometheus metrics endpoint
    m_resp = await client.get("/metrics", follow_redirects=True)
    assert m_resp.status_code == 200
    assert (
        "python_info" in m_resp.text
        or "process_cpu_seconds" in m_resp.text
        or m_resp.headers["content-type"].startswith("text/plain")
    )
