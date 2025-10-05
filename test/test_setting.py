from app.config import settings

print("Extractor mode:", settings.EXTRACTOR_MODE)
print("Gemini key exists?", bool(settings.GEMINI_API_KEY))
print("Model:", settings.LLM_MODEL)
