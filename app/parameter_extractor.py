import re
import json
from typing import Dict, Any, List
from .config import settings

# ---------- CLEANUP UTILITY ----------
def clean_topic(topic: str) -> str:
    if not topic:
        return "General"

    topic = topic.strip()

    fillers = ["please", "with examples", "can you", "give me", "i need"]
    for f in fillers:
        topic = re.sub(rf"\b{f}\b", "", topic, flags=re.IGNORECASE).strip()

    # If it's still just "explain", default back to General
    if topic.lower() in ["", "explain", "general"]:
        return "General"

    return topic.capitalize()


# ---------- RULE-BASED extractor ----------
def rule_extract(message: str, chat_history: List[Dict]) -> Dict[str, Any]:
    m = message.lower()
    result = {}

    # Detect tool
    if any(w in m for w in ["flashcard", "cards", "practice", "problems"]):
        result["tool"] = "flashcard_generator"
    elif any(w in m for w in ["note", "notes", "summarize"]):
        result["tool"] = "note_maker"
    elif any(w in m for w in ["explain", "concept", "teach", "understand"]):
        result["tool"] = "concept_explainer"
    else:
        result["tool"] = "concept_explainer"  # fallback

    # Extract topic
    topic_match = re.search(r"(about|on|for)\s+([a-z0-9\s]+)", m)
    if topic_match:
        topic = topic_match.group(2).strip()
    else:
        words = re.findall(r"[a-z0-9]+", m)
        topic = " ".join(words[-2:]) if words else "general"

    result["topic"] = clean_topic(topic)

    # Difficulty
    if "struggle" in m or "hard" in m or "difficult" in m:
        result["difficulty"] = "easy"
    elif "medium" in m or "okay" in m:
        result["difficulty"] = "medium"
    else:
        result["difficulty"] = "medium"

    # Number of questions
    num_match = re.search(r"(\d+)\s+(questions|problems|flashcards|cards)", m)
    result["num_questions"] = int(num_match.group(1)) if num_match else 5

    return result


# ---------- GEMINI-based extractor ----------
def gemini_extract(message: str, chat_history: List[Dict]) -> Dict[str, Any]:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.schema import HumanMessage, SystemMessage

    llm = ChatGoogleGenerativeAI(
        model=settings.LLM_MODEL,
        google_api_key=settings.GEMINI_API_KEY,
        temperature=0
    )

    prompt = f"""
You are a parameter extraction assistant for an autonomous AI tutor.

From the given user message, extract ONLY the requested fields and return STRICT JSON (no explanation).

Rules:
- Extract only the MAIN academic concept as "topic" (e.g., "photosynthesis", "derivatives"). 
- Do NOT include verbs like "explain", "make", "give me".
- If "subject" is not explicitly mentioned (like math, biology), return null.
- If "num_questions" is not specified, return null.
- Difficulty defaults to "medium" if not clearly mentioned.
- If user asks for practice/exercises, set "question_type": "practice".
- If user asks for assessment/test/quiz, set "question_type": "assessment".
- If not mentioned, set "question_type": null.

Return JSON ONLY in this format:
{{
  "tool": one of ["note_maker", "flashcard_generator", "concept_explainer"],
  "topic": string,
  "subject": string or null,
  "difficulty": one of ["easy", "medium", "hard"],
  "question_type": one of ["practice", "assessment", null],
  "num_questions": integer or null
}}

User message: "{message}"
Chat history (for context): {chat_history}
    """

    messages = [
        SystemMessage(content="You output strictly valid JSON. Do not explain."),
        HumanMessage(content=prompt)
    ]

    try:
        response = llm.invoke(messages)
        text = response.content.strip()
        parsed = json.loads(text)

        # cleanup topic
        parsed["topic"] = clean_topic(parsed.get("topic", ""))

        return parsed
    except Exception as e:
        print(f"[Gemini extractor error] {e}")
        # fallback to rule-based extraction
        return rule_extract(message, chat_history)


# ---------- MAIN entry ----------
def extract_params(message: str, chat_history: List[Dict]) -> Dict[str, Any]:
    """
    Automatically choose rule-based or Gemini-based extraction.
    """
    if settings.EXTRACTOR_MODE == "llm" and settings.GEMINI_API_KEY:
        return gemini_extract(message, chat_history)
    else:
        return rule_extract(message, chat_history)
