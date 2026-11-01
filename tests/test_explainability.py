"""Tests for SHAP feature attribution and local explainability."""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from src.ml.explainability import ShapExplainerService


def test_shap_explainer_service():
    np.random.seed(42)
    X = np.random.randn(50, 4)
    y = (X[:, 0] > 0).astype(int)

    rf = RandomForestClassifier(n_estimators=10, random_state=42)
    rf.fit(X, y)

    feature_names = ["bmi", "systolic_bp", "fasting_glucose", "age"]
    explainer = ShapExplainerService(rf, background_sample=X[:20], feature_names=feature_names)

    factors = explainer.explain_instance(
        x_patient=X[:1],
        raw_patient_dict={"bmi": 28.5, "systolic_bp": 140, "fasting_glucose": 130, "age": 52},
        top_k=3,
    )

    assert len(factors) == 3
    for f in factors:
        assert f.feature in feature_names
        assert f.impact_score >= 0.0
        assert f.direction in ["increases_risk", "decreases_risk", "neutral"]
        assert len(f.clinical_reference) > 0
