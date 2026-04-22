"""
services/query_pipeline.py — Main Orchestrator: Full Query Pipeline
====================================================================

This is the BRAIN of the application. It orchestrates all 9 pipeline steps
in the correct order, calls the right services, and handles errors at each step.

THE 9-STEP PIPELINE:

  Step 0 — Query Classification (runs in parallel with Step 1)
    Calls llm_service.classify_query(). If BLOCKED_* -> stop immediately and
    return an error response. No further processing happens.

  Step 1 — Embed the Query (runs in parallel with Step 0)
    Calls embedding_service.embed_text() to get a 1024-dim vector of the query.
    Run in parallel with Step 0 using ThreadPoolExecutor to save 2-3 seconds.
    If Step 0 returns BLOCKED, the embedding result is discarded (no waste).

  Step 2 — Pinecone Semantic Search
    Calls pinecone_service.search_similar() with the embedding vector.
    Returns top 10 most relevant table schemas by cosine similarity.

  Step 3 — Auto-fetch FK-Related Tables
    Parses each retrieved schema for "ColumnName -> TableName.ColumnName" lines.
    If any referenced TableName was NOT in the top-10 results, fetches it
    directly from Pinecone by ID. Ensures the LLM has full JOIN context.

  Step 4 — Build Schema Context String
    Joins all retrieved schema texts into one string for the LLM prompt.
    Also builds a list of table names (returned in the response for UI display).

  Step 5 — Generate SQL
    Calls llm_service.generate_sql() with schema context + memory context + query.
    Memory context = last 5 queries from memory_service for this session.

  Step 6 — SQL Safety Check (Regex word-boundary matching)
    Uses re.search() with \\b word boundaries to detect destructive SQL keywords.
    Blocked: DELETE, DROP, TRUNCATE, ALTER, INSERT, UPDATE, MERGE, EXEC, EXECUTE,
             CREATE, REPLACE.
    Word boundaries prevent false positives like "UpdatedAt" triggering "UPDATE".

  Step 7 — Execute SQL on SQL Server
    Calls database_service.execute_query(). Returns columns + all rows.

  Step 8 — Generate Summary
    Non-streaming version: calls generate_summary (collects full text).
    Streaming version: calls generate_summary_stream and yields chunks as SSE events.

  Step 9 — Save Memory + CSV
    Adds NL query + SQL to memory_service (max 5, FIFO).
    If total rows > 10, saves all rows to data/exports/export_<timestamp>.csv.

TWO ENTRY POINTS:

  run_pipeline(nl_query, session_id) -> dict
    Blocking version. Returns complete response dict. Used by POST /query.

  run_pipeline_stream(nl_query, session_id) -> Generator[dict]
    Generator version. Yields SSE event dicts at each pipeline stage.
    Used by GET /query/stream. Frontend receives live updates as they happen.

PARALLEL STEP 0+1 IMPLEMENTATION:
  with ThreadPoolExecutor(max_workers=2) as executor:
      classify_future = executor.submit(classify_query, nl_query)
      embed_future = executor.submit(embed_text, nl_query)
      classification = classify_future.result()
      if classification != "ALLOWED":
          return blocked_response  # embed result discarded
      query_embedding = embed_future.result()

Used by: routes/query_routes.py
Imports: all service modules, config, utils/prompt_templates
"""