# Sanjivani AI Clinical Data Pipeline: Data Dictionary & Specification

Version: **1.0.0**  
Schema Standard: **Sanjivani AI Canonical Clinical Schema v1.2**  
Compliance: **Digital Personal Data Protection (DPDP) Act 2023**  
Target Population: **Adults in India (ICMR-INDIAB & WHO South Asian Guidelines)**

---

## 1. Canonical Schema Specification

| Field Name | Type | Unit | Range / Values | Physiological Bounds | Clinical Description & Source Mapping |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`age`** | `float` | Years | $18.0 - 100.0$ | $[1.0, 120.0]$ | Chronological age. Out-of-range (<1 or >120) converted to `NaN`. |
| **`sex`** | `string` | Categorical | `male`, `female`, `other` | Enum check | Biological sex at birth. Mapped from binary or string codes. |
| **`height_cm`** | `float` | cm | $130.0 - 210.0$ | $[50.0, 250.0]$ | Standing stature. Converted from inches via $\times 2.54$. |
| **`weight_kg`** | `float` | kg | $30.0 - 220.0$ | $[15.0, 300.0]$ | Total body weight. Converted from lbs via $\times 0.453592$. |
| **`bmi`** | `float` | $\text{kg/m}^2$ | $14.0 - 55.0$ | $[10.0, 75.0]$ | Body Mass Index ($\text{weight} / \text{height}^2$). Asian Indian cutoffs: Overweight $\ge 23$, Obese $\ge 25$. |
| **`waist_circumference_cm`** | `float` | cm | $55.0 - 160.0$ | $[40.0, 200.0]$ | Abdominal circumference. Marker of visceral central adiposity. Asian cut-offs: $\ge 90$ cm (men), $\ge 80$ cm (women). |
| **`systolic_bp`** | `float` | mmHg | $80.0 - 230.0$ | $[60.0, 260.0]$ | Peak arterial pressure during ventricular contraction. $0$ is physically impossible -> converted to `NaN`. |
| **`diastolic_bp`** | `float` | mmHg | $45.0 - 130.0$ | $[35.0, 160.0]$ | Minimum arterial pressure between beats. $0$ -> converted to `NaN`. |
| **`heart_rate`** | `float` | bpm | $40.0 - 160.0$ | $[30.0, 220.0]$ | Resting radial or pulse rate in beats per minute. |
| **`fasting_glucose`** | `float` | mg/dL | $50.0 - 450.0$ | $[40.0, 600.0]$ | Venous plasma glucose after $\ge 8\text{h}$ fast. Normal: $70-99$, Impaired: $100-125$, Diabetic: $\ge 126$. |
| **`hba1c`** | `float` | % | $4.0 - 15.0$ | $[3.0, 20.0]$ | Glycated hemoglobin, reflecting 90-day mean glucose levels. |
| **`total_cholesterol`** | `float` | mg/dL | $90.0 - 450.0$ | $[50.0, 700.0]$ | Total serum cholesterol. Converted from mmol/L via $\times 38.67$. |
| **`hdl_cholesterol`** | `float` | mg/dL | $20.0 - 100.0$ | $[10.0, 150.0]$ | High-density lipoprotein cholesterol ("protective cholesterol"). |
| **`ldl_cholesterol`** | `float` | mg/dL | $30.0 - 280.0$ | $[20.0, 450.0]$ | Low-density lipoprotein cholesterol (atherogenic fraction). |
| **`triglycerides`** | `float` | mg/dL | $40.0 - 800.0$ | $[30.0, 1200.0]$ | Fasting serum triglycerides. High in South Asians ($\ge 150$). |
| **`physical_activity_hours_per_week`** | `float` | Hours | $0.0 - 30.0$ | $[0.0, 40.0]$ | Moderate-to-vigorous exercise. Target $\ge 2.5\text{h/wk}$ (ICMR/WHO). |
| **`smoking_status`** | `string` | Categorical | `never`, `former`, `current` | Enum check | Cigarette or bidi consumption habit. |
| **`alcohol_consumption`** | `string` | Categorical | `none`, `occasional`, `regular` | Enum check | Alcohol intake frequency. |
| **`family_history_diabetes`** | `float` | Binary | $0.0, 1.0$ | $[0, 1]$ | First-degree relative diagnosed with Type 2 diabetes. |
| **`family_history_heart_disease`** | `float` | Binary | $0.0, 1.0$ | $[0, 1]$ | Premature coronary heart disease in parents or siblings. |
| **`target_diabetes`** | `float` | Binary | $0.0, 1.0$ | $[0, 1]$ | Classification label for Type 2 Diabetes risk screening. |
| **`target_heart_disease`** | `float` | Binary | $0.0, 1.0$ | $[0, 1]$ | Classification label for Coronary Artery Disease risk screening. |
| **`target_hypertension`** | `float` | Binary | $0.0, 1.0$ | $[0, 1]$ | Classification label for Hypertension ($\text{SBP} \ge 140$ or $\text{DBP} \ge 90$). |
| **`target_progression_risk`** | `float` | Continuous | $0.0 - 100.0$ | $[0.0, 100.0]$ | Continuous progression index for longitudinal regression. |
| **`source`** | `string` | Metadata | Enum | Provenance tag | Identifies source origin for subgroup and algorithmic audit. |
| **`patient_id`** | `string` | Pseudonym | String | HMAC-SHA256 | Hashed identifier with salt; direct PII strictly excluded. |

