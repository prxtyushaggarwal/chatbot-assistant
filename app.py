import streamlit as st
from google import genai

st.set_page_config(page_title="Roxy-AI", page_icon="🤖", layout="wide")
st.title("🤖 Roxy-AI")

st.sidebar.header("API Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

st.sidebar.header("Model Settings")
temperature = st.sidebar.slider("Temperature", 0.0, 2.0, 1.0, 0.1)
top_p = st.sidebar.slider("Top P", 0.0, 1.0, 0.95, 0.05)
max_tokens = st.sidebar.number_input("Max Output Tokens", 100, 8192, 8192, 1000)

user_input = st.text_area("Enter your prompt:", height=150, placeholder="Ask anything...")

if st.button("Generate Response", type="primary"):
    if not api_key.strip():
        st.error("Please enter your API Key in the sidebar.")
    elif not user_input.strip():
        st.warning("Please enter a prompt.")
    else:
        try:
            client = genai.Client(api_key=api_key.strip())
            
            with st.spinner("Processing request..."):
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=user_input,
                    config={
                        'temperature': temperature,
                        'top_p': top_p,
                        'max_output_tokens': max_tokens,
                    }
                )
                
                st.subheader("Response")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
