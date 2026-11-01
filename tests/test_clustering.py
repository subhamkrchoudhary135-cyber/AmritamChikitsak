"""Tests for patient phenotyping, clustering, and anomaly detection."""

import numpy as np
from src.ml.clustering import PatientPhenotypeSegmenter, evaluate_optimal_k


def test_evaluate_optimal_k():
    np.random.seed(42)
    # 3 synthetic clusters
    c1 = np.random.normal(0, 0.5, (30, 4))
    c2 = np.random.normal(5, 0.5, (30, 4))
    c3 = np.random.normal(10, 0.5, (30, 4))
    X = np.vstack([c1, c2, c3])

    best_k, sil, db = evaluate_optimal_k(X, k_range=range(2, 5))
    assert 2 <= best_k <= 4
    assert len(sil) > 0
    assert len(db) > 0


def test_patient_segmenter_and_anomaly_detector():
    np.random.seed(42)
    X = np.random.randn(80, 6)
    feature_names = ["bmi", "systolic_bp", "fasting_glucose", "hba1c", "physical_activity", "age"]

    segmenter = PatientPhenotypeSegmenter(n_clusters=3)
    segmenter.fit(X, feature_names)

    # Segment regular sample
    c_id, label, priorities, is_anomaly, score, pca_coords = segmenter.segment_patient(X[:1])
    assert 0 <= c_id < 3
    assert len(label) > 0
    assert len(priorities) > 0
    assert len(pca_coords) == 2

    # Segment extreme physiological anomaly
    extreme_sample = np.array([[15.0, 20.0, 18.0, 12.0, -10.0, 10.0]])
    _, _, _, is_anom_extreme, anom_score, _ = segmenter.segment_patient(extreme_sample)
    assert is_anom_extreme is True or anom_score > score
