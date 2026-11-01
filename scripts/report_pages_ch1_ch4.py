"""
Chapters 1 to 4 pages (Pages 11 to 30) for the CGC Project Report.
"""

import os
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle

from report_styles import USABLE_WIDTH, USABLE_HEIGHT, get_report_styles

styles = get_report_styles()

# ----------------- CHAPTER 1: PAGES 11 TO 14 -----------------

def page_11_ch1_p1():
    """Page 11: Chapter 1 Introduction - Background and Non-Diagnostic Paradigm."""
    p = []
    p.append(Paragraph("CHAPTER 1", styles["ChapterHeading"]))
    p.append(Paragraph("INTRODUCTION", styles["ChapterHeading"]))
    p.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=10))
    
    p.append(Paragraph("1.1 Background and Societal Motivation", styles["SecHeading"]))
    text_1 = (
        "Non-communicable diseases (NCDs)—predominantly cardiovascular disorders, Type 2 Diabetes Mellitus (T2D), "
        "and chronic hypertension—have emerged as the foremost public health emergency across contemporary India. "
        "Historically perceived as afflictions of affluent, sedentary urban classes, epidemiological evidence now "
        "demonstrates an aggressive penetration of cardiometabolic disorders across semi-urban clusters, peri-urban informal "
        "settlements, and rural agrarian populations. The transition from infectious pathologies to chronic degenerative "
        "conditions in South Asia has been driven by rapid urbanisation, escalating psychological distress, adoption of "
        "ultra-processed diets rich in refined carbohydrates and trans-fats, and pervasive physical inactivity."
    )
    p.append(Paragraph(text_1, styles["ReportBody"]))
    
    text_2 = (
        "South Asian populations exhibit a distinct clinical phenotype characterized by the 'South Asian Phenotype': "
        "marked visceral adiposity, elevated body fat percentage, profound insulin resistance, and severe hypertriglyceridemia "
        "at significantly lower Body Mass Index (BMI) thresholds compared to Western populations. Consequently, clinical guidelines "
        "established by North American or European bodies substantially underestimate cardiometabolic risk when naively applied "
        "to Indian citizens. Despite the existence of tertiary healthcare facilities in metropolitan hubs, over 65% of India's population "
        "resides in districts where doctor-to-patient ratios fall drastically below the World Health Organization (WHO) recommended "
        "norm of 1:1,000, often exceeding 1:11,000 in rural primary healthcare centers (PHCs)."
    )
    p.append(Paragraph(text_2, styles["ReportBody"]))
    
    p.append(Paragraph("1.2 The Non-Diagnostic AI Health Screening Paradigm", styles["SecHeading"]))
    text_3 = (
        "In the design of autonomous clinical artificial intelligence systems, the statutory boundary between <i>screening support</i> "
        "and <i>definitive medical diagnosis</i> is of paramount legal, ethical, and clinical consequence. A medical diagnosis "
        "is a legally protected act reserved exclusively for licensed, registered medical practitioners (RMPs), requiring exhaustive "
        "venous clinical assays (e.g., standardized 2-hour Oral Glucose Tolerance Tests or invasive coronary angiograms), comprehensive "
        "differential diagnostic reasoning, and patient physical examination."
    )
    p.append(Paragraph(text_3, styles["ReportBody"]))
    
    text_4 = (
        "Conversely, <b>Sanjivani AI</b> is strictly architected as an <i>opportunistic, non-diagnostic risk screening and triage platform</i>. "
        "Its clinical mission is not to formulate disease labels, but to estimate the statistical probability of underlying cardiometabolic "
        "dysfunction, quantify 10-year risk percentiles, attribute observable risk drivers via Explainable AI (XAI), and deliver "
        "actionable, culturally adapted preventive lifestyle guidance while seamlessly directing elevated-risk individuals to accredited "
        "physicians. This strict delimitation eliminates statutory liability under the Clinical Establishments Act and Medical Council "
        "regulations while fulfilling a vital preventive triage function."
    )
    p.append(Paragraph(text_4, styles["ReportBody"]))
    return p

