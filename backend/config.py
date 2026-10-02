import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    APP_NAME: str = "LegalEase"
    APP_VERSION: str = "1.0.0"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"
    FRONTEND_URL: str = "http://localhost:8501"
    LEGALEASE_API_URL: str = "http://127.0.0.1:8000"
    BACKEND_HOST: str = "127.0.0.1"
    BACKEND_PORT: int = 8000

    @classmethod
    def load(cls) -> "Settings":
        model_name = os.getenv("GEMINI_MODEL", cls.GEMINI_MODEL)
        if model_name.startswith("gemini-3"):
            model_name = "gemini-2.5-flash"

        return cls(
            APP_NAME=os.getenv("APP_NAME", cls.APP_NAME),
            APP_VERSION=os.getenv("APP_VERSION", cls.APP_VERSION),
            GEMINI_API_KEY=os.getenv("GEMINI_API_KEY", cls.GEMINI_API_KEY),
            GEMINI_MODEL=model_name,
            FRONTEND_URL=os.getenv("FRONTEND_URL", cls.FRONTEND_URL),
            LEGALEASE_API_URL=os.getenv("LEGALEASE_API_URL", cls.LEGALEASE_API_URL),
            BACKEND_HOST=os.getenv("BACKEND_HOST", cls.BACKEND_HOST),
            BACKEND_PORT=int(os.getenv("BACKEND_PORT", str(cls.BACKEND_PORT))),
        )


settings = Settings.load()
