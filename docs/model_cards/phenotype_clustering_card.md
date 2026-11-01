# Model Card: Sanjivani AI Patient Phenotyping & Anomaly Detector

## 1. Model Details
- **Model Name:** Sanjivani AI Unsupervised Phenotype Clusterer & Outlier Detector
- **Version:** 1.0.0
- **Model Architecture:**
  - Clustering: K-Means ($k=4$), Gaussian Mixture Models (GMM), and HDBSCAN
  - Dimensionality Reduction: 2D Principal Component Analysis (PCA)
  - Anomaly Detection: Isolation Forest & One-Class SVM ($\nu = 0.03$)
- **Cluster Selection Criteria:** Silhouette Score maximization & Davies-Bouldin Index minimization.

---

## 2. Phenotype Segments & Auto-Labels
1. **Cluster 0: "Elevated BMI & Low Physical Activity"**
   - High BMI, sedentary habit (< 1 hr/wk), elevated triglycerides.
   - Priority: Aerobic conditioning, caloric deficit, ICMR portion control plate.
2. **Cluster 1: "Vascular Strain & Elevated Blood Pressure"**
   - SBP ≥ 135 mmHg, DBP ≥ 85 mmHg, normal-to-mildly elevated glucose.
   - Priority: DASH-style diet, dietary sodium restriction (< 5g/day), stress reduction.
3. **Cluster 2: "Impaired Glycemic Control & High Diabetes Risk"**
   - Fasting glucose > 110 mg/dL, elevated HbA1c, positive family history.
   - Priority: Low-glycemic millets, carbohydrate restriction, routine glucose monitoring.
4. **Cluster 3: "Balanced Cardiometabolic Profile"**
   - Normotensive, normoglycemic, active lifestyle (≥ 3 hrs/wk activity).
   - Priority: Annual preventive wellness check.

---

## 3. Anomaly Detection Engine
- **Purpose:** Flags corrupted, physiologically implausible, or extreme outlier readings (e.g. SBP 250 with DBP 40, or fasting glucose 28 mg/dL).
- **Flagged Action:** Signals clinical coordinator to verify lab report manual entry or re-test biomarker sample.