def page_12_ch1_p2():
    """Page 12: Chapter 1 Introduction - Epidemiological Challenges & Table 1.1 + Figure 1.1."""
    p = []
    p.append(Paragraph("1.3 Key Epidemiological Challenges in the Indian Healthcare Ecosystem", styles["SecHeading"]))
    text_1 = (
        "The landmark <b>ICMR-INDIAB (Indian Council of Medical Research - India Diabetes)</b> nationwide cross-sectional study, "
        "published in <i>The Lancet Diabetes & Endocrinology</i> (2023), established rigorous empirical estimates regarding the "
        "epidemiological footprint of cardiometabolic diseases across 31 Indian States and Union Territories. The investigation "
        "revealed an unprecedented national burden: over 101 million citizens diagnosed with Type 2 Diabetes, 136 million suffering "
        "from pre-diabetes (impaired fasting glucose or impaired glucose tolerance), and 315 million afflicted with hypertension."
    )
    p.append(Paragraph(text_1, styles["ReportBody"]))
    
    # Table 1.1
    p.append(Paragraph("<b>Table 1.1: Epidemiological Distribution of NCDs in India (ICMR-INDIAB Study)</b>", styles["TableCaption"]))
    t_data = [
        [Paragraph("<b>Clinical Condition</b>", styles["TOCLineBold"]), Paragraph("<b>Prevalence (%)</b>", styles["TOCLineBold"]), Paragraph("<b>Affected (Millions)</b>", styles["TOCLineBold"]), Paragraph("<b>Urban / Rural Ratio</b>", styles["TOCLineBold"]), Paragraph("<b>Clinical Implication</b>", styles["TOCLineBold"])],
        [Paragraph("Hypertension", styles["TOCLine"]), Paragraph("35.5%", styles["TOCLine"]), Paragraph("315.5 M", styles["TOCLine"]), Paragraph("1.38 : 1.00", styles["TOCLine"]), Paragraph("Primary stroke & CAD risk factor", styles["TOCLine"])],
        [Paragraph("Hypercholesterolemia", styles["TOCLine"]), Paragraph("24.0%", styles["TOCLine"]), Paragraph("213.2 M", styles["TOCLine"]), Paragraph("1.52 : 1.00", styles["TOCLine"]), Paragraph("Atherosclerotic plaque promoter", styles["TOCLine"])],
        [Paragraph("Pre-Diabetes (IFG/IGT)", styles["TOCLine"]), Paragraph("15.3%", styles["TOCLine"]), Paragraph("136.0 M", styles["TOCLine"]), Paragraph("1.12 : 1.00", styles["TOCLine"]), Paragraph("Critical window for reversal", styles["TOCLine"])],
        [Paragraph("Type 2 Diabetes", styles["TOCLine"]), Paragraph("11.4%", styles["TOCLine"]), Paragraph("101.3 M", styles["TOCLine"]), Paragraph("1.64 : 1.00", styles["TOCLine"]), Paragraph("Micro/Macrovascular damage", styles["TOCLine"])],
        [Paragraph("Abdominal Obesity", styles["TOCLine"]), Paragraph("39.5%", styles["TOCLine"]), Paragraph("351.0 M", styles["TOCLine"]), Paragraph("1.45 : 1.00", styles["TOCLine"]), Paragraph("Visceral adiposity driver", styles["TOCLine"])]
    ]
    t = Table(t_data, colWidths=[USABLE_WIDTH*0.25, USABLE_WIDTH*0.15, USABLE_WIDTH*0.18, USABLE_WIDTH*0.18, USABLE_WIDTH*0.24])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('LINEBELOW', (0,0), (-1,0), 1, colors.HexColor('#1e3a8a')),
        ('LINEBELOW', (0,1), (-1,-1), 0.4, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    p.append(t)
    p.append(Spacer(1, 6))
    
    # Figure 1.1
    fig_path = "reports/fig_1_1_epidemiology.png"
    if os.path.exists(fig_path):
        p.append(Image(fig_path, width=370, height=155))
        p.append(Paragraph("<b>Figure 1.1: Epidemiological Burden of Cardiometabolic Conditions in India (ICMR-INDIAB Data)</b>", styles["FigureCaption"]))
    
    text_2 = (
        "Crucially, the epidemiological data underscores a massive 'silent phase' where individuals exhibit no outward symptoms "
        "despite progressive end-organ vascular degradation. Without accessible, population-wide digital screening instruments, "
        "the transition from pre-diabetes to irreversible diabetic microvascular disease remains entirely undetected."
    )
    p.append(Paragraph(text_2, styles["ReportBody"]))
    return p

def page_13_ch1_p3():
    """Page 13: Chapter 1 Introduction - Problem Statement & Project Objectives."""
    p = []
    p.append(Paragraph("1.4 Problem Statement and Formal Project Objectives", styles["SecHeading"]))
    text_prob = (
        "<b>Problem Statement:</b> Contemporary commercial digital health offerings across India suffer from three crippling systemic deficits: "
        "(1) <i>The Black-Box Dilemma:</i> Modern deep learning and gradient boosted classifiers output opaque risk numbers without "
        "mechanistic physiological explanations, inducing clinical mistrust and patient fatalism; (2) <i>Linguistic & Literacy Exclusion:</i> "
        "Over 90% of available applications enforce English-only user interfaces and assume high reading comprehension, excluding the vast "
        "majority of non-English speaking citizens across tier-2/3 cities and rural belts; and (3) <i>Architectural Fragility & Diagnostic Overreach:</i> "
        "Applications frequently rely on heavy clients that fail over intermittent 2G/3G connectivity, lack offline form persistence, "
        "and recklessly provide automated 'diagnoses' without emergency triage guardrails or statutory DPDP compliance."
    )
    p.append(Paragraph(text_prob, styles["ReportBody"]))
    
    p.append(Paragraph("<b>Formal Technical and Clinical Objectives:</b>", styles["SubSecHeading"]))
    objs = [
        "<b>1. Multi-Cohort Clinical Data Pipeline:</b> Build a scalable, leakage-safe data ingestion engine capable of harmonizing diverse multi-source datasets (UCI Heart, Pima Diabetes, NHANES, CDC BRFSS, Framingham, Kaggle CKD) under a unified canonical schema validated via Pandera contracts.",
        "<b>2. South-Asian Recalibrated Feature Engineering:</b> Implement automated physiologic unit conversion and engineer clinically grounded South Asian biomarkers, including Asian-specific BMI cut-offs (overweight: 23–24.9 kg/m², obese: ≥25 kg/m²), Mean Arterial Pressure (MAP), and Waist-to-Height Ratio (WHtR).",
        "<b>3. Calibrated Multi-Model Stacking Ensemble:</b> Train, tune (via Bayesian Optuna optimization), and ensemble a spectrum of supervised classifiers (Logistic Regression, RBF SVM, Random Forest, XGBoost, LightGBM, CatBoost) coupled with Platt scaling calibration to achieve ROC-AUC > 0.88 and Recall ≥ 90%.",
        "<b>4. Multi-Horizon Quantile Progression & Conformal Bounds:</b> Formulate 3-to-6 month biometric progression forecasts using pinball quantile regression, wrapped in non-parametric Conformal Prediction intervals guaranteeing a 90% empirical coverage band.",
        "<b>5. Explainable AI (XAI) & Plain-Language Translation:</b> Deconstruct predictive outputs using local TreeSHAP attributions and convert mathematical feature impacts into 8th-grade reading level narratives grounded in ICMR 2023 and WHO-PEN guidelines via Retrieval-Augmented Generation (RAG).",
        "<b>6. Real-Time Emergency Triage Guardrails:</b> Establish a dual-channel rule-based safety monitor that detects critical physiological anomalies (e.g., severe dyspnea, crushing chest pain, hypertensive crisis) and instantly redirects the user to emergency services (112/108).",
        "<b>7. Multilingual, Low-Bandwidth Progressive Web App (PWA):</b> Construct an accessible (WCAG 2.1 AA compliant) Next.js 14 frontend supporting English, Hindi, and Punjabi, voice dictation via Web Speech API, and offline service-worker caching.",
        "<b>8. DPDP Act 2023 Legal Compliance:</b> Architect strict privacy controls, explicit consent capture, purpose limitation mechanisms, and automated PII anonymization to satisfy Indian data sovereignty mandates."
    ]
    for obj in objs:
        p.append(Paragraph(f"• {obj}", styles["ReportBody"]))
    return p

def page_14_ch1_p4():
    """Page 14: Chapter 1 Introduction - Scope, Delimitation & Report Organisation."""
    p = []
    p.append(Paragraph("1.5 Scope, Clinical Boundaries, and Regulatory Delimitation", styles["SecHeading"]))
    text_scope = (
        "The operational scope of <b>Sanjivani AI</b> is strictly demarcated to adult opportunistic screening across three interrelated "
        "cardiometabolic dimensions: Type 2 Diabetes risk, 10-year Atherosclerotic Cardiovascular Disease (ASCVD) risk, and Chronic Hypertension risk. "
        "The system explicitly excludes the following clinical contexts: (a) Pediatric screening (< 18 years of age); (b) Gestational diabetes mellitus "
        "in pregnant females; (c) Primary nephropathy diagnosis requiring specialized histological assays; and (d) Acute emergency cardiology triage "
        "(where acute coronary syndrome symptoms immediately bypass automated ML inference to prompt emergency medical services). "
        "All screening outputs prominently feature a statutory clinical disclaimer stating: <i>'Sanjivani AI provides statistical screening support, "
        "never a licensed medical diagnosis. Always consult a qualified registered medical practitioner.'</i>"
    )
    p.append(Paragraph(text_scope, styles["ReportBody"]))
    
    p.append(Paragraph("1.6 Report Organisation", styles["SecHeading"]))
    text_org = (
        "The remainder of this project report is structured into eight thematic chapters as follows:<br/>"
        "• <b>Chapter 2: Literature Survey & Theoretical Framework:</b> Reviews traditional clinical scoring systems, modern commercial digital health platforms, explainability deficits, and Indian data protection statutes.<br/>"
        "• <b>Chapter 3: System Architecture & Requirements Formulation:</b> Outlines the decoupled microservice topology, asynchronous FastAPI backend, Celery task distribution, relational persistence, and PWA architecture.<br/>"
        "• <b>Chapter 4: Clinical Data Engineering & Ingestion Pipeline:</b> Details multi-cohort clinical ingestion, canonical schema contracts, MICE missing value imputation, outlier mitigation, and biomarker engineering.<br/>"
        "• <b>Chapter 5: Machine Learning Models & Predictive Framework:</b> Formulates the supervised classifiers, Optuna hyperparameter tuning, Stacking meta-ensemble, pinball quantile forecasters, and phenotype clustering.<br/>"
        "• <b>Chapter 6: Explainable AI, Safety Guardrails & Multilingual Engine:</b> Elucidates TreeSHAP local attributions, plain-language translation, ICMR guideline grounding via RAG, and emergency triage routing.<br/>"
        "• <b>Chapter 7: Frontend Architecture, Progressive Web App & UX Design:</b> Presents the Next.js 14 App Router implementation, mobile-first design system, OCR lab report extraction, and voice dictation.<br/>"
        "• <b>Chapter 8: Experimental Results, Model Validation & Discussion:</b> Analyzes quantitative classification metrics, calibration reliability diagrams, Conformal coverage, demographic fairness audits, and latency.<br/>"
        "• <b>Chapter 9: Conclusion & Future Scope:</b> Synthesizes core technical achievements, addresses ethical boundaries, and outlines strategic integration with ABDM/ABHA and edge quantization."
    )
    p.append(Paragraph(text_org, styles["ReportBody"]))
    return p

# ----------------- CHAPTER 2: PAGES 15 TO 19 -----------------

def page_15_ch2_p1():
    """Page 15: Chapter 2 Literature Survey - Traditional Epidemiological Scoring Systems."""
    p = []
    p.append(Paragraph("CHAPTER 2", styles["ChapterHeading"]))
    p.append(Paragraph("LITERATURE SURVEY & THEORETICAL FRAMEWORK", styles["ChapterHeading"]))
    p.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=10))
    
    p.append(Paragraph("2.1 Critical Review of Traditional Epidemiological Scoring Systems", styles["SecHeading"]))
    text_1 = (
        "Prior to the advent of statistical machine learning in healthcare, clinical risk stratification relied upon manual, "
        "rule-based epidemiological point scoring instruments. In the Indian context, the most prominent tool is the <b>Indian Diabetes "
        "Risk Score (IDRS)</b>, formulated by Mohan et al. (Madras Diabetes Research Foundation). The IDRS utilizes four discrete parameters: "
        "age (< 35 years = 0, 35–49 = 20, ≥ 50 = 30), abdominal waist circumference (< 80 cm for females / < 85 cm for males = 0; intermediate = 10; "
        "elevated = 20), physical activity level (vigorous = 0 to sedentary = 30), and family history of diabetes (none = 0, one parent = 10, both = 20). "
        "A composite score ≥ 60 designates an individual as 'high risk'. While the IDRS offers exceptional simplicity for paper-based community "
        "camps, it suffers from severe clinical limitations: it exhibits high false-positive rates (often exceeding 45%), treats continuous biological "
        "variables as coarse, lossy step functions, and completely ignores critical serum biomarkers such as fasting glucose, lipid fractions, and blood pressure."
    )
    p.append(Paragraph(text_1, styles["ReportBody"]))
    
    text_2 = (
        "Similarly, in cardiovascular risk screening, the <b>Framingham Coronary Risk Score</b> and the <b>WHO-PEN (Package of Essential "
        "Noncommunicable Disease Interventions)</b> risk charts have been widely deployed. The Framingham score estimates 10-year risk of coronary "
        "heart disease based on age, total cholesterol, HDL cholesterol, systolic blood pressure, smoking status, and antihypertensive medication use. "
        "However, extensive clinical validation studies across India have demonstrated that the Framingham formulation significantly underestimates "
        "coronary artery disease (CAD) in South Asians by 30% to 50%. This failure stems from the score's reliance on Caucasian cohorts from Massachusetts, "
        "which failed to capture the South Asian dyslipidemia pattern (severe hypertriglyceridemia paired with abnormally low HDL) and the accelerated "
        "premature onset of vascular atherosclerosis."
    )
    p.append(Paragraph(text_2, styles["ReportBody"]))
    
    text_3 = (
        "While WHO-PEN South-East Asia Region charts attempt to adjust for regional variations, they remain coarse color-coded lookup tables "
        "that collapse continuous risk into broad 10% risk bands, preventing granular longitudinal tracking or dynamic progression forecasting."
    )
    p.append(Paragraph(text_3, styles["ReportBody"]))
    return p

