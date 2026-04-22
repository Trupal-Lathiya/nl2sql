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

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.query_routes import router

app = FastAPI(title="NL2SQL API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event("startup")
async def startup_event():
    print("=" * 55)
    print("NL2SQL starting — preloading all resources...")
    print("BGE-M3 model takes 30-60 seconds on first load.")
    print("=" * 55)
    from services.embedding_service import get_model
    get_model()
    from services.pinecone_service import get_index
    get_index()
    from services.llm_service import get_client
    get_client()
    print("=" * 55)
    print("✅ Server ready!  http://localhost:8000")
    print("   API docs:      http://localhost:8000/docs")
    print("=" * 55)


@app.get("/health")
def health():
    return {"status": "ok"}