---

## 2. Engineered Clinical Features

| Feature Key | Formula / Logic | Clinical Significance |
| :--- | :--- | :--- |
| **`mean_arterial_pressure`** | $\text{DBP} + \frac{1}{3}(\text{SBP} - \text{DBP})$ | Perfusion pressure seen by organs; indicator of vascular resistance. |
| **`pulse_pressure`** | $\text{SBP} - \text{DBP}$ | Arterial stiffness and aortic elasticity biomarker. |
| **`waist_to_height_ratio`** | $\text{waist\_cm} / \text{height\_cm}$ | Superior to BMI for South Asian central adiposity; cutoff 0.5. |
| **`total_to_hdl_ratio`** | $\text{total\_chol} / \text{hdl\_chol}$ | Framingham coronary heart disease risk ratio. |
| **`tg_to_hdl_ratio`** | $\text{triglycerides} / \text{hdl\_chol}$ | Surrogate marker of insulin resistance and small dense LDL particles. |
| **`bmi_category`** | $<18.5$ (Underweight), $18.5-22.9$ (Normal), $23.0-24.9$ (Overweight), $\ge 25.0$ (Obese) | WHO & ICMR consensus classification for Asian Indians. |
| **`lifestyle_risk_score`** | Composite score ($0-4$) from inactivity, current smoking, and regular alcohol | Aggregates modifiable behavioural risk factors. |
| **`metabolic_syndrome_flag`** | Binary indicator: $\ge 3$ of IDF Asian criteria met | Identifies multi-system cardiometabolic disease clustering. |
| **`interaction_age_bmi`** | $\text{age} \times \text{bmi}$ | Non-linear interaction between age and adiposity. |
| **`pca_dim_1`, `pca_dim_2`** | 2D PCA projection of standardized clinical vitals | Unsupervised patient segmentation & clustering manifold. |

---

## 3. Approved Datasets and Provenance Tracking

| Source ID | Name | Records | Format | Primary Task Fed |
| :--- | :--- | :--- | :--- | :--- |
| **DS-001** | UCI Heart Disease (Cleveland, Hungarian, VA, Swiss) | 920 | CSV | Heart Disease Classification |
| **DS-002** | Pima Indians Diabetes Database (NIDDK) | 768 | CSV | Diabetes Classification |
| **DS-003** | Scikit-Learn Diabetes Progression Benchmark | 442 | Builtin | 1-Year Quantitative Progression Regression |
| **DS-004** | Framingham Heart Study Cohort | 4,240 | CSV | 10-Year Cardiovascular & Hypertension Risk |
| **DS-005** | CDC NHANES Biomonitoring Subset | 5,000 | Parquet/CSV | Glycemic, Lipid, & BP Distribution Calibration |
| **DS-006** | CDC BRFSS Chronic Disease Surveillance Subset | 10,000 | Parquet/CSV | Lifestyle & Hypertension Risk Modeling |
| **DS-007** | Kaggle Chronic Kidney Disease (Apollo Hospitals) | 400 | CSV | South Asian Hypertensive & Glycemic Phenotypes |
| **DS-008** | Sanjivani AI Consented Production Screenings | Dynamic | Parquet/SQL | Post-market Monitoring & Continuous Learning |
| **TOTAL** | **Harmonized Master Cohort** | **21,920** | **Parquet** | **Feeds Classification, Regression, & Clustering** |