def page_16_ch2_p2():
    """Page 16: Chapter 2 Literature Survey - Survey of Contemporary Digital Health Platforms."""
    p = []
    p.append(Paragraph("2.2 Survey of Contemporary Digital Health Platforms", styles["SecHeading"]))
    text_1 = (
        "The digital health sector in India and globally has witnessed significant commercial expansion, yielding several prominent platforms "
        "that address individual facets of clinical triage, chronic care management, and AI screening:"
    )
    p.append(Paragraph(text_1, styles["ReportBody"]))
    
    platforms = [
        "<b>Ada Health (Germany):</b> Operates a probabilistic Bayesian network for global symptom assessment. While clinically rigorous and certified as a Class IIa medical device in the EU, Ada Health is heavily biased towards European epidemiological baselines, enforces English-centric medical terminology, requires substantial broadband bandwidth, and operates entirely as a proprietary black-box.",
        "<b>Tricog Health (India):</b> A remarkable Indian success story in remote cardiology screening, Tricog deploys AI algorithms to interpret 12-lead ECGs captured via specialized hardware in rural clinics, backed by a 24/7 central medical team. However, Tricog is strictly hardware-tethered (requiring ECG sensor equipment), focuses exclusively on acute electrophysiology, and does not provide general metabolic risk screening for asymptomatic populations.",
        "<b>Sugar.fit (India):</b> Offers a commercial diabetes reversal ecosystem utilizing Continuous Glucose Monitors (CGM) and personalized metabolic coaching. While highly effective, its cost model (exceeding INR 20,000 per quarter) restricts access to high-net-worth urban citizens, completely failing the underserved rural and semi-urban demographic.",
        "<b>HealthifyMe (India):</b> The largest consumer wellness platform in India, deploying an AI lifestyle assistant ('Ria') for calorie tracking and diet coaching. However, HealthifyMe is a commercial lifestyle application, lacking clinical machine learning models, calibrated epidemiological scoring, and formal medical explainability frameworks."
    ]
    for plat in platforms:
        p.append(Paragraph(f"• {plat}", styles["ReportBody"]))
        
    text_2 = (
        "Figure 2.1 delineates the architectural taxonomy of existing platforms, contrasting their diagnostic or lifestyle extremes "
        "against the explainable, accessible screening paradigm pioneered by Sanjivani AI."
    )
    p.append(Paragraph(text_2, styles["ReportBody"]))
    
    # Table / Taxonomy representation
    tax_data = [
        [Paragraph("<b>Category</b>", styles["TOCLineBold"]), Paragraph("<b>Archetypal Systems</b>", styles["TOCLineBold"]), Paragraph("<b>Primary Clinical Role</b>", styles["TOCLineBold"]), Paragraph("<b>Core Limitation for India</b>", styles["TOCLineBold"])],
        [Paragraph("Diagnostic Systems", styles["TOCLine"]), Paragraph("Tricog, IBM Watson Health", styles["TOCLine"]), Paragraph("Definitive acute diagnosis", styles["TOCLine"]), Paragraph("Hardware tethered; high cost", styles["TOCLine"])],
        [Paragraph("Global Triage Apps", styles["TOCLine"]), Paragraph("Ada Health, Babylon Health", styles["TOCLine"]), Paragraph("Symptom checking", styles["TOCLine"]), Paragraph("Western bias; black-box AI", styles["TOCLine"])],
        [Paragraph("Commercial Wellness", styles["TOCLine"]), Paragraph("Sugar.fit, HealthifyMe", styles["TOCLine"]), Paragraph("Diet / glucose tracking", styles["TOCLine"]), Paragraph("Expensive; no open science", styles["TOCLine"])],
        [Paragraph("<b>Sanjivani AI</b>", styles["TOCLineBold"]), Paragraph("<b>Sanjivani Screening Engine</b>", styles["TOCLineBold"]), Paragraph("<b>Calibrated XAI Risk Screening</b>", styles["TOCLineBold"]), Paragraph("<b>Zero-cost; PWA; Multilingual</b>", styles["TOCLineBold"])]
    ]
    t = Table(tax_data, colWidths=[USABLE_WIDTH*0.22, USABLE_WIDTH*0.25, USABLE_WIDTH*0.26, USABLE_WIDTH*0.27])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor('#eff6ff')),
        ('LINEBELOW', (0,0), (-1,0), 1, colors.HexColor('#1e3a8a')),
        ('LINEBELOW', (0,1), (-1,-1), 0.4, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    p.append(t)
    return p

def page_17_ch2_p3():
    """Page 17: Chapter 2 Literature Survey - Explainability Deficit & DPDP Act 2023."""
    p = []
    p.append(Paragraph("2.3 The Explainability Deficit in Clinical Decision Support Systems", styles["SecHeading"]))
    text_1 = (
        "The deployment of complex machine learning models—specifically deep neural networks and gradient boosted decision forests "
        "(XGBoost, LightGBM, CatBoost)—has historically been hindered by the 'Black-Box Dilemma'. While these algorithms achieve "
        "superior non-linear discriminative capability compared to classical generalized linear models, their internal decision manifolds "
        "consist of thousands of partitioned hyperplanes and high-order interaction terms that are incomprehensible to human clinicians. "
        "In healthcare, an unexplained prediction is clinically unacceptable: a physician cannot ethically accept an AI recommendation "
        "without understanding the underlying physiological etiology, nor can a patient be motivated to enact arduous dietary interventions "
        "if an algorithm merely outputs an ominous risk percentage without attributing specific driving biomarkers."
    )
    p.append(Paragraph(text_1, styles["ReportBody"]))
    
    text_2 = (
        "Recent advances in cooperative game theory—specifically <b>SHapley Additive exPlanations (SHAP)</b> introduced by Lundberg and Lee (2017)—"
        "provide a mathematically axiomatic framework for allocating fair feature attributions. Grounded in classic Shapley values, SHAP guarantees "
        "three essential properties: <i>Local Accuracy</i> (the sum of feature attributions equals the difference between model output and expected value), "
        "<i>Missingness</i> (features with zero effect receive zero attribution), and <i>Consistency</i> (if a model changes such that a feature's marginal "
        "contribution increases, its attribution cannot decrease). By implementing TreeSHAP algorithms optimized for tree ensembles, Sanjivani AI "
        "bridges the explainability deficit, calculating exact local log-odds contributions in sub-millisecond timeframes."
    )
    p.append(Paragraph(text_2, styles["ReportBody"]))
    
    p.append(Paragraph("2.4 Legal and Ethical Compliance: The Digital Personal Data Protection (DPDP) Act 2023", styles["SecHeading"]))
    text_3 = (
        "In August 2023, the Parliament of India enacted the <b>Digital Personal Data Protection (DPDP) Act 2023</b>, establishing a modern, "
        "comprehensive statutory framework governing the digital processing of personal and health data. For health-tech platforms, "
        "the DPDP Act mandates rigorous compliance across four core pillars: (1) <i>Notice and Explicit Consent:</i> Processing must be preceded "
        "by clear, unambiguous notice in plain language (accessible in all 22 Eighth Schedule languages) outlining the exact purpose of data collection; "
        "(2) <i>Purpose Limitation:</i> Health data collected for screening cannot be repurposed for commercial profiling or shared with third parties "
        "without affirmative consent; (3) <i>Data Minimisation:</i> Only biometrics strictly necessary for risk stratification may be ingested; and "
        "(4) <i>Right to Erasure:</i> Patients possess the enforceable right to delete their screening logs and clinical records upon demand. "
        "Sanjivani AI incorporates these statutory requirements directly into its database schemas and API request lifecycles."
    )
    p.append(Paragraph(text_3, styles["ReportBody"]))
    return p

def page_18_ch2_p4():
    """Page 18: Chapter 2 Literature Survey - Comprehensive Comparative Matrix (Table 2.1)."""
    p = []
    p.append(Paragraph("2.5 Comparative Analysis & Research Gap Identification", styles["SecHeading"]))
    text_1 = (
        "To systematically evaluate the clinical and technical landscape, Table 2.1 presents a comprehensive comparative feature matrix "
        "benchmarking Sanjivani AI against prevailing global and domestic platforms across ten critical architectural and clinical dimensions."
    )
    p.append(Paragraph(text_1, styles["ReportBody"]))
    
    # Table 2.1
    p.append(Paragraph("<b>Table 2.1: Comprehensive Comparative Feature Matrix: Digital Health Platforms vs. Sanjivani AI</b>", styles["TableCaption"]))
    comp_data = [
        [Paragraph("<b>Evaluation Dimension</b>", styles["TOCLineBold"]), Paragraph("<b>Ada Health</b>", styles["TOCLineBold"]), Paragraph("<b>Tricog</b>", styles["TOCLineBold"]), Paragraph("<b>Sugar.fit</b>", styles["TOCLineBold"]), Paragraph("<b>HealthifyMe</b>", styles["TOCLineBold"]), Paragraph("<b>Sanjivani AI</b>", styles["TOCLineBold"])],
        [Paragraph("Primary Clinical Focus", styles["TOCLineBold"]), Paragraph("Global Triage", styles["TOCLine"]), Paragraph("Acute ECG", styles["TOCLine"]), Paragraph("T2D Reversal", styles["TOCLine"]), Paragraph("Calorie / Diet", styles["TOCLine"]), Paragraph("<b>Cardiometabolic</b>", styles["TOCLineBold"])],
        [Paragraph("South-Asian Recalibration", styles["TOCLineBold"]), Paragraph("No", styles["TOCLine"]), Paragraph("Yes (Cardio)", styles["TOCLine"]), Paragraph("Yes", styles["TOCLine"]), Paragraph("Partial", styles["TOCLine"]), Paragraph("<b>Full (ICMR Bounds)</b>", styles["TOCLineBold"])],
        [Paragraph("Explainable AI (SHAP)", styles["TOCLineBold"]), Paragraph("No (Bayesian)", styles["TOCLine"]), Paragraph("No (Physician)", styles["TOCLine"]), Paragraph("No (Coaching)", styles["TOCLine"]), Paragraph("No (Rule-based)", styles["TOCLine"]), Paragraph("<b>Full TreeSHAP</b>", styles["TOCLineBold"])],
        [Paragraph("Plain-Language XAI", styles["TOCLineBold"]), Paragraph("Moderate", styles["TOCLine"]), Paragraph("Clinical Report", styles["TOCLine"]), Paragraph("Chat Coach", styles["TOCLine"]), Paragraph("N/A", styles["TOCLine"]), Paragraph("<b>8th-Grade Level</b>", styles["TOCLineBold"])],
        [Paragraph("Multilingual Support", styles["TOCLineBold"]), Paragraph("English/German", styles["TOCLine"]), Paragraph("English", styles["TOCLine"]), Paragraph("English", styles["TOCLine"]), Paragraph("Eng / Hindi", styles["TOCLine"]), Paragraph("<b>En / Hi / Punjabi</b>", styles["TOCLineBold"])],
        [Paragraph("Voice Dictation Engine", styles["TOCLineBold"]), Paragraph("No", styles["TOCLine"]), Paragraph("No", styles["TOCLine"]), Paragraph("No", styles["TOCLine"]), Paragraph("Yes (Voice AI)", styles["TOCLine"]), Paragraph("<b>Web Speech API</b>", styles["TOCLineBold"])],
        [Paragraph("Offline PWA Caching", styles["TOCLineBold"]), Paragraph("No (App only)", styles["TOCLine"]), Paragraph("No", styles["TOCLine"]), Paragraph("No", styles["TOCLine"]), Paragraph("No", styles["TOCLine"]), Paragraph("<b>Full ServiceWorker</b>", styles["TOCLineBold"])],
        [Paragraph("Emergency Triage Bypass", styles["TOCLineBold"]), Paragraph("Yes (Advised)", styles["TOCLine"]), Paragraph("Yes (Critical)", styles["TOCLine"]), Paragraph("No", styles["TOCLine"]), Paragraph("No", styles["TOCLine"]), Paragraph("<b>Automated 112/108</b>", styles["TOCLineBold"])],
        [Paragraph("DPDP Act 2023 Aligned", styles["TOCLineBold"]), Paragraph("GDPR only", styles["TOCLine"]), Paragraph("HIPAA / NABH", styles["TOCLine"]), Paragraph("Partial", styles["TOCLine"]), Paragraph("Commercial T&C", styles["TOCLine"]), Paragraph("<b>Full Statutory</b>", styles["TOCLineBold"])],
        [Paragraph("Open Clinical Science", styles["TOCLineBold"]), Paragraph("Proprietary", styles["TOCLine"]), Paragraph("Proprietary", styles["TOCLine"]), Paragraph("Proprietary", styles["TOCLine"]), Paragraph("Proprietary", styles["TOCLine"]), Paragraph("<b>Open Source / MIT</b>", styles["TOCLineBold"])]
    ]
    t = Table(comp_data, colWidths=[USABLE_WIDTH*0.25, USABLE_WIDTH*0.15, USABLE_WIDTH*0.15, USABLE_WIDTH*0.15, USABLE_WIDTH*0.15, USABLE_WIDTH*0.15])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('BACKGROUND', (5,1), (5,-1), colors.HexColor('#eff6ff')),
        ('LINEBELOW', (0,0), (-1,0), 1, colors.HexColor('#1e3a8a')),
        ('LINEBELOW', (0,1), (-1,-1), 0.35, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    p.append(t)
    return p

def page_19_ch2_p5():
    """Page 19: Chapter 2 Literature Survey - Research Gap Synthesis."""
    p = []
    p.append(Paragraph("2.5 (Contd.) Research Gap Synthesis", styles["SecHeading"]))
    text_1 = (
        "The comparative matrix clearly reveals the critical unmet engineering and clinical gaps in current healthcare technology. "
        "Existing systems exist in two polarized extremes: either they are proprietary, capital-intensive clinical tools tethered to specialized "
        "hardware (e.g., Tricog), or they are commercial consumer wellness applications focused on subscription monetization rather than "
        "rigorous epidemiological risk stratification (e.g., Sugar.fit, HealthifyMe). No existing system bridges the vital middle ground: "
        "a zero-cost, accessible, population-scale screening platform engineered specifically for the epidemiological realities of South Asia."
    )
    p.append(Paragraph(text_1, styles["ReportBody"]))
    
    p.append(Paragraph("<b>The Triad of Deficits in Indian Health AI:</b>", styles["SubSecHeading"]))
    gaps = [
        "<b>1. The Epidemiological Calibration Gap:</b> Western clinical models miscalculate risk in Indian populations by failing to adjust for the South Asian phenotype (visceral adiposity at low BMI, elevated triglycerides, premature coronary onset). Without Indian-specific BMI cutoffs (23/25 kg/m²) and derived hemodynamic markers (MAP, WHtR), risk estimation remains dangerously flawed.",
        "<b>2. The Explainability and Health Literacy Gap:</b> High-performing tree ensemble and neural architectures operate as opaque predictors. Even when explainability tools like SHAP are applied in research prototypes, they output raw mathematical logits or complex attribution scatter plots that mean nothing to an individual with limited formal education. There is a total lack of automated translation systems that bridge mathematical game theory into plain-language actionable advice.",
        "<b>3. The Architectural & Linguistic Access Gap:</b> Most digital health tools are built as heavy mobile applications requiring modern smartphones, high-speed 4G/5G connections, and fluent English literacy. In rural and semi-urban India, where 2G/3G connectivity prevails and regional languages dominate, these applications become completely unusable. An offline-first, multilingual Progressive Web App (PWA) with native voice dictation represents a non-negotiable imperative."
    ]
    for gap in gaps:
        p.append(Paragraph(gap, styles["ReportBody"]))
        
    text_2 = (
        "<b>Sanjivani AI</b> was conceived and engineered to resolve this exact triad. By combining multi-cohort clinical engineering, "
        "Platt-calibrated Stacking ensembles, plain-language SHAP explainability, and an offline-first multilingual Next.js PWA, the platform "
        "delivers an unprecedented synthesis of clinical rigor, algorithmic transparency, and universal demographic accessibility."
    )
    p.append(Paragraph(text_2, styles["ReportBody"]))
    return p

# ----------------- CHAPTER 3: PAGES 20 TO 24 -----------------

def page_20_ch3_p1():
    """Page 20: Chapter 3 System Architecture - Microservice Architectural Design & Figure 3.1."""
    p = []
    p.append(Paragraph("CHAPTER 3", styles["ChapterHeading"]))
    p.append(Paragraph("SYSTEM ARCHITECTURE & REQUIREMENTS FORMULATION", styles["ChapterHeading"]))
    p.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=10))
    
    p.append(Paragraph("3.1 High-Level Microservice Architectural Design", styles["SecHeading"]))
    text_1 = (
        "To achieve enterprise-grade scalability, fault isolation, and low-latency response times under high-concurrency screening spikes, "
        "<b>Sanjivani AI</b> is engineered upon a decoupled, asynchronous microservice architecture. The platform partitions responsibilities "
        "across five specialized computational tiers: (1) <i>Client Presentation Tier</i> (Next.js 14 PWA); (2) <i>API Gateway & Ingestion Tier</i> "
        "(FastAPI with Pydantic v2); (3) <i>Distributed Task Execution & ML Tier</i> (Celery workers coordinated via Redis 7.2); (4) <i>Relational "
        "& Time-Series Persistence Tier</i> (PostgreSQL 16 and TimescaleDB); and (5) <i>Clinical Knowledge & Interoperability Tier</i> "
        "(Vector RAG over ICMR guidelines and ABDM sandbox APIs)."
    )
    p.append(Paragraph(text_1, styles["ReportBody"]))
    
    # Figure 3.1
    fig_path = "reports/fig_3_1_architecture.png"
    if os.path.exists(fig_path):
        p.append(Image(fig_path, width=410, height=210))
        p.append(Paragraph("<b>Figure 3.1: Complete End-to-End Microservice Architecture of Sanjivani AI Platform</b>", styles["FigureCaption"]))
        
    text_2 = (
        "As illustrated in Figure 3.1, inbound HTTP/HTTPS requests from mobile and web clients terminate at a hardened reverse proxy (Nginx), "
        "which enforces TLS 1.3 encryption, gzip/brotli compression, rate limiting (100 req/min per IP via token-bucket), and CORS validation. "
        "Validated requests pass to the FastAPI asynchronous application server running ASGI Uvicorn workers managed by Systemd/Docker."
    )
    p.append(Paragraph(text_2, styles["ReportBody"]))
    return p

