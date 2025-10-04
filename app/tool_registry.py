from typing import Dict, Callable
from .schemas import NoteMakerInput, FlashcardInput, ConceptExplainerInput

TOOL_REGISTRY: Dict[str, Dict] = {}

def register_tool(name: str, schema, adapter: Callable):
    TOOL_REGISTRY[name] = {"schema": schema, "adapter": adapter}

def get_tool(name: str):
    return TOOL_REGISTRY.get(name)
