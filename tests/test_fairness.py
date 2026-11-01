"""Tests for Fairlearn algorithmic fairness across demographic subgroups."""

import numpy as np
import pandas as pd
from src.ml.fairness import evaluate_fairlearn_metrics


def test_fairlearn_evaluation():
    np.random.seed(42)
    n = 100
    y_true = np.random.choice([0, 1], size=n, p=[0.7, 0.3])
    y_pred = y_true.copy()  # ideal accurate predictor
    # Inject mild error
    y_pred[:5] = 1 - y_pred[:5]

    sensitive_df = pd.DataFrame(
        {
            "gender": np.random.choice(["male", "female"], size=n),
            "age": np.random.randint(20, 75, size=n),
        }
    )

    report = evaluate_fairlearn_metrics(y_true, y_pred, sensitive_df)

    assert "gender" in report
    assert "demographic_parity_difference" in report["gender"]
    assert "equalized_odds_difference" in report["gender"]
    assert "fairness_passed" in report["gender"]

    assert "age_bracket" in report
    assert "demographic_parity_difference" in report["age_bracket"]
