"""
FastAPI application factory.

CORS origins are controlled via environment variables so the same
codebase works locally (localhost Streamlit) and in production
(Streamlit Cloud or any other frontend host).

Required env vars:
  GEMINI_API_KEY       — Google Gemini API key (required for AI generation)

Optional env vars:
  FRONTEND_URL         — Primary frontend origin added to CORS allow-list
                         (default: http://localhost:8501)
  ALLOWED_ORIGINS      — Comma-separated extra origins, e.g.:
                         https://your-app.streamlit.app,https://your-domain.com
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.routes import router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="LegalEase AI-powered legal document generation API.",
)

# ── CORS ─────────────────────────────────────────────────────────────────────
# Build the allowed-origins set from env vars.  The ALLOWED_ORIGINS variable
# accepts a comma-separated list so any number of extra origins (Streamlit
# Cloud URL, custom domain, etc.) can be added without code changes.
_extra = [
    o.strip()
    for o in os.getenv("ALLOWED_ORIGINS", "").split(",")
    if o.strip()
]

CORS_ORIGINS: list[str] = list(
    {
        settings.FRONTEND_URL,        # from FRONTEND_URL env var
        "http://localhost:8501",
        "http://127.0.0.1:8501",
        "http://localhost:3000",
        *_extra,
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Routes ───────────────────────────────────────────────────────────────────
@app.get("/")
def root() -> dict:
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "message": "LegalEase API is running.",
    }


@app.get("/health")
def health() -> dict:
    return {"status": "healthy"}


app.include_router(router)
