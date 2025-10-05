import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/orchestrate"

st.set_page_config(page_title="AI Tutor", page_icon="🎓")

# --- Custom CSS to reduce spacing ---
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎓 AI Tutor Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat history with Streamlit’s chat UI
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# Chat input at the bottom
if prompt := st.chat_input("Type your message..."):
    # show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Prepare payload
    payload = {
        "session_id": "ui1",
        "user_info": {
            "user_id": "s_ui",
            "name": "Student",
            "grade_level": "11",
            "learning_style_summary": "visual",
            "emotional_state_summary": "ok",
            "mastery_level_summary": "Level 2",
        },
        "chat_history": st.session_state.messages,
        "message": prompt,
        "target_tool": None,
    }

    try:
        res = requests.post(API_URL, json=payload)
        data = res.json()
        answer = data.get("result", data)  # show result only
    except Exception as e:
        answer = f"Error: {e}"

    # show assistant message
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)
