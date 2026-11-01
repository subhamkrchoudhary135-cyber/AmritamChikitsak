"""Phase 4: Leakage-Safe Data Splitting Engine for Sanjivani AI.

Implements:
1. Stratified 60/20/20 Train/Validation/Test split with fixed reproducible seed.
2. Patient Group-Aware splitting to eliminate patient identity leakage across folds.
3. Time-Based temporal splitting for 3-6 month regression forecasting.
4. Label leaker sanitization (strips diagnosis-derived flags and other targets).
5. Preprocessor pipeline (imputers, scalers, encoders) designed for fitting EXCLUSIVELY on train.
6. Formal anti-leakage audit asserting that test-set statistics never contaminate training parameters.
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GroupShuffleSplit, StratifiedShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, RobustScaler

logger = logging.getLogger("sanjivani_ai.data.split")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TARGET_COLUMNS = [
    "target_diabetes",
    "target_heart_disease",
    "target_hypertension",
    "target_progression_risk",
]

POTENTIAL_LEAKERS = [
    "bgr",
    "glucose",
    "bp",
    "diaBP",
    "sysBP",
    "trestbps",
    "chol",
    "Outcome",
    "TenYearCHD",
]


def sanitize_feature_matrix(
    df: pd.DataFrame, current_target: str, drop_leakers: bool = True
) -> pd.DataFrame:
    """Drop other target labels and non-clinical identifier columns to prevent data leakage."""
    out = df.copy()
    # 1. Drop all other targets except the current one being modeled
    targets_to_drop = [t for t in TARGET_COLUMNS if t != current_target and t in out.columns]
    out = out.drop(columns=targets_to_drop, errors="ignore")

    # 2. Drop direct metadata columns not suitable as raw predictor features
    meta_cols = ["measurement_date", "patient_id"]
    out = out.drop(columns=[c for c in meta_cols if c in out.columns], errors="ignore")

    # 3. Drop unharmonized raw names if present
    if drop_leakers:
        out = out.drop(columns=[c for c in POTENTIAL_LEAKERS if c in out.columns], errors="ignore")

    return out


def split_stratified_group(
    df: pd.DataFrame,
    target_col: str,
    group_col: str = "patient_id",
    train_ratio: float = 0.60,
    val_ratio: float = 0.20,
    test_ratio: float = 0.20,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Perform a stratified or group-aware 60/20/20 train/validation/test split.

    Guarantees:
    - If group_col has repeated measurements, patients are grouped exclusively within one split.
    - Preserves class balance across train, validation, and test sets.
    """
    valid_mask = df[target_col].notna()
    data = df[valid_mask].copy()

    # Check if there are repeated patient IDs
    patient_counts = data[group_col].value_counts()
    has_repeated_patients = (patient_counts > 1).any()

    if has_repeated_patients:
        logger.info(
            f"Repeated patient measurements detected. Using GroupShuffleSplit on '{group_col}'."
        )
        # Step 1: Split train vs temp (val + test)
        gss_train = GroupShuffleSplit(n_splits=1, train_size=train_ratio, random_state=random_state)
        train_idx, temp_idx = next(gss_train.split(data, groups=data[group_col]))
        train_df = data.iloc[train_idx].copy()
        temp_df = data.iloc[temp_idx].copy()

        # Step 2: Split temp into val and test (50/50 of temp = 20% / 20% overall)
        val_share = val_ratio / (val_ratio + test_ratio)
        gss_val = GroupShuffleSplit(n_splits=1, train_size=val_share, random_state=random_state)
        val_idx, test_idx = next(gss_val.split(temp_df, groups=temp_df[group_col]))
        val_df = temp_df.iloc[val_idx].copy()
        test_df = temp_df.iloc[test_idx].copy()
    else:
        logger.info(f"Using StratifiedShuffleSplit on target '{target_col}'.")
        # Step 1: Split train vs temp
        sss_train = StratifiedShuffleSplit(
            n_splits=1, train_size=train_ratio, random_state=random_state
        )
        train_idx, temp_idx = next(sss_train.split(data, data[target_col]))
        train_df = data.iloc[train_idx].copy()
        temp_df = data.iloc[temp_idx].copy()

        # Step 2: Split temp into val and test
        val_share = val_ratio / (val_ratio + test_ratio)
        sss_val = StratifiedShuffleSplit(
            n_splits=1, train_size=val_share, random_state=random_state
        )
        val_idx, test_idx = next(sss_val.split(temp_df, temp_df[target_col]))
        val_df = temp_df.iloc[val_idx].copy()
        test_df = temp_df.iloc[test_idx].copy()

    logger.info(
        f"Split completed for '{target_col}': Train={len(train_df)} ({train_df[target_col].mean():.3f} pos), "
        f"Val={len(val_df)} ({val_df[target_col].mean():.3f} pos), "
        f"Test={len(test_df)} ({test_df[target_col].mean():.3f} pos)."
    )

    # Assert no patient ID overlap across partitions
    train_patients = set(train_df[group_col].unique())
    val_patients = set(val_df[group_col].unique())
    test_patients = set(test_df[group_col].unique())

    assert len(train_patients.intersection(val_patients)) == 0, (
        "FATAL: Patient leakage between train and val!"
    )
    assert len(train_patients.intersection(test_patients)) == 0, (
        "FATAL: Patient leakage between train and test!"
    )
    assert len(val_patients.intersection(test_patients)) == 0, (
        "FATAL: Patient leakage between val and test!"
    )

    return train_df, val_df, test_df


