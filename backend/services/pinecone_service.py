"""
services/pinecone_service.py — Pinecone Vector Database Client Wrapper
======================================================================

This service handles all communication with Pinecone, the vector database
that stores table schema embeddings. When a user asks a question, we embed
it and search Pinecone to find which database tables are most likely relevant.

WHY VECTOR SEARCH FOR SCHEMAS?
  A database might have 100+ tables. Instead of sending ALL schemas to the LLM
  (expensive and hits context limits), we embed each schema once and store in
  Pinecone. At query time we embed the user's question and find the top 10
  most semantically relevant tables to send to the LLM.

LAZY SINGLETON PATTERN:
  _index = None  (module-level global)
  get_index() connects to Pinecone once and returns the same index object.
  Triggered at startup in app.py.

INDEX AUTO-CREATION:
  If the Pinecone index named in config doesn't exist yet, get_index() creates
  it automatically with cosine similarity metric and ServerlessSpec.

FUNCTIONS EXPORTED:

  get_index() -> Pinecone Index object
    Returns the connected index. Creates it if it doesn't exist.

  upsert_schemas(records: list[dict]) -> dict
    Takes list of {id, values, metadata} dicts.
    Upserts to Pinecone in batches of 100 (Pinecone API limit per request).
    Used by scripts/ingest_schema.py to load all table schemas.

  search_similar(query_embedding, top_k=10) -> list[dict]
    Queries Pinecone with the user's embedded question.
    Returns top_k results as list of {id, score, metadata} dicts.
    Metadata contains the schema text for each table.

  fetch_by_ids(ids: list[str]) -> list[dict]
    Fetches specific vectors by their table name IDs.
    Used in Step 3 of the pipeline to get FK-referenced tables that
    weren't in the top-10 similarity results.

Used by: query_pipeline.py (Steps 2, 3), scripts/ingest_schema.py
"""