from fastapi import APIRouter, HTTPException

from backend.ai_core.gemini_generator import (
    GeminiDocumentGenerator
)

from backend.schemas import (
    DocumentRequest,
    DocumentResponse
)

from backend.utils.text import sanitize_text


router = APIRouter()


@router.post(
    "/generate",
    response_model=DocumentResponse
)
def generate_document(
    request: DocumentRequest
):

    try:

        generator = (
            GeminiDocumentGenerator()
        )

        generated_text = (
            generator.generate_document(
                document_type=request.document_type,
                parties=request.parties,
                terms=request.terms,
                effective_date=request.effective_date
            )
        )

        generated_text = sanitize_text(
            generated_text
        )

        return DocumentResponse(
            success=True,
            document_type=request.document_type,
            content=generated_text,
            message="Document generated successfully."
        )

    except ValueError as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Document generation failed: "
                f"{str(error)}"
            )
        )