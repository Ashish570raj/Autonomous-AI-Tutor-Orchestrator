from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Any

class ChatMessage(BaseModel):
    role: Literal["user","assistant"]
    content: str

class UserInfo(BaseModel):
    user_id: str
    name: str
    grade_level: str
    learning_style_summary: str
    emotional_state_summary: str
    mastery_level_summary: str

# --- Note Maker Input (per PDF) ---
class NoteMakerInput(BaseModel):
    user_info: UserInfo
    chat_history: List[ChatMessage]
    topic: str
    subject: str
    note_taking_style: Literal["outline","bullet_points","narrative","structured"]
    include_examples: Optional[bool] = True
    include_analogies: Optional[bool] = False

# --- Flashcard Generator Input ---
class FlashcardInput(BaseModel):
    user_info: UserInfo
    topic: str
    count: int = Field(..., ge=1, le=20)
    difficulty: Literal["easy","medium","hard"]
    include_examples: Optional[bool] = True
    subject: str

# --- Concept Explainer Input ---
class ConceptExplainerInput(BaseModel):
    user_info: UserInfo
    chat_history: List[ChatMessage]
    concept_to_explain: str
    current_topic: str
    desired_depth: Literal["basic","intermediate","advanced","comprehensive"]

# Orchestrator request wrapper
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
