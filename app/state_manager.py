# Simple in-memory state manager (can later replace with Redis/MySQL)

_conversations = {}  # {user_id: [messages]}

def push_message(user_id: str, role: str, content: str):
    """Store a message in conversation history"""
    if user_id not in _conversations:
        _conversations[user_id] = []
    _conversations[user_id].append({"role": role, "content": content})

def get_conversation(user_id: str):
    """Retrieve conversation history"""
    return _conversations.get(user_id, [])

def clear_conversation(user_id: str):
    """Reset history for a user/session"""
    if user_id in _conversations:
        del _conversations[user_id]
