import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from translate import translate_hindi_to_santali

TOPICS_FILE = os.path.join(os.path.dirname(__file__), "topics.json")
FONTS_DIR = os.path.join(os.path.dirname(__file__), "fonts")

# These are the same 3 topics your original worksheet always used.
# Kept as the default so your existing /download-worksheet button
# on the homepage keeps behaving exactly as it did before.
DEFAULT_TOPIC_KEYS = ["numbers", "greetings", "objects"]

# --- Font registration -----------------------------------------------
# Helvetica (ReportLab's default font) has no Devanagari or Ol Chiki
# glyphs, which is why the PDF was showing empty boxes. We register
# proper Unicode fonts here and use them for the Hindi/Santali cells.
# If the font files are missing, we fall back to Helvetica so the app
# doesn't crash - but you'll see boxes again until the fonts are added.
DEVANAGARI_FONT = "NotoSansDevanagari"
OLCHIKI_FONT = "NotoSansOlChiki"

_devanagari_path = os.path.join(FONTS_DIR, "NotoSansDevanagari-Regular.ttf")
_olchiki_path = os.path.join(FONTS_DIR, "NotoSansOlChiki-Regular.ttf")

try:
    pdfmetrics.registerFont(TTFont(DEVANAGARI_FONT, _devanagari_path))
except Exception as e:
    print(f"WARNING: could not load Devanagari font ({e}); Hindi text may show as boxes.")
    DEVANAGARI_FONT = "Helvetica"

try:
    pdfmetrics.registerFont(TTFont(OLCHIKI_FONT, _olchiki_path))
except Exception as e:
    print(f"WARNING: could not load Ol Chiki font ({e}); Santali text may show as boxes.")
    OLCHIKI_FONT = "Helvetica"
# -----------------------------------------------------------------------


def load_topics():
    """Load the full topic bank from topics.json."""
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_worksheet(output_path="worksheet_output.pdf", topic_keys=None):
    """
    Builds a bilingual (Hindi + Santali) worksheet PDF.

    output_path: where to save the PDF (same as before).
    topic_keys: list of topic keys to include, e.g. ["numbers", "animals"].
                If not given, defaults to the original 3 topics
                (numbers, greetings, objects) - so any existing code
                that calls generate_worksheet(output_path) alone
                still works exactly like before.
    """
    if topic_keys is None:
        topic_keys = DEFAULT_TOPIC_KEYS

    topics = load_topics()
    styles = getSampleStyleSheet()

    heading_style = ParagraphStyle(
        "Heading", parent=styles["Heading2"], spaceAfter=6
    )
    note_style = ParagraphStyle(
        "Note", parent=styles["Normal"], textColor=colors.green,
        fontName="Helvetica-Oblique", spaceAfter=10
    )

    # Cell-level paragraph styles so each column can use the right font.
    hindi_cell_style = ParagraphStyle(
        "HindiCell", parent=styles["Normal"], fontName=DEVANAGARI_FONT, fontSize=11
    )
    santali_cell_style = ParagraphStyle(
        "SantaliCell", parent=styles["Normal"], fontName=OLCHIKI_FONT, fontSize=11
    )
    header_style = ParagraphStyle(
        "HeaderCell", parent=styles["Normal"], fontName="Helvetica-Bold",
        textColor=colors.white
    )

    doc = SimpleDocTemplate(output_path, pagesize=A4)
    elements = []

    for key in topic_keys:
        if key not in topics:
            continue  # skip unknown topic keys safely

        topic = topics[key]
        elements.append(Paragraph(topic["title"], heading_style))
        elements.append(Paragraph(topic["instruction"], note_style))

        table_data = [[
            Paragraph("Hindi", header_style),
            Paragraph("Santali", header_style),
        ]]
        for hindi_word in topic["items"]:
            santali_word = translate_hindi_to_santali(hindi_word)
            table_data.append([
                Paragraph(hindi_word, hindi_cell_style),
                Paragraph(santali_word, santali_cell_style),
            ])

        table = Table(table_data, colWidths=[200, 200])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E7D32")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F1F8E9")]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 20))

    doc.build(elements)
    print(f"Worksheet saved to: {output_path}")


if __name__ == "__main__":
    # Quick standalone test - generates the default worksheet,
    # same as your existing homepage button would produce.
    generate_worksheet("sample_worksheet.pdf")
