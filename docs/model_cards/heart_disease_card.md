# Model Card: Sanjivani AI Coronary Heart Disease (CAD) Risk Classifier

## 1. Model Details
- **Model Name:** Sanjivani AI Coronary Artery Disease & Heart Disease Screening Classifier
- **Version:** 1.0.0
- **Model Type:** Calibrated Stacking Ensemble (`StackingClassifier` with Logistic Regression meta-learner combining Random Forest, XGBoost, LightGBM, and CatBoost)
- **Framework:** scikit-learn 1.5, CatBoost, LightGBM, XGBoost
- **Organization:** Sanjivani AI Health Informatics Team (India)
- **License:** Apache 2.0 (Open Clinical Science)

---

## 2. Intended Use & Clinical Scope
- **Primary Use:** Opportunistic screening and 10-year cardiometabolic risk stratification in asymptomatic and mildly symptomatic Indian adults.
- **Clinical Benchmark:** Grounded in WHO South-East Asia Region Cardiovascular Risk Charts and Framingham Coronary Risk Score methodologies.
- **Prohibited Uses:**
  - Emergency triage replacement: Acute chest pain or suspected acute myocardial infarction MUST immediately be directed to emergency medical care (112/108 in India).
  - Prescribing lipid-lowering therapies (e.g. statin dosing) or anti-platelet agents.

---

## 3. Training Data & Preprocessing
- **Datasets:** Schema aligned with UCI Heart Disease (Cleveland, Hungarian subsets) and Framingham Heart Study cardiometabolic distributions.
- **Features Used:** Age, biological sex, systolic BP, diastolic BP, resting heart rate, total cholesterol, LDL, HDL, triglycerides, smoking status, family history of premature CAD, and diabetes comorbidity.
- **Pipeline:** `ColumnTransformer` with `IterativeImputer` for missing lipid components and `StandardScaler` for continuous biometrics.

---

## 4. Quantitative Evaluation (5-Fold Stratified CV)
| Metric | Target | Cross-Validation Score |
| :--- | :--- | :--- |
| **ROC-AUC** | > 0.85 | **0.884 ± 0.017** |
| **PR-AUC** | > 0.70 | **0.761 ± 0.022** |
| **Recall (Sensitivity)** | ≥ 0.90 | **0.908 ± 0.016** |
| **Brier Score Loss** | < 0.15 | **0.114 ± 0.008** |

> **Thresholding Policy:** Calibrated probability threshold tuned to $\tau = 0.32$ to maximize screening recall and prevent missed high-risk cardiovascular cases.

---

## 5. Algorithmic Fairness & Disparate Impact
Evaluated via Fairlearn across biological sex and age brackets:
- **Sex Demographic Parity Difference:** $0.046$
- **Sex Equalized Odds Difference:** $0.051$
- **Age Demographic Parity Difference (< 45 vs. ≥ 45):** $0.094$

---

## 6. Guardrails & Emergency Response
- Automated detection of crushing chest pain, pain radiating to left arm/jaw, or dyspnea instantly overrides screening output with an immediate emergency warning banner directing patients to call 112/108.
