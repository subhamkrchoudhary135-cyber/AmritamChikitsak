"""
Official CGC Project Report Master Generator (Expanded with Executed Python ML Step Screenshots)
Orchestrates all 82 pages and compiles the final publication-grade PDF document.
Verifies the output using pypdf to ensure exactly 82 pages.
"""

import os
import sys
from pypdf import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, PageBreak

from report_styles import (
    LEFT_MARGIN, RIGHT_MARGIN, TOP_MARGIN, BOTTOM_MARGIN,
    CGCOfficialNumberedCanvas
)

from report_pages_front import (
    page_01_cover, page_02_inner_title, page_03_certificate,
    page_04_acknowledgement, page_05_abstract, page_06_toc_1,
    page_07_toc_2, page_08_list_of_tables, page_09_list_of_figures,
    page_10_abbreviations
)

from report_pages_ch1_ch4 import (
    page_11_ch1_p1, page_12_ch1_p2, page_13_ch1_p3, page_14_ch1_p4,
    page_15_ch2_p1, page_16_ch2_p2, page_17_ch2_p3, page_18_ch2_p4, page_19_ch2_p5,
    page_20_ch3_p1, page_21_ch3_p2, page_22_ch3_p3, page_23_ch3_p4, page_24_ch3_p5,
    page_25_ch4_p1, page_26_ch4_p2, page_27_ch4_p3, page_28_ch4_p4, page_29_ch4_p5, page_30_ch4_p6
)

from report_pages_pipeline_steps import (
    page_ch4_step1, page_ch4_step2,
    page_ch5_step3, page_ch5_step4, page_ch5_step5,
    page_ch6_step6, page_ch6_step7,
    page_ch7_step8
)

from report_pages_ch5_ch9 import (
    page_31_ch5_p1, page_32_ch5_p2, page_33_ch5_p3, page_34_ch5_p4, page_35_ch5_p5, page_36_ch5_p6,
    page_37_ch6_p1, page_38_ch6_p2, page_39_ch6_p3, page_40_ch6_p4, page_41_ch6_p5,
    page_42_ch7_p1, page_43_ch7_p2, page_44_ch7_p3, page_45_ch7_p4, page_46_ch7_p5,
    page_61_eval_p1, page_62_eval_p2, page_63_eval_p3, page_64_eval_p4, page_65_eval_p5, page_66_eval_p6, page_67_eval_p7,
    page_68_ch9_p1, page_69_ch9_p2, page_70_ch9_p3
)

from report_pages_screenshots import (
    page_47_ss_p1, page_48_ss_p2, page_49_ss_p3, page_50_ss_p4,
    page_51_ss_p5, page_52_ss_p6, page_53_ss_p7, page_54_ss_p8,
    page_55_ss_p9, page_56_ss_p10, page_57_ss_p11, page_58_ss_p12,
    page_59_ss_p13, page_60_ss_p14
)

from report_pages_back import (
    page_71_ref_p1, page_72_ref_p2, page_73_app_p1, page_74_app_p2
)

OUTPUT_DIR = "reports"
OUTPUT_PDF = os.path.join(OUTPUT_DIR, "Sanjivani_AI_Project_Report_CGC.pdf")

