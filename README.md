# 🤖 Sachi Priya AI — Intelligent Gemini Chatbot

A high-performance, modern conversational AI assistant powered by **Google Gemini** (via the official `google-genai` SDK).

The project offers **two distinct ways** to run your chatbot:
1. **Streamlit Application (`app.py` / `app2.py`)**: Instant interactive UI with full chat streaming, customizable personas, parameter tuning, and markdown download.
2. **Full-Stack Web App (`server.py` + `index.html`)**: FastAPI backend with SSE (Server-Sent Events) streaming + responsive dark glassmorphism web interface featuring syntax-highlighted code blocks, copy-to-clipboard buttons, settings drawer, and prompt chips.

---

## ✨ Features

- ⚡ **Real-Time Token Streaming**: Watch responses generate smoothly in real time.
- 🧠 **Latest Gemini Models**:
  - `gemini-2.5-flash` (Default — fast, highly intelligent, lightweight)
  - `gemini-2.5-pro` (Deep reasoning & complex tasks)
  - `gemini-2.0-flash`
  - `gemini-1.5-flash` & `gemini-1.5-pro`
- 🎨 **Modern Dark Glassmorphism UI**: High-contrast, responsive slate-theme layout that looks great on both desktop and mobile.
- 💻 **Syntax Highlighting & Code Copy**: Instant copy button for code snippets with language badges.
- 🎭 **AI Personas**: Easily switch between Senior Software Engineer, Data Scientist, Creative Brainstormer, or Custom system instructions.
- 📥 **Export Chat**: Download the entire conversation as clean Markdown at any time.
- 🔑 **Flexible API Key Management**:
  - Automatically reads `GEMINI_API_KEY` from system environment variables.
  - Or enter your key directly into the UI (saved in session / browser `localStorage`).

---

## 🚀 Quick Start

### 1. Prerequisites & Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/prxtyushaggarwal/chatbot.git
cd chatbot
pip install -r requirements.txt
```

### 2. Get Your Free Gemini API Key

Obtain your API key for free at [Google AI Studio](https://aistudio.google.com/app/apikey).

*(Optional)* Set it in your environment:
- **Windows (PowerShell)**:
  ```powershell
  $env:GEMINI_API_KEY="your-api-key-here"
  ```
- **macOS / Linux**:
  ```bash
  export GEMINI_API_KEY="your-api-key-here"
  ```

---

## 🏃 Running the Application

### Option A: Streamlit Chatbot

Run the Streamlit application with:

```bash
streamlit run app.py
```
*(or `streamlit run app2.py`)*

Then open your browser at `http://localhost:8501`.

### Option B: Full-Stack Web Application

Run the FastAPI backend server:

```bash
python server.py
```

Then open your browser at `http://localhost:8000`.

---

## 📁 Project Structure

```
chatbot/
├── app.py              # Streamlit entrypoint
├── app2.py             # Streamlit chatbot application code
├── server.py           # FastAPI backend server with SSE streaming
├── index.html          # Web frontend with modern dark UI & code highlighting
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── README.md           # Documentation
```

---

## 🛠️ Tech Stack

- **AI SDK**: `google-genai` (Google GenAI Python SDK)
- **Frontend / Full-stack**: HTML5, CSS3, Vanilla JS, `marked.js`, `highlight.js`
- **Backend**: FastAPI, Uvicorn, Pydantic
- **Data App**: Streamlit
