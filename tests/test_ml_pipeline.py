"""Tests for ML data generation, preprocessing, and SMOTE balancing."""

import numpy as np
from src.ml.datasets import generate_synthetic_clinical_cohort
from src.ml.preprocessor import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    balance_training_data,
    build_preprocessor_pipeline,
)


def test_clinical_cohort_generation():
    df = generate_synthetic_clinical_cohort(n_samples=200, random_state=42)
    assert len(df) == 200
    assert "target_diabetes" in df.columns
    assert "target_heart_disease" in df.columns
    assert "target_hypertension" in df.columns

    # Verify Asian Indian BMI traits
    assert df["bmi"].min() >= 15.0
    assert df["systolic_bp"].mean() > 100.0


def test_preprocessor_with_iterative_imputer():
    df = generate_synthetic_clinical_cohort(n_samples=100, random_state=42)
    preprocessor = build_preprocessor_pipeline(use_iterative_imputer=True)

    X_trans = preprocessor.fit_transform(df[NUMERIC_FEATURES + CATEGORICAL_FEATURES])
    assert not np.isnan(X_trans).any()
    assert X_trans.shape[0] == 100


def test_smote_balancing():
    X = np.random.randn(100, 5)
    y = np.array([0] * 85 + [1] * 15)  # imbalanced 15% positive

    X_bal, y_bal = balance_training_data(X, y)
    assert len(y_bal) >= len(y)
    assert sum(y_bal == 1) > 15
