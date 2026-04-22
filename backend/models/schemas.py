"""
models/schemas.py — Pydantic Data Models (Request & Response Shapes)
=====================================================================

This file defines the DATA CONTRACTS between the frontend and backend.
Pydantic models serve two purposes:
  1. INPUT VALIDATION — FastAPI automatically validates incoming JSON against
     these models and returns 422 errors if the shape is wrong.
  2. DOCUMENTATION — FastAPI auto-generates OpenAPI docs at /docs using these.

MODELS DEFINED:

  QueryRequest
    What the frontend sends to POST /query.
    Fields: natural_language_query (string), session_id (UUID string)

  QuerySuccessResponse
    What the backend returns when everything succeeds.
    Fields: status="success", nl_query, sql, retrieved_tables (list of table
    names from Pinecone), columns, rows (2D list), total_row_count, summary,
    csv_path (optional — only set if rows > 10)

  QueryErrorResponse
    What the backend returns when blocked or an error occurs.
    Fields: status="error", message (human-readable error string)

  QueryResponse
    A Union type = QuerySuccessResponse OR QueryErrorResponse.
    FastAPI uses this as the return type annotation on route handlers.

These models are imported by query_routes.py (for type annotations) and by
query_pipeline.py (to build the response dict that gets serialized).
"""