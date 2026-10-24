"""Build the public CV with a compact academic layout.

Layout reference: https://jackcollison.github.io/assets/pdf/collison_cv.pdf
Content: existing CV, current homepage, SA_Broadband_TP_prose_revised_20261024.pdf,
and the official KER 2026 program (p. 15). No reference CV content is reused.
"""

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Flowable, Frame, LongTable, NextPageTemplate,
    PageTemplate, Paragraph, Spacer, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "CV_YoorimSon.pdf"
FONT_DIR = Path("C:/Windows/Fonts")
for name, filename in (
    ("CVSerif", "cambria.ttc"),
    ("CVSerifBold", "cambriab.ttf"),
    ("CVSerifItalic", "cambriai.ttf"),
    ("CVSerifBoldItalic", "cambriaz.ttf"),
):
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / filename)))
pdfmetrics.registerFontFamily(
    "CVSerif", normal="CVSerif", bold="CVSerifBold", italic="CVSerifItalic",
    boldItalic="CVSerifBoldItalic",
)

WIDTH, HEIGHT = letter
LEFT, RIGHT, BOTTOM = 36, 50.4, 30
LABEL_WIDTH = 100.8
CONTENT_WIDTH = WIDTH - LEFT - RIGHT - LABEL_WIDTH
CONTENT_X = LEFT + LABEL_WIDTH
LINK_COLOR = "#0073aa"
BODY = ParagraphStyle(
    "Body", fontName="CVSerif", fontSize=9.2, leading=12,
    textColor=colors.black, spaceAfter=0,
)
DATE = ParagraphStyle("Date", parent=BODY, fontSize=8.2, alignment=TA_RIGHT)
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


class SmallCapsLabel(Flowable):
    """Section labels occupy the narrow left column, as in the reference."""

    def __init__(self, text):
        super().__init__()
        self.lines = text.split("\n")
        self.width, self.height = LABEL_WIDTH - 8, len(self.lines) * 12

    def draw(self):
        for row, line in enumerate(self.lines):
            text = self.canv.beginText(0, self.height - 9.2 - row * 12)
            for word_index, word in enumerate(line.split()):
                if word_index:
                    text.setFont("CVSerif", 7.5)
                    text.textOut(" ")
                text.setFont("CVSerif", 9.2)
                text.textOut(word[0].upper())
                text.setFont("CVSerif", 7.5)
                text.textOut(word[1:].upper())
            self.canv.drawText(text)


def dated(title, date):
    table = Table(
        [[p(title), p(escape(date), DATE)]],
        colWidths=[CONTENT_WIDTH - 96, 96], hAlign="LEFT",
    )
    table.setStyle(TABLE_STYLE)
    return table


rows = []


def section(label, entries):
    if rows:
        rows.append([Spacer(1, 0), Spacer(1, 8)])
    for index, entry in enumerate(entries):
        if index:
            rows.append([Spacer(1, 0), Spacer(1, 3)])
        rows.append([SmallCapsLabel(label) if index == 0 else "", entry])


section("Education", [
    [dated("Sogang University, Seoul, Korea", "Mar 2025-present"),
     p("M.A. in Economics; expected graduation: 2027"),
     p("Advisor: Hyunjoo Yang")],
    [dated("Hankuk University of Foreign Studies", "Mar 2017-Feb 2021"),
     p("B.A. in South African Languages and Cultures; Yongin, Korea"),
     p("Minor in Political Science and Diplomacy")],
    [dated("University of Botswana, Gaborone, Botswana", "Jan-May 2018"),
     p("Visiting / Exchange Student; coursework in Political Science")],
])

section("Research Fields", [[p(
    "Development economics; applied microeconomics; digital infrastructure; local economic "
    "development and spatial inequality; geospatial and satellite-based economic measurement."
)]])

section("Working Papers", [[
    p(link("Mobile Broadband Upgrading and Spatial Inequality in South Africa",
           "https://yoorims.github.io/yoorimson/assets/SA_Broadband_TP_prose_revised_20261024.pdf")
      + " (with Hyunjoo Yang). October 2026."),
    Spacer(1, 2),
    p("Uses quarterly Ookla measurements to compare mobile broadband upgrading across South African "
      "municipalities by initial service quality, baseline poverty, and regulatory priority "
      "during the 2021-2024 spectrum transition."),
    Spacer(1, 2),
    p("Tracks low-speed service, average performance, and high-speed expansion to distinguish "
      "local improvements from changes in gaps across places. Separate exploratory poverty "
      "comparisons include inference and measurement-coverage checks."),
]])

