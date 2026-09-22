import os
import json
import asyncio
import time
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types

# Load from .env if present
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                if k and v and k not in os.environ:
                    os.environ[k] = v

PERMANENT_GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "AQ.Ab8RN6IfN_B69ELmxDUEHjv_81PEorIaOVswzDUM7MsjWlr3qw"

app = FastAPI(title="Pratyush AI Chatbot", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str
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
]

def generate_smart_fallback_response(query: str, persona: Optional[str] = None) -> str:
    """
    Intelligent built-in response engine for seamless demonstration
    when cloud API key credentials are not yet configured or invalid.
    """
    q = query.lower()

    if "recursion" in q or "memoization" in q:
        return """### Understanding Recursion with Memoization in Python

Recursion is a programming technique where a function solves a problem by calling itself with a smaller sub-problem until it reaches a **base case**.

#### The Classic Problem: Fibonacci Numbers
Without memoization, computing Fibonacci recursively has an exponential time complexity of **O(2ⁿ)** because the function recalculates identical subproblems repeatedly.

With **memoization**, we cache the results of previous function calls, dropping the complexity down to **O(n)** time and **O(n)** space!

```python
import functools
import time

# 1. Manual Memoization using a Dictionary Cache
def fibonacci_memo(n: int, memo: dict = None) -> int:
    if memo is None:
        memo = {}
    
    # Base Cases
    if n <= 0:
        return 0
    if n == 1:
        return 1
        
    # Check if already computed
    if n in memo:
        return memo[n]
        
    # Recursive Call & Store in Cache
    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]


# 2. Pythonic Memoization using @functools.lru_cache
@functools.lru_cache(maxsize=None)
def fibonacci_lru(n: int) -> int:
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


# Demonstration & Performance Comparison
if __name__ == "__main__":
    n = 35
    print(f"Calculating Fibonacci({n})...")
    
    start = time.perf_counter()
    result = fibonacci_memo(n)
    elapsed = time.perf_counter() - start
    print(f"Result (Memoized Dict): {result} in {elapsed*1000:.3f} ms")
    
    start = time.perf_counter()
    result_lru = fibonacci_lru(n)
    elapsed_lru = time.perf_counter() - start
    print(f"Result (lru_cache):     {result_lru} in {elapsed_lru*1000:.3f} ms")
