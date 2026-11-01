"""Algorithmic fairness evaluation across demographic sub-populations using Fairlearn."""

from typing import Any

import numpy as np
import pandas as pd
from fairlearn.metrics import (
    MetricFrame,
    demographic_parity_difference,
    demographic_parity_ratio,
    equalized_odds_difference,
    false_positive_rate,
    selection_rate,
    true_positive_rate,
)


def evaluate_fairlearn_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    sensitive_features_df: pd.DataFrame,
) -> dict[str, Any]:
    """Calculate demographic parity and equalized odds metrics across gender and age brackets."""
    report: dict[str, Any] = {}

    # Define standard evaluation metrics
    metrics_dict = {
        "selection_rate": selection_rate,
        "true_positive_rate": true_positive_rate,
        "false_positive_rate": false_positive_rate,
    }

    # Evaluate across Gender
    if "gender" in sensitive_features_df.columns:
        gender_col = sensitive_features_df["gender"]
        gender_frame = MetricFrame(
            metrics=metrics_dict,
            y_true=y_true,
            y_pred=y_pred,
            sensitive_features=gender_col,
        )

        dp_diff_gender = float(
            demographic_parity_difference(y_true, y_pred, sensitive_features=gender_col)
        )
        dp_ratio_gender = float(
            demographic_parity_ratio(y_true, y_pred, sensitive_features=gender_col)
        )
        eo_diff_gender = float(
            equalized_odds_difference(y_true, y_pred, sensitive_features=gender_col)
        )

        report["gender"] = {
            "demographic_parity_difference": round(dp_diff_gender, 4),
            "demographic_parity_ratio": round(dp_ratio_gender, 4),
            "equalized_odds_difference": round(eo_diff_gender, 4),
            "by_group": gender_frame.by_group.to_dict(),
            "fairness_passed": bool(abs(dp_diff_gender) < 0.15 and eo_diff_gender < 0.15),
        }

    # Evaluate across Age Categories (< 45 vs >= 45)
    if "age" in sensitive_features_df.columns:
        age_groups = np.where(sensitive_features_df["age"] < 45, "age_under_45", "age_45_and_above")
        age_frame = MetricFrame(
            metrics=metrics_dict,
            y_true=y_true,
            y_pred=y_pred,
            sensitive_features=age_groups,
        )

        dp_diff_age = float(
            demographic_parity_difference(y_true, y_pred, sensitive_features=age_groups)
        )
        dp_ratio_age = float(
            demographic_parity_ratio(y_true, y_pred, sensitive_features=age_groups)
        )
        eo_diff_age = float(
            equalized_odds_difference(y_true, y_pred, sensitive_features=age_groups)
        )

        report["age_bracket"] = {
            "demographic_parity_difference": round(dp_diff_age, 4),
            "demographic_parity_ratio": round(dp_ratio_age, 4),
            "equalized_odds_difference": round(eo_diff_age, 4),
            "by_group": age_frame.by_group.to_dict(),
            "fairness_passed": bool(abs(dp_diff_age) < 0.20 and eo_diff_age < 0.20),
        }

    return report