def generate_report():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Initializing Document Builder: {OUTPUT_PDF}...")
    
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN
    )
    
    pages = [
        # Front Matter: Pages 1 to 10 (Roman i to x)
        page_01_cover, page_02_inner_title, page_03_certificate,
        page_04_acknowledgement, page_05_abstract, page_06_toc_1,
        page_07_toc_2, page_08_list_of_tables, page_09_list_of_figures,
        page_10_abbreviations,
        
        # Chapter 1: Introduction (Pages 11 to 14: Arabic 1 to 4)
        page_11_ch1_p1, page_12_ch1_p2, page_13_ch1_p3, page_14_ch1_p4,
        
        # Chapter 2: Literature Survey & Theoretical Framework (Pages 15 to 19: Arabic 5 to 9)
        page_15_ch2_p1, page_16_ch2_p2, page_17_ch2_p3, page_18_ch2_p4, page_19_ch2_p5,
        
        # Chapter 3: System Architecture & Requirements (Pages 20 to 24: Arabic 10 to 14)
        page_20_ch3_p1, page_21_ch3_p2, page_22_ch3_p3, page_23_ch3_p4, page_24_ch3_p5,
        
        # Chapter 4: Clinical Data Engineering & Ingestion Pipeline (Pages 25 to 32: Arabic 15 to 22)
        page_25_ch4_p1, page_26_ch4_p2, page_ch4_step1, page_27_ch4_p3, page_28_ch4_p4, page_ch4_step2, page_29_ch4_p5, page_30_ch4_p6,
        
        # Chapter 5: Machine Learning Models & Predictive Framework (Pages 33 to 41: Arabic 23 to 31)
        page_31_ch5_p1, page_32_ch5_p2, page_33_ch5_p3, page_ch5_step3, page_34_ch5_p4, page_35_ch5_p5, page_ch5_step4, page_36_ch5_p6, page_ch5_step5,
        
        # Chapter 6: Explainable AI, Safety Guardrails & Multilingual Engine (Pages 42 to 48: Arabic 32 to 38)
        page_37_ch6_p1, page_38_ch6_p2, page_ch6_step6, page_39_ch6_p3, page_40_ch6_p4, page_ch6_step7, page_41_ch6_p5,
        
        # Chapter 7: Frontend Architecture, Progressive Web App & UX Design (Pages 49 to 54: Arabic 39 to 44)
        page_42_ch7_p1, page_43_ch7_p2, page_ch7_step8, page_44_ch7_p3, page_45_ch7_p4, page_46_ch7_p5,
        
        # Chapter 8 Part A: Executed Result Screenshots & Explanations (Pages 55 to 68: Arabic 45 to 58)
        page_47_ss_p1, page_48_ss_p2, page_49_ss_p3, page_50_ss_p4,
        page_51_ss_p5, page_52_ss_p6, page_53_ss_p7, page_54_ss_p8,
        page_55_ss_p9, page_56_ss_p10, page_57_ss_p11, page_58_ss_p12,
        page_59_ss_p13, page_60_ss_p14,
        
        # Chapter 8 Part B: Quantitative Empirical Validation (Pages 69 to 75: Arabic 59 to 65)
        page_61_eval_p1, page_62_eval_p2, page_63_eval_p3, page_64_eval_p4,
        page_65_eval_p5, page_66_eval_p6, page_67_eval_p7,
        
        # Chapter 9: Conclusion & Future Scope (Pages 76 to 78: Arabic 66 to 68)
        page_68_ch9_p1, page_69_ch9_p2, page_70_ch9_p3,
        
        # Back Matter: References & Appendices (Pages 79 to 82: Arabic 69 to 72)
        page_71_ref_p1, page_72_ref_p2, page_73_app_p1, page_74_app_p2
    ]
    
    print(f"Total Planned Pages in Sequence: {len(pages)}")
    assert len(pages) == 82, f"Error: Page sequence length is {len(pages)}, expected 82!"
    
    story = []
    for i, page_fn in enumerate(pages):
        page_flowables = page_fn()
        story.extend(page_flowables)
        if i < len(pages) - 1:
            story.append(PageBreak())
            
    print("Building Document Flow with CGCOfficialNumberedCanvas...")
    doc.build(story, canvasmaker=CGCOfficialNumberedCanvas)
    print("Document successfully compiled.")
    
    # Verification with pypdf
    reader = PdfReader(OUTPUT_PDF)
    actual_pages = len(reader.pages)
    print(f"==================================================")
    print(f"VERIFICATION RESULT: Total Pages = {actual_pages}")
    print(f"File Path: {OUTPUT_PDF}")
    print(f"File Size: {os.path.getsize(OUTPUT_PDF):,} bytes")
    print(f"==================================================")
    
    if actual_pages != 82:
        print(f"WARNING: Actual page count ({actual_pages}) != 82. Inspecting page flow...")
        sys.exit(1)
    else:
        print("SUCCESS: Exact 82-page publication-grade PDF project report verified and ready!")

if __name__ == "__main__":
    generate_report()