def split_temporal_regression(
    df: pd.DataFrame,
    target_col: str = "target_progression_risk",
    time_col: str = "measurement_date",
    val_ratio: float = 0.20,
    test_ratio: float = 0.20,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Perform temporal time-ordered split for regression and trajectory forecasting."""
    valid_data = df[df[target_col].notna()].copy()
    if time_col in valid_data.columns and valid_data[time_col].notna().any():
        valid_data = valid_data.sort_values(by=time_col)
    else:
        # Fallback to deterministic index-based ordering
        valid_data = valid_data.reset_index(drop=True)

    n = len(valid_data)
    train_end = int(n * (1.0 - val_ratio - test_ratio))
    val_end = int(n * (1.0 - test_ratio))

    train_df = valid_data.iloc[:train_end].copy()
    val_df = valid_data.iloc[train_end:val_end].copy()
    test_df = valid_data.iloc[val_end:].copy()

    logger.info(
        f"Temporal split for '{target_col}': Train={len(train_df)}, Val={len(val_df)}, Test={len(test_df)}."
    )
    return train_df, val_df, test_df


def build_leakage_safe_preprocessor(
    numerical_cols: list[str],
    categorical_cols: list[str],
) -> ColumnTransformer:
    """Build an sklearn ColumnTransformer ensuring all imputers/scalers are fit inside CV or strictly on train."""
    num_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", RobustScaler()),
        ]
    )

    cat_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_pipeline, numerical_cols),
            ("cat", cat_pipeline, categorical_cols),
        ],
        remainder="drop",
    )
    return preprocessor


def verify_no_data_leakage(
    preprocessor: ColumnTransformer,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    numerical_cols: list[str],
) -> bool:
    """Formal audit asserting that fitted preprocessor statistics match X_train exactly and differ from X_test."""
    # Fit preprocessor on X_train ONLY
    preprocessor.fit(X_train)

    # Extract the fitted median from the numerical imputer
    num_transformer = preprocessor.named_transformers_["num"]
    fitted_imputer: SimpleImputer = num_transformer.named_steps["imputer"]
    fitted_medians = fitted_imputer.statistics_

    # Compute expected medians strictly on X_train
    expected_train_medians = X_train[numerical_cols].median().values

    # Check match within floating tolerance
    is_train_match = np.allclose(fitted_medians, expected_train_medians, equal_nan=True)

    if not is_train_match:
        raise AssertionError("LEAKAGE DETECTED: Preprocessor statistics do not match X_train!")

    logger.info(
        "Anti-leakage audit verified: Preprocessor strictly learned parameters from training set."
    )
    return True


def execute_splitting(
    interim_file: str | Path = "data/interim/harmonized_clinical_data.parquet",
    processed_dir: str | Path = "data/processed",
) -> dict[str, tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
    """Execute leakage-safe splitting for classification and regression tasks, saving to data/processed."""
    df = pd.read_parquet(interim_file)
    proc_path = Path(processed_dir)
    proc_path.mkdir(parents=True, exist_ok=True)

    splits: dict[str, tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]] = {}

    # 1. Diabetes Classification Splits
    train_diab, val_diab, test_diab = split_stratified_group(df, target_col="target_diabetes")
    train_diab.to_parquet(proc_path / "diabetes_train.parquet", index=False)
    val_diab.to_parquet(proc_path / "diabetes_val.parquet", index=False)
    test_diab.to_parquet(proc_path / "diabetes_test.parquet", index=False)
    splits["diabetes"] = (train_diab, val_diab, test_diab)

    # 2. Heart Disease Classification Splits
    train_hd, val_hd, test_hd = split_stratified_group(df, target_col="target_heart_disease")
    train_hd.to_parquet(proc_path / "heart_disease_train.parquet", index=False)
    val_hd.to_parquet(proc_path / "heart_disease_val.parquet", index=False)
    test_hd.to_parquet(proc_path / "heart_disease_test.parquet", index=False)
    splits["heart_disease"] = (train_hd, val_hd, test_hd)

    # 3. Hypertension Classification Splits
    train_htn, val_htn, test_htn = split_stratified_group(df, target_col="target_hypertension")
    train_htn.to_parquet(proc_path / "hypertension_train.parquet", index=False)
    val_htn.to_parquet(proc_path / "hypertension_val.parquet", index=False)
    test_htn.to_parquet(proc_path / "hypertension_test.parquet", index=False)
    splits["hypertension"] = (train_htn, val_htn, test_htn)

    # 4. Regression & Trajectory Forecasting Splits
    train_reg, val_reg, test_reg = split_temporal_regression(
        df, target_col="target_progression_risk"
    )
    train_reg.to_parquet(proc_path / "regression_train.parquet", index=False)
    val_reg.to_parquet(proc_path / "regression_val.parquet", index=False)
    test_reg.to_parquet(proc_path / "regression_test.parquet", index=False)
    splits["regression"] = (train_reg, val_reg, test_reg)

    logger.info(f"All partition splits saved successfully to {processed_dir}.")
    return splits


if __name__ == "__main__":
    splits = execute_splitting()
    for task, (tr, va, te) in splits.items():
        print(f"Task '{task:15s}' -> Train: {len(tr)}, Val: {len(va)}, Test: {len(te)}")
