"""
app.py — FastAPI Application Entry Point
========================================

This is the ROOT of the entire backend server. It does four things:

1. CREATES the FastAPI application instance with CORS enabled so that
   the React frontend (running on localhost:5173) can call the API on
   localhost:8000 without browser security errors.

2. REGISTERS the query router (/query, /query/stream, /query/memory endpoints)
   so that FastAPI knows where to route incoming HTTP requests.

3. PRELOADS heavy resources at startup via @app.on_event("startup"):
   - BGE-M3 embedding model (~2GB, takes 30-60 seconds to load)
   - Pinecone index connection
   - Groq LLM client
   Doing this at startup means the FIRST user request is fast. If we loaded
   on demand, the first request would time out waiting for the model.

4. EXPOSES a GET /health endpoint so you can quickly check the server
   is alive without running a real query.

Start the server with:
    uvicorn app:app --reload --port 8000

Dependencies used: fastapi, uvicorn, sse_starlette, all service modules
"""