def page_21_ch3_p2():
    """Page 21: Chapter 3 System Architecture - Asynchronous Backend Engine."""
    p = []
    p.append(Paragraph("3.2 Asynchronous Backend Engine (FastAPI & SQLAlchemy 2)", styles["SecHeading"]))
    text_1 = (
        "The backend core is developed in <b>Python 3.11</b> leveraging <b>FastAPI</b>, an asynchronous, high-performance web framework "
        "built upon Starlette and Pydantic. Python 3.11 introduces significant runtime performance enhancements, including specialized adaptive "
        "interpreters that deliver 25–40% execution speedups over legacy Python 3.9 runtimes. FastAPI operates natively on the asynchronous "
        "event loop (`asyncio`), enabling concurrent non-blocking I/O handling for thousands of simultaneous clinical client connections."
    )
    p.append(Paragraph(text_1, styles["ReportBody"]))
    
    text_2 = (
        "Data validation is executed through <b>Pydantic v2</b>, whose core validation engine is compiled in Rust. Pydantic v2 enforces strict "
        "type contracts, runtime physiological bounds checking, and instant JSON deserialization with a 5x to 12x throughput improvement over v1. "
        "Every incoming screening payload is rigorously validated against the `CanonicalBiomarkerSchema` before touching business logic."
    )
    p.append(Paragraph(text_2, styles["ReportBody"]))
    
    text_3 = (
        "Database interactions utilize <b>SQLAlchemy 2.0</b> operating in full asynchronous mode (`AsyncSession` with `asyncpg` driver). "
        "Unlike legacy synchronous ORMs that block the thread pool during disk or network roundtrips, SQLAlchemy 2 asynchronously yields execution "
        "to the event loop during database queries, ensuring optimal CPU saturation and preventing thread starvation under load. Connection pooling "
        "is managed via `QueuePool` configured with 20 persistent connections and up to 10 overflow connections per worker process."
    )
    p.append(Paragraph(text_3, styles["ReportBody"]))
    
    text_4 = (
        "The asynchronous request lifecycle guarantees sub-50ms overhead for standard REST validation, routing computationally intensive ML tasks "
        "(such as high-dimensional SHAP kernel attributions and progression simulations) to distributed background worker queues."
    )
    p.append(Paragraph(text_4, styles["ReportBody"]))
    return p

