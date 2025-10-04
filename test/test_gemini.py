import requests
import json

URL = "http://127.0.0.1:8000/orchestrate"

# Sample request WITHOUT target_tool
# => lets Gemini LLM extractor decide which tool to use
payload = {
    "session_id": "gemini_test_01",
    "user_info": {
        "user_id": "student001",
        "name": "Alice",
        "grade_level": "12",
        "learning_style_summary": "Prefers step-by-step explanations",
        "emotional_state_summary": "motivated",
        "mastery_level_summary": "Level 2 - Foundation"
    },
    "chat_history": [
        {
            "role": "user",
            "content": "Explain photosynthesis with examples."
        }
    ],
    "message": "Explain photosynthesis with examples.",
    # target_tool intentionally omitted → Gemini should infer "concept_explainer"
    "teaching_style": "direct",
    "emotional_state": "curious",
    "mastery_level": 2,
    "preferred_tools": []
}

print("Sending request to orchestrator...")
r = requests.post(URL, json=payload)

print("\nSTATUS:", r.status_code)
try:
    data = r.json()
    print(json.dumps(data, indent=2))
except Exception as e:
    print("Failed to parse JSON:", e)
    print("Raw response:", r.text)
