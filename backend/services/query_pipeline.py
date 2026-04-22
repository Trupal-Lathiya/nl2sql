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


import re
import os
import csv
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from services.embedding_service import embed_text
from services.llm_service import classify_query, generate_sql, generate_summary_stream
from services.pinecone_service import search_similar, fetch_by_ids
from services.database_service import execute_query
from services.memory_service import add_to_memory, format_memory_for_prompt

DESTRUCTIVE_PATTERN = re.compile(
    r"\b(DELETE|DROP|TRUNCATE|ALTER|INSERT|UPDATE|MERGE|EXEC|EXECUTE|CREATE|REPLACE)\b",
    re.IGNORECASE,
)

MSG_DESTRUCTIVE = (
    "🚫 This assistant is read-only. "
    "Queries that delete, update, insert, or modify data are not allowed."
)
MSG_IRRELEVANT = (
    "🗄️ Please ask a question related to your database — "
    "for example: 'Show me all drivers' or 'How many journeys happened this week?'"
)


def _get_fk_table_names(schema_text: str) -> list:
    return re.findall(r"→\s*(\w+)\.\w+", schema_text)


def _save_csv(columns: list, rows: list) -> str:
    os.makedirs("data/exports", exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    path = f"data/exports/export_{ts}.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)
    return path


# ── Non-streaming (POST /query) ──────────────────────────────

def run_pipeline(nl_query: str, session_id: str, top_k: int = 10) -> dict:

    # Step 0 + 1 parallel
    with ThreadPoolExecutor(max_workers=2) as ex:
        clf_fut   = ex.submit(classify_query, nl_query)
        embed_fut = ex.submit(embed_text, nl_query)
        classification = clf_fut.result()
        if classification == "BLOCKED_DESTRUCTIVE":
            return {"status": "error", "message": MSG_DESTRUCTIVE}
        if classification == "BLOCKED_IRRELEVANT":
            return {"status": "error", "message": MSG_IRRELEVANT}
        query_embedding = embed_fut.result()

    # Step 2
    results   = search_similar(query_embedding, top_k=top_k)
    found_ids = {r["id"] for r in results}
    schemas   = {r["id"]: r["metadata"].get("text", "") for r in results}

    # Step 3 — FK auto-fetch
    extra_ids = set()
    for text in list(schemas.values()):
        for tid in _get_fk_table_names(text):
            if tid not in found_ids:
                extra_ids.add(tid)
    if extra_ids:
        for item in fetch_by_ids(list(extra_ids)):
            schemas[item["id"]] = item["metadata"].get("text", "")

    # Step 4
    schema_context   = "\n\n".join(schemas.values())
    retrieved_tables = list(schemas.keys())

    # Step 5
    memory_context = format_memory_for_prompt(session_id)
    sql_result     = generate_sql(nl_query, schema_context, memory_context)
    if sql_result["status"] == "error":
        return {"status": "error", "message": sql_result["message"]}
    sql = sql_result["sql"]

    # Step 6
    if DESTRUCTIVE_PATTERN.search(sql):
        return {"status": "error", "message": MSG_DESTRUCTIVE}

    # Step 7
    db_result = execute_query(sql)
    if db_result["status"] == "error":
        return {"status": "error", "message": db_result["message"]}
    columns = db_result["columns"]
    rows    = db_result["rows"]

    # Step 8
    summary = "".join(generate_summary_stream(nl_query, sql, columns, rows))

    # Step 9
    add_to_memory(session_id, nl_query, sql)
    csv_path = _save_csv(columns, rows) if len(rows) > 10 else None

    return {
        "status":           "success",
        "nl_query":         nl_query,
        "sql":              sql,
        "retrieved_tables": retrieved_tables,
        "columns":          columns,
        "rows":             rows[:10],
        "total_row_count":  len(rows),
        "summary":          summary,
        "csv_path":         csv_path,
    }


# ── Streaming (GET /query/stream SSE) ────────────────────────

def run_pipeline_stream(nl_query: str, session_id: str, top_k: int = 10):

    yield {"event": "status", "message": "Classifying query..."}

    with ThreadPoolExecutor(max_workers=2) as ex:
        clf_fut   = ex.submit(classify_query, nl_query)
        embed_fut = ex.submit(embed_text, nl_query)
        classification = clf_fut.result()
        if classification == "BLOCKED_DESTRUCTIVE":
            yield {"event": "error", "message": MSG_DESTRUCTIVE}
            return
        if classification == "BLOCKED_IRRELEVANT":
            yield {"event": "error", "message": MSG_IRRELEVANT}
            return
        query_embedding = embed_fut.result()

    yield {"event": "status", "message": "Searching relevant schemas..."}

    results   = search_similar(query_embedding, top_k=top_k)
    found_ids = {r["id"] for r in results}
    schemas   = {r["id"]: r["metadata"].get("text", "") for r in results}

    extra_ids = set()
    for text in list(schemas.values()):
        for tid in _get_fk_table_names(text):
            if tid not in found_ids:
                extra_ids.add(tid)
    if extra_ids:
        for item in fetch_by_ids(list(extra_ids)):
            schemas[item["id"]] = item["metadata"].get("text", "")

    schema_context   = "\n\n".join(schemas.values())
    retrieved_tables = list(schemas.keys())
    memory_context   = format_memory_for_prompt(session_id)

    yield {"event": "status", "message": "Generating SQL..."}

    sql_result = generate_sql(nl_query, schema_context, memory_context)
    if sql_result["status"] == "error":
        yield {"event": "error", "message": sql_result["message"]}
        return
    sql = sql_result["sql"]

    if DESTRUCTIVE_PATTERN.search(sql):
        yield {"event": "error", "message": MSG_DESTRUCTIVE}
        return

    yield {"event": "sql_ready", "sql": sql, "tables": retrieved_tables}
    yield {"event": "status", "message": "Running query on database..."}

    db_result = execute_query(sql)
    if db_result["status"] == "error":
        yield {"event": "error", "message": db_result["message"]}
        return
    columns = db_result["columns"]
    rows    = db_result["rows"]

    yield {"event": "row_data", "columns": columns, "rows": rows[:10], "total": len(rows)}
    yield {"event": "status", "message": "Generating summary..."}

    for chunk in generate_summary_stream(nl_query, sql, columns, rows):
        yield {"event": "summary_chunk", "chunk": chunk}

    add_to_memory(session_id, nl_query, sql)
    csv_path = _save_csv(columns, rows) if len(rows) > 10 else None

    yield {"event": "done", "csv_path": csv_path}