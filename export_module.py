from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def write_to_pdf(header, contents):
    font_path = 'DejaVuSans.ttf'
    pdfmetrics.registerFont(TTFont('DejaVu', font_path))
    c = canvas.Canvas("output.pdf", pagesize=letter)

    c.setFont("DejaVu", 24)
    c.drawString(50, 750, header)

    c.setFont("DejaVu", 16)
    c.drawString(50, 700, contents)

    c.save()
