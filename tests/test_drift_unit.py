"""Unit tests for Evidently and KS drift monitoring."""

import pandas as pd
from src.ml.drift import DriftMonitoringService


def test_drift_monitoring_service():
    ref_df = pd.DataFrame(
        {
            "age": [25, 30, 35, 40, 45, 50, 55, 60],
            "bmi": [21.0, 22.5, 23.0, 24.5, 25.0, 26.5, 27.0, 28.5],
            "systolic_bp": [115, 120, 122, 128, 130, 135, 140, 145],
            "fasting_glucose": [85, 90, 95, 100, 105, 110, 115, 120],
        }
    )

    curr_df = pd.DataFrame(
        {
            "age": [26, 31, 36, 41, 46, 51, 56, 61],
            "bmi": [21.2, 22.7, 23.1, 24.6, 25.2, 26.7, 27.1, 28.6],
            "systolic_bp": [116, 121, 123, 129, 131, 136, 141, 146],
            "fasting_glucose": [86, 91, 96, 101, 106, 111, 116, 121],
        }
    )

    service = DriftMonitoringService(reference_data=ref_df)
    res = service.run_drift_analysis(curr_df)

    assert "dataset_drift_detected" in res
    assert "drifted_features_ratio" in res
    assert res["status"] in ["HEALTHY", "ALERT"]
