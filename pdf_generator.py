from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
import os
# pdf_generator.py
# Schriftarten registrieren
def register_fonts():
    fonts = {
        "Arial": "C:/Windows/Fonts/arial.ttf",
        "Calibri": "C:/Windows/Fonts/calibri.ttf"
    }
    for font_name, font_path in fonts.items():
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont(font_name, font_path))
        else:
            print(f"Warnung: Schriftart {font_name} nicht gefunden unter {font_path}.")
            pdfmetrics.registerFont(TTFont(font_name, "Helvetica"))

register_fonts()

# Funktionen zum Zeichnen von PDF-Elementen
def draw_header(pdf, name, template):
    if template == "Vorlage 1":
        pdf.setFont("Arial", 12)
        pdf.drawString(100, 750, f"Name: {name}")
    elif template == "Vorlage 2":
        pdf.setFont("Calibri", 16)
        pdf.drawString(80, 750, f"Name: {name}")
    elif template == "Vorlage 3":
        pdf.setFont("Arial", 14)
        pdf.drawString(120, 750, f"Lebenslauf: {name}")

def draw_wrapped_text(pdf, text, x, y, width, font_name, font_size):
    style = getSampleStyleSheet()["Normal"]
    style.fontName = font_name
    style.fontSize = font_size
    paragraph = Paragraph(text, style)
    paragraph.wrapOn(pdf, width, 800)
    paragraph.drawOn(pdf, x, y)

def draw_experience(pdf, experience, template):
    if template == "Vorlage 1":
        draw_wrapped_text(pdf, experience, 100, 700, 400, "Arial", 12)
    elif template == "Vorlage 2":
        draw_wrapped_text(pdf, experience, 80, 700, 400, "Calibri", 16)
    elif template == "Vorlage 3":
        draw_wrapped_text(pdf, experience, 120, 650, 400, "Arial", 14)

def draw_skills(pdf, skills, template):
    if template == "Vorlage 1":
        draw_wrapped_text(pdf, skills, 100, 650, 400, "Arial", 12)
    elif template == "Vorlage 2":
        draw_wrapped_text(pdf, skills, 80, 650, 400, "Calibri", 16)
    elif template == "Vorlage 3":
        draw_wrapped_text(pdf, skills, 120, 700, 400, "Arial", 14)

# Hauptfunktion
def create_pdf(name, experience, skills, template, photo_path=None):
    try:
        file_name = f"{name}_lebenslauf.pdf"
        pdf = canvas.Canvas(file_name)

        # Foto hinzufügen
        if photo_path and os.path.exists(photo_path):
            image = ImageReader(photo_path)
            pdf.drawImage(image, 400, 700, width=100, height=100)
        else:
            print("Warnung: Foto nicht gefunden oder Pfad ungültig.")

        # Elemente in PDF zeichnen
        draw_header(pdf, name, template)
        draw_experience(pdf, experience, template)
        draw_skills(pdf, skills, template)

        pdf.save()
        return file_name
    except Exception as e:
        print(f"Fehler beim Erstellen des PDFs: {str(e)}")
        return None