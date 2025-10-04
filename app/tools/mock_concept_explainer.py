# mock_concept_explainer.py
from typing import Dict, Any
from ..schemas import ConceptExplainerInput

def explain_concept(payload: ConceptExplainerInput) -> Dict[str, Any]:
    return {
        "explanation": f"{payload.concept_to_explain} explained at {payload.desired_depth} depth.",
        "examples": [f"Example illustrating {payload.concept_to_explain}"],
        "related_concepts": ["related1","related2"],
        "practice_questions": ["Practice Q1", "Practice Q2"]
    }
