"""
services/memory_service.py — In-Memory Session Conversation History
===================================================================

This service stores recent NL-to-SQL pairs per user session so the LLM can
understand follow-up questions that use pronouns like "them", "those", "their".

EXAMPLE PROBLEM IT SOLVES:
  User query 1: "show me all drivers in London"
  User query 2: "how many of them are active?"
  Without memory, the LLM doesn't know what "them" refers to.
  With memory, it sees query 1 in context and resolves "them" = "drivers in London".

HOW IT WORKS:
  Stores a global Python dict: { session_id: [ {nl_query, sql}, ... ] }
  Max 5 entries per session (FIFO — oldest removed when full).
  Lives in process memory — resets when the server restarts.
  Thread-safe enough for single-worker uvicorn (no async races in CPython GIL).

FUNCTIONS EXPORTED:

  get_memory(session_id) -> list of dicts
    Returns the stored query history for a session.

  add_to_memory(session_id, nl_query, sql) -> None
    Appends new entry. If already 5 entries, removes the oldest first.

  clear_memory(session_id) -> None
    Deletes all entries for a session. Called on "Clear Chat".

  format_memory_for_prompt(session_id) -> str
    Formats memory as a readable string injected into the SQL generation prompt.
    Example output:
      "Previous queries for context:
       Q1: show me all drivers -> SELECT * FROM Driver
       Q2: how many are active? -> SELECT COUNT(*) FROM Driver WHERE Active = 1"
    Returns "No previous queries in this session." if memory is empty.

Used by: query_pipeline.py (inject into SQL generation prompt)
Called by: query_routes.py (DELETE endpoint to clear memory)
"""



_memory: dict = {}
MAX_MEMORY = 5


def get_memory(session_id: str) -> list:
    return _memory.get(session_id, [])


def add_to_memory(session_id: str, nl_query: str, sql: str) -> None:
    if session_id not in _memory:
        _memory[session_id] = []
    _memory[session_id].append({"nl_query": nl_query, "sql": sql})
    if len(_memory[session_id]) > MAX_MEMORY:
        _memory[session_id].pop(0)


def clear_memory(session_id: str) -> None:
    _memory.pop(session_id, None)


def format_memory_for_prompt(session_id: str) -> str:
    entries = get_memory(session_id)
    if not entries:
        return "No previous queries in this session."
    lines = ["Previous queries for context:"]
    for i, e in enumerate(entries, 1):
        lines.append(f"Q{i}: {e['nl_query']} → {e['sql']}")
    return "\n".join(lines)