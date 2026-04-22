"""
routes/query_routes.py — HTTP Route Handlers (API Endpoints)
============================================================

This file wires HTTP endpoints to pipeline logic. It is the THIN LAYER
between HTTP and business logic — it should contain no business logic itself.

THREE ENDPOINTS:

  1. POST /query
     Non-streaming version of the pipeline.
     Reads QueryRequest from request body.
     Calls run_pipeline() from query_pipeline.py.
     Returns QueryResponse (success or error JSON).
     Use this for testing; the frontend uses the streaming endpoint.

  2. GET /query/stream
     The MAIN endpoint the React frontend uses.
     Parameters: session_id (query param), query (query param, URL-encoded).
     Uses SSE (Server-Sent Events) via sse_starlette.
     Calls run_pipeline_stream() which is a generator that yields event dicts.
     Each yielded dict becomes one SSE message that the browser reads.
     Events in order: status → status → sql_ready → status → row_data →
       summary_chunk (many) → done
     Headers set:
       Content-Type: text/event-stream
       Cache-Control: no-cache
       X-Accel-Buffering: no  (disables nginx buffering for real-time streaming)

  3. DELETE /query/memory
     Parameter: session_id (query param)
     Calls clear_memory() from memory_service.py
     Called when user clicks "Clear Chat" in the sidebar.
     Returns {"status": "ok"}

Router prefix: /query
This router is registered in app.py with app.include_router(router)
"""


import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from models.schemas import QueryRequest, QueryResponse
from services.query_pipeline import run_pipeline, run_pipeline_stream
from services.memory_service import clear_memory

router = APIRouter(prefix="/query")


@router.post("", response_model=QueryResponse)
async def query_post(request: QueryRequest):
    result = run_pipeline(request.natural_language_query, request.session_id)
    return result


@router.get("/stream")
async def query_stream(session_id: str, query: str):
    def event_generator():
        for event_dict in run_pipeline_stream(query, session_id):
            yield f"data: {json.dumps(event_dict)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@router.delete("/memory")
async def delete_memory(session_id: str):
    clear_memory(session_id)
    return {"status": "ok"}