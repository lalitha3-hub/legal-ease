from backend.utils.exporters import create_docx, create_pdf, create_txt


def test_exporters_return_bytes():
    text = "Sample legal clause.\nSecond paragraph."

    txt_data = create_txt(text)
    docx_data = create_docx(text=text, document_type="Service Agreement", terms="Payment in 30 days.", logo_bytes=None)
    pdf_data = create_pdf(text=text, document_type="Service Agreement")

    assert isinstance(txt_data, bytes)
    assert len(txt_data) > 0
    assert isinstance(docx_data, bytes)
    assert len(docx_data) > 0
    assert isinstance(pdf_data, bytes)
    assert len(pdf_data) > 0
