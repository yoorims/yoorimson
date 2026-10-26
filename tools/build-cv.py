"""Build the public CV with a single-column academic layout.

Layout reference: https://hy263.github.io/assets/cv.pdf
Dates remain right-aligned; Education and Research Interests come first.
Content: existing CV, current homepage, SA_Broadband_TP_prose_revised_20261024.pdf,
the official KER 2026 program (p. 15), and the user's project participation record.
No reference CV content is reused.
"""

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, NextPageTemplate, PageBreak,
    PageTemplate, Paragraph, Spacer, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "CV_YoorimSon.pdf"
FONT_DIR = Path("C:/Windows/Fonts")
for name, filename in (
    ("CVSerif", "pala.ttf"),
    ("CVSerifBold", "palab.ttf"),
    ("CVSerifItalic", "palai.ttf"),
    ("CVSerifBoldItalic", "palabi.ttf"),
):
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / filename)))
pdfmetrics.registerFontFamily(
    "CVSerif", normal="CVSerif", bold="CVSerifBold", italic="CVSerifItalic",
    boldItalic="CVSerifBoldItalic",
)

WIDTH, HEIGHT = A4
LEFT, RIGHT, BOTTOM = 50.4, 50.4, 38
CONTENT_X = LEFT + 12
CONTENT_WIDTH = WIDTH - RIGHT - CONTENT_X
LINK_COLOR = "#0073aa"
BODY = ParagraphStyle(
    "Body", fontName="CVSerif", fontSize=11.5, leading=15,
    textColor=colors.black, spaceAfter=0,
)
TITLE = ParagraphStyle("Title", parent=BODY, fontName="CVSerifBold")
META = ParagraphStyle("Meta", parent=BODY, fontName="CVSerifItalic", fontSize=10.5, leading=13.5)
SECTION = ParagraphStyle(
    "Section", parent=TITLE, fontSize=13.5, leading=18,
    spaceAfter=6, keepWithNext=True,
)
DATE = ParagraphStyle("Date", parent=BODY, fontSize=9.7, alignment=TA_RIGHT)
TABLE_STYLE = TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ("TOPPADDING", (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
])


def p(text, style=BODY):
    return Paragraph(text, style)


def link(text, url, color="black"):
    return f'<link href="{escape(url, {chr(34): "&quot;"})}" color="{color}">{escape(text)}</link>'


def dated(title, date, style=TITLE):
    table = Table(
        [[p(title, style), p(escape(date), DATE)]],
        colWidths=[CONTENT_WIDTH - 108, 108], hAlign="LEFT",
    )
    table.setStyle(TABLE_STYLE)
    return table


story = []


def section(label, entries):
    if story:
        story.append(Spacer(1, 12))
    story.append(p(label.replace("\n", " "), SECTION))
    for index, entry in enumerate(entries):
        if index:
            story.append(Spacer(1, 7))
        table = Table([[entry]], colWidths=[CONTENT_WIDTH], hAlign="RIGHT")
        table.setStyle(TABLE_STYLE)
        story.append(table)


section("Education", [
    [dated("Sogang University, Seoul, Korea", "Mar 2025-present"),
     p("M.A. in Economics; expected graduation: 2027"),
     p("Advisor: Hyunjoo Yang", META),
     Spacer(1, 2),
     dated(link("BK21 FOUR (Brain Korea 21), Participating Graduate Student",
                "https://bk21econ.sogang.ac.kr/bk21econ/D_3822_23620.html"),
           "Sep 2026-Feb 2027", META)],
    [dated("Hankuk University of Foreign Studies", "Mar 2017-Feb 2021"),
     p("B.A. in South African Languages and Cultures; Yongin, Korea"),
     p("Minor in Political Science and Diplomacy", META)],
    [dated("University of Botswana, Gaborone, Botswana", "Jan-May 2018"),
     p("Visiting / Exchange Student", META)],
])

section("Research Interests", [[p(
    "Development economics; applied microeconomics; digital infrastructure; local economic "
    "development and spatial inequality; geospatial and satellite-based economic measurement."
)]])

section("Working Papers", [[
    dated(link("Mobile Broadband Upgrading and Spatial Inequality in South Africa",
               "https://yoorims.github.io/yoorimson/assets/SA_Broadband_TP_prose_revised_20261024.pdf"),
          "October 2026"),
    p("(with Hyunjoo Yang).", META),
    Spacer(1, 2),
    p("Uses quarterly Ookla data to examine how mobile broadband upgrading during South Africa's "
      "2021-2024 spectrum transition varies with initial quality, poverty, and regulatory priority."),
    Spacer(1, 2),
    p("Narrowing low-speed disadvantage can coexist with widening absolute speed "
      "gaps across municipalities."),
]])

