from .parameter_extractor import extract_params
from .tool_registry import get_tool
from .state_manager import push_message, get_conversation
from .schemas import OrchestratorRequest
from pydantic import ValidationError,BaseModel,Field
from typing import List, Optional, Literal, Any
from .schemas import UserInfo, ChatMessage

class OrchestrationError(Exception):
    """Raised when orchestration fails"""
    pass

# --- Orchestrator request wrapper (extended version) ---
class OrchestratorRequest(BaseModel):
    session_id: Optional[str] = None
    user_info: UserInfo
    chat_history: List[ChatMessage]
    message: str
    target_tool: Optional[str] = None
    teaching_style: Optional[str] = "direct"
    emotional_state: Optional[str] = None
    mastery_level: Optional[int] = None
    preferred_tools: Optional[List[str]] = []


def orchestrate(req: OrchestratorRequest):
    # store incoming message
    push_message(req.user_info.user_id, "user", req.message)

    # get full conversation history for this user
    full_history = get_conversation(req.user_info.user_id)

    # extract params + tool suggestion (using full history)
    extracted = extract_params(req.message, full_history)
    selected_tool = req.target_tool or extracted.get("tool")
    if not selected_tool:
        raise OrchestrationError("No tool selected or inferred.")

    reg = get_tool(selected_tool)
    if not reg:
        raise OrchestrationError(f"Tool {selected_tool} not registered.")

    schema = reg["schema"]
    adapter = reg["adapter"]

    # Build payload dict
    payload = {}
    payload["user_info"] = req.user_info.dict()
    payload["chat_history"] = full_history

    # Fill tool-specific
    if selected_tool == "note_maker":
        payload["topic"] = extracted.get("topic") or "General"
        payload["subject"] = extracted.get("subject") or "General"
        payload["note_taking_style"] = extracted.get("note_taking_style") or "structured"
        payload["include_examples"] = extracted.get("include_examples", True)
        payload["include_analogies"] = extracted.get("include_analogies", False)
    elif selected_tool == "flashcard_generator":
        payload["topic"] = extracted.get("topic") or "General"
        payload["count"] = extracted.get("num_questions") or 5
        payload["difficulty"] = extracted.get("difficulty") or "medium"
        payload["include_examples"] = extracted.get("include_examples", True)
        payload["subject"] = extracted.get("subject") or "General"
    elif selected_tool == "concept_explainer":
        payload["concept_to_explain"] = extracted.get("topic") or "General"
        payload["current_topic"] = extracted.get("subject") or "General"
        payload["desired_depth"] = extracted.get("desired_depth") or "basic"

    # Validate payload
    try:
        validated = schema(**payload)
    except ValidationError as e:
        raise OrchestrationError(f"Validation error: {e}")

    # Call adapter
    try:
        result = adapter(validated)
    except Exception as e:
        raise OrchestrationError(f"Tool call failed: {e}")

    # push assistant message (summary)
    push_message(req.user_info.user_id, "assistant", f"Tool {selected_tool} executed")

    return {"tool": selected_tool, "request": payload, "result": result}
 