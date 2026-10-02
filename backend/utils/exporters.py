from io import BytesIO

from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from fpdf import FPDF


def clean_text(text: str) -> str:
    """Normalize unicode characters to latin-1-safe equivalents."""
    text = str(text or "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u00a0": " ",
        "\u2022": "-",
        "\u2011": "-",
        "\u00b7": "-",
        "\u25cf": "-",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text.encode("latin-1", "replace").decode("latin-1")


def create_txt(text: str) -> bytes:
    """Return plain-text bytes (UTF-8)."""
    return text.encode("utf-8", errors="replace")


def create_docx(
    *,
    text: str,
    document_type: str,
    terms: str,
    logo_bytes: bytes | None = None,
) -> bytes:
    """Build and return a .docx file as bytes."""
    doc = Document()

    if logo_bytes:
        try:
            stream = BytesIO(logo_bytes)
            doc.add_picture(stream, width=Inches(1.5))
            doc.add_paragraph("")
        except Exception:
            pass

    title = doc.add_heading(document_type.strip(), level=1)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph("")

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            doc.add_paragraph("")
            continue
        if stripped.startswith("**") and stripped.endswith("**"):
            doc.add_heading(stripped.strip("*").strip(), level=2)
        else:
            p = doc.add_paragraph(stripped)
            p.paragraph_format.space_after = Pt(2)

    output = BytesIO()
    doc.save(output)
    return output.getvalue()


def create_pdf(*, text: str, document_type: str) -> bytes:
    """
    Build and return a PDF file as bytes.

    Workaround for fpdf2 v2.8.x bug: calling set_font() with a different
    style corrupts the internal c_margin, causing multi_cell(0, ...) to
    raise 'Not enough horizontal space to render a single character'.
    Fix: always use explicit cell width (epw) and reset c_margin after
    every font change.
    """
    LEFT = RIGHT = TOP = BOTTOM_MARGIN = 20  # mm

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=BOTTOM_MARGIN)
    pdf.set_margins(LEFT, TOP, RIGHT)
    pdf.add_page()

    # Snapshot the correct c_margin once, after page setup with a known font.
    pdf.set_font("Helvetica", "", 11)
    good_c_margin = pdf.c_margin  # typically ~0.567 mm for Helvetica 11pt
    epw = pdf.epw                  # effective page width (never changes)

    def _set_font(style: str, size: int) -> None:
        """Set font and restore c_margin to prevent the fpdf2 width bug."""
        pdf.set_font("Helvetica", style, size)
        pdf.c_margin = good_c_margin

    def _write(txt: str, h: float, align: str = "L") -> None:
        """Write one logical line, force-breaking words wider than epw."""
        if not txt:
            return
        words = txt.split(" ")
        current = ""
        for word in words:
            # If a single word is too wide, break it by characters
            while pdf.get_string_width(word) > epw:
                cut = len(word) - 1
                while cut > 0 and pdf.get_string_width(word[:cut]) > epw:
                    cut -= 1
                pdf.multi_cell(epw, h, word[:cut], border=0, align=align)
                word = word[cut:]
            if not word:
                continue
            candidate = (current + " " + word).lstrip() if current else word
            if pdf.get_string_width(candidate) <= epw:
                current = candidate
            else:
                if current:
                    pdf.multi_cell(epw, h, current, border=0, align=align)
                current = word
        if current:
            pdf.multi_cell(epw, h, current, border=0, align=align)

    # ── Title ──────────────────────────────────────────────────────────
    _set_font("B", 16)
    _write(clean_text(document_type.strip()), h=10, align="C")
    pdf.ln(6)

    # ── Body ───────────────────────────────────────────────────────────
    for raw_line in clean_text(text).split("\n"):
        stripped = raw_line.strip()

        if not stripped:
            pdf.ln(4)
            continue

        is_md_heading  = stripped.startswith("**") and stripped.endswith("**")
        is_caps_heading = stripped.isupper() and len(stripped) < 80

        if is_md_heading:
            _set_font("B", 12)
            _write(stripped.strip("*").strip(), h=8)
            pdf.ln(2)
        elif is_caps_heading:
            _set_font("B", 11)
            _write(stripped, h=8)
            pdf.ln(2)
        else:
            _set_font("", 11)
            _write(stripped, h=7)

    result = pdf.output(dest="S")
    if isinstance(result, str):
        return result.encode("latin-1")
    return bytes(result)
