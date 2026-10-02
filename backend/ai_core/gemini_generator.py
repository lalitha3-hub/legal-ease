from __future__ import annotations

from typing import Any

from google import genai

from backend.config import settings


class GeminiDocumentGenerator:
    def __init__(self) -> None:
        self.api_key = settings.GEMINI_API_KEY
        self.model = settings.GEMINI_MODEL
        self.client = None

        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)

    def _fallback_document(self, *, document_type: str, parties: str, terms: str, effective_date: str) -> str:
        terms_list = [term.strip() for term in terms.split(";") if term.strip()]
        terms_block = "\n".join(f"- {term}" for term in terms_list) if terms_list else "- Standard confidentiality, payment, and compliance obligations."

        return (
            f"{document_type}\n\n"
            f"Effective Date: {effective_date}\n\n"
            "This Agreement is entered into by and between the parties identified below.\n\n"
            f"Parties:\n{parties}\n\n"
            "The parties agree as follows:\n"
            f"{terms_block}\n\n"
            "This draft is provided as an AI-assisted template and should be reviewed by a qualified legal professional before use."
        )

    def generate_document(self, *, document_type: str, parties: str, terms: str, effective_date: str) -> str:
        if not self.api_key or self.client is None:
            return self._fallback_document(
                document_type=document_type,
                parties=parties,
                terms=terms,
                effective_date=effective_date,
            )

        prompt = (
            "Draft a professional legal document in formal style. "
            f"Document type: {document_type}. "
            f"Effective date: {effective_date}. "
            f"Parties: {parties}. "
            f"Terms and conditions: {terms}. "
            "Return a clean, readable legal agreement with a title, parties section, terms section, and signature section. "
            "Keep it concise but complete and suitable for review by a legal professional."
        )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            return self._extract_text(response)
        except Exception:
            return self._fallback_document(
                document_type=document_type,
                parties=parties,
                terms=terms,
                effective_date=effective_date,
            )

    @staticmethod
    def _extract_text(response: Any) -> str:
        if hasattr(response, "text") and response.text:
            return str(response.text)

        if hasattr(response, "candidates"):
            for candidate in response.candidates:
                parts = getattr(candidate, "content", None)
                if parts is None:
                    continue
                text = getattr(parts, "parts", [])
                if not text:
                    continue
                for part in text:
                    value = getattr(part, "text", None)
                    if value:
                        return str(value)

        raise ValueError("No content returned by Gemini API.")
