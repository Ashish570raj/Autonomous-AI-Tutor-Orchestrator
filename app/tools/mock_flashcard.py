# mock_flashcard.py
from typing import Dict, Any
from ..schemas import FlashcardInput

def generate_flashcards(payload: FlashcardInput) -> Dict[str, Any]:
    cards = []
    for i in range(payload.count):
        cards.append({
            "title": payload.topic,
            "question": f"Q{i+1}: What about {payload.topic}?",
            "answer": f"A{i+1}: Short answer for {payload.topic}.",
            "example": "Example" if payload.include_examples else None
        })
    return {"flashcards": cards, "topic": payload.topic, "difficulty": payload.difficulty}
