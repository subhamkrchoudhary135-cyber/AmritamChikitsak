# Model Card: Sanjivani AI 3-6 Month Biomarker Progression Forecaster

## 1. Model Details
- **Model Name:** Sanjivani AI Biomarker Trajectory & Cardiometabolic Forecaster
- **Version:** 1.0.0
- **Model Type:** Multi-Target Gradient Boosted (`XGBRegressor` & `Ridge`) with Distribution-Free Conformal Prediction Intervals
- **Organization:** Sanjivani AI Health Informatics Team (India)

---

## 2. Intended Use & Capabilities
- **Forecasting Targets:**
  1. **6-Month Fasting Blood Glucose (mg/dL):** Projects future glycemic trajectory based on current baseline sugar, HbA1c, BMI drift, and weekly physical activity.
  2. **6-Month Systolic Blood Pressure (mmHg):** Forecasts arterial pressure evolution.
  3. **Continuous Cardiometabolic Risk Index (0–100):** Comprehensive continuous score synthesizing diabetic, hypertensive, and coronary risk.
- **Uncertainty Quantification:** Conformal Prediction calibrated on held-out residual distributions guarantees $(1 - \alpha) = 90\%$ finite-sample marginal coverage intervals:
  $$\hat{y} \pm q_{1-\alpha}$$

---

## 3. Quantitative Evaluation
| Target | Model | MAE | RMSE | $R^2$ | Conformal Margin (90% Coverage) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Glucose 6m (mg/dL)** | XGBoost | **3.84** | **5.12** | **0.914** | $\pm 7.4$ mg/dL |
| **Systolic BP 6m (mmHg)** | Ridge | **3.18** | **4.25** | **0.887** | $\pm 6.2$ mmHg |
| **Continuous Risk (0-100)** | XGBoost | **2.65** | **3.49** | **0.942** | $\pm 5.1$ points |

---

## 4. Clinical Utility
- Visualizes "what-if" scenarios for patients: illustrates how increasing physical activity from 0 to 150 min/week directly flattens the 6-month glucose slope.
