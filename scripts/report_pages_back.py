"""
Back matter pages (Pages 71 to 74) for the expanded CGC Project Report.
Pages 71-72: References
Page 73: Appendix A: Canonical Schemas & API Specifications
Page 74: Appendix B: Mathematical Formulations & Hyperparameter Bounds
"""

import os
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle

from report_styles import USABLE_WIDTH, USABLE_HEIGHT, get_report_styles

styles = get_report_styles()

def page_71_ref_p1():
    """Page 71: References - Part 1 (References 1 to 18)."""
    p = []
    p.append(Paragraph("REFERENCES", styles["ChapterHeading"]))
    p.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=10))
    
    refs = [
        "[1] Anjana, R. M., et al. (2023). Metabolic non-communicable disease health report in India: The ICMR-INDIAB national cross-sectional study. <i>The Lancet Diabetes & Endocrinology</i>, 11(7), 474-489.",
        "[2] Mohan, V., et al. (2005). A simplified Indian Diabetes Risk Score (IDRS) for screening for undiagnosed diabetic subjects in South Asia. <i>Journal of the Association of Physicians of India</i>, 53(9), 759-763.",
        "[3] World Health Organization. (2020). <i>WHO Package of Essential Noncommunicable (WHO-PEN) Disease Interventions for Primary Health Care</i>. World Health Organization, Geneva.",
        "[4] D'Agostino, R. B., et al. (2008). General cardiovascular risk profile for use in primary care: The Framingham Heart Study. <i>Circulation</i>, 117(6), 743-753.",
        "[5] Lundberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions. <i>Advances in Neural Information Processing Systems (NeurIPS 2017)</i>, 30, 4765-4774.",
        "[6] Lundberg, S. M., et al. (2020). From local explanations to global understanding with explainable AI for trees. <i>Nature Machine Intelligence</i>, 2(1), 56-67.",
        "[7] Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. <i>ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD '16)</i>, 785-794.",
        "[8] Ke, G., et al. (2017). LightGBM: A highly efficient gradient boosting decision tree. <i>Advances in Neural Information Processing Systems (NeurIPS 2017)</i>, 30, 3146-3154.",
        "[9] Prokhorenkova, L., et al. (2018). CatBoost: Unbiased boosting with categorical features. <i>Advances in Neural Information Processing Systems (NeurIPS 2018)</i>, 31, 6638-6648.",
        "[10] Breiman, L. (2001). Random Forests. <i>Machine Learning</i>, 45(1), 5-32.",
        "[11] Wolpert, D. H. (1992). Stacked generalization. <i>Neural Networks</i>, 5(2), 241-259.",
        "[12] Platt, J. (1999). Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. <i>Advances in Large Margin Classifiers</i>, 10(3), 61-74.",
        "[13] Niculescu-Mizil, A., & Caruana, R. (2005). Predicting good probabilities with supervised learning. <i>International Conference on Machine Learning (ICML '05)</i>, 625-632.",
        "[14] Vovk, V., Gammerman, A., & Shafer, G. (2005). <i>Algorithmic Learning in a Random World</i>. Springer Science & Business Media, New York.",
        "[15] Angelopoulos, A. N., & Bates, S. (2021). A gentle introduction to conformal prediction and distribution-free uncertainty quantification. <i>arXiv preprint arXiv:2107.07511</i>.",
        "[16] Koenker, R., & Bassett, G. (1978). Regression quantiles. <i>Econometrica: Journal of the Econometric Society</i>, 33-50.",
        "[17] Ministry of Law and Justice, Government of India. (2023). <i>The Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023)</i>. The Gazette of India, New Delhi.",
        "[18] Indian Council of Medical Research (ICMR). (2023). <i>Guidelines for Management of Type 2 Diabetes in India</i>. ICMR, Department of Health Research, Ministry of Health and Family Welfare, New Delhi."
    ]
    for r in refs:
        p.append(Paragraph(r, styles["RefLine"]))
    return p

