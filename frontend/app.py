import html
import os

import requests
import streamlit as st

from dotenv import load_dotenv

from backend.utils.exporters import (
    create_docx,
    create_pdf,
    create_txt
)


load_dotenv()


BACKEND_URL = os.getenv(
    "LEGALEASE_API_URL",
    "http://127.0.0.1:8000"
)


st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


st.markdown(
    """
    <style>

    .main {
        background-color: #0b1120;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
    }

    .hero {
        padding: 25px;
        border-radius: 18px;
        background: linear-gradient(
            135deg,
            #111827,
            #172554
        );
        border: 1px solid #26324d;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: #f8fafc;
        font-size: 42px;
        margin-bottom: 5px;
    }

    .hero p {
        color: #94a3b8;
        font-size: 17px;
    }

    .preview {
        background: #111827;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 25px;
        max-height: 650px;
        overflow-y: auto;
        color: #e5e7eb;
        white-space: pre-wrap;
        line-height: 1.7;
        font-family: Georgia, serif;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .warning {
        padding: 12px;
        border-radius: 10px;
        background: #422006;
        border: 1px solid #92400e;
        color: #fed7aa;
    }

    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="hero">
        <h1>⚖️ LegalEase</h1>
        <p>
            AI-Powered Legal Document Generator
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="warning">
        <strong>Important:</strong>
        LegalEase creates AI-assisted document drafts.
        Generated documents should be reviewed by a qualified
        legal professional before being used for legal purposes.
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    '<div class="section-title">Document Information</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


with col1:

    document_type = st.selectbox(
        "Document Type",
        [
            "Employment Contract",
            "Non-Disclosure Agreement",
            "Lease Agreement",
            "Freelance Work Contract",
            "Service Agreement",
            "Employment Offer Letter",
            "Partnership Agreement",
            "Business Agreement",
            "General Contract",
            "Custom Agreement"
        ]
    )


with col2:

    effective_date = st.text_input(
        "Effective Date",
        placeholder="Example: April 10, 2026"
    )


parties = st.text_area(
    "Parties Involved",
    placeholder=(
        "Example:\n"
        "Jane Doe (Service Provider)\n"
        "TechNova Inc. (Client)"
    ),
    height=120
)


terms = st.text_area(
    "Terms & Conditions",
    placeholder=(
        "Separate each term using a semicolon (;)\n\n"
        "Example:\n"
        "Payment within 30 days; "
        "Confidentiality must be maintained; "
        "Work must be completed by the deadline"
    ),
    height=160
)


logo = st.file_uploader(
    "Optional Company Logo",
    type=[
        "png",
        "jpg",
        "jpeg"
    ]
)


if "document_text" not in st.session_state:

    st.session_state.document_text = ""


if "generated" not in st.session_state:

    st.session_state.generated = False


st.markdown("")


generate_button = st.button(
    "✨ Generate Document",
    type="primary",
    use_container_width=True
)


if generate_button:

    if not effective_date.strip():

        st.error(
            "Please enter the effective date."
        )

    elif not parties.strip():

        st.error(
            "Please enter the parties involved."
        )

    elif not terms.strip():

        st.error(
            "Please enter the terms and conditions."
        )

    else:

        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "effective_date": effective_date
        }

        with st.spinner(
            "Generating your legal document..."
        ):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=120
                )

                if response.status_code == 200:

                    result = response.json()

                    st.session_state.document_text = (
                        result["content"]
                    )

                    st.session_state.generated = True

                    st.success(
                        "Document generated successfully."
                    )

                else:

                    try:
                        detail = response.json().get(
                            "detail",
                            response.text
                        )
                    except Exception:
                        detail = response.text

                    st.error(
                        f"Backend error: {detail}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to FastAPI backend. "
                    "Make sure the backend is running on "
                    f"{BACKEND_URL}."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "The request timed out. "
                    "Please try again."
                )

            except Exception as error:

                st.error(
                    f"Unexpected error: {error}"
                )


if st.session_state.generated:

    st.markdown("---")

    st.markdown(
        '<div class="section-title">Document Preview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        st.session_state.document_text,
        unsafe_allow_html=False
    )

    st.markdown(
        '<div class="section-title">Edit Document</div>',
        unsafe_allow_html=True
    )

    edited_text = st.text_area(
        "Edit the generated document below",
        value=st.session_state.document_text,
        height=600,
        label_visibility="collapsed"
    )

    st.session_state.document_text = edited_text

    st.markdown(
        '<div class="section-title">Branding</div>',
        unsafe_allow_html=True
    )

    logo_bytes = None

    if logo is not None:

        logo_bytes = logo.getvalue()

        st.image(
            logo,
            width=150
        )


    st.markdown(
        '<div class="section-title">Download</div>',
        unsafe_allow_html=True
    )


    download_col1, download_col2, download_col3 = (
        st.columns(3)
    )


    safe_name = (
        document_type
        .replace(" ", "_")
        .replace("/", "_")
    )


    txt_data = create_txt(
        st.session_state.document_text
    )


    docx_data = create_docx(
        text=st.session_state.document_text,
        document_type=document_type,
        terms=terms,
        logo_bytes=logo_bytes
    )


    pdf_data = create_pdf(
        text=st.session_state.document_text,
        document_type=document_type
    )


    with download_col1:

        st.download_button(
            label="📄 Download TXT",
            data=txt_data,
            file_name=f"{safe_name}.txt",
            mime="text/plain",
            use_container_width=True
        )


    with download_col2:

        st.download_button(
            label="📝 Download DOCX",
            data=docx_data,
            file_name=f"{safe_name}.docx",
            mime=(
                "application/"
                "vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            use_container_width=True
        )


    with download_col3:

        st.download_button(
            label="📕 Download PDF",
            data=pdf_data,
            file_name=f"{safe_name}.pdf",
            mime="application/pdf",
            use_container_width=True
        )


st.markdown("---")

st.caption(
    "LegalEase | AI-assisted legal document drafting"
)