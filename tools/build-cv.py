"""Build the public CV. Run with the bundled Python (reportlab required).

Sources: preserved original CV; current homepage research descriptions;
https://hy263.github.io/projects/; https://miracle.bookangseol.com/;
SA_Broadband_TP_prose_revised_20261024.pdf (title page and abstract).
Education dates, training, contact and language details retain the original CV.
Personal project contributions retain the existing homepage descriptions.
"""

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "CV_YoorimSon.pdf"
FONT_DIR = Path("C:/Windows/Fonts")
for name, filename in (
    ("CVSerif", "times.ttf"),
    ("CVSerifBold", "timesbd.ttf"),
    ("CVSerifItalic", "timesi.ttf"),
    ("CVSerifBoldItalic", "timesbi.ttf"),
):
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / filename)))
pdfmetrics.registerFontFamily(
    "CVSerif", normal="CVSerif", bold="CVSerifBold", italic="CVSerifItalic",
    boldItalic="CVSerifBoldItalic",
)

INK = colors.HexColor("#171717")
BLUE = colors.HexColor("#173f6b")
GRAY = colors.HexColor("#60636a")
LINE = colors.HexColor("#d8d8d2")
BODY = ParagraphStyle(
    "Body", fontName="CVSerif", fontSize=10.5, leading=14.2,
    textColor=INK, spaceAfter=4, alignment=TA_LEFT,
)
TITLE = ParagraphStyle(
    "Name", parent=BODY, fontName="CVSerifBold", fontSize=25, leading=29,
    spaceAfter=7,
)
SECTION = ParagraphStyle(
    "Section", parent=BODY, fontName="CVSerifBold", fontSize=11.5, leading=15,
    textColor=BLUE, spaceBefore=12, spaceAfter=7,
)
ENTRY = ParagraphStyle(
    "Entry", parent=BODY, fontName="CVSerifBold", fontSize=11, leading=14.5,
    spaceBefore=5, spaceAfter=3,
)
META = ParagraphStyle(
    "Meta", parent=BODY, fontSize=9.5, leading=12.5, textColor=GRAY,
)
BULLET = ParagraphStyle(
    "Bullet", parent=BODY, leftIndent=11, firstLineIndent=-8, spaceAfter=4,
)


def p(text, style=BODY):
    return Paragraph(text, style)


def link(text, url):
    return f'<link href="{escape(url, {chr(34): "&quot;"})}" color="#173f6b">{escape(text)}</link>'


story = []


def section(title):
    story.append(p(title.upper(), SECTION))
    story.append(HRFlowable(width="100%", thickness=0.45, color=LINE, spaceAfter=7))


def entry(title, meta, lines=(), bullets=()):
    items = [p(title, ENTRY), p(meta, META)]
    items.extend(p(line) for line in lines)
    items.extend(p("- " + line, BULLET) for line in bullets)
    items.append(Spacer(1, 5))
    story.append(KeepTogether(items))


story.extend([
    p("Yoorim Son", TITLE),
    p("M.A. Student in Economics | Sogang University | Seoul, Korea"),
    p(link("yoorim0917@gmail.com", "mailto:yoorim0917@gmail.com")
      + " | Mobile: +82 10-5093-5917"),
    p(link("Homepage", "https://yoorims.github.io/yoorimson/index.html")
      + " | " + link("GitHub", "https://github.com/yoorims")),
])

section("Research Interests")
story.append(p("Development economics; applied microeconomics; digital infrastructure; "
               "local economic development and spatial inequality; geospatial and satellite-based economic measurement."))

section("Education")
entry("Sogang University, Seoul, Korea", "Mar 2025 - Present | Expected graduation: 2027", [
    "M.A. in Economics | Advisor: Hyunjoo Yang",
])
entry("Hankuk University of Foreign Studies, Yongin, Korea", "Mar 2017 - Feb 2021", [
    "B.A. in South African Languages and Cultures",
    "Minor in Political Science and Diplomacy",
])
entry("University of Botswana, Gaborone, Botswana", "Jan 2018 - May 2018", [
    "Visiting / Exchange Student | Coursework in Political Science",
])

