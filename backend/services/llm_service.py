"""
services/llm_service.py — Groq LLM API Wrapper
===============================================

This service wraps all calls to the Groq LLM API. Three distinct LLM calls
happen in the pipeline, each with a different purpose, temperature, and prompt.

GROQ CLIENT SINGLETON:
  _client = None (module-level global)
  get_client() creates the Groq client once using GROQ_API_KEY from config.

FUNCTIONS EXPORTED:

  classify_query(nl_query: str) -> str
    Purpose: Decide if the user's question is allowed before doing any real work.
    Returns exactly one of: "ALLOWED", "BLOCKED_DESTRUCTIVE", "BLOCKED_IRRELEVANT"
    Settings: temperature=0.0 (fully deterministic), max_tokens=5 (needs 1 word only)
    Uses BOTH a system prompt (enforces one-word output) and a user prompt
    (provides examples and categories). The system prompt is CRITICAL — without
    it the LLM sometimes returns explanations instead of a single word.

  generate_sql(nl_query, schema_context, memory_context) -> dict
    Purpose: Convert natural language into T-SQL for Microsoft SQL Server.
    Returns: {"status": "success", "sql": "SELECT ..."} or {"status": "error", ...}
    schema_context = combined text of all relevant table schemas from Pinecone.
    memory_context = last 5 NL-to-SQL pairs from session, so LLM resolves pronouns.
    The LLM is instructed to return ONLY the SQL with no markdown or explanation.

  generate_summary_stream(nl_query, sql, columns, rows) -> Generator
    Purpose: Explain the query results in plain English to the user.
    Uses Groq's stream=True mode — returns a generator that yields text chunks.
    Only the first 10 rows are sent to the LLM to keep token usage low.
    Each yielded value is a string chunk (e.g. "There are ", "42 ", "drivers.")
    These chunks are forwarded to the browser via SSE in query_pipeline.py.

All prompts are imported from utils/prompt_templates.py.
Used by: query_pipeline.py (Steps 0, 5, 8)
"""