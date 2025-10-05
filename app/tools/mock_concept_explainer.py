import json
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings

def concept_explainer_adapter(input):
    llm = ChatGoogleGenerativeAI(
        model=settings.LLM_MODEL,
        google_api_key=settings.GEMINI_API_KEY,
        temperature=0.5
    )

    prompt = f"""
    You are a concept explainer for students.

    Explain the concept "{input.concept_to_explain}" (topic: {input.current_topic}) 
    at "{input.desired_depth}" depth.

    Include:
    - explanation
    - examples
    - related_concepts
    - practice_questions

    Return STRICT JSON ONLY in this format:
    {{
      "explanation": "...",
      "examples": ["...", "..."],
      "related_concepts": ["...", "..."],
      "practice_questions": ["...", "..."]
    }}
    """

    try:
        response = llm.invoke(prompt)
        text = response.content.strip()
        return json.loads(text)
    except Exception as e:
        print("[Concept explainer parse error]", e)
        return {
            "explanation": f"Fallback explanation for {input.concept_to_explain}",
            "examples": [],
            "related_concepts": [],
            "practice_questions": []
        }
