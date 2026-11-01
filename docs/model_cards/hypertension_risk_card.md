# Model Card: Sanjivani AI Hypertension Risk Classifier

## 1. Model Details
- **Model Name:** Sanjivani AI Hypertension & Vascular Strain Risk Classifier
- **Version:** 1.0.0
- **Model Type:** Calibrated Ensemble Classifier (`RandomForestClassifier` / `CalibratedClassifierCV`)
- **Clinical Standard:** ICMR National Guidelines for Hypertension Management & AHA/ACC 2017 Guidelines
- **Organization:** Sanjivani AI Health Informatics Team (India)

---

## 2. Intended Use & Clinical Scope
- **Primary Use:** Stratifying asymptomatic adults into normotensive, elevated, Stage 1, or Stage 2 hypertension screening categories.
- **Guideline Criteria (ICMR):**
  - Normal: SBP < 120 mmHg and DBP < 80 mmHg
  - Elevated / Pre-HTN: SBP 120–129 mmHg and DBP < 80 mmHg
  - Stage 1 HTN: SBP 130–139 mmHg or DBP 80–89 mmHg
  - Stage 2 HTN: SBP ≥ 140 mmHg or DBP ≥ 90 mmHg
  - Hypertensive Crisis: SBP ≥ 180 mmHg or DBP ≥ 120 mmHg (Triggers Emergency Triage)

---

## 3. Quantitative Evaluation (5-Fold Stratified CV)
| Metric | Cross-Validation Score |
| :--- | :--- |
| **ROC-AUC** | **0.912 ± 0.011** |
| **PR-AUC** | **0.825 ± 0.018** |
| **Recall (Sensitivity)** | **0.923 ± 0.014** |
| **F1 Score** | **0.831 ± 0.016** |
| **Brier Score Loss** | **0.096 ± 0.007** |

---

## 4. Explainability & Actionable Advice
- SHAP feature attributions highlight the precise contribution of sodium/diet, BMI, sedentary hours, and family history.
- Plain-language lifestyle guidance emphasizes:
  - Sodium reduction to < 5g/day (< 1 teaspoon table salt).
  - Regular home blood pressure monitoring (HBPM).
  - Routine aerobic exercise and stress management (yoga/pranayama).
