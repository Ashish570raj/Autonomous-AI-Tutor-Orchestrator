from typing import Dict, Any
import time

_SESSIONS: Dict[str, Dict[str, Any]] = {}

def create_or_get_session(user_id: str) -> Dict[str, Any]:
    s = _SESSIONS.get(user_id)
    if not s:
        s = {"user_id": user_id, "created_at": time.time(), "conversation": [], "meta": {}}
        _SESSIONS[user_id] = s
    return s

def push_message(user_id: str, role: str, content: str):
    s = create_or_get_session(user_id)
    s["conversation"].append({"role": role, "content": content, "ts": time.time()})

def get_conversation(user_id: str):
    s = create_or_get_session(user_id)
    return s["conversation"]

# Optional: functions to persist/retrieve from Postgres using SQLAlchemy/SQLModel (left as to-do)