section("Research\nExperience", [
    [dated(link("Sogang Spatial Economics & AI Lab", "https://hy263.github.io/projects/"),
           "Apr 2026-present"),
     p("Research Assistant to Hyunjoo Yang, Sogang University", META),
     Spacer(1, 2),
     p("Satellite-Based Global Crop Mapping and Yield-Prediction Design", TITLE),
     p("Constructed maize and rice ground-truth data and completed rice sampling; am developing "
       "XGBoost features for crop-area prediction."),
     Spacer(1, 2),
     p("North Korean Industrial Production and Economic Activity", TITLE),
     p("Supported a Bank of Korea collaboration using daytime satellite imagery, atmospheric gas data, and AI to measure "
       "North Korean industrial production and economic activity.")],
])

story.append(PageBreak())
section("Research Experience (continued)", [
    [dated(link("MIRACLE: Subnational Economic Data for South Korea, 1960-1989",
                "https://miracle.bookangseol.com/"), "Nov 2025-present"),
     p("Research Assistant to BooKang Seol (LSE)", META),
     p("Project Leads: BooKang Seol, Changkeun Lee, and Hyunjoo Yang", META),
     Spacer(1, 2),
     p("Help build a consistent township-year economic panel from historical yearbooks and archival records."),
     Spacer(1, 2),
     p("Completed administrative-region data collection and now "
       "work on OCR extraction and processing.")],
])

section("Seminars &\nConferences", [[
    dated(link("2026 Korean Economic Review (KER) International Conference",
               "https://sites.google.com/view/ker2026/program"), "June 22, 2026"),
    p("Halla Convention Center, Jeju, South Korea", META),
    Spacer(1, 2),
    p("<i>The Economic Impact of Submarine Cable Arrival on Local Economic Activity:<br/>"
      "Evidence from South Africa</i> (with Hyunjoo Yang)."),
]])

section("Methods & Data", [[
    p("<i>Programming:</i> Python."),
    p("<i>Empirical methods:</i> Fixed effects, event studies, spatial exposure designs, "
      "synthetic-control diagnostics; training in difference-in-differences and instrumental variables."),
    p("<i>Machine learning:</i> XGBoost, sampling, and feature construction."),
    p("<i>Data:</i> Panel and administrative data, broadband performance, GIS and satellite-derived "
      "measures, historical archives, crop ground-truth data, and OCR workflows."),
]])

section("Languages", [[p("Korean: Native; English: Intermediate (academic reading and writing).")]])


def first_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.black)
    canvas.setFont("CVSerifBold", 22)
    canvas.drawString(LEFT, HEIGHT - 48, "Yoorim Son")
    canvas.setFont("CVSerifItalic", 9.2)
    canvas.drawRightString(WIDTH - RIGHT, HEIGHT - 44, "October 2026")
    left_lines = ["Sogang University", "M.A. Student in Economics", "Seoul, Korea"]
    right_lines = [
        [("yoorim0917@gmail.com", "mailto:yoorim0917@gmail.com")],
        [("yoorims.github.io/yoorimson", "https://yoorims.github.io/yoorimson/index.html"),
         (" | ", None), ("GitHub", "https://github.com/yoorims")],
        [],
    ]
    for index, (left, segments) in enumerate(zip(left_lines, right_lines)):
        y = HEIGHT - 69 - 12 * index
        canvas.setFont("CVSerif", 9.7)
        canvas.drawString(LEFT, y, left)
        x = WIDTH - RIGHT - sum(pdfmetrics.stringWidth(text, "CVSerif", 9.7)
                               for text, _ in segments)
        for text, url in segments:
            width = pdfmetrics.stringWidth(text, "CVSerif", 9.7)
            canvas.setFillColor(colors.HexColor(LINK_COLOR) if url else colors.black)
            canvas.drawString(x, y, text)
            if url:
                canvas.linkURL(url, (x, y - 2, x + width, y + 9), relative=0)
            x += width
        canvas.setFillColor(colors.black)
    canvas.restoreState()


def later_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.black)
    canvas.setFont("CVSerifItalic", 9.2)
    canvas.drawString(LEFT, HEIGHT - 34, "Yoorim Son: Curriculum Vitae")
    canvas.drawRightString(WIDTH - RIGHT, HEIGHT - 34, str(doc.page))
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=LEFT, rightMargin=RIGHT,
    title="Yoorim Son - Curriculum Vitae", author="Yoorim Son",
    subject="Education, research, conference presentations, and skills",
)
first_frame = Frame(LEFT, BOTTOM, WIDTH - LEFT - RIGHT, HEIGHT - 114 - BOTTOM,
                    leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
later_frame = Frame(LEFT, BOTTOM, WIDTH - LEFT - RIGHT, HEIGHT - 52 - BOTTOM,
                    leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates([
    PageTemplate(id="First", frames=first_frame, onPage=first_page),
    PageTemplate(id="Later", frames=later_frame, onPage=later_page),
])
doc.build([NextPageTemplate("Later"), *story])
print(OUTPUT)
