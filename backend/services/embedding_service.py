"""
services/embedding_service.py — BGE-M3 Text Embedding Model Wrapper
====================================================================

This service converts text strings into 1024-dimensional numerical vectors
(embeddings). These vectors capture semantic meaning — similar sentences get
similar vectors — which allows Pinecone to find relevant table schemas by
meaning, not just keyword matching.

MODEL USED: BAAI/bge-m3 (via FlagEmbedding library)
  State-of-the-art multilingual embedding model.
  Outputs 1024-dimensional dense vectors.
  Approximately 2GB in size, so it loads once at startup (not per request).

LAZY SINGLETON PATTERN:
  _model = None  (module-level global)
  get_model() checks if _model is None, loads if needed, returns it.
  This ensures the model is loaded ONCE and reused across all requests.
  The actual loading is triggered in app.py's startup event.

FUNCTIONS EXPORTED:

  get_model() -> BGEM3FlagModel
    Returns the singleton model instance. Loads it on first call.
    Logs "Loading BGE-M3 model..." and "BGE-M3 model loaded successfully."

  embed_text(text: str) -> list[float]
    Encodes a single string into a 1024-dim vector.
    Used in query_pipeline.py to embed the user's NL query.
    Returns a plain Python list (not numpy array) for JSON serialization.

  embed_texts(texts: list[str]) -> list[list[float]]
    Batch encodes multiple strings. More efficient than calling embed_text
    in a loop. Used by ingest_schema.py to embed all table schemas at once.

Used by: query_pipeline.py (Step 1), scripts/ingest_schema.py
"""