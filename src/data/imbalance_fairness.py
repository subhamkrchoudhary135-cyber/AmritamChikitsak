"""Phase 6: Class Imbalance Evaluation & Fairness Subgroup Audit for Sanjivani AI.

Implements:
1. Class imbalance quantification per disease (diabetes, heart disease, hypertension).
2. Rigorous comparison of resampling methods applied INSIDE Cross-Validation:
   - Baseline (No resampling)
   - Balanced Class Weights
   - SMOTE (Synthetic Minority Over-sampling Technique)
   - BorderlineSMOTE
   - RandomUnderSampler
   Using imblearn.pipeline.Pipeline to strictly eliminate leakage into validation folds.
3. Subgroup representation audit across Sex, Age Bands, and Source origins.
4. Export of fairness metrics and small subgroup warnings to reports/fairness_subgroup_audit.csv.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE, BorderlineSMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.under_sampling import RandomUnderSampler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import RobustScaler

logger = logging.getLogger("sanjivani_ai.data.imbalance_fairness")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def audit_class_imbalance(
    df: pd.DataFrame,
    targets: list[str] | None = None,
) -> pd.DataFrame:
    """Measure class distributions and minority proportions across target diseases."""
    target_list = targets or ["target_diabetes", "target_heart_disease", "target_hypertension"]
    stats = []

    for t in target_list:
        if t in df.columns:
            s = df[t].dropna()
            total = len(s)
            positives = int((s == 1).sum())
            negatives = int((s == 0).sum())
            pos_pct = (positives / total) * 100.0 if total > 0 else 0.0
            imbalance_ratio = (negatives / positives) if positives > 0 else np.nan

            stats.append(
                {
                    "target": t,
                    "total_valid_cases": total,
                    "negative_count": negatives,
                    "positive_count": positives,
                    "positive_prevalence_pct": round(pos_pct, 2),
                    "imbalance_ratio_neg_to_pos": round(imbalance_ratio, 2)
                    if not np.isnan(imbalance_ratio)
                    else "N/A",
                    "severity": "High"
                    if pos_pct < 15 or pos_pct > 85
                    else ("Moderate" if pos_pct < 30 or pos_pct > 70 else "Balanced"),
                }
            )

    report = pd.DataFrame(stats)
    logger.info(f"Class imbalance audit:\n{report.to_string(index=False)}")
    return report


def compare_resampling_strategies_inside_cv(
    X: pd.DataFrame,
    y: pd.Series,
    n_splits: int = 5,
    random_state: int = 42,
) -> pd.DataFrame:
    """Evaluate resampling strategies INSIDE cross-validation folds using imblearn.pipeline.

    Guarantees zero validation data contamination during synthetic sampling.
    """
    logger.info(f"Comparing 5 resampling strategies across {n_splits}-fold Stratified CV...")
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)

    strategies: dict[str, Any] = {
        "baseline_unweighted": None,
        "class_weight_balanced": "balanced",
        "smote": SMOTE(random_state=random_state),
        "borderline_smote": BorderlineSMOTE(random_state=random_state),
        "random_undersampling": RandomUnderSampler(random_state=random_state),
    }

    results = []

    # Select numerical columns and impute for benchmark classifier
    X_num = X.select_dtypes(include=[np.number]).copy()
    feature_cols = [
        c for c in X_num.columns if not c.startswith("target_") and c not in ["patient_id"]
    ]
    X_matrix = X_num[feature_cols].copy()

    for name, sampler in strategies.items():
        roc_scores, pr_recalls, f1_scores = [], [], []

        for train_idx, val_idx in skf.split(X_matrix, y):
            X_tr, X_val = X_matrix.iloc[train_idx].copy(), X_matrix.iloc[val_idx].copy()
            y_tr, y_val = y.iloc[train_idx], y.iloc[val_idx]

            # Impute training fold only
            imp = SimpleImputer(strategy="median")
            X_tr_imp = imp.fit_transform(X_tr)
            X_val_imp = imp.transform(X_val)

            # Build pipeline step with RobustScaler to prevent convergence warnings
            scaler = RobustScaler()
            X_tr_scaled = scaler.fit_transform(X_tr_imp)
            X_val_scaled = scaler.transform(X_val_imp)

            if sampler is None:
                clf = LogisticRegression(max_iter=1000, random_state=random_state)
                clf.fit(X_tr_scaled, y_tr)
            elif sampler == "balanced":
                clf = LogisticRegression(
                    class_weight="balanced", max_iter=1000, random_state=random_state
                )
                clf.fit(X_tr_scaled, y_tr)
            else:
                pipe = ImbPipeline(
                    [
                        ("sampler", sampler),
                        ("clf", LogisticRegression(max_iter=1000, random_state=random_state)),
                    ]
                )
                pipe.fit(X_tr_scaled, y_tr)
                clf = pipe.named_steps["clf"]

            # Evaluate on uncontaminated validation fold
            y_pred = clf.predict(X_val_scaled)
            y_proba = (
                clf.predict_proba(X_val_scaled)[:, 1] if hasattr(clf, "predict_proba") else y_pred
            )

            roc_scores.append(roc_auc_score(y_val, y_proba))
            pr_recalls.append(recall_score(y_val, y_pred, zero_division=0))
            f1_scores.append(f1_score(y_val, y_pred, zero_division=0))

        results.append(
            {
                "resampling_strategy": name,
                "mean_roc_auc": round(float(np.mean(roc_scores)), 4),
                "mean_recall": round(float(np.mean(pr_recalls)), 4),
                "mean_f1": round(float(np.mean(f1_scores)), 4),
            }
        )

    eval_df = pd.DataFrame(results).sort_values(by="mean_recall", ascending=False)
    logger.info(
        f"Resampling comparison results (prioritizing recall for clinical safety):\n{eval_df.to_string(index=False)}"
    )
    return eval_df


def audit_fairness_subgroups(
    df: pd.DataFrame,
    min_sample_threshold: int = 30,
    reports_dir: str | Path = "reports",
) -> pd.DataFrame:
    """Audit representation across demographics (Sex, Age Bands) and Data Sources."""
    subgroup_metrics = []

    # 1. Sex Representation
    for s_val, group in df.groupby("sex"):
        n_samples = len(group)
        subgroup_metrics.append(
            {
                "dimension": "sex",
                "subgroup": s_val,
                "sample_count": n_samples,
                "population_share_pct": round(n_samples / len(df) * 100.0, 2),
                "diabetes_prevalence_pct": round(group["target_diabetes"].mean() * 100.0, 2)
                if "target_diabetes" in group
                else np.nan,
                "warning": "UNDERREPRESENTED (<30 samples)"
                if n_samples < min_sample_threshold
                else "Adequate",
            }
        )

    # 2. Age Band Representation
    if "age_band" in df.columns:
        for a_val, group in df.groupby("age_band"):
            n_samples = len(group)
            subgroup_metrics.append(
                {
                    "dimension": "age_band",
                    "subgroup": a_val,
                    "sample_count": n_samples,
                    "population_share_pct": round(n_samples / len(df) * 100.0, 2),
                    "diabetes_prevalence_pct": round(group["target_diabetes"].mean() * 100.0, 2)
                    if "target_diabetes" in group
                    else np.nan,
                    "warning": "UNDERREPRESENTED (<30 samples)"
                    if n_samples < min_sample_threshold
                    else "Adequate",
                }
            )

    # 3. Source Origin Representation
    for src_val, group in df.groupby("source"):
        n_samples = len(group)
        subgroup_metrics.append(
            {
                "dimension": "source",
                "subgroup": src_val,
                "sample_count": n_samples,
                "population_share_pct": round(n_samples / len(df) * 100.0, 2),
                "diabetes_prevalence_pct": round(group["target_diabetes"].mean() * 100.0, 2)
                if "target_diabetes" in group
                else np.nan,
                "warning": "UNDERREPRESENTED (<30 samples)"
                if n_samples < min_sample_threshold
                else "Adequate",
            }
        )

    audit_df = pd.DataFrame(subgroup_metrics)

    # Check for warnings
    underrep = audit_df[audit_df["warning"].str.startswith("UNDERREPRESENTED")]
    if not underrep.empty:
        logger.warning(f"FAIRNESS WARNING: Found {len(underrep)} underrepresented subgroups!")
        for _, row in underrep.iterrows():
            logger.warning(
                f"  Underrepresented subgroup: {row['dimension']}='{row['subgroup']}' (Count: {row['sample_count']})"
            )
    else:
        logger.info(
            "Fairness subgroup representation check passed. All groups exceed minimum sample size threshold."
        )

    # Save to reports
    rep_path = Path(reports_dir)
    rep_path.mkdir(parents=True, exist_ok=True)
    csv_file = rep_path / "fairness_subgroup_audit.csv"
    audit_df.to_csv(csv_file, index=False)
    logger.info(f"Fairness subgroup audit saved to {csv_file}.")
    return audit_df


def execute_imbalance_and_fairness_phase(
    featured_file: str | Path = "data/processed/featured_clinical_data.parquet",
    reports_dir: str | Path = "reports",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Execute complete Phase 6 analysis on processed data."""
    df = pd.read_parquet(featured_file)

    # 1. Audit class distributions
    imbalance_df = audit_class_imbalance(df)

    # 2. Compare Resampling Strategies on Diabetes cohort inside CV
    diab_df = df[df["target_diabetes"].notna()].copy()
    y = diab_df["target_diabetes"].astype(int)
    X = diab_df.drop(columns=["target_diabetes"])
    # Run on sample of 3000 to keep CV fast
    if len(diab_df) > 3000:
        sample_idx = diab_df.sample(n=3000, random_state=42).index
        X_sub = X.loc[sample_idx]
        y_sub = y.loc[sample_idx]
    else:
        X_sub, y_sub = X, y

    resampling_df = compare_resampling_strategies_inside_cv(X_sub, y_sub, n_splits=5)

    # 3. Subgroup representation audit
    fairness_df = audit_fairness_subgroups(df, min_sample_threshold=30, reports_dir=reports_dir)

    return imbalance_df, resampling_df, fairness_df


if __name__ == "__main__":
    imb, res, fair = execute_imbalance_and_fairness_phase()
    print("\nSummary of Resampling Comparison (Top 3 for Recall):")
    print(res.head(3))
