"""
Application settings loaded from environment variables.

Local development: copy .env.example → .env and fill in values.
Production (Vercel): set variables in Vercel Project Settings → Environment Variables.
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Safe no-op on Vercel (env vars are injected directly).
# Loads .env when running locally.
load_dotenv()

_VALID_GEMINI_MODELS = frozenset(
    [
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
    ]
)


@dataclass(frozen=True)
class Settings:
    APP_NAME: str = "LegalEase"
    APP_VERSION: str = "1.0.0"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"
    # Set FRONTEND_URL in Vercel env vars to your Streamlit Cloud URL.
    # Example: https://your-app.streamlit.app
    FRONTEND_URL: str = "http://localhost:8501"
    LEGALEASE_API_URL: str = "http://127.0.0.1:8000"
    BACKEND_HOST: str = "127.0.0.1"
    BACKEND_PORT: int = 8000

    @classmethod
    def load(cls) -> "Settings":
        # Guard: ensure GEMINI_MODEL is a non-empty recognised value.
        model_name = (os.getenv("GEMINI_MODEL") or "").strip()
        if model_name not in _VALID_GEMINI_MODELS:
            model_name = cls.GEMINI_MODEL  # fall back to default

        # Guard: BACKEND_PORT must be a valid integer.
        try:
            backend_port = int(os.getenv("BACKEND_PORT", str(cls.BACKEND_PORT)))
        except ValueError:
            backend_port = cls.BACKEND_PORT

        return cls(
            APP_NAME=os.getenv("APP_NAME", cls.APP_NAME),
            APP_VERSION=os.getenv("APP_VERSION", cls.APP_VERSION),
            GEMINI_API_KEY=(os.getenv("GEMINI_API_KEY") or "").strip(),
            GEMINI_MODEL=model_name,
            FRONTEND_URL=(os.getenv("FRONTEND_URL") or cls.FRONTEND_URL).strip(),
            LEGALEASE_API_URL=(
                os.getenv("LEGALEASE_API_URL") or cls.LEGALEASE_API_URL
            ).strip(),
            BACKEND_HOST=(os.getenv("BACKEND_HOST") or cls.BACKEND_HOST).strip(),
            BACKEND_PORT=backend_port,
        )


settings = Settings.load()
