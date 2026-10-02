"""Quick sanity-check for the three exporters. Run from the repo root."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.utils.exporters import create_docx, create_pdf, create_txt

text = "hello world"

txt = create_txt(text)
docx = create_docx(text=text, document_type="Test", terms="Payment due", logo_bytes=None)
pdf = create_pdf(text=text, document_type="Test")

print(type(txt).__name__, len(txt))
print(type(docx).__name__, len(docx))
print(type(pdf).__name__, len(pdf))