section("Working Papers")
entry(
    link("Mobile Broadband Upgrading and Spatial Inequality in South Africa",
         "https://yoorims.github.io/yoorimson/assets/SA_Broadband_TP_prose_revised_20261024.pdf"),
    "With Hyunjoo Yang | October 2026", bullets=[
        "Follows South Africa's 2021-2024 spectrum transition using quarterly Ookla measurements, "
        "comparing municipalities by initial quality, baseline poverty, and regulatory priority.",
        "Documents narrowing low-speed and relative-speed disadvantages alongside widening absolute "
        "speed gaps. Separate exploratory poverty comparisons examine high-speed expansion, "
        "with inference and measurement-coverage qualifications.",
    ],
)
entry(
    link("Where Do International Connectivity Gains Arrive?",
         "https://yoorims.github.io/yoorimson/papers.html#equiano"),
    "Draft", lines=["<i>Spatial Broadband Upgrading and Employment after Equiano in South Africa</i>"],
    bullets=[
        "Combines municipal broadband measurements, sectoral administrative employment data, "
        "spatial measures, and satellite-derived controls to study post-2023 spatial adjustment.",
        "Examines spatial broadband gradients using fixed effects, event studies, and "
        "synthetic-control diagnostics, with explicit limits on causal attribution.",
    ],
)

story.append(PageBreak())
section("Research Experience")
entry(
    link("Sogang Spatial Economics & AI Lab", "https://hy263.github.io/projects/"),
    "Apr 2026 - Present | Sogang University", lines=[
        "Research Group Member (Master's Student) | Lab Head: Hyunjoo Yang",
    ], bullets=[
        "Contribute to agricultural prediction using machine learning and spatial data within "
        "a lab working on geospatial data, economics, and Korea's development.",
        "Collected and constructed maize and rice ground-truth datasets; completed the rice "
        "sampling workflow and am constructing XGBoost features to predict cultivated area across Asian countries.",
    ],
)
entry(
    link("MIRACLE: Subnational Economic Data for South Korea, 1960-1989",
         "https://miracle.bookangseol.com/"),
    "Nov 2025 - Present | Research Associate", lines=[
        "Project Leads: BooKang Seol, Changkeun Lee, and Hyunjoo Yang",
    ], bullets=[
        "Contribute to a consistent township-year economic panel using municipal statistical "
        "yearbooks and archival records, with geographic identifiers spanning administrative boundary changes.",
        "Completed administrative-region data collection and coordinated a five-person collection team.",
        "Currently work on OCR-based extraction and processing of historical statistical records.",
    ],
)

section("Planned Collaboration")
entry("Satellite-Based Measurement of North Korean Economic Activity", "Upcoming | Bank of Korea", [
    "Planned collaboration using satellite data to estimate industrial production and develop "
    "measures of economic activity where conventional statistics are limited.",
])

section("Training")
entry("MultiCampus, Seoul, Korea", "Feb 2024 - Jul 2024", [
    "Data Analyst Training (Python) | Government-Sponsored Program",
    "Data collection and handling, basic machine learning, and visualization using Python.",
])

section("Methods & Data")
story.extend([
    p("<b>Programming:</b> Python."),
    p("<b>Empirical methods:</b> Fixed effects, event studies, spatial exposure designs, "
      "synthetic-control diagnostics; training in difference-in-differences and instrumental variables."),
    p("<b>Machine learning:</b> XGBoost, sampling, and feature construction."),
    p("<b>Data:</b> Panel and administrative data, broadband performance, GIS and satellite-derived "
      "measures, historical archives, crop ground-truth data, and OCR workflows."),
])

section("Languages")
story.append(p("Korean: Native | English: Intermediate (academic reading and writing)."))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.45)
    canvas.line(20 * mm, 16 * mm, A4[0] - 20 * mm, 16 * mm)
    canvas.setFont("CVSerif", 9)
    canvas.setFillColor(GRAY)
    canvas.drawString(20 * mm, 11.5 * mm, "Yoorim Son | Updated October 24, 2026")
    canvas.drawRightString(A4[0] - 20 * mm, 11.5 * mm, str(doc.page))
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(OUTPUT), pagesize=A4, rightMargin=20 * mm, leftMargin=20 * mm,
    topMargin=18 * mm, bottomMargin=20 * mm,
    title="Yoorim Son - Curriculum Vitae", author="Yoorim Son",
    subject="Education, working papers, research experience, and skills",
)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUTPUT)
