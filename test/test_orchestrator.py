import requests, json

URL = "http://127.0.0.1:8000/orchestrate"
samples = [
    {
      "session_id":"s_note",
      "user_info":{ "user_id":"u_note","name":"M","grade_level":"10","learning_style_summary":"bullet","emotional_state_summary":"ok","mastery_level_summary":"3"},
      "chat_history":[{"role":"user","content":"Please make notes on mitosis"}],
      "message":"Please make notes on mitosis",
      "target_tool":"note_maker"
    },
    {
      "session_id":"s_explain",
      "user_info":{ "user_id":"u_exp","name":"N","grade_level":"9","learning_style_summary":"story","emotional_state_summary":"curious","mastery_level_summary":"1"},
      "chat_history":[{"role":"user","content":"Explain photosynthesis"}],
      "message":"Explain photosynthesis",
      "target_tool":"concept_explainer"
    }
]

for s in samples:
    r = requests.post(URL, json=s)
    print("STATUS", r.status_code)
    print(json.dumps(r.json(), indent=2))
    print("-"*60)