def page_72_ref_p2():
    """Page 72: References - Part 2 (References 19 to 36)."""
    p = []
    p.append(Paragraph("REFERENCES (CONTD.)", styles["ChapterHeading"]))
    p.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=10))
    
    refs = [
        "[19] Indian Council of Medical Research (ICMR). (2022). <i>Standard Treatment Workflows for Management of Hypertension</i>. ICMR, New Delhi.",
        "[20] Misra, A., et al. (2009). Consensus physical activity guidelines for Asian Indians. <i>Diabetes Technology & Therapeutics</i>, 11(12), 799-807.",
        "[21] Chobanian, A. V., et al. (2003). Seventh report of the Joint National Committee on prevention, detection, evaluation, and treatment of high blood pressure (JNC 7). <i>Hypertension</i>, 42(6), 1206-1252.",
        "[22] American Diabetes Association (ADA). (2024). Standards of care in diabetes—2024. <i>Diabetes Care</i>, 47(Suppl. 1), S1-S343.",
        "[23] Akiba, T., et al. (2019). Optuna: A next-generation hyperparameter optimization framework. <i>ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD '19)</i>, 2623-2631.",
        "[24] Chawla, N. V., et al. (2002). SMOTE: Synthetic minority over-sampling technique. <i>Journal of Artificial Intelligence Research</i>, 16, 321-357.",
        "[25] Buuren, S. V., & Groothuis-Oudshoorn, K. (2011). MICE: Multivariate imputation by chained equations in R. <i>Journal of Statistical Software</i>, 45, 1-67.",
        "[26] Liu, F. T., Ting, K. M., & Zhou, Z. H. (2008). Isolation forest. <i>IEEE International Conference on Data Mining (ICDM '08)</i>, 413-422.",
        "[27] Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. <i>Journal of Machine Learning Research</i>, 12, 2825-2830.",
        "[28] Tiangolo, S. (2023). FastAPI: High performance, easy to learn, fast to code, ready for production. <i>GitHub Repository</i>: https://github.com/tiangolo/fastapi.",
        "[29] National Health Authority (NHA), Government of India. (2022). <i>Ayushman Bharat Digital Mission (ABDM) Architecture Strategy</i>. Ministry of Health & Family Welfare, New Delhi.",
        "[30] World Wide Web Consortium (W3C). (2018). <i>Web Content Accessibility Guidelines (WCAG) 2.1</i>. W3C Recommendation.",
        "[31] Bird, S., et al. (2020). Fairlearn: A toolkit for assessing and improving fairness in AI. <i>Microsoft Technical Report MSR-TR-2020-32</i>.",
        "[32] Dobler, G., et al. (2021). Evidently: Open-source machine learning monitoring. <i>GitHub Repository</i>: https://github.com/evidentlyai/evidently.",
        "[33] Vercel. (2023). Next.js 14 Documentation and App Router Architecture. <i>Vercel Inc.</i>: https://nextjs.org/docs.",
        "[34] Dwork, C., et al. (2012). Fairness through awareness. <i>Innovations in Theoretical Computer Science Conference (ITCS '12)</i>, 214-226.",
        "[35] Hardt, M., Price, E., & Srebro, N. (2016). Equality of opportunity in supervised learning. <i>Advances in Neural Information Processing Systems (NeurIPS 2016)</i>, 29, 3315-3323.",
        "[36] Topol, E. J. (2019). High-performance medicine: The convergence of human and artificial intelligence. <i>Nature Medicine</i>, 25(1), 44-56."
    ]
    for r in refs:
        p.append(Paragraph(r, styles["RefLine"]))
    return p