section("Research\nExperience", [
    [dated(link("Sogang Spatial Economics & AI Lab", "https://hy263.github.io/projects/"),
           "Apr 2026-present"),
     p("Research Group Member (Master's Student), Sogang University"),
     p("Lab Head: Hyunjoo Yang"),
     Spacer(1, 2),
     p("Contribute to agricultural prediction using machine learning and spatial data within "
       "a lab working on geospatial data, economics, and Korea's development."),
     Spacer(1, 2),
     p("Collected and constructed maize and rice ground-truth datasets; completed the rice "
       "sampling workflow and am constructing XGBoost features to predict cultivated area across Asian countries.")],
    [dated(link("MIRACLE: Subnational Economic Data for South Korea, 1960-1989",
                "https://miracle.bookangseol.com/"), "Nov 2025-present"),
     p("Research Associate; Project Leads: BooKang Seol, Changkeun Lee, and Hyunjoo Yang"),
     Spacer(1, 2),
     p("Contribute to a consistent township-year economic panel using municipal statistical "
       "yearbooks and archival records, with geographic identifiers spanning administrative boundary changes."),
     Spacer(1, 2),
     p("Completed administrative-region data collection and coordinated a five-person collection team."),
     Spacer(1, 2),
     p("Currently work on OCR-based extraction and processing of historical statistical records.")],
])

section("Seminars &\nConferences", [[
    dated(link("2026 Korean Economic Review (KER) International Conference",
               "https://sites.google.com/view/ker2026/program"), "June 22, 2026"),
    p("Halla Convention Center, Jeju, South Korea"),
    Spacer(1, 2),
    p("<i>The Economic Impact of Submarine Cable Arrival on Local Economic Activity: "
      "Evidence from South Africa</i> (with Hyunjoo Yang)."),
    p("Presenter; Contributed Session A5: Empirical Microeconomics"),
]])

section("Planned\nCollaboration", [[
    dated("Satellite-Based Measurement of North Korean Economic Activity", "Upcoming"),
    p("Bank of Korea"),
    Spacer(1, 2),
    p("Planned collaboration using satellite data to estimate industrial production and develop "
      "measures of economic activity where conventional statistics are limited."),
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
    canvas.setFont("CVSerifBold", 16)
    canvas.drawString(LEFT, HEIGHT - 66, "Yoorim Son")
    canvas.setFont("CVSerif", 8.2)
    canvas.drawRightString(WIDTH - RIGHT, HEIGHT - 59, "October 2026")
    canvas.setLineWidth(0.4)
    canvas.line(LEFT, HEIGHT - 80, WIDTH - RIGHT, HEIGHT - 80)
    left_lines = ["Sogang University", "M.A. Student in Economics", "Seoul, Korea"]
    right_lines = [
        [("+82 10-5093-5917", None)],
        [("yoorim0917@gmail.com", "mailto:yoorim0917@gmail.com")],
        [("yoorims.github.io/yoorimson", "https://yoorims.github.io/yoorimson/index.html"),
         (" | ", None), ("GitHub", "https://github.com/yoorims")],
    ]
    for index, (left, segments) in enumerate(zip(left_lines, right_lines)):
        y = HEIGHT - 93 - 12 * index
        canvas.setFont("CVSerif", 9.2)
        canvas.drawString(CONTENT_X, y, left)
        x = WIDTH - RIGHT - sum(pdfmetrics.stringWidth(text, "CVSerif", 9.2)
                               for text, _ in segments)
        for text, url in segments:
            width = pdfmetrics.stringWidth(text, "CVSerif", 9.2)
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
    canvas.setFont("CVSerif", 8.2)
    canvas.drawRightString(WIDTH - RIGHT, HEIGHT - 36, f"Son, p. {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=letter, leftMargin=LEFT, rightMargin=RIGHT,
    title="Yoorim Son - Curriculum Vitae", author="Yoorim Son",
    subject="Education, research, conference presentations, and skills",
)
first_frame = Frame(LEFT, BOTTOM, WIDTH - LEFT - RIGHT, HEIGHT - 124 - BOTTOM,
                    leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
later_frame = Frame(LEFT, BOTTOM, WIDTH - LEFT - RIGHT, HEIGHT - 52 - BOTTOM,
                    leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates([
    PageTemplate(id="First", frames=first_frame, onPage=first_page),
    PageTemplate(id="Later", frames=later_frame, onPage=later_page),
])
table = LongTable(rows, colWidths=[LABEL_WIDTH, CONTENT_WIDTH], hAlign="LEFT",
                  splitByRow=1, splitInRow=0)
table.setStyle(TABLE_STYLE)
doc.build([NextPageTemplate("Later"), table])
print(OUTPUT)
