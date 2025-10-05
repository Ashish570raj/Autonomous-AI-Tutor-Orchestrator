import json
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings

def flashcard_adapter(input):
    llm = ChatGoogleGenerativeAI(
        model=settings.LLM_MODEL,
        google_api_key=settings.GEMINI_API_KEY,
        temperature=0.5
    )

    prompt = f"""
    You are a flashcard generator for students.

    Create exactly {input.count} flashcards on the topic "{input.topic}" 
    (subject: {input.subject}, difficulty: {input.difficulty}).

    Each flashcard must include:
    - title (same as topic)
    - question (short, clear)
    - answer (concise, accurate)
    - example (if {input.include_examples})

    Return STRICT JSON ONLY in this format:
    {{
      "flashcards": [
        {{
          "title": "{input.topic}",
          "question": "...",
          "answer": "...",
          "example": "..."
        }}
      ],
      "topic": "{input.topic}",
      "difficulty": "{input.difficulty}"
    }}
    """

    try:
        response = llm.invoke(prompt)
        text = response.content.strip()
        return json.loads(text)
    except Exception as e:
        print("[Flashcard parse error]", e)
        return {
            "flashcards": [
                {
                    "title": input.topic,
                    "question": "Parsing failed",
                    "answer": "",
                    "example": ""
                }
            ],
            "topic": input.topic,
            "difficulty": input.difficulty
        }