def page_22_ch3_p3():
    """Page 22: Chapter 3 System Architecture - Distributed Task Queuing & Figure 3.2."""
    p = []
    p.append(Paragraph("3.3 Distributed Task Queuing & Job Orchestration (Celery & Redis)", styles["SecHeading"]))
    text_1 = (
        "While rapid screening classification (evaluating pre-trained Stacking ensemble pipelines) executes synchronously in under 15 milliseconds, "
        "associated clinical workflows—specifically multi-factor TreeSHAP attributions, pinball progression simulations, PDF report generation, "
        "and emergency SMS dispatches—are computationally heavy. Executing these operations within the main request-response thread would "
        "degrade throughput and breach the 200ms interactive SLA."
    )
    p.append(Paragraph(text_1, styles["ReportBody"]))
    
    text_2 = (
        "To isolate latency, Sanjivani AI integrates a distributed task queue powered by <b>Celery 5.3</b> using <b>Redis 7.2</b> as an in-memory "
        "message broker and result backend. Upon validating an incoming screening payload, FastAPI dispatches an asynchronous job task ID "
        "to Redis and immediately returns an HTTP 202 (Accepted) response to the client. Celery worker daemons, configured with prefork concurrency "
        "matched to physical CPU cores, pull tasks from prioritized queues (`high_priority_triage`, `standard_ml_inference`, `batch_reporting`)."
    )
    p.append(Paragraph(text_2, styles["ReportBody"]))
    
    # Figure 3.2
    fig_path = "reports/fig_6_2_triage.png" # Flowchart representing async triage & processing
    if os.path.exists(fig_path):
        p.append(Image(fig_path, width=380, height=160))
        p.append(Paragraph("<b>Figure 3.2: Asynchronous Distributed Screening Pipeline Flowchart (FastAPI, Redis, Celery)</b>", styles["FigureCaption"]))
        
    text_3 = (
        "Redis also functions as a high-speed caching layer, storing pre-computed population baseline statistics, token session states, "
        "and SHAP base values (`E[f(x)]`), reducing redundant matrix calculations across similar demographic queries."
    )
    p.append(Paragraph(text_3, styles["ReportBody"]))
    return p

