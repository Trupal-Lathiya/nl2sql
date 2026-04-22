"""
utils/prompt_templates.py — All LLM Prompt Strings
===================================================

This file centralizes ALL prompt text used in Groq LLM calls.
Keeping prompts here (not scattered in service files) makes them easy to:
  - Read and review in one place
  - Tune and experiment with without touching service logic
  - Version control as readable text (easy to diff changes between versions)

PROMPTS DEFINED:

  CLASSIFIER_SYSTEM_PROMPT
    System role message for the query classifier.
    Enforces strict one-word output: ALLOWED, BLOCKED_DESTRUCTIVE, or BLOCKED_IRRELEVANT.
    CRITICAL: The system prompt is what prevents the LLM from writing explanations.
    Without it, Groq sometimes returns "The answer is ALLOWED because..." instead of "ALLOWED".

  RELEVANCE_CHECK_PROMPT
    User role message for the query classifier.
    Contains detailed category definitions + 10+ labeled examples.
    Template variable: {nl_query} — the user's actual question to classify.
    Used together with CLASSIFIER_SYSTEM_PROMPT in a two-message Groq API call.

  SYSTEM_PROMPT
    System role message for T-SQL generation.
    Rules enforced: output ONLY SQL, use T-SQL (TOP not LIMIT), never use
    destructive statements, always qualify column names with table names,
    use session memory to resolve pronouns like "them" and "those".

  SQL_GENERATION_PROMPT
    User role message for T-SQL generation.
    Template variables:
      {schema_context}  — combined schema text from Pinecone results
      {memory_context}  — formatted session memory (last 5 NL-to-SQL pairs)
      {nl_query}        — the user's natural language question

  RESPONSE_SUMMARY_PROMPT
    User role message for summary generation after query executes.
    Template variables:
      {nl_query}       — user's original question
      {sql}            — the SQL that was executed
      {preview_count}  — number of rows shown to LLM (max 10)
      {total_count}    — actual total rows returned from DB
      {columns}        — column names as a list
      {rows_preview}   — first 10 rows of data
      {csv_note}       — message about CSV file if rows > 10, else empty string
    Instructs LLM to answer directly: count questions -> "There are X ...",
    name questions -> list them.

Imported by: services/llm_service.py
"""