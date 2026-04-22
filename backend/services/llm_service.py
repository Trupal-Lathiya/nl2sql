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






import config
from utils.prompt_templates import (
    CLASSIFIER_SYSTEM_PROMPT,
    RELEVANCE_CHECK_PROMPT,
    SYSTEM_PROMPT,
    SQL_GENERATION_PROMPT,
    RESPONSE_SUMMARY_PROMPT,
)

_client = None


def get_client():
    global _client
    if _client is None:
        from groq import Groq
        _client = Groq(api_key=config.GROQ_API_KEY)
        print("Groq client initialized.")
    return _client


def classify_query(nl_query: str) -> str:
    client = get_client()
    resp = client.chat.completions.create(
        model=config.GROQ_MODEL,
        messages=[
            {"role": "system", "content": CLASSIFIER_SYSTEM_PROMPT},
            {"role": "user", "content": RELEVANCE_CHECK_PROMPT.format(nl_query=nl_query)},
        ],
        temperature=0.0,
        max_tokens=5,
    )
    result = resp.choices[0].message.content.strip().upper()
    for token in ("ALLOWED", "BLOCKED_DESTRUCTIVE", "BLOCKED_IRRELEVANT"):
        if token in result:
            return token
    return "BLOCKED_IRRELEVANT"


def generate_sql(nl_query: str, schema_context: str, memory_context: str) -> dict:
    client = get_client()
    try:
        resp = client.chat.completions.create(
            model=config.GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": SQL_GENERATION_PROMPT.format(
                    schema_context=schema_context,
                    memory_context=memory_context,
                    nl_query=nl_query,
                )},
            ],
            temperature=0.1,
            max_tokens=1000,
        )
        sql = resp.choices[0].message.content.strip()
        # Strip markdown code fences if present
        if sql.startswith("```"):
            lines = sql.split("\n")
            lines = [ln for ln in lines if not ln.strip().startswith("```")]
            sql = "\n".join(lines).strip()
        return {"status": "success", "sql": sql}
    except Exception as e:
        return {"status": "error", "message": f"SQL generation failed: {str(e)}"}


def generate_summary_stream(nl_query: str, sql: str, columns: list, rows: list):
    client = get_client()
    preview = rows[:10]
    csv_note = (
        f"\nNote: Full result has {len(rows)} rows. Complete data saved to CSV."
        if len(rows) > 10 else ""
    )
    stream = client.chat.completions.create(
        model=config.GROQ_MODEL,
        messages=[{"role": "user", "content": RESPONSE_SUMMARY_PROMPT.format(
            nl_query=nl_query,
            sql=sql,
            preview_count=len(preview),
            total_count=len(rows),
            columns=columns,
            rows_preview=preview,
            csv_note=csv_note,
        )}],
        temperature=0.3,
        max_tokens=600,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta