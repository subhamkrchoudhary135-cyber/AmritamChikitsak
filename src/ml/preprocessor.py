"""Feature preprocessing pipeline with ColumnTransformer, IterativeImputer, and SMOTE."""

import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn.compose import ColumnTransformer
from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import IterativeImputer, SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Canonical feature lists
NUMERIC_FEATURES: list[str] = [
    "age",
    "height_cm",
    "weight_kg",
    "bmi",
    "systolic_bp",
    "diastolic_bp",
    "resting_heart_rate",
    "fasting_glucose",
    "hba1c",
    "total_cholesterol",
    "ldl_cholesterol",
    "hdl_cholesterol",
    "triglycerides",
    "physical_activity_hours_per_week",
    "family_history_diabetes",
    "family_history_heart_disease",
]

CATEGORICAL_FEATURES: list[str] = [
    "gender",
    "smoking_status",
    "alcohol_consumption",
    "diet_type",
]


def build_preprocessor_pipeline(
    numeric_features: list[str] | None = None,
    categorical_features: list[str] | None = None,
    use_iterative_imputer: bool = True,
) -> ColumnTransformer:
    """Build scikit-learn ColumnTransformer with imputation and standard scaling.

    Uses IterativeImputer (MICE) for numeric features to accurately impute
    clinically correlated biomarkers like HbA1c and cholesterol panels.
    """
    num_cols = numeric_features or NUMERIC_FEATURES
    cat_cols = categorical_features or CATEGORICAL_FEATURES

    if use_iterative_imputer:
        numeric_imputer = IterativeImputer(
            max_iter=10,
            random_state=42,
            initial_strategy="median",
            min_value=0.0,
        )
    else:
        numeric_imputer = SimpleImputer(strategy="median")

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", numeric_imputer),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, num_cols),
            ("cat", categorical_transformer, cat_cols),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )

    return preprocessor


def balance_training_data(
    X: np.ndarray, y: np.ndarray, random_state: int = 42
) -> tuple[np.ndarray, np.ndarray]:
    """Apply SMOTE over-sampling to handle imbalanced clinical screening positive targets."""
    # Only apply SMOTE if minority class has at least 6 samples and is under-represented
    pos_count = int(np.sum(y == 1))
    neg_count = int(np.sum(y == 0))
    if min(pos_count, neg_count) >= 6 and (pos_count / max(neg_count, 1)) < 0.45:
        smote = SMOTE(random_state=random_state, k_neighbors=min(5, min(pos_count, neg_count) - 1))
        X_res, y_res = smote.fit_resample(X, y)
        return X_res, y_res
    return X, y