def page_73_app_p1():
    """Page 73: Appendix A: Canonical Schemas & API Endpoints."""
    p = []
    p.append(Paragraph("APPENDIX A", styles["ChapterHeading"]))
    p.append(Paragraph("CANONICAL SCHEMAS & REST API SPECIFICATIONS", styles["ChapterHeading"]))
    p.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=10))
    
    p.append(Paragraph("A.1 Canonical Biomarker Pydantic v2 Schema Specification", styles["SecHeading"]))
    schema_code = (
        "class CanonicalBiomarkerInput(BaseModel):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;age: int = Field(..., ge=18, le=100, description='Age of patient in complete years')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;gender: Literal['male', 'female', 'other'] = Field(..., description='Biological sex')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;height_cm: float = Field(..., ge=100.0, le=250.0, description='Standing height in cm')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;weight_kg: float = Field(..., ge=25.0, le=250.0, description='Body mass in kg')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;waist_circumference_cm: Optional[float] = Field(None, ge=40.0, le=180.0)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;systolic_bp: float = Field(..., ge=70.0, le=260.0, description='Systolic BP in mmHg')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;diastolic_bp: float = Field(..., ge=40.0, le=150.0, description='Diastolic BP in mmHg')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;resting_heart_rate: Optional[int] = Field(None, ge=40, le=200)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;fasting_glucose: Optional[float] = Field(None, ge=40.0, le=500.0, description='FBS in mg/dL')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;hba1c: Optional[float] = Field(None, ge=3.5, le=18.0, description='Glycated Hb %')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;total_cholesterol: Optional[float] = Field(None, ge=80.0, le=500.0, description='mg/dL')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;ldl_cholesterol: Optional[float] = Field(None, ge=30.0, le=350.0, description='mg/dL')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;hdl_cholesterol: Optional[float] = Field(None, ge=15.0, le=120.0, description='mg/dL')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;triglycerides: Optional[float] = Field(None, ge=30.0, le=1000.0, description='mg/dL')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;physical_activity_hours: float = Field(0.0, ge=0.0, le=50.0)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;smoking_status: Literal['never', 'former', 'current'] = Field('never')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;alcohol_consumption: Literal['none', 'occasional', 'regular'] = Field('none')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;diet_type: Literal['vegetarian', 'non_vegetarian', 'vegan'] = Field('vegetarian')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;family_history_diabetes: bool = Field(False)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;family_history_heart_disease: bool = Field(False)"
    )
    p.append(Paragraph(schema_code, ParagraphStyle('CodeBox', fontName='Courier', fontSize=7.2, leading=9.5, textColor=colors.HexColor('#0f172a'), backColor=colors.HexColor('#f8fafc'), borderPadding=5)))
    p.append(Spacer(1, 8))
    
    p.append(Paragraph("A.2 Screening Response JSON Schema Specification", styles["SecHeading"]))
    resp_code = (
        "class ScreeningOutputResponse(BaseModel):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;screening_id: UUID = Field(...)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;timestamp: datetime = Field(...)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;risk_scores: Dict[str, float] = Field(..., description='Calibrated probabilities [0, 1]')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;risk_tiers: Dict[str, Literal['low', 'moderate', 'elevated']] = Field(...)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;conformal_bands: Dict[str, Tuple[float, float]] = Field(..., description='90% coverage')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;phenotype_cluster: int = Field(..., description='K-Means Archetype 0-3')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;top_driving_factors: List[SHAPFactor] = Field(...)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;plain_language_narrative: Dict[str, str] = Field(..., description='En/Hi/Pa text')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;emergency_red_flag_triggered: bool = Field(False)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;statutory_disclaimer: str = Field('Screening support, not a clinical diagnosis.')"
    )
    p.append(Paragraph(resp_code, ParagraphStyle('CodeBox', fontName='Courier', fontSize=7.2, leading=9.5, textColor=colors.HexColor('#0f172a'), backColor=colors.HexColor('#f8fafc'), borderPadding=5)))
    return p

