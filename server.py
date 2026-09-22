import os
import json
import asyncio
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

# Permanent backend Gemini API Key
PERMANENT_GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "AQ.Ab8RN6IfN_B69ELmxDUEHjv_81PEorIaOVswzDUM7MsjWlr3qw"

app = FastAPI(title="Pratyush AI Chatbot API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str # "user" or "assistant" / "model"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str] = "gemini-2.5-flash"
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.95
    max_tokens: Optional[int] = 4096
    system_instruction: Optional[str] = None
    stream: Optional[bool] = True

AVAILABLE_MODELS = [
    {"id": "gemini-2.5-flash", "name": "Gemini 2.5 Flash (Fast & Smart)", "recommended": True},
    {"id": "gemini-2.5-pro", "name": "Gemini 2.5 Pro (Deep Reasoning)", "recommended": False},
    {"id": "gemini-2.0-flash", "name": "Gemini 2.0 Flash", "recommended": False},
    {"id": "gemini-1.5-flash", "name": "Gemini 1.5 Flash", "recommended": False},
    {"id": "gemini-1.5-pro", "name": "Gemini 1.5 Pro", "recommended": False},
]

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "ready": True}

@app.get("/api/models")
async def get_models():
    return {"models": AVAILABLE_MODELS}

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    if not req.messages:
        raise HTTPException(status_code=400, detail="No messages provided.")

    # Convert chat history into Gemini format
    contents = []
    for msg in req.messages:
        role = "user" if msg.role.lower() in ["user", "human"] else "model"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=msg.content)],
            )
        )

    config = types.GenerateContentConfig(
        temperature=req.temperature,
        top_p=req.top_p,
        max_output_tokens=req.max_tokens,
        system_instruction=req.system_instruction.strip() if req.system_instruction and req.system_instruction.strip() else None,
    )

    try:
        client = genai.Client(api_key=PERMANENT_GEMINI_API_KEY)
        model_name = req.model or "gemini-2.5-flash"

        if req.stream:
            async def event_stream():
                try:
                    stream = await asyncio.to_thread(
                        client.models.generate_content_stream,
                        model=model_name,
                        contents=contents,
                        config=config,
                    )
                    for chunk in stream:
                        text = chunk.text or ""
                        if text:
                            payload = json.dumps({"text": text})
                            yield f"data: {payload}\n\n"
                    yield "data: [DONE]\n\n"
                except Exception as stream_err:
                    err_payload = json.dumps({"error": str(stream_err)})
                    yield f"data: {err_payload}\n\n"

            return StreamingResponse(
                event_stream(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",
                },
            )
        else:
            response = await asyncio.to_thread(
                client.models.generate_content,
                model=model_name,
                contents=contents,
                config=config,
            )
            return {"reply": response.text or ""}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    return HTMLResponse("<h1>index.html not found</h1>", status_code=404)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    print(f"Starting Pratyush AI Server on http://localhost:{port}")
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
