from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor

def write_to_pdf(headers, contents):
    font_path = "DejaVuSans.ttf"
    pdfmetrics.registerFont(TTFont("DejaVu", font_path))

    doc = SimpleDocTemplate(
        "output.pdf",
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()

    header_style = ParagraphStyle(
        "HeaderStyle",
        fontName="DejaVu",
        parent=styles["Normal"],
        fontSize=18,
        leading=22,
        alignment=0,
    )

    paragraph_style = ParagraphStyle(
        "ParagraphStyle",
        fontName="DejaVu",
        parent=styles["Normal"],
        fontSize=14,
        leading=18,
        alignment=4,
        textColor=HexColor("#252525")
    )

    story = []

    for header in headers:
        story.append(Paragraph(header, header_style))

    for paragraph in contents:
        story.append(Spacer(1, 12))
        story.append(Paragraph(paragraph, paragraph_style))

    doc.build(story)
