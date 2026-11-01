"""Generator script to produce clean, executable Jupyter training notebooks."""

import json
from pathlib import Path


def make_notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3.11 (Sanjivani AI)",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.11.17",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def md_cell(text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.split("\n")],
    }


def code_cell(code):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in code.split("\n")],
    }


def generate_all():
    nb_dir = Path("notebooks")
    nb_dir.mkdir(exist_ok=True)

    # 1. 01_data_exploration_and_preprocessing.ipynb
    nb1 = make_notebook([
        md_cell("# 01 - Sanjivani AI Clinical Data Exploration & Preprocessing\n"
                "This notebook explores the clinical biometrics and epidemiological distributions "
                "(ICMR-INDIAB, Pima Indian Diabetes, Framingham, and UCI Heart Disease), "
                "handles missing values using **IterativeImputer (MICE)**, and addresses class imbalance with **SMOTE**."),
        code_cell("import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path.cwd().parent))\n\n"
                  "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\n"
                  "from src.ml.datasets import generate_synthetic_clinical_cohort, save_dataset_manifest\n"
                  "from src.ml.preprocessor import build_preprocessor_pipeline, balance_training_data, NUMERIC_FEATURES, CATEGORICAL_FEATURES"),
        md_cell("### 1. Generate & Inspect Indian Cardiometabolic Cohort"),
        code_cell("df = generate_synthetic_clinical_cohort(n_samples=2500, random_state=42)\n"
                  "print(f'Cohort Dimensions: {df.shape}')\n"
                  "df.head()"),
        md_cell("### 2. Missing Value Analysis & Iterative Imputer (MICE)"),
        code_cell("print('Missing Values Count:\\n', df[NUMERIC_FEATURES].isnull().sum())\n"
                  "preprocessor = build_preprocessor_pipeline(use_iterative_imputer=True)\n"
                  "X_trans = preprocessor.fit_transform(df[NUMERIC_FEATURES + CATEGORICAL_FEATURES])\n"
                  "print(f'Processed Feature Matrix Shape: {X_trans.shape}')"),
        md_cell("### 3. Handle Class Imbalance with SMOTE"),
        code_cell("y_diab = df['target_diabetes'].values\n"
                  "print(f'Before SMOTE: Positive={sum(y_diab==1)}, Negative={sum(y_diab==0)}')\n"
                  "X_bal, y_bal = balance_training_data(X_trans, y_diab)\n"
                  "print(f'After SMOTE: Positive={sum(y_bal==1)}, Negative={sum(y_bal==0)}')"),
        md_cell("### 4. Save DVC Versioned Dataset Manifest"),
        code_cell("manifest = save_dataset_manifest(df)\nprint('Dataset Manifest SHA256:', manifest['sha256'])"),
    ])
    with open(nb_dir / "01_data_exploration_and_preprocessing.ipynb", "w", encoding="utf-8") as f:
        json.dump(nb1, f, indent=2)

    # 2. 02_classification_model_comparison_and_optuna.ipynb
    nb2 = make_notebook([
        md_cell("# 02 - Multi-Condition Classification, Optuna Tuning & Probability Calibration\n"
                "Comprehensive model comparison across Logistic Regression, KNN, SVM, Random Forest, "
                "XGBoost, LightGBM, CatBoost, and Stacking Ensemble, followed by Optuna hyperparameter optimization, "
                "Stratified K-Fold CV, probability calibration (`CalibratedClassifierCV`), and recall-prioritized threshold tuning."),
        code_cell("import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path.cwd().parent))\n\n"
                  "import numpy as np\nimport pandas as pd\n"
                  "from src.ml.datasets import generate_synthetic_clinical_cohort\n"
                  "from src.ml.preprocessor import build_preprocessor_pipeline, NUMERIC_FEATURES, CATEGORICAL_FEATURES\n"
                  "from src.ml.classifiers import (\n"
                  "    get_base_classifier, build_stacking_ensemble, evaluate_classifier_cv, "
                  "    tune_xgboost_optuna, find_recall_prioritized_threshold, CalibratedConditionClassifier\n)"),
        md_cell("### 1. Evaluate Multi-Algorithm Baseline on Diabetes Target"),
        code_cell("df = generate_synthetic_clinical_cohort(n_samples=1500, random_state=42)\n"
                  "preprocessor = build_preprocessor_pipeline()\n"
                  "X = preprocessor.fit_transform(df[NUMERIC_FEATURES + CATEGORICAL_FEATURES])\n"
                  "y = df['target_diabetes'].values\n\n"
                  "algorithms = ['logistic_regression', 'knn', 'svm', 'random_forest', 'xgboost', 'lightgbm', 'catboost']\n"
                  "results = {}\n"
                  "for algo in algorithms:\n"
                  "    clf = get_base_classifier(algo)\n"
                  "    scores = evaluate_classifier_cv(clf, X, y, n_splits=3)\n"
                  "    results[algo] = scores\n"
                  "pd.DataFrame(results).T"),
        md_cell("### 2. Optuna Hyperparameter Optimization on XGBoost"),
        code_cell("best_params = tune_xgboost_optuna(X, y, n_trials=8)\nprint('Optuna Best Params:', best_params)"),
        md_cell("### 3. Probability Calibration & Recall-Prioritized Thresholding"),
        code_cell("calibrated_clf = CalibratedConditionClassifier('diabetes', base_model_name='random_forest', min_recall=0.92)\n"
                  "calibrated_clf.fit(X, y)\n"
                  "print('Calibrated Decision Threshold (Recall Prioritized):', calibrated_clf.decision_threshold)\n"
                  "print('Evaluation Metrics at Threshold:\\n', calibrated_clf.metrics)"),
    ])
    with open(nb_dir / "02_classification_model_comparison_and_optuna.ipynb", "w", encoding="utf-8") as f:
        json.dump(nb2, f, indent=2)

    # 3. 03_regression_forecasting_and_conformal.ipynb
    nb3 = make_notebook([
        md_cell("# 03 - 3-6 Month Trajectory Forecasting & Conformal Prediction\n"
                "Forecasting future glycemic trajectories (Fasting Glucose mg/dL), blood pressure (Systolic BP mmHg), "
                "and continuous cardiometabolic risk with Ridge, Lasso, SVR, KNN, and XGBoost, with $(1 - \\alpha) = 90\\%$ "
                "distribution-free Conformal Prediction intervals."),
        code_cell("import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path.cwd().parent))\n\n"
                  "import pandas as pd\nimport numpy as np\n"
                  "from src.ml.datasets import generate_synthetic_clinical_cohort\n"
                  "from src.ml.preprocessor import build_preprocessor_pipeline, NUMERIC_FEATURES, CATEGORICAL_FEATURES\n"
                  "from src.ml.regressors import ConformalBiomarkerForecaster, MultiTargetHealthForecaster"),
        md_cell("### 1. Fit Multi-Target Health Forecaster"),
        code_cell("df = generate_synthetic_clinical_cohort(n_samples=1500, random_state=42)\n"
                  "preprocessor = build_preprocessor_pipeline()\n"
                  "X = preprocessor.fit_transform(df[NUMERIC_FEATURES + CATEGORICAL_FEATURES])\n"
                  "y_dict = {\n"
                  "    'target_glucose_6m': df['target_glucose_6m'].values,\n"
                  "    'target_sbp_6m': df['target_sbp_6m'].values,\n"
                  "    'target_continuous_risk': df['target_continuous_risk'].values,\n"
                  "}\n"
                  "forecaster = MultiTargetHealthForecaster(random_state=42)\n"
                  "forecaster.fit(X, y_dict)\n"
                  "print('Glucose Forecaster Metrics:', forecaster.glucose_forecaster.metrics)"),
        md_cell("### 2. Generate Prediction with Conformal Intervals"),
        code_cell("sample_patient = X[:1]\n"
                  "pred = forecaster.forecast(sample_patient)\n"
                  "for k, v in pred.items():\n"
                  "    print(f'{k}: {v}')"),
    ])
    with open(nb_dir / "03_regression_forecasting_and_conformal.ipynb", "w", encoding="utf-8") as f:
        json.dump(nb3, f, indent=2)

    # 4. 04_clustering_phenotyping_and_anomalies.ipynb
    nb4 = make_notebook([
        md_cell("# 04 - Patient Phenotype Clustering & Biometric Anomaly Detection\n"
                "Unsupervised patient segmentation using K-Means, Gaussian Mixture Models (GMM), and HDBSCAN, "
                "evaluating optimal $k$ with Silhouette score and Davies-Bouldin index, 2D PCA projection, "
                "semantic auto-labeling, and anomaly detection via Isolation Forest."),
        code_cell("import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path.cwd().parent))\n\n"
                  "import pandas as pd\nimport numpy as np\n"
                  "from src.ml.datasets import generate_synthetic_clinical_cohort\n"
                  "from src.ml.preprocessor import build_preprocessor_pipeline, NUMERIC_FEATURES, CATEGORICAL_FEATURES\n"
                  "from src.ml.clustering import evaluate_optimal_k, PatientPhenotypeSegmenter"),
        md_cell("### 1. Optimal k Selection (Silhouette & Davies-Bouldin)"),
        code_cell("df = generate_synthetic_clinical_cohort(n_samples=1500, random_state=42)\n"
                  "preprocessor = build_preprocessor_pipeline()\n"
                  "X = preprocessor.fit_transform(df[NUMERIC_FEATURES + CATEGORICAL_FEATURES])\n"
                  "best_k, sil_scores, db_scores = evaluate_optimal_k(X, k_range=range(2, 6))\n"
                  "print(f'Optimal k: {best_k}')\n"
                  "print('Silhouette Scores:', sil_scores)\n"
                  "print('Davies-Bouldin Scores:', db_scores)"),
        md_cell("### 2. Auto-Labeled Phenotype Profiles"),
        code_cell("feature_names = list(preprocessor.get_feature_names_out())\n"
                  "segmenter = PatientPhenotypeSegmenter(n_clusters=best_k, random_state=42)\n"
                  "segmenter.fit(X, feature_names)\n"
                  "for cid, prof in segmenter.cluster_profiles.items():\n"
                  "    print(f'Cluster {cid}: {prof[\"label\"]} (Size={prof[\"size\"]})')"),
    ])
    with open(nb_dir / "04_clustering_phenotyping_and_anomalies.ipynb", "w", encoding="utf-8") as f:
        json.dump(nb4, f, indent=2)

    # 5. 05_shap_explainability_and_fairness.ipynb
    nb5 = make_notebook([
        md_cell("# 05 - SHAP Explainability & Fairlearn Algorithmic Fairness\n"
                "Extracting local top 5 contributing factors per patient prediction with SHAP, "
                "and conducting rigorous algorithmic fairness evaluations across biological sex and age categories."),
        code_cell("import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path.cwd().parent))\n\n"
                  "import pandas as pd\nimport numpy as np\n"
                  "from src.ml.registry import model_registry\n"
                  "from src.schemas.screening import ScreeningInput"),
        md_cell("### 1. Load Pretrained Sanjivani AI Model Registry"),
        code_cell("model_registry.load_or_train()\nprint('Model Registry Loaded successfully!')"),
        md_cell("### 2. Run Inference & Extract Top 5 SHAP Factors"),
        code_cell("test_input = ScreeningInput(\n"
                  "    age=48,\n"
                  "    gender='male',\n"
                  "    height_cm=168.0,\n"
                  "    weight_kg=78.0,\n"
                  "    systolic_bp=138.0,\n"
                  "    diastolic_bp=88.0,\n"
                  "    fasting_glucose=118.0,\n"
                  "    hba1c=6.1,\n"
                  "    physical_activity_hours_per_week=1.0,\n"
                  "    smoking_status='never',\n"
                  "    alcohol_consumption='none',\n"
                  "    family_history_diabetes=True,\n"
                  ")\n"
                  "conds, fore, pheno, shap_factors = model_registry.run_screening_inference(test_input)\n"
                  "print('Phenotype:', pheno.cluster_label)\n"
                  "print('Top 5 SHAP Contributing Factors:')\n"
                  "for f in shap_factors:\n"
                  "    print(f' - {f.feature_name_friendly}: {f.direction} (Impact: {f.impact_score})')"),
        md_cell("### 3. Fairlearn Fairness Evaluation"),
        code_cell("for cond, fair in model_registry.fairness_reports.items():\n"
                  "    print(f'=== Fairness Report for {cond} ===')\n"
                  "    for attr, stats in fair.items():\n"
                  "        print(f'{attr}: Demographic Parity Diff = {stats.get(\"demographic_parity_difference\")}, Passed = {stats.get(\"fairness_passed\")}')"),
    ])
    with open(nb_dir / "05_shap_explainability_and_fairness.ipynb", "w", encoding="utf-8") as f:
        json.dump(nb5, f, indent=2)

    print("All 5 Jupyter training notebooks generated successfully in notebooks/!")


if __name__ == "__main__":
    generate_all()
