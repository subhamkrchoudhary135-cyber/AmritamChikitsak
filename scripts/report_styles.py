"""
ReportLab Styles and Canvas definitions for the CGC Project Report.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT_MARGIN = 99.21   # 3.5 cm
RIGHT_MARGIN = 35.43  # 1.25 cm
TOP_MARGIN = 70.87    # 2.5 cm
BOTTOM_MARGIN = 35.43 # 1.25 cm
USABLE_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN # 460.63 pt
USABLE_HEIGHT = PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN # 735.59 pt

LOGO_PATH = "docs/assets/cgc_logo.png"

def get_report_styles():
    styles = getSampleStyleSheet()
    
    # Custom styles
    styles.add(ParagraphStyle(
        name="CoverTitle",
        fontName="Times-Bold",
        fontSize=17,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#f8fafc")
    ))
    styles.add(ParagraphStyle(
        name="CoverSubtitle",
        fontName="Times-Roman",
        fontSize=10.5,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#cbd5e1")
    ))
    styles.add(ParagraphStyle(
        name="CoverDetails",
        fontName="Times-Bold",
        fontSize=11.5,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#f1f5f9")
    ))
    styles.add(ParagraphStyle(
        name="CoverGold",
        fontName="Times-Bold",
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#fbbf24")
    ))
    styles.add(ParagraphStyle(
        name="InnerTitle",
        fontName="Times-Bold",
        fontSize=16,
        leading=21,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0f172a")
    ))
    styles.add(ParagraphStyle(
        name="InnerSub",
        fontName="Times-Roman",
        fontSize=10.5,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#334155")
    ))
    styles.add(ParagraphStyle(
        name="InnerDetails",
        fontName="Times-Bold",
        fontSize=11,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1e293b")
    ))
    styles.add(ParagraphStyle(
        name="ChapterHeading",
        fontName="Times-Bold",
        fontSize=14,
        leading=18,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        name="FrontHeading",
        fontName="Times-Bold",
        fontSize=14,
        leading=18,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=12
    ))
    styles.add(ParagraphStyle(
        name="SecHeading",
        fontName="Times-Bold",
        fontSize=11.5,
        leading=15,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#1e3a8a"),
        spaceBefore=7,
        spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        name="SubSecHeading",
        fontName="Times-Bold",
        fontSize=10.5,
        leading=14,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=5,
        spaceAfter=2
    ))
    styles.add(ParagraphStyle(
        name="ReportBody",
        fontName="Times-Roman",
        fontSize=9.8,
        leading=14.2,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=4,
        firstLineIndent=14
    ))
    styles.add(ParagraphStyle(
        name="ReportBodyNoIndent",
        fontName="Times-Roman",
        fontSize=9.8,
        leading=14.2,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        name="FigureCaption",
        fontName="Times-Bold",
        fontSize=8.5,
        leading=11.5,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#334155"),
        spaceBefore=3,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        name="TableCaption",
        fontName="Times-Bold",
        fontSize=8.5,
        leading=11.5,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=4,
        spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        name="TOCLine",
        fontName="Times-Roman",
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#0f172a")
    ))
    styles.add(ParagraphStyle(
        name="TOCLineBold",
        fontName="Times-Bold",
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#0f172a")
    ))
    styles.add(ParagraphStyle(
        name="RefLine",
        fontName="Times-Roman",
        fontSize=8.8,
        leading=12.2,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=3.5,
        leftIndent=16,
        firstLineIndent=-16
    ))
    styles.add(ParagraphStyle(
        name="FormulaBox",
        fontName="Times-Italic",
        fontSize=9.5,
        leading=13.5,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1e3a8a"),
        spaceBefore=3,
        spaceAfter=3
    ))
    return styles

class CGCOfficialNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        page_num = self._pageNumber
        
        # Page 1: Hard bound cover page (Black background, double gold border)
        if page_num == 1:
            self.saveState()
            self.setFillColor(colors.HexColor("#0b0f19"))
            self.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
            
            # Gold ornamental border
            self.setStrokeColor(colors.HexColor("#d4af37"))
            self.setLineWidth(2.2)
            self.rect(22, 22, PAGE_WIDTH - 44, PAGE_HEIGHT - 44, fill=0, stroke=1)
            self.setLineWidth(0.8)
            self.rect(26, 26, PAGE_WIDTH - 52, PAGE_HEIGHT - 52, fill=0, stroke=1)
            self.restoreState()
            return

        # Page 2: Inner Title Page
        if page_num == 2:
            self.saveState()
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(1.0)
            self.rect(LEFT_MARGIN - 8, BOTTOM_MARGIN, USABLE_WIDTH + 16, USABLE_HEIGHT + 18, fill=0, stroke=1)
            self.restoreState()
            return

        # Pages 3 to 60: Content Pages with Running Header & Footer
        self.saveState()
        header_y = PAGE_HEIGHT - 45
        rule_y = PAGE_HEIGHT - 52
        
        # CGC Logo on Top Right
        if os.path.exists(LOGO_PATH):
            logo_w = 46
            logo_h = 20
            self.drawImage(LOGO_PATH, PAGE_WIDTH - RIGHT_MARGIN - logo_w, header_y - 3, 
                           width=logo_w, height=logo_h, mask='auto', preserveAspectRatio=True)
            
        # Header Text on Top Left
        self.setFont("Times-Bold", 8)
        self.setFillColor(colors.HexColor("#1e3a8a"))
        self.drawString(LEFT_MARGIN, header_y + 8, "CHANDIGARH ENGINEERING COLLEGE, CGC LANDRAN, MOHALI")
        self.setFont("Times-Roman", 7.5)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(LEFT_MARGIN, header_y - 2, "Department of Computer Science & Engineering | Sanjivani AI Project Report")
        
        # Header Line
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.7)
        self.line(LEFT_MARGIN, rule_y, PAGE_WIDTH - RIGHT_MARGIN, rule_y)
        
        # Running Footer (Page Numbers at Bottom Centre)
        footer_y = 20
        self.setFont("Times-Roman", 10)
        self.setFillColor(colors.HexColor("#1e293b"))
        
        if 3 <= page_num <= 10:
            roman_numerals = ["", "i", "ii", "iii", "iv", "v", "vi", "vii", "viii"]
            roman_str = roman_numerals[page_num - 2]
            self.drawCentredString(LEFT_MARGIN + (USABLE_WIDTH / 2.0), footer_y, roman_str)
        elif page_num >= 11:
            arabic_str = str(page_num - 10)
            self.drawCentredString(LEFT_MARGIN + (USABLE_WIDTH / 2.0), footer_y, arabic_str)
            
        self.restoreState()
