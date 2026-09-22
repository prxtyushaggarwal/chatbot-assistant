import os
import streamlit as st
from google import genai
from google.genai import types

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Pratyush AI - Gemini Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# CUSTOM CSS / MODERN DARK GLASSMORPHISM
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Main background */
        .stApp {
            background: linear-gradient(135deg, #090d16 0%, #0f172a 50%, #0a0e1a 100%);
            color: #f3f4f6;
        }

        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(12px);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }

        /* Main content container */
        .block-container {
            max-width: 950px;
            padding-top: 1.5rem;
            padding-bottom: 6rem;
        }

        /* App Header */
        .app-header {
            text-align: center;
            padding: 10px 0 25px 0;
            margin-bottom: 10px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }

        .app-title {
            font-size: 2.4rem;
            font-weight: 800;
            background: linear-gradient(135deg, #60a5fa 0%, #a855f7 50%, #ec4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 6px;
            letter-spacing: -0.02em;
        }

        .app-subtitle {
            color: #94a3b8;
            font-size: 0.95rem;
            font-weight: 400;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-top: 8px;
        }
        .badge-online {
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }
        .badge-warning {
            background: rgba(245, 158, 11, 0.15);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }

        /* Starter cards */
        .starter-card {
            background: rgba(30, 41, 59, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 16px;
            text-align: left;
            transition: all 0.2s ease;
            cursor: pointer;
            margin-bottom: 10px;
        }
        .starter-card:hover {
            background: rgba(30, 41, 59, 0.85);
            border-color: rgba(96, 165, 250, 0.4);
            transform: translateY(-2px);
        }
        .starter-icon {
            font-size: 1.5rem;
            margin-bottom: 8px;
        }
        .starter-title {
            font-weight: 600;
            color: #e2e8f0;
            font-size: 0.95rem;
        }
        .starter-desc {
            font-size: 0.8rem;
            color: #94a3b8;
            margin-top: 4px;
        }

        /* Sidebar headers */
        .sidebar-heading {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #94a3b8;
            font-weight: 700;
            margin-bottom: 10px;
        }

        /* Buttons */
        .stButton > button {
            border-radius: 10px;
            font-weight: 500;
            transition: all 0.2s ease;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .stButton > button:hover {
            border-color: #60a5fa;
            box-shadow: 0 0 12px rgba(96, 165, 250, 0.25);
        }

        /* Chat messages styling */
        div[data-testid="stChatMessage"] {
            border-radius: 14px;
            padding: 12px 18px;
            margin-bottom: 12px;
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
            background: rgba(37, 99, 235, 0.15);
            border: 1px solid rgba(59, 130, 246, 0.25);
        }

        /* Code block styling */
        pre {
            border-radius: 10px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Detect API Key from environment or session state
default_api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
if "api_key" not in st.session_state:
    st.session_state.api_key = default_api_key

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# System personas
PERSONAS = {
    "Helpful AI Assistant": "You are Pratyush AI, a helpful, precise, friendly, and knowledgeable assistant powered by Google Gemini.",
    "Expert Software Engineer": "You are an expert senior software engineer. Provide robust, clean, well-documented code with concise explanations and best practices.",
    "Data Scientist & Analyst": "You are an expert data scientist and statistical analyst. Explain concepts clearly and write clean Python, pandas, and scikit-learn code.",
    "Creative Writer & Brainstormer": "You are a creative writer and ideation specialist. Provide innovative, engaging, and imaginative ideas.",
    "Custom Persona": "",
}

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-heading">🔑 Authentication</div>', unsafe_allow_html=True)
    
    api_key_input = st.text_input(
        "Gemini API Key",
        type="password",
        value=st.session_state.api_key,
        placeholder="AIzaSy...",
        help="Get your API key free from Google AI Studio: https://aistudio.google.com/app/apikey",
    )
    if api_key_input:
        st.session_state.api_key = api_key_input.strip()

    if st.session_state.api_key:
        st.markdown('<span class="badge badge-online">● API Key Connected</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge badge-warning">⚠ API Key Required</span>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    st.markdown('<div class="sidebar-heading">🧠 Model Selection</div>', unsafe_allow_html=True)
    model_options = [
        "gemini-3.6-Flash",
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "Custom Model ID",
    ]
    selected_model = st.selectbox(
        "Model",
        options=model_options,
        index=0,
        help="gemini-2.5-flash is fast, lightweight, and versatile.",
    )

    if selected_model == "Custom Model ID":
        custom_model = st.text_input("Enter Model Name", value="gemini-2.5-flash")
        active_model = custom_model.strip()
    else:
        active_model = selected_model

    st.divider()

    st.markdown('<div class="sidebar-heading">🎭 AI Persona</div>', unsafe_allow_html=True)
    persona_choice = st.selectbox("Persona", list(PERSONAS.keys()), index=0)
    
    if persona_choice == "Custom Persona":
        system_instruction = st.text_area(
            "Custom System Instruction",
            value="You are a helpful AI assistant.",
            height=100,
        )
    else:
        system_instruction = PERSONAS[persona_choice]

    st.divider()

    st.markdown('<div class="sidebar-heading">🎛️ Parameters</div>', unsafe_allow_html=True)
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.05,
        help="Higher values make output more creative; lower values make it more focused and deterministic.",
    )

    top_p = st.slider(
        "Top P",
        min_value=0.0,
        max_value=1.0,
        value=0.95,
        step=0.05,
    )

    max_tokens = st.number_input(
        "Max Output Tokens",
        min_value=256,
        max_value=8192,
        value=4096,
        step=512,
    )

    st.divider()

    # Chat Actions
    col_clear, col_export = st.columns(2)
    with col_clear:
        if st.button("🗑️ Clear", use_container_width=True, help="Clear chat history"):
            st.session_state.messages = []
            st.session_state.pending_prompt = None
            st.rerun()

    with col_export:
        if st.session_state.messages:
            # Prepare conversation as markdown
            chat_md = "# Conversation with Pratyush AI\n\n"
            for m in st.session_state.messages:
                speaker = "User" if m["role"] == "user" else "Pratyush AI"
                chat_md += f"### {speaker}:\n{m['content']}\n\n"
            st.download_button(
                "📥 Export",
                data=chat_md,
                file_name="pratyush_ai_conversation.md",
                mime="text/markdown",
                use_container_width=True,
                help="Download conversation as Markdown",
            )

    st.caption("🤖 **Pratyush AI** | Powered by Google GenAI SDK")

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown(
    f"""
    <div class="app-header">
        <div class="app-title">🤖 Pratyush AI</div>
        <div class="app-subtitle">
            Your intelligent assistant powered by Google Gemini (<code>{active_model}</code>)
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# EMPTY STATE & STARTERS
# ---------------------------------------------------------
if not st.session_state.messages:
    st.markdown(
        """
        <div style="text-align: center; margin: 30px 0 25px 0;">
            <p style="font-size: 1.25rem; font-weight: 600; color: #f1f5f9; margin-bottom: 6px;">
                How can I assist you today?
            </p>
            <p style="color: #94a3b8; font-size: 0.9rem;">
                Select a quick prompt below or type your question in the chat bar.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(
            "💻  Code Recursion\n\nWrite a clean Python program that demonstrates recursion with memoization.",
            use_container_width=True,
        ):
            st.session_state.pending_prompt = "Write a clean Python program that demonstrates recursion with memoization and visual explanations."
            st.rerun()

    with col2:
        if st.button(
            "🧠  Explain Concept\n\nExplain how Transformers and Large Language Models work in simple analogies.",
            use_container_width=True,
        ):
            st.session_state.pending_prompt = "Explain how Transformers and Large Language Models work using simple, intuitive analogies."
            st.rerun()

    with col3:
        if st.button(
            "💡  Brainstorm Ideas\n\nGive me 5 unique, high-impact AI project ideas for full-stack developers.",
            use_container_width=True,
        ):
            st.session_state.pending_prompt = "Give me 5 unique, high-impact AI project ideas suitable for modern full-stack web developers."
            st.rerun()

# ---------------------------------------------------------
# DISPLAY CHAT HISTORY
# ---------------------------------------------------------
for message in st.session_state.messages:
    role = message["role"]
    avatar = "👤" if role == "user" else "🤖"
    with st.chat_message(role, avatar=avatar):
        st.markdown(message["content"])

# ---------------------------------------------------------
# CHAT INPUT & EXECUTION
# ---------------------------------------------------------
user_input = st.chat_input("Message Pratyush AI...")

# Trigger on either chat_input or a clicked quick-start button
prompt_to_run = user_input or st.session_state.pending_prompt

if prompt_to_run:
    # Clear pending prompt so it doesn't trigger again on subsequent renders
    st.session_state.pending_prompt = None

    if not st.session_state.api_key.strip():
        st.error("⚠️ Please enter your Gemini API Key in the sidebar to begin.")
        st.info("You can get a free API key at [Google AI Studio](https://aistudio.google.com/app/apikey).")
        st.stop()

    # Append user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt_to_run,
    })

    # Render user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt_to_run)

    # Format history into Gemini types.Content
    contents = []
    for msg in st.session_state.messages:
        gemini_role = "user" if msg["role"] == "user" else "model"
        contents.append(
            types.Content(
                role=gemini_role,
                parts=[types.Part.from_text(text=msg["content"])],
            )
        )

    # Stream bot response
    with st.chat_message("assistant", avatar="🤖"):
        try:
            client = genai.Client(api_key=st.session_state.api_key.strip())

            config = types.GenerateContentConfig(
                temperature=temperature,
                top_p=top_p,
                max_output_tokens=max_tokens,
                system_instruction=system_instruction.strip() if system_instruction.strip() else None,
            )

            # Stream generator
            def stream_response():
                stream = client.models.generate_content_stream(
                    model=active_model,
                    contents=contents,
                    config=config,
                )
                for chunk in stream:
                    if chunk.text:
                        yield chunk.text

            # Stream with Streamlit's native write_stream
            full_response = st.write_stream(stream_response)

            # Save assistant message to session state
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response,
            })

        except Exception as e:
            error_message = f"❌ **Error generating response:**\n\n```\n{str(e)}\n```"
            st.markdown(error_message)
            st.caption("Please check your API key and model selection in the sidebar.")
