from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    EXTRACTOR_MODE: str = "rule"   # default is "rule", can be overridden by env
    GEMINI_API_KEY: str            # required
    LLM_MODEL: str = "gemini-2.5-flash"  # or "gemini-1.5-flash", etc.
    DATABASE_URL: str | None = None  # optional

    class Config:
        env_file = ".env"

settings = Settings()