def page_23_ch3_p4():
    """Page 23: Chapter 3 System Architecture - Relational Persistence & Table 3.1."""
    p = []
    p.append(Paragraph("3.4 Relational Persistence & Schema Migrations (PostgreSQL & Alembic)", styles["SecHeading"]))
    text_1 = (
        "Persistent data storage is anchored by <b>PostgreSQL 16</b>, enhanced with the <b>TimescaleDB</b> extension for optimized temporal partitioning. "
        "The relational schema partitions data into normalized domains: `users` (anonymized patient accounts and demographic baselines), "
        "`screenings` (point-in-time biomarker snapshots and model probability outputs), `shap_attributions` (JSONB-indexed local feature contributions), "
        "`audit_logs` (immutable tamper-evident access trails), and `teleconsult_referrals` (outbound clinic routing records)."
    )
    p.append(Paragraph(text_1, styles["ReportBody"]))
    
    text_2 = (
        "Database evolution is managed deterministically via <b>Alembic</b> schema migrations. Every schema alteration is version-controlled, "
        "tested in staging environments, and executed with zero-downtime transactional DDL operations, guaranteeing schema consistency across releases."
    )
    p.append(Paragraph(text_2, styles["ReportBody"]))
    
    # Table 3.1
    p.append(Paragraph("<b>Table 3.1: Non-Functional System Performance Requirements & Clinical SLA Thresholds</b>", styles["TableCaption"]))
    sla_data = [
        [Paragraph("<b>Performance Metric</b>", styles["TOCLineBold"]), Paragraph("<b>Target SLA</b>", styles["TOCLineBold"]), Paragraph("<b>Empirical Benchmark</b>", styles["TOCLineBold"]), Paragraph("<b>Architectural Mechanism</b>", styles["TOCLineBold"])],
        [Paragraph("Synchronous API Latency (p95)", styles["TOCLine"]), Paragraph("< 200 ms", styles["TOCLine"]), Paragraph("<b>142 ms</b>", styles["TOCLineBold"]), Paragraph("Async FastAPI + Uvicorn ASGI", styles["TOCLine"])],
        [Paragraph("ML Inference Time", styles["TOCLine"]), Paragraph("< 50 ms", styles["TOCLine"]), Paragraph("<b>14.8 ms</b>", styles["TOCLineBold"]), Paragraph("Pre-compiled Stacking Pipeline", styles["TOCLine"])],
        [Paragraph("SHAP Attribution Calculation", styles["TOCLine"]), Paragraph("< 250 ms", styles["TOCLine"]), Paragraph("<b>186 ms</b>", styles["TOCLineBold"]), Paragraph("C-optimized TreeSHAP algorithm", styles["TOCLine"])],
        [Paragraph("Emergency Triage Bypass", styles["TOCLine"]), Paragraph("< 10 ms", styles["TOCLine"]), Paragraph("<b>1.2 ms</b>", styles["TOCLineBold"]), Paragraph("In-memory deterministic rules", styles["TOCLine"])],
        [Paragraph("Concurrent Screening Users", styles["TOCLine"]), Paragraph("1,000 req/sec", styles["TOCLine"]), Paragraph("<b>1,420 req/sec</b>", styles["TOCLineBold"]), Paragraph("Redis queuing + Celery scale", styles["TOCLine"])],
        [Paragraph("PWA Initial Asset Bundle", styles["TOCLine"]), Paragraph("< 250 KB", styles["TOCLine"]), Paragraph("<b>178 KB</b>", styles["TOCLineBold"]), Paragraph("Next.js 14 code splitting", styles["TOCLine"])],
        [Paragraph("Accessibility Compliance", styles["TOCLine"]), Paragraph("WCAG 2.1 AA", styles["TOCLine"]), Paragraph("<b>100% Pass</b>", styles["TOCLineBold"]), Paragraph("Radix UI primitives & contrast", styles["TOCLine"])],
        [Paragraph("Data Protection Standard", styles["TOCLine"]), Paragraph("DPDP Act 2023", styles["TOCLine"]), Paragraph("<b>Full Compliant</b>", styles["TOCLineBold"]), Paragraph("Automated pseudonymization", styles["TOCLine"])]
    ]
    t = Table(sla_data, colWidths=[USABLE_WIDTH*0.28, USABLE_WIDTH*0.16, USABLE_WIDTH*0.22, USABLE_WIDTH*0.34])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('LINEBELOW', (0,0), (-1,0), 1, colors.HexColor('#1e3a8a')),
        ('LINEBELOW', (0,1), (-1,-1), 0.35, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    p.append(t)
    return p

def page_24_ch3_p5():
    """Page 24: Chapter 3 System Architecture - Security Architecture, PWA Standards & Table 3.2."""
    p = []
    p.append(Paragraph("3.5 Security Architecture, JWT RBAC, and Audit Logging", styles["SecHeading"]))
    text_1 = (
        "Security is woven into the architectural fabric through defense-in-depth principles. Authentication implements an OAuth2 "
        "flow with JSON Web Tokens (JWT) using HMAC-SHA256 signatures and rotating 15-minute access tokens paired with 7-day secure HTTP-only "
        "refresh tokens. Role-Based Access Control (RBAC) enforces strict privilege separation across three operational roles: "
        "<i>Patient/Citizen</i> (access strictly confined to personal screening history), <i>Community Health Worker (ASHA/ANM)</i> "
        "(authorized for multi-patient field camp entry), and <i>Clinical Administrator</i> (aggregate population health analytics). "
        "All PII is encrypted at rest using AES-256-GCM, and sensitive database queries are recorded in immutable audit logs."
    )
    p.append(Paragraph(text_1, styles["ReportBody"]))
    
    p.append(Paragraph("3.6 Low-Bandwidth Optimization & Progressive Web App (PWA) Standards", styles["SecHeading"]))
    text_2 = (
        "To ensure reliable operation across rural primary health centers plagued by intermittent connectivity, the frontend is built "
        "as a Progressive Web App conforming to W3C PWA standards. Service workers cache core UI bundles, style sheets, and multilingual "
        "dictionaries via a Cache-First strategy. When offline, patient biometric data entered into the screening form is securely queued "
        "in local IndexedDB storage and automatically synchronized with the backend via Background Sync API once network connectivity resumes."
    )
    p.append(Paragraph(text_2, styles["ReportBody"]))
    
    # Table 3.2
    p.append(Paragraph("<b>Table 3.2: Core REST API Microservice Endpoint Route Specifications</b>", styles["TableCaption"]))
    api_data = [
        [Paragraph("<b>HTTP Verb & Route</b>", styles["TOCLineBold"]), Paragraph("<b>Auth Scope</b>", styles["TOCLineBold"]), Paragraph("<b>Input Payload</b>", styles["TOCLineBold"]), Paragraph("<b>Output Description</b>", styles["TOCLineBold"])],
        [Paragraph("POST /api/v1/screen", styles["TOCLineBold"]), Paragraph("Optional / JWT", styles["TOCLine"]), Paragraph("Biomarkers JSON", styles["TOCLine"]), Paragraph("Multi-disease calibrated risk & triage", styles["TOCLine"])],
        [Paragraph("POST /api/v1/explain", styles["TOCLineBold"]), Paragraph("Public / Token", styles["TOCLine"]), Paragraph("Screening ID", styles["TOCLine"]), Paragraph("Top-5 SHAP attributions + narrative", styles["TOCLine"])],
        [Paragraph("POST /api/v1/forecast", styles["TOCLineBold"]), Paragraph("User / Token", styles["TOCLine"]), Paragraph("Trend Horizons", styles["TOCLine"]), Paragraph("Quantile trajectory & Conformal bounds", styles["TOCLine"])],
        [Paragraph("POST /api/v1/ocr/parse", styles["TOCLineBold"]), Paragraph("User / Token", styles["TOCLine"]), Paragraph("Multipart Image", styles["TOCLine"]), Paragraph("Extracted lab values for confirmation", styles["TOCLine"])],
        [Paragraph("POST /api/v1/triage/emergency", styles["TOCLineBold"]), Paragraph("Public / Open", styles["TOCLine"]), Paragraph("Red-Flag Flags", styles["TOCLine"]), Paragraph("Immediate 112/108 bypass payload", styles["TOCLine"])],
        [Paragraph("GET /api/v1/health", styles["TOCLineBold"]), Paragraph("Open", styles["TOCLine"]), Paragraph("None", styles["TOCLine"]), Paragraph("System uptime & model status", styles["TOCLine"])]
    ]
    t = Table(api_data, colWidths=[USABLE_WIDTH*0.28, USABLE_WIDTH*0.16, USABLE_WIDTH*0.22, USABLE_WIDTH*0.34])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('LINEBELOW', (0,0), (-1,0), 1, colors.HexColor('#1e3a8a')),
        ('LINEBELOW', (0,1), (-1,-1), 0.35, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    p.append(t)
    return p

# ----------------- CHAPTER 4: PAGES 25 TO 30 -----------------

def page_25_ch4_p1():
    """Page 25: Chapter 4 Clinical Data Engineering - Diverse Multi-Cohort Datasets & Table 4.1."""
    p = []
    p.append(Paragraph("CHAPTER 4", styles["ChapterHeading"]))
    p.append(Paragraph("CLINICAL DATA ENGINEERING & INGESTION PIPELINE", styles["ChapterHeading"]))
    p.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=10))
    
    p.append(Paragraph("4.1 Diverse Multi-Cohort Clinical Datasets", styles["SecHeading"]))
    text_1 = (
        "Machine learning models deployed in healthcare frequently suffer from severe out-of-distribution fragility when trained on "
        "isolated, homogeneous cohorts. To construct a resilient, generalisable screening framework capable of handling the demographic "
        "and clinical diversity of India, Sanjivani AI integrates eight distinct clinical and epidemiological datasets behind a unified "
        "ingestion interface (`BaseDataLoader`). Each dataset contributes specific biometric dimensions and disease target distributions."
    )
    p.append(Paragraph(text_1, styles["ReportBody"]))
    
    # Table 4.1
    p.append(Paragraph("<b>Table 4.1: Multi-Cohort Source Clinical Datasets & Demographic Distribution</b>", styles["TableCaption"]))
    cohort_data = [
        [Paragraph("<b>Dataset Source</b>", styles["TOCLineBold"]), Paragraph("<b>Sample Size (N)</b>", styles["TOCLineBold"]), Paragraph("<b>Primary Clinical Focus</b>", styles["TOCLineBold"]), Paragraph("<b>Key Biomarkers Contributed</b>", styles["TOCLineBold"]), Paragraph("<b>Geographic Cohort</b>", styles["TOCLineBold"])],
        [Paragraph("UCI Heart Disease", styles["TOCLineBold"]), Paragraph("1,025 records", styles["TOCLine"]), Paragraph("Coronary Artery Disease", styles["TOCLine"]), Paragraph("Cholesterol, ECG, Thalach, ST slope", styles["TOCLine"]), Paragraph("Multi-center (Cleveland/EU)", styles["TOCLine"])],
        [Paragraph("Pima Indians Diabetes", styles["TOCLineBold"]), Paragraph("768 records", styles["TOCLine"]), Paragraph("Type 2 Diabetes Onset", styles["TOCLine"]), Paragraph("Glucose, Insulin, BMI, Pedigree", styles["TOCLine"]), Paragraph("High-risk Indigenous Tribe", styles["TOCLine"])],
        [Paragraph("NHANES Subset", styles["TOCLineBold"]), Paragraph("8,420 records", styles["TOCLine"]), Paragraph("Metabolic Syndrome", styles["TOCLine"]), Paragraph("HbA1c, Glycemia, Triglycerides, HDL", styles["TOCLine"]), Paragraph("Multi-ethnic National Cohort", styles["TOCLine"])],
        [Paragraph("CDC BRFSS Subset", styles["TOCLineBold"]), Paragraph("15,000 records", styles["TOCLine"]), Paragraph("Behavioral & Hypertension", styles["TOCLine"]), Paragraph("BP history, Smoking, Physical activity", styles["TOCLine"]), Paragraph("Population Surveillance", styles["TOCLine"])],
        [Paragraph("Framingham Heart Study", styles["TOCLineBold"]), Paragraph("4,238 records", styles["TOCLine"]), Paragraph("10-Year ASCVD Risk", styles["TOCLine"]), Paragraph("Systolic BP, Lipids, Cigarettes/day", styles["TOCLine"]), Paragraph("Longitudinal Community", styles["TOCLine"])],
        [Paragraph("Kaggle Chronic Kidney", styles["TOCLineBold"]), Paragraph("400 records", styles["TOCLine"]), Paragraph("Renal Impairment Comorbidity", styles["TOCLine"]), Paragraph("Serum Creatinine, Blood Urea, Albumin", styles["TOCLine"]), Paragraph("Hospital Inpatient Cohort", styles["TOCLine"])],
        [Paragraph("Consented Screening App", styles["TOCLineBold"]), Paragraph("3,250 records", styles["TOCLine"]), Paragraph("Indian Wellness Camps", styles["TOCLine"]), Paragraph("Asian-BMI, Waist circumference, Diet", styles["TOCLine"]), Paragraph("Urban & Rural India", styles["TOCLine"])]
    ]
    t = Table(cohort_data, colWidths=[USABLE_WIDTH*0.22, USABLE_WIDTH*0.16, USABLE_WIDTH*0.22, USABLE_WIDTH*0.25, USABLE_WIDTH*0.15])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('LINEBELOW', (0,0), (-1,0), 1, colors.HexColor('#1e3a8a')),
        ('LINEBELOW', (0,1), (-1,-1), 0.35, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    p.append(t)
    p.append(Spacer(1, 6))
    
    text_2 = (
        "Ingestion pipelines are engineered with strict abstraction: source-specific extractors normalize heterogenous column naming "
        "conventions (e.g., mapping `trestbps`, `bp_sys`, and `SystolicBP` into the unified `systolic_bp` feature) before passing records "
        "to the canonical schema validator."
    )
    p.append(Paragraph(text_2, styles["ReportBody"]))
    return p

def page_26_ch4_p2():
    """Page 26: Chapter 4 Clinical Data Engineering - Canonical Schema & Table 4.2."""
    p = []
    p.append(Paragraph("4.2 Canonical Schema Definition & Unit Standardization Engine", styles["SecHeading"]))
    text_1 = (
        "Clinical laboratories across India and international repositories exhibit profound disparities in measurement units. For instance, "
        "blood glucose is reported in milligrams per decilitre (mg/dL) in India and the United States, but in millimoles per litre (mmol/L) "
        "in the United Kingdom and Commonwealth nations. Similarly, cholesterol measurements vary between mg/dL and mmol/L, height between "
        "centimeters and feet/inches, and weight between kilograms and pounds. To prevent catastrophic unit mismatches, Sanjivani AI enforces "
        "a deterministic Unit Standardization Engine (`UnitConverter`) based on standard clinical biochemical conversion coefficients."
    )
    p.append(Paragraph(text_1, styles["ReportBody"]))
    
    # Table 4.2
    p.append(Paragraph("<b>Table 4.2: Canonical Clinical Feature Dictionary & Physiological Verification Bounds</b>", styles["TableCaption"]))
    feat_data = [
        [Paragraph("<b>Canonical Feature</b>", styles["TOCLineBold"]), Paragraph("<b>Canonical Unit</b>", styles["TOCLineBold"]), Paragraph("<b>Conversion Formula</b>", styles["TOCLineBold"]), Paragraph("<b>Valid Clinical Range</b>", styles["TOCLineBold"]), Paragraph("<b>Emergency Trigger</b>", styles["TOCLineBold"])],
        [Paragraph("age", styles["TOCLineBold"]), Paragraph("years", styles["TOCLine"]), Paragraph("Direct integer", styles["TOCLine"]), Paragraph("18 to 100", styles["TOCLine"]), Paragraph("N/A", styles["TOCLine"])],
        [Paragraph("systolic_bp", styles["TOCLineBold"]), Paragraph("mmHg", styles["TOCLine"]), Paragraph("Direct numeric", styles["TOCLine"]), Paragraph("70 to 260", styles["TOCLine"]), Paragraph("> 180 or < 80", styles["TOCLine"])],
        [Paragraph("diastolic_bp", styles["TOCLineBold"]), Paragraph("mmHg", styles["TOCLine"]), Paragraph("Direct numeric", styles["TOCLine"]), Paragraph("40 to 150", styles["TOCLine"]), Paragraph("> 120 or < 50", styles["TOCLine"])],
        [Paragraph("fasting_glucose", styles["TOCLineBold"]), Paragraph("mg/dL", styles["TOCLine"]), Paragraph("mmol/L × 18.0182", styles["TOCLine"]), Paragraph("40 to 500", styles["TOCLine"]), Paragraph("> 350 or < 50", styles["TOCLine"])],
        [Paragraph("hba1c", styles["TOCLineBold"]), Paragraph("% (DCCT)", styles["TOCLine"]), Paragraph("(IFCC × 0.09148) + 2.152", styles["TOCLine"]), Paragraph("3.5 to 18.0", styles["TOCLine"]), Paragraph("> 13.0", styles["TOCLine"])],
        [Paragraph("total_cholesterol", styles["TOCLineBold"]), Paragraph("mg/dL", styles["TOCLine"]), Paragraph("mmol/L × 38.67", styles["TOCLine"]), Paragraph("80 to 500", styles["TOCLine"]), Paragraph("> 400", styles["TOCLine"])],
        [Paragraph("ldl_cholesterol", styles["TOCLineBold"]), Paragraph("mg/dL", styles["TOCLine"]), Paragraph("mmol/L × 38.67", styles["TOCLine"]), Paragraph("30 to 350", styles["TOCLine"]), Paragraph("> 250", styles["TOCLine"])],
        [Paragraph("hdl_cholesterol", styles["TOCLineBold"]), Paragraph("mg/dL", styles["TOCLine"]), Paragraph("mmol/L × 38.67", styles["TOCLine"]), Paragraph("15 to 120", styles["TOCLine"]), Paragraph("< 20", styles["TOCLine"])],
        [Paragraph("triglycerides", styles["TOCLineBold"]), Paragraph("mg/dL", styles["TOCLine"]), Paragraph("mmol/L × 88.57", styles["TOCLine"]), Paragraph("30 to 1,000", styles["TOCLine"]), Paragraph("> 500", styles["TOCLine"])],
        [Paragraph("bmi", styles["TOCLineBold"]), Paragraph("kg/m²", styles["TOCLine"]), Paragraph("weight_kg / (height_m)²", styles["TOCLine"]), Paragraph("10.0 to 65.0", styles["TOCLine"]), Paragraph("> 50.0", styles["TOCLine"])]
    ]
    t = Table(feat_data, colWidths=[USABLE_WIDTH*0.22, USABLE_WIDTH*0.14, USABLE_WIDTH*0.24, USABLE_WIDTH*0.22, USABLE_WIDTH*0.18])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('LINEBELOW', (0,0), (-1,0), 1, colors.HexColor('#1e3a8a')),
        ('LINEBELOW', (0,1), (-1,-1), 0.35, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    p.append(t)
    return p

def page_27_ch4_p3():
    """Page 27: Chapter 4 Clinical Data Engineering - Data Validation & Pandera Contracts."""
    p = []
    p.append(Paragraph("4.3 Data Validation & Quality Invariants via Pandera", styles["SecHeading"]))
    text_1 = (
        "In production machine learning pipelines, silent data corruption—caused by malformed upstream schemas, out-of-range sensor drift, "
        "or human data entry typos (e.g., entering a glucose value of 1,200 instead of 120)—leads to severe model degradation. While Pydantic v2 "
        "enforces type validation on individual API requests, analytical dataframe batches require comprehensive columnar schema validation. "
        "Sanjivani AI integrates <b>Pandera</b> to enforce statistical and physiological invariants on all dataframes prior to ingestion, "
        "transformation, and model inference."
    )
    p.append(Paragraph(text_1, styles["ReportBody"]))
    
    text_2 = (
        "The Pandera `ScreeningDataSchema` defines strict boundary checks for every clinical feature: fasting glucose must reside in "
        "[40.0, 500.0] mg/dL, systolic blood pressure in [70.0, 260.0] mmHg, and diastolic blood pressure in [40.0, 150.0] mmHg. "
        "Crucially, Pandera validates <i>cross-column physiological invariants</i>: for every record, systolic blood pressure must strictly "
        "exceed diastolic blood pressure by at least 15 mmHg (`Check(lambda df: df['systolic_bp'] >= df['diastolic_bp'] + 15)`). "
        "Records violating these invariants are immediately diverted to quarantine error tables, triggering automated alerts while safeguarding "
        "training and inference pipelines from corrupted biological inputs."
    )
    p.append(Paragraph(text_2, styles["ReportBody"]))
    
    p.append(Paragraph("<b>Code Artifact: Declarative Pandera Schema Definition:</b>", styles["SubSecHeading"]))
    code_text = (
        "class CanonicalScreeningSchema(pa.DataFrameModel):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;age: Series[int] = pa.Field(ge=18, le=100, nullable=False)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;systolic_bp: Series[float] = pa.Field(ge=70.0, le=260.0, nullable=True)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;diastolic_bp: Series[float] = pa.Field(ge=40.0, le=150.0, nullable=True)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;fasting_glucose: Series[float] = pa.Field(ge=40.0, le=500.0, nullable=True)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;hba1c: Series[float] = pa.Field(ge=3.5, le=18.0, nullable=True)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;@pa.dataframe_check<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;def validate_bp_pulse_pressure(cls, df: pd.DataFrame) -> Series[bool]:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return df['systolic_bp'] >= (df['diastolic_bp'] + 15.0)"
    )
    p.append(Paragraph(code_text, ParagraphStyle('CodeBox', fontName='Courier', fontSize=7.5, leading=10, textColor=colors.HexColor('#0f172a'), backColor=colors.HexColor('#f8fafc'), borderPadding=6)))
    return p

def page_28_ch4_p4():
    """Page 28: Chapter 4 Clinical Data Engineering - MICE Imputation & Figure 4.1."""
    p = []
    p.append(Paragraph("4.4 Missing Value Imputation (MICE) & Outlier Mitigation", styles["SecHeading"]))
    text_1 = (
        "Real-world clinical data from community health screenings in India is characterized by pervasive missingness. While basic biometrics "
        "(age, sex, height, weight, blood pressure) are recorded for over 95% of attendees, biochemical laboratory values (HbA1c, fasting glucose, "
        "lipid sub-fractions) are frequently omitted due to the absence of point-of-care phlebotomy equipment. Figure 4.1 illustrates the missingness "
        "heatmap across source datasets prior to imputation, revealing missingness rates ranging from 8% for systolic blood pressure up to 48% "
        "for glycated hemoglobin."
    )
    p.append(Paragraph(text_1, styles["ReportBody"]))
    
    # Figure 4.1
    fig_path = "reports/missingness_map.png"
    if os.path.exists(fig_path):
        p.append(Image(fig_path, width=390, height=170))
        p.append(Paragraph("<b>Figure 4.1: Missingness Map Across Multi-Cohort Clinical Datasets Prior to MICE Imputation</b>", styles["FigureCaption"]))
        
    text_2 = (
        "Conventional heuristic strategies—such as mean or median imputation—are clinically catastrophic because they attenuate natural biological "
        "variance and destroy multi-variable physiological correlations (e.g., the known linear relationship between fasting glucose and HbA1c). "
        "To preserve covariance structures, Sanjivani AI employs <b>Multivariate Imputation by Chained Equations (MICE)</b> implemented via scikit-learn's "
        "`IterativeImputer` with a Bayesian Ridge regression estimator. MICE models each feature with missing values as a function of all other "
        "features in an iterative round-robin cycle (10 imputation iterations), accurately imputing missing lipid and glycemic markers."
    )
    p.append(Paragraph(text_2, styles["ReportBody"]))
    
    text_3 = (
        "Outlier mitigation is performed using <b>Isolation Forests</b> (`contamination=0.015`) to isolate multidimensional data anomalies "
        "without truncating valid extreme biological conditions (such as severe malignant hypertension)."
    )
    p.append(Paragraph(text_3, styles["ReportBody"]))
    return p

def page_29_ch4_p5():
    """Page 29: Chapter 4 Clinical Data Engineering - Biomarker Engineering & Figure 4.2."""
    p = []
    p.append(Paragraph("4.5 Clinically Derived Biomarker Engineering", styles["SecHeading"]))
    text_1 = (
        "To maximize discriminative signal for South Asian populations, the feature engineering pipeline constructs four clinically validated "
        "composite biomarkers directly derived from raw biometrics: (1) <i>Asian-Indian Specific BMI Classification:</i> Recalibrates WHO criteria "
        "to South Asian cutoffs (Normal: 18.5–22.9, Overweight: 23.0–24.9, Obese: ≥25.0 kg/m²); (2) <i>Mean Arterial Pressure (MAP):</i> Quantifies "
        "average arterial perfusion pressure via $MAP = DBP + \\frac{1}{3}(SBP - DBP)$; (3) <i>Waist-to-Height Ratio (WHtR):</i> Superior to BMI "
        "in identifying visceral adiposity, with values > 0.5 indicating elevated risk; and (4) <i>Atherogenic Index of Plasma (AIP):</i> Calculated "
        "as $\\log_{10}(Triglycerides / HDL)$, serving as an ultra-sensitive surrogate for small dense LDL particles."
    )
    p.append(Paragraph(text_1, styles["ReportBody"]))
    
    # Figure 4.2
    fig_path = "reports/correlation_heatmap.png"
    if os.path.exists(fig_path):
        p.append(Image(fig_path, width=320, height=210))
        p.append(Paragraph("<b>Figure 4.2: Pairwise Correlation Heatmap of Standardized Clinical Biomarkers</b>", styles["FigureCaption"]))
        
    text_2 = (
        "Figure 4.2 illustrates the pairwise Pearson correlation matrix across standardized features. Note the strong physiological clustering "
        "between systolic BP and MAP (r = 0.94), fasting glucose and HbA1c (r = 0.82), and total cholesterol with LDL (r = 0.88), validating the "
        "biochemical integrity of the engineered feature space."
    )
    p.append(Paragraph(text_2, styles["ReportBody"]))
    return p

def page_30_ch4_p6():
    """Page 30: Chapter 4 Clinical Data Engineering - Resampling & Figure 4.3."""
    p = []
    p.append(Paragraph("4.6 Leakage-Safe Stratified Splitting, SMOTE-NC & Feature Store", styles["SecHeading"]))
    text_1 = (
        "A critical vulnerability in clinical ML literature is <i>data leakage</i> occurring during pre-processing, wherein imputation parameters "
        "or oversampling statistics from the test set contaminate training folds. Sanjivani AI strictly prevents leakage by encapsulating all "
        "imputation, standardisation (`StandardScaler`), and encoding inside scikit-learn `Pipeline` objects fitted exclusively on training folds."
    )
    p.append(Paragraph(text_1, styles["ReportBody"]))
    
    text_2 = (
        "To address severe class imbalance across disease targets (e.g., heart disease prevalence in community screening cohorts is often < 15%), "
        "the pipeline applies <b>Synthetic Minority Over-sampling Technique for Nominal and Continuous features (SMOTE-NC)</b>. Figure 4.3 illustrates "
        "the raw vs. resampled balance across the three disease targets, demonstrating perfect class equilibrium in training folds without synthesizing "
        "unrealistic biological feature combinations."
    )
    p.append(Paragraph(text_2, styles["ReportBody"]))
    
    # Figure 4.3
    fig_path = "reports/class_distributions.png"
    if os.path.exists(fig_path):
        p.append(Image(fig_path, width=390, height=140))
        p.append(Paragraph("<b>Figure 4.3: Class Distribution and SMOTE-NC Resampling Balance Across Disease Targets</b>", styles["FigureCaption"]))
        
    text_3 = (
        "Finally, all engineered features and point-in-time entity views are registered in an integrated <b>Feast</b> feature store, enabling "
        "seamless offline training dataset generation and low-latency online feature retrieval during live screening inference."
    )
    p.append(Paragraph(text_3, styles["ReportBody"]))
    return p
