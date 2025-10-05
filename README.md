# 🎓 Autonomous AI Tutor Orchestrator

An **AI-powered tutoring backend** that dynamically selects the best teaching tool (notes, flashcards, or concept explanations) for a student query.
Built with **FastAPI**, **Pydantic**, and **Gemini AI** for parameter extraction & content generation.

---

## 🚀 Features

* **Tool Orchestration**: Routes student queries to the right tool (note maker, flashcard generator, or concept explainer).
* **Parameter Extraction**: Uses either:

  * Rule-based extraction (regex + heuristics)
  * **Gemini AI** (LLM-powered extraction)
* **Conversation Management**: In-memory conversation history (can be extended with MySQL).
* **Schemas & Validation**: Strict input/output models with Pydantic.
* **Mock Tool Adapters**: Generate placeholder flashcards, notes, or explanations (can be upgraded with real Gemini calls).
* **REST API**: `/orchestrate` endpoint tested via Swagger UI, curl, and Python test scripts.

---

## 🛠️ Tech Stack

* **Backend**: FastAPI, Uvicorn
* **AI/LLM**: Google Gemini (via LangChain integration)
* **Validation**: Pydantic v2
* **Testing**: Python requests, curl
* **State**: In-memory (extensible to MySQL/Redis)

---

## 📂 Project Structure

```
autotutor-orchestrator/
│── app/
│   ├── main.py              # FastAPI entrypoint
│   ├── orchestrator.py      # Core orchestration logic
│   ├── schemas.py           # Pydantic schemas
│   ├── parameter_extractor.py # Rule & Gemini-based extraction
│   ├── tool_registry.py     # Tool definitions
│   ├── state_manager.py     # Conversation state
│   └── tools/
│       ├── mock_note_maker.py
│       ├── mock_flashcard_generator.py
│       └── mock_concept_explainer.py
│
│── test/
│   ├── test_orchestrator.py
│   ├── test_gemini.py
│   └── test_setting.py
│
│── .env                     # API keys & config
│── requirements.txt
│── README.md
```

---

## ⚙️ Setup & Installation

1. **Clone the repo**

```bash
git clone https://github.com/your-username/autotutor-orchestrator.git
cd autotutor-orchestrator
```

2. **Create virtual environment**

```bash
python -m venv orchenv
source orchenv/bin/activate   # (Linux/Mac)
orchenv\Scripts\activate      # (Windows)
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment**
   Create a `.env` file:

```ini
GEMINI_API_KEY="your-gemini-key"
EXTRACTOR_MODE="llm"   # or "rule"
```

---

## ▶️ Run the API

```bash
uvicorn app.main:app --reload --port 8000
```

API available at: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## 🧪 Testing

Run tests:

```bash
python test/test_orchestrator.py
python test/test_gemini.py
```

Example curl request:

```bash
curl -X POST "http://127.0.0.1:8000/orchestrate" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "s1",
    "user_info": {
      "user_id": "u1",
      "name": "Alice",
      "grade_level": "11",
      "learning_style_summary": "visual",
      "emotional_state_summary": "curious",
      "mastery_level_summary": "Level 2"
    },
    "chat_history": [{"role": "user", "content": "Explain photosynthesis"}],
    "message": "Explain photosynthesis",
    "target_tool": null
  }'
```

---

## ✅ Current Status

* Orchestrator working ✅
* Gemini extraction integrated ✅
* Mock tool outputs ✅
* In-memory state ✅
* UI (Streamlit) optional

---

## 📌 Future Work

* Replace mock adapters with **real Gemini outputs**.
* Add **persistent storage** (MySQL/Redis).
* Improve **evaluation & feedback** (student ratings).
* Deploy via **Docker + cloud hosting**.

---

## 📜 License

MIT License © 2025