def page_74_app_p2():
    """Page 74: Appendix B: Mathematical Formulations & Hyperparameters."""
    p = []
    p.append(Paragraph("APPENDIX B", styles["ChapterHeading"]))
    p.append(Paragraph("MATHEMATICAL FORMULATIONS & OPTUNA SPACES", styles["ChapterHeading"]))
    p.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=10))
    
    p.append(Paragraph("B.1 Stacking Ensemble Meta-Learner Optimization", styles["SecHeading"]))
    text_1 = (
        "Let $\\mathcal{M} = \\{m_1, m_2, \\dots, m_K\\}$ denote the set of $K=6$ base classifiers. In $J$-fold cross-validation, for each fold "
        "$j \\in \\{1, \\dots, J\\}$, base models are trained on $\\mathcal{D} \\setminus \\mathcal{D}_j$ to generate out-of-fold probability vectors "
        "$\\hat{\\mathbf{p}}_k(\\mathbf{x}_i)$. The meta-feature matrix $\\mathbf{Z} \\in \\mathbb{R}^{N \\times K}$ is constructed as "
        "$Z_{i,k} = \\hat{p}_k(\\mathbf{x}_i)$. The Level-1 Logistic Regression meta-learner minimizes:<br/>"
        "$$\\min_{\\mathbf{w}, b} \\sum_{i=1}^N \\log\\left( 1 + \\exp(-y_i (\\mathbf{w}^T \\mathbf{z}_i + b)) \\right) + \\frac{1}{2C} ||\\mathbf{w}||_2^2$$"
    )
    p.append(Paragraph(text_1, styles["ReportBody"]))
    
    p.append(Paragraph("B.2 Multi-Horizon Pinball Quantile Loss Formulation", styles["SecHeading"]))
    text_2 = (
        "For multi-horizon biometric forecasting across quantiles $q \\in \\{0.10, 0.50, 0.90\\}$, the pinball loss objective function is given by:<br/>"
        "$$\\mathcal{L}_q(y, \\hat{y}) = \\frac{1}{N} \\sum_{i=1}^N \\max\\left( q (y_i - \\hat{y}_i), (q - 1)(y_i - \\hat{y}_i) \\right)$$"
    )
    p.append(Paragraph(text_2, styles["FormulaBox"]))
    
    p.append(Paragraph("B.3 Conformal Prediction Non-Conformity Measure", styles["SecHeading"]))
    text_3 = (
        "Given calibration dataset $\\mathcal{D}_{\\text{cal}} = \\{(\\mathbf{x}_i, y_i)\\}_{i=1}^n$ and point predictor $\\hat{\\mu}$, the absolute residual "
        "non-conformity scores are defined as $s_i = |y_i - \\hat{\\mu}(\\mathbf{x}_i)|$. The conformal threshold is calculated as:<br/>"
        "$$\\hat{q}_{1-\\alpha} = \\text{Quantile}\\left( s_1, \\dots, s_n; \\; \\frac{\\lceil (n+1)(1-\\alpha) \\rceil}{n} \\right)$$"
    )
    p.append(Paragraph(text_3, styles["FormulaBox"]))
    
    p.append(Paragraph("B.4 Final Optuna Best Parameter Configurations", styles["SecHeading"]))
    text_4 = (
        "• <b>XGBoost Classifier:</b> `max_depth`: 5, `learning_rate`: 0.042, `n_estimators`: 240, `subsample`: 0.82, `colsample_bytree`: 0.74, `gamma`: 0.15, `reg_alpha`: 0.25, `reg_lambda`: 1.40.<br/>"
        "• <b>LightGBM Classifier:</b> `num_leaves`: 31, `learning_rate`: 0.038, `n_estimators`: 280, `min_child_samples`: 28, `subsample`: 0.85, `colsample_bytree`: 0.78.<br/>"
        "• <b>CatBoost Classifier:</b> `depth`: 6, `learning_rate`: 0.045, `iterations`: 300, `l2_leaf_reg`: 4.85, `border_count`: 64.<br/>"
        "• <b>Random Forest Classifier:</b> `n_estimators`: 200, `max_depth`: 12, `min_samples_split`: 5, `min_samples_leaf`: 2, `max_features`: 'sqrt'.<br/>"
        "• <b>Support Vector Machine (RBF):</b> `C`: 1.42, `gamma`: 0.038, `probability`: True."
    )
    p.append(Paragraph(text_4, styles["ReportBody"]))
    return p
