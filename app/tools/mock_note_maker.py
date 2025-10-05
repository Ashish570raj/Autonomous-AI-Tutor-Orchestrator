import json
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings

def note_maker_adapter(input):
    llm = ChatGoogleGenerativeAI(
        model=settings.LLM_MODEL,
        google_api_key=settings.GEMINI_API_KEY,
        temperature=0.5
    )

    prompt = f"""
    You are a study note maker.

    Create structured notes for the topic "{input.topic}" 
    (subject: {input.subject}, style: {input.note_taking_style}).

    Include:
    - summary
    - key concepts
    - note_sections with title, content, key_points
    - examples if requested
    - analogies if requested

    Return STRICT JSON ONLY in this format:
    {{
      "topic": "{input.topic}",
      "title": "...",
      "summary": "...",
      "note_sections": [
        {{
          "title": "...",
          "content": "...",
          "key_points": ["...", "..."],
          "examples": ["..."],
          "analogies": ["..."]
        }}
      ],
      "key_concepts": ["...", "..."],
      "note_taking_style": "{input.note_taking_style}"
    }}
    """

    try:
        response = llm.invoke(prompt)
        text = response.content.strip()
        return json.loads(text)
    except Exception as e:
        print("[Note maker parse error]", e)
        # fallback safe output
        return {
            "topic": input.topic,
            "title": f"{input.topic} — Notes",
            "summary": f"Could not generate full notes, but here’s a summary placeholder.",
            "note_sections": [],
            "key_concepts": [],
            "note_taking_style": input.note_taking_style
        }
