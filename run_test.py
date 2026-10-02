"""Smoke test for all three exporters."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from backend.utils.exporters import create_txt, create_docx, create_pdf

SAMPLE = (
    "EMPLOYMENT CONTRACT\n\n"
    "**1. PARTIES**\n"
    "This Employment Contract is made between Acme Corp (Employer) and Jane Doe (Employee).\n\n"
    "**2. TERMS**\n"
    "Payment within 30 days; Confidentiality must be maintained; Work must be completed by the agreed deadline.\n\n"
    "**3. EFFECTIVE DATE**\n"
    "This agreement is effective as of January 1, 2026.\n\n"
    "SIGNATURES\n"
    "__________________________         __________________________\n"
    "Employer                            Employee\n"
)

errors = []

try:
    txt = create_txt(SAMPLE)
    assert isinstance(txt, bytes) and len(txt) > 0
    print(f"[OK] TXT  -> {len(txt)} bytes")
except Exception as e:
    errors.append(str(e))
    print(f"[FAIL] TXT: {e}")

try:
    docx = create_docx(text=SAMPLE, document_type="Employment Contract", terms="N/A", logo_bytes=None)
    assert isinstance(docx, bytes) and len(docx) > 0
    print(f"[OK] DOCX -> {len(docx)} bytes")
except Exception as e:
    errors.append(str(e))
    print(f"[FAIL] DOCX: {e}")

try:
    pdf = create_pdf(text=SAMPLE, document_type="Employment Contract")
    assert isinstance(pdf, bytes) and len(pdf) > 0
    print(f"[OK] PDF  -> {len(pdf)} bytes")
except Exception as e:
    errors.append(str(e))
    print(f"[FAIL] PDF: {e}")

print()
if errors:
    print("FAILED:", errors)
    sys.exit(1)
else:
    print("All exporters passed.")
