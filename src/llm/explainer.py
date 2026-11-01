"""Multilingual explanation generator producing Class 8 reading level guidance in English, Hindi, and Punjabi."""

from src.schemas.screening import (
    ConditionRiskResult,
    MultilingualExplanation,
    RiskLevel,
    ScreeningInput,
    ShapFactor,
)


def generate_multilingual_explanation(
    patient_input: ScreeningInput,
    conditions: dict[str, ConditionRiskResult],
    top_shap_factors: list[ShapFactor],
) -> dict[str, MultilingualExplanation]:
    """Produce plain-language, culturally tailored explanations at Class 8 reading level.

    Provides identical clinical intent rendered natively in English, Hindi (हिन्दी), and Punjabi (ਪੰਜਾਬੀ).
    """
    # Identify primary elevated condition
    primary_cond = max(conditions.values(), key=lambda c: c.calibrated_probability)
    is_high_risk = primary_cond.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]

    # Extract top 2 contributing factors for plain-language mention
    top_factor_names = [f.feature_name_friendly for f in top_shap_factors[:2]]
    factor_str_en = ", ".join(top_factor_names) if top_factor_names else "overall lifestyle markers"

    # ==========================
    # 1. ENGLISH (Class 8 Level)
    # ==========================
    en_headline = (
        f"Your Health Screening Summary: {primary_cond.risk_level.value} Risk for {primary_cond.condition_name}"
        if is_high_risk
        else f"Your Health Screening Summary: Moderate or Manageable Risk for {primary_cond.condition_name}"
    )

    en_overview = (
        f"This screening shows your risk for {primary_cond.condition_name} is currently in the {primary_cond.risk_level.value} category. "
        f"This is not a medical diagnosis, but an early warning sign. "
        f"The two main factors influencing this score right now are {factor_str_en}. "
        "With simple, daily lifestyle steps, your body can heal and risk can be significantly lowered."
    )

    en_factors = [
        f"• {f.feature_name_friendly}: Current value is {f.patient_value}. {f.actionable_advice}"
        for f in top_shap_factors[:3]
    ]

    en_actions = [
        "Walk briskly for 30 minutes every day (aim for 5 days a week).",
        "Replace white rice and refined flour with whole grains like jowar, bajra, and oats.",
        "Cut down on sugary tea, sweets, and packaged fried snacks.",
        "Schedule an in-person routine health check with a doctor to discuss these numbers.",
    ]

    en_exp = MultilingualExplanation(
        language="en",
        language_name="English",
        headline=en_headline,
        summary_overview=en_overview,
        top_factors_plain_text=en_factors,
        actionable_steps=en_actions,
        reading_level="Class 8",
    )

    # ==========================
    # 2. HINDI (हिन्दी - कक्षा ८ स्तर)
    # ==========================
    hi_headline = (
        f"आपकी स्वास्थ्य जांच रिपोर्ट: {primary_cond.condition_name} के लिए {primary_cond.risk_level.value} जोखिम"
        if is_high_risk
        else f"आपकी स्वास्थ्य जांच रिपोर्ट: {primary_cond.condition_name} के लिए सामान्य/नियंत्रित स्थिति"
    )

    hi_overview = (
        f"इस जांच से पता चलता है कि {primary_cond.condition_name} की संभावना {primary_cond.risk_level.value} स्तर पर है। "
        "यह कोई बीमारी का पक्का फैसला (निदान) नहीं है, बल्कि समय रहते संभलने का एक संकेत है। "
        "आपके शरीर के मुख्य कारण खान-पान, वजन और दैनिक शारीरिक गतिविधि से जुड़े हैं। "
        "अच्छी खबर यह है कि सही आदतों से इस जोखिम को काफी कम किया जा सकता है।"
    )

    hi_factors = [
        f"• {f.feature_name_friendly}: आपका स्तर {f.patient_value} है। {f.actionable_advice}"
        for f in top_shap_factors[:3]
    ]

    hi_actions = [
        "हर दिन कम से कम ३० मिनट तेज कदमों से टहलें (सप्ताह में ५ दिन)।",
        "सफेद चावल और मैदा कम करें, भोजन में ज्वार, बाजरा, रागी और हरी सब्जियां शामिल करें।",
        "मीठी चाय, कोल्ड ड्रिंक्स और तली-भुनी चीजों से परहेज करें।",
        "नजदीकी डॉक्टर से मिलकर इन जांच रिपोर्टों पर सलाह लें।",
    ]

    hi_exp = MultilingualExplanation(
        language="hi",
        language_name="हिन्दी (Hindi)",
        headline=hi_headline,
        summary_overview=hi_overview,
        top_factors_plain_text=hi_factors,
        actionable_steps=hi_actions,
        reading_level="Class 8",
    )

    # ==========================
    # 3. PUNJABI (ਪੰਜਾਬੀ - ਅੱਠਵੀਂ ਜਮਾਤ ਦਾ ਪੱਧਰ)
    # ==========================
    pa_headline = (
        f"ਤੁਹਾਡੀ ਸਿਹਤ ਜਾਂਚ ਰਿਪੋਰਟ: {primary_cond.condition_name} ਲਈ {primary_cond.risk_level.value} ਖ਼ਤਰਾ"
        if is_high_risk
        else f"ਤੁਹਾਡੀ ਸਿਹਤ ਜਾਂਚ ਰਿਪੋਰਟ: {primary_cond.condition_name} ਲਈ ਆਮ/ਕਾਬੂ ਹੇਠ ਸਥਿਤੀ"
    )

    pa_overview = (
        f"ਇਸ ਸਕ੍ਰੀਨਿੰਗ ਤੋਂ ਪਤਾ ਲੱਗਦਾ ਹੈ ਕਿ {primary_cond.condition_name} ਦਾ ਖ਼ਤਰਾ ਇਸ ਸਮੇਂ {primary_cond.risk_level.value} ਸ਼੍ਰੇਣੀ ਵਿੱਚ ਹੈ। "
        "ਇਹ ਕੋਈ ਡਾਕਟਰੀ ਫੈਸਲਾ ਜਾਂ ਬਿਮਾਰੀ ਦਾ ਪੱਕਾ ਐਲਾਨ ਨਹੀਂ ਹੈ, ਸਗੋਂ ਸਮੇਂ ਸਿਰ ਧਿਆਨ ਦੇਣ ਦੀ ਚੇਤਾਵਨੀ ਹੈ। "
        "ਤੁਹਾਡੀ ਰੋਜ਼ਾਨਾ ਕਸਰਤ, ਭੋਜਨ ਅਤੇ ਭਾਰ ਇਸ ਨਤੀਜੇ ਨੂੰ ਬਹੁਤ ਪ੍ਰਭਾਵਿਤ ਕਰਦੇ ਹਨ। "
        "ਸਹੀ ਜੀਵਨ ਸ਼ੈਲੀ ਨਾਲ ਤੁਸੀਂ ਆਪਣੇ ਸਰੀਰ ਨੂੰ ਤੰਦਰੁਸਤ ਰੱਖ ਸਕਦੇ ਹੋ।"
    )

    pa_factors = [
        f"• {f.feature_name_friendly}: ਤੁਹਾਡਾ ਅੰਕੜਾ {f.patient_value} ਹੈ। {f.actionable_advice}"
        for f in top_shap_factors[:3]
    ]

    pa_actions = [
        "ਹਰ ਰੋਜ਼ ਘੱਟੋ-ਘੱਟ 30 ਮਿੰਟ ਤੇਜ਼ ਸੈਰ ਕਰੋ (ਹਫ਼ਤੇ ਵਿੱਚ 5 ਦਿਨ)।",
        "ਰੋਟੀ ਵਿੱਚ ਮੋਟਾ ਅਨਾਜ ਜਿਵੇਂ ਜਵਾਰ, ਬਾਜਰਾ ਅਤੇ ਮੱਕੀ ਸ਼ਾਮਲ ਕਰੋ ਅਤੇ ਮੈਦਾ ਬੰਦ ਕਰੋ।",
        "ਮਿੱਠੀ ਚਾਹ, ਗੁੜ-ਸ਼ੱਕਰ ਅਤੇ ਤਲੀਆਂ ਚੀਜ਼ਾਂ ਤੋਂ ਪਰਹੇਜ਼ ਰੱਖੋ।",
        "ਕਿਸੇ ਯੋਗ ਡਾਕਟਰ ਨੂੰ ਮਿਲ ਕੇ ਆਪਣੀ ਰੁਟੀਨ ਜਾਂਚ ਕਰਵਾਓ।",
    ]

    pa_exp = MultilingualExplanation(
        language="pa",
        language_name="ਪੰਜਾਬੀ (Punjabi)",
        headline=pa_headline,
        summary_overview=pa_overview,
        top_factors_plain_text=pa_factors,
        actionable_steps=pa_actions,
        reading_level="Class 8",
    )

    return {
        "en": en_exp,
        "hi": hi_exp,
        "pa": pa_exp,
    }
