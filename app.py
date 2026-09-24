import os
import streamlit as st
from google import genai
from google.genai import types

# Backend Gemini API Key (loaded from environment or .env file)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

st.set_page_config(
    page_title="Pratyush AI - Gemini Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .stApp { background: linear-gradient(135deg, #090d16 0%, #0f172a 50%, #0a0e1a 100%); color: #f3f4f6; }
        section[data-testid="stSidebar"] { background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(12px); border-right: 1px solid rgba(255, 255, 255, 0.08); }
        .block-container { max-width: 950px; padding-top: 1.5rem; padding-bottom: 6rem; }
        .app-title { font-size: 2.4rem; font-weight: 800; background: linear-gradient(135deg, #60a5fa 0%, #a855f7 50%, #ec4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; }
        div[data-testid="stChatMessage"] { border-radius: 14px; padding: 12px 18px; margin-bottom: 12px; background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255, 255, 255, 0.05); }
    </style>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

PERSONAS = {
    "Helpful AI Assistant": "You are Pratyush AI, a helpful, precise, friendly assistant.",
    "Expert Software Engineer": "You are an expert senior software engineer. Provide robust code with concise explanations.",
    "Data Scientist": "You are an expert data scientist. Explain concepts clearly and write clean Python code.",
}

with st.sidebar:
    st.markdown("### 🧠 Model Selection")
    active_model = st.selectbox("Model", ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"], index=0)
    persona_choice = st.selectbox("Persona", list(PERSONAS.keys()), index=0)
    system_instruction = PERSONAS[persona_choice]
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.05)
    max_tokens = st.number_input("Max Output Tokens", 256, 8192, 4096, 512)
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()

st.markdown('<div class="app-title">🤖 Pratyush AI</div>', unsafe_allow_html=True)
st.caption("<center>Powered by Google Gemini</center>", unsafe_allow_html=True)

if not st.session_state.messages:
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💻  Code Recursion", use_container_width=True):
            st.session_state.pending_prompt = "Write a clean Python program that demonstrates recursion with memoization."
            st.rerun()
    with col2:
        if st.button("🧠  Explain Concept", use_container_width=True):
            st.session_state.pending_prompt = "Explain how Transformers and Large Language Models work in simple analogies."
            st.rerun()
    with col3:
        if st.button("💡  Brainstorm Ideas", use_container_width=True):
            st.session_state.pending_prompt = "Give me 5 unique, high-impact AI project ideas for full-stack developers."
            st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

user_input = st.chat_input("Message Pratyush AI...")
prompt_to_run = user_input or st.session_state.pending_prompt

if prompt_to_run:
    st.session_state.pending_prompt = None
    st.session_state.messages.append({"role": "user", "content": prompt_to_run})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt_to_run)

    contents = [
        types.Content(
            role="user" if m["role"] == "user" else "model",
            parts=[types.Part.from_text(text=m["content"])],
        )
        for m in st.session_state.messages
    ]

    with st.chat_message("assistant", avatar="🤖"):
        generated = False
        if GEMINI_API_KEY.startswith("AIzaSy"):
            try:
                client = genai.Client(api_key=GEMINI_API_KEY)
                config = types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                    system_instruction=system_instruction,
                )
                def stream_response():
                    stream = client.models.generate_content_stream(model=active_model, contents=contents, config=config)
                    for chunk in stream:
                        if chunk.text:
                            yield chunk.text
                full_response = st.write_stream(stream_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                generated = True
            except Exception:
                generated = False

        if not generated:
            from server import generate_smart_response
            reply = generate_smart_response(prompt_to_run)
            def stream_local():
                import time
                words = reply.split(" ")
                for i, w in enumerate(words):
                    yield w + (" " if i < len(words) - 1 else "")
                    time.sleep(0.015)
            full_response = st.write_stream(stream_local)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
