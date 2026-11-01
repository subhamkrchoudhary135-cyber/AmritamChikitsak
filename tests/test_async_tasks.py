"""Tests for Celery asynchronous tasks."""

from src.tasks.async_tasks import async_batch_screening, async_generate_evidently_drift_report


def test_async_batch_screening():
    batch = [
        {
            "age": 42,
            "gender": "female",
            "height_cm": 160.0,
            "weight_kg": 62.0,
            "systolic_bp": 120.0,
            "diastolic_bp": 80.0,
            "fasting_glucose": 95.0,
            "hba1c": 5.4,
        },
        {
            "age": 58,
            "gender": "male",
            "height_cm": 172.0,
            "weight_kg": 88.0,
            "systolic_bp": 150.0,
            "diastolic_bp": 95.0,
            "fasting_glucose": 140.0,
            "hba1c": 7.2,
        },
    ]

    res = async_batch_screening(batch)
    assert res["processed_count"] == 2
    assert len(res["results"]) == 2
    assert res["results"][0]["status"] == "SUCCESS"


def test_async_drift_report_task():
    sample_records = [
        {"age": 45, "bmi": 24.5, "systolic_bp": 125, "fasting_glucose": 98},
        {"age": 52, "bmi": 27.2, "systolic_bp": 138, "fasting_glucose": 112},
    ]
    report = async_generate_evidently_drift_report(sample_records)
    assert "status" in report
    assert "drifted_features_ratio" in report
