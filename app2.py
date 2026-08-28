# python
import streamlit as st
from google import genai
from google.genai import types

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Pratyush AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>
        /* Main background */
        .stApp {
            background: #0b0f19;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: #111827;
            border-right: 1px solid #1f2937;
        }

        /* Main content width */
        .block-container {
            max-width: 1000px;
            padding-top: 2rem;
            padding-bottom: 7rem;
        }

        /* Header */
        .app-header {
            text-align: center;
            padding: 20px 0 30px 0;
        }

        .app-title {
            font-size: 38px;
            font-weight: 800;
            color: #f9fafb;
            margin-bottom: 5px;
        }

        .app-subtitle {
            color: #9ca3af;
            font-size: 15px;
        }

        /* Chat bubbles */
        .user-message {
            background: #1d4ed8;
            color: white;
            padding: 14px 18px;
            border-radius: 18px 18px 4px 18px;
            margin: 12px 0 12px auto;
            max-width: 80%;
            width: fit-content;
        }

        .assistant-message {
            background: #151b2b;
            color: #e5e7eb;
            border: 1px solid #273244;
            padding: 16px 20px;
            border-radius: 18px 18px 18px 4px;
            margin: 12px auto 12px 0;
            max-width: 85%;
        }

        .message-label {
            font-size: 12px;
            font-weight: 700;
            opacity: 0.65;
            margin-bottom: 6px;
        }

        /* Empty state */
        .empty-state {
            text-align: center;
            padding: 80px 20px 40px;
        }

        .empty-icon {
            font-size: 60px;
        }

        .empty-title {
            color: #f9fafb;
            font-size: 28px;
            font-weight: 700;
            margin-top: 15px;
        }

        .empty-text {
            color: #9ca3af;
            font-size: 15px;
        }

        /* Sidebar headings */
        .sidebar-title {
            font-size: 18px;
            font-weight: 700;
            color: #f9fafb;
            margin-bottom: 15px;
        }

        /* Status badge */
        .status {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 999px;
            background: #064e3b;
            color: #6ee7b7;
            font-size: 12px;
            font-weight: 600;
        }

        /* Remove excessive top spacing */
        div[data-testid="stChatMessage"] {
            background: transparent;
        }

        /* Buttons */
        .stButton > button {
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">⚙️ Configuration</div>',
        unsafe_allow_html=True,
    )

    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        value=st.session_state.api_key,
        placeholder="Paste your API key",
        help="Your API key is used only for requests from this Streamlit session.",
    )

    st.session_state.api_key = api_key

    st.divider()

    st.markdown(
        '<div class="sidebar-title">🧠 Model</div>',
        unsafe_allow_html=True,
    )

    model = st.selectbox(
        "Select model",
        [
            "gemini-3.6-flash",
            "gemini-3.6-pro",
        ],
        index=0,
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown(
        '<div class="sidebar-title">🎛️ Generation</div>',
        unsafe_allow_html=True,
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=1.0,
        step=0.1,
        help="Higher values make responses more creative/random.",
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
        min_value=100,
        max_value=8192,
        value=4096,
        step=500,
    )

    st.divider()

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.caption("🤖 Pratyush AI")
    st.caption("Powered by Google Gemini")


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="app-header">
        <div class="app-title">🤖 Pratyush AI</div>
        <div class="app-subtitle">
            Your intelligent Gemini-powered assistant
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# EMPTY STATE
# ---------------------------------------------------------

if not st.session_state.messages:

    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-icon">✨</div>
            <div class="empty-title">How can I help you?</div>
            <div class="empty-text">
                Ask me anything — coding, writing, research, ideas, explanations and more.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(
            "💻 Write Code",
            use_container_width=True,
        ):
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": "Write a Python program that explains recursion with an example.",
                }
            )
            st.rerun()

    with col2:
        if st.button(
            "🧠 Explain Something",
            use_container_width=True,
        ):
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": "Explain artificial intelligence in simple terms.",
                }
            )
            st.rerun()

    with col3:
        if st.button(
            "💡 Brainstorm",
            use_container_width=True,
        ):
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": "Give me 10 creative ideas for an AI-powered project.",
                }
            )
            st.rerun()


# ---------------------------------------------------------
# DISPLAY CHAT HISTORY
# ---------------------------------------------------------

for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message("user", avatar="👤"):
            st.markdown(message["content"])

    else:

        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(message["content"])


# ---------------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------------

prompt = st.chat_input(
    "Message Pratyush AI..."
)

if prompt:

    if not st.session_state.api_key.strip():

        st.error(
            "Please enter your Gemini API key in the sidebar."
        )
        st.stop()

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    # Display user message immediately
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    try:

        client = genai.Client(
            api_key=st.session_state.api_key.strip()
        )

        # Convert chat history into Gemini format
        contents = []

        for message in st.session_state.messages:

            role = (
                "user"
                if message["role"] == "user"
                else "model"
            )

            contents.append(
                types.Content(
                    role=role,
                    parts=[
                        types.Part.from_text(
                            text=message["content"]
                        )
                    ],
                )
            )

        # Generate response
        with st.chat_message("assistant", avatar="🤖"):

            with st.spinner("Thinking..."):

                response = client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        temperature=temperature,
                        top_p=top_p,
                        max_output_tokens=max_tokens,
                    ),
                )

                answer = response.text

                st.markdown(answer)

        # Save response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

    except Exception as e:

        st.error(
            f"Something went wrong:\n\n{str(e)}"
        )

