import os
import streamlit as st
from google import genai

# Page configuration
st.set_page_config(page_title="Gemini Web Interface", page_icon="🤖", layout="wide")
st.title("🤖 Gemini 3.1 Pro Web Interface")

# Initialize GenAI Client
@st.cache_resource
def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        st.error("GEMINI_API_KEY environment variable is missing!")
        st.stop()
    return genai.Client(api_key=api_key)

client = get_client()

# Sidebar configuration
st.sidebar.header("Model Settings")

temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=2.0, value=1.0, step=0.1)
top_p = st.sidebar.slider("Top P", min_value=0.0, max_value=1.0, value=0.95, step=0.05)
max_tokens = st.sidebar.number_input("Max Output Tokens", min_value=100, max_value=65536, value=65536, step=1000)
thinking_level = st.sidebar.selectbox("Thinking Level", ["low", "medium", "high"], index=2)

st.sidebar.header("Tools")
enable_search = st.sidebar.checkbox("Google Search", value=True)
enable_url_context = st.sidebar.checkbox("URL Context", value=True)

# User Input
user_input = st.text_area("Enter your prompt:", height=150, placeholder="Ask anything...")

if st.button("Generate Response", type="primary"):
    if not user_input.strip():
        st.warning("Please enter a prompt before submitting.")
    else:
        # Build tools dynamically based on user selection
        tools = []
        if enable_search:
            tools.append({'type': 'google_search'})
        if enable_url_context:
            tools.append({'type': 'url_context'})

        # Generation config from sidebar controls
        generation_config = {
            'temperature': temperature,
            'max_output_tokens': max_tokens,
            'top_p': top_p,
            'thinking_level': thinking_level,
        }

        with st.spinner("Processing request..."):
            try:
                interaction = client.interactions.create(
                    model='models/gemini-3.1-pro-preview',
                    input=user_input,
                    tools=tools,
                    generation_config=generation_config,
                )
                
                # Render output
                st.subheader("Response")
                st.write(interaction.steps[-1])
                
            except Exception as e:
                st.error(f"An error occurred: {e}")