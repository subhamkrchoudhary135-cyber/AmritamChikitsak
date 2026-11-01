# Model Card: Sanjivani AI Diabetes Risk Classifier

## 1. Model Details
- **Model Name:** Sanjivani AI Type 2 Diabetes Screening Classifier
- **Version:** 1.0.0
- **Model Type:** Calibrated Ensemble Classifier (`RandomForestClassifier` / `StackingClassifier` with `CalibratedClassifierCV`)
- **Framework:** scikit-learn 1.5, XGBoost, imbalanced-learn
- **Organization:** Sanjivani AI Health Informatics Team (India)
- **License:** Apache 2.0 (Open Clinical Science)
- **Clinical Scope:** Non-diagnostic cardiometabolic risk screening support.

---

## 2. Intended Use & Clinical Scope
- **Primary Use:** Early identification of adults at elevated risk of Type 2 Diabetes (T2D) or pre-diabetes within Indian and South Asian demographics.
- **Target Population:** Indian adults aged 18–80 presenting in outpatient wellness clinics, corporate screening camps, or digital health platforms.
- **Out-of-Scope / Prohibited Uses:**
  - Definitive medical diagnosis of diabetes (which requires laboratory venous fasting plasma glucose or oral glucose tolerance test per ICMR).
  - Determining drug dosing or initiating pharmacological therapy (e.g., insulin or metformin titration).
  - Screening pediatric cohorts (< 18 years) or gestational diabetes without clinical supervision.

---

## 3. Factors & Demographic Considerations
- **South Asian Specific Phenotype:** Incorporates lower BMI thresholds established by ICMR and WHO Asia-Pacific guidelines:
  - Normal: 18.5 – 22.9 kg/m²
  - Overweight: 23.0 – 24.9 kg/m²
  - Obese: ≥ 25.0 kg/m²
- **Sub-Populations Evaluated:** Evaluated across biological sex (Male vs Female) and age brackets (< 45 vs ≥ 45 years).

---

## 4. Training Data & Preprocessing
- **Datasets:** Synthesized cohort matching epidemiological distributions from the ICMR-INDIAB study and Pima Indian Diabetes dataset schemas.
- **Missing Value Handling:** `IterativeImputer` (Multivariate Imputation by Chained Equations - MICE) with median initialization to capture physiological inter-correlations between fasting glucose and HbA1c.
- **Class Imbalance:** Synthetic Minority Over-sampling Technique (`SMOTE`) applied strictly to training folds.
- **Probability Calibration:** Sigmoid-based Platt scaling via `CalibratedClassifierCV` ensuring predicted probabilities correspond to true empirical frequencies.

---

## 5. Quantitative Evaluation
Evaluated with 5-Fold Stratified Cross-Validation:

| Metric | Target | Cross-Validation Score |
| :--- | :--- | :--- |
| **ROC-AUC** | > 0.85 | **0.892 ± 0.015** |
| **PR-AUC** | > 0.70 | **0.784 ± 0.021** |
| **Recall (Sensitivity)** | ≥ 0.90 | **0.915 ± 0.018** |
| **F1 Score** | > 0.75 | **0.796 ± 0.024** |
| **Brier Score Loss** | < 0.15 | **0.108 ± 0.009** |

> **Decision Threshold:** Adjusted to $\tau = 0.35$ to strictly prioritize clinical recall (minimizing dangerous false negatives where high-risk pre-diabetic patients are missed).

---

## 6. Algorithmic Fairness (Fairlearn)
Fairness evaluation using Fairlearn across sensitive attributes:
- **Biological Sex (Male vs. Female):**
  - Demographic Parity Difference: $0.038$ (Threshold: $< 0.15$)
  - Equalized Odds Difference: $0.042$ (Threshold: $< 0.15$)
- **Age Bracket (< 45 vs. ≥ 45):**
  - Demographic Parity Difference: $0.082$
  - Equalized Odds Difference: $0.071$
- **Outcome:** Model passes all predefined equity and non-discrimination thresholds.

---

## 7. Explainability
- Evaluated per prediction using **SHAP (SHapley Additive exPlanations)**.
- Top 5 positive and negative contributing factors are extracted, normalized, and displayed with actionable lifestyle guidance and clinical reference ranges.

---

## 8. Ethical Considerations & Guardrails
- **Statutory Non-Diagnostic Disclaimer:** Every output explicitly states that Sanjivani AI is a screening aid, never a medical diagnosis.
- **Emergency Triage:** Inputs reflecting extreme hypoglycemia (< 50 mg/dL) or hyperglycemic crisis (≥ 400 mg/dL) immediately trigger emergency triage (112/108 helpline).
- **DPDP Act Compliance:** All patient identifiers (PII) are encrypted at rest with AES-256/Fernet; training data is strictly de-identified.
