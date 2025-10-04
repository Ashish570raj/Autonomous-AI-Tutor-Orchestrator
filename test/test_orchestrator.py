from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_note_maker_flow():
    payload = {
      "user_info": {
        "user_id": "student1",
        "name": "Sam",
        "grade_level": "10",
        "learning_style_summary": "prefers outlines",
        "emotional_state_summary": "focused",
        "mastery_level_summary": "Level 3 - building"
      },
      "chat_history": [{"role":"user","content":"I need notes on the Water Cycle"}],
      "message": "I need notes on the Water Cycle"
    }
    resp = client.post("/orchestrate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["tool"] == "note_maker"
    assert "result" in data
