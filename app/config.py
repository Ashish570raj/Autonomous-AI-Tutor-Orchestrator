import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    EXTRACTOR_MODE: str = os.getenv("EXTRACTOR_MODE", "rule")  # "rule" or "llm"
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")  # adapt as needed
    # Postgres optional
    DATABASE_URL: str | None = os.getenv("DATABASE_URL")

settings = Settings()
