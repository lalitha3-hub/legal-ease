from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=1)
    parties: str = Field(..., min_length=1)
    terms: str = Field(..., min_length=1)
    effective_date: str = Field(..., min_length=1)


class DocumentResponse(BaseModel):
    success: bool
    document_type: str
    content: str
    message: str
