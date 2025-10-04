import re, json
from typing import Dict, Any, Tuple, List
from .config import settings

# RULE-BASED extractor (quick & deterministic)
def rule_extract(message: str, chat_history: List[Dict]) -> Dict[str, Any]:
    m = message.lower()
    result = {}
    # simple tool selection
    if any(w in m for w in ["flashcard","flashcards","cards"]):
        result["tool"] = "flashcard_generator"
    elif any(w in m for w in ["note","notes","summarize"]):
        result["tool"] = "note_maker"
    elif any(w in m for w in ["explain","explain to me","what is","concept"]):
        result["tool"] = "concept_explainer"
    elif "practice" in m or "problem" in m or "questions" in m:
        result["tool"] = "flashcard_generator"
    else:
        result["tool"] = "concept_explainer"  # default fallback

    # extract topic: nearest noun phrase heuristic (very simple)
    topic = None
    # look for "with {topic}" or "about {topic}" or first noun sequence
    match = re.search(r"(about|on|with|for)\s+([a-z0-9\s]+)", m)
    if match:
        topic = match.group(2).strip()
    else:
        # fallback: last two words
        words = [w for w in re.findall(r"[a-z0-9]+", m)]
        topic = " ".join(words[-2:]) if words else "general"

    result["topic"] = topic

    # difficulty inference
    if any(w in m for w in ["struggling","hard","difficult","can't"]):
        diff = "easy"
    elif any(w in m for w in ["medium","ok","moderate"]):
        diff = "medium"
    else:
        diff = "medium"
    result["difficulty"] = diff

    # question type & num_questions
    result["question_type"] = "practice" if "practice" in m else "assessment"
    num_match = re.search(r"(\d+)\s+(questions|problems|flashcards|cards)", m)
    result["num_questions"] = int(num_match.group(1)) if num_match else None

    return result

# LLM-based extractor using LangChain/OpenAI
def llm_extract(message: str, chat_history: List[Dict]) -> Dict[str, Any]:
    from langchain.llms import OpenAI
    from langchain.prompts import PromptTemplate

    # Prompt: ask model to output strict JSON with only these keys
    prompt_template = """
You are an assistant that extracts parameters for educational tools.
Return only valid JSON (no extra text) with keys:
tool, topic, subject (if inferable), difficulty (easy|medium|hard), question_type, num_questions (int or null).
User message: {message}
Conversation history: {history}
"""
    history_text = "\n".join([f"{m['role']}: {m['content']}" for m in chat_history])
    prompt = prompt_template.format(message=message, history=history_text)

    llm = OpenAI(openai_api_key=settings.OPENAI_API_KEY, model=settings.LLM_MODEL, temperature=0)
    completion = llm(prompt)
    try:
        parsed = json.loads(completion)
        return parsed
    except Exception:
        # best-effort: fall back to rule
        return rule_extract(message, chat_history)

def extract_params(message: str, chat_history: List[Dict]) -> Dict[str, Any]:
    if settings.EXTRACTOR_MODE == "llm" and settings.OPENAI_API_KEY:
        return llm_extract(message, chat_history)
    else:
        return rule_extract(message, chat_history)
