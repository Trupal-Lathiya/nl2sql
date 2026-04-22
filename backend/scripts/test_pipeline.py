"""
scripts/test_pipeline.py — End-to-End Pipeline Test (No HTTP)
=============================================================

Tests the full query pipeline directly (bypassing FastAPI and HTTP) so you
can debug pipeline steps without needing the frontend or running the web server.

WHAT IT DOES:
  1. Accepts a hardcoded test query (or command-line argument via sys.argv).
  2. Calls run_pipeline() directly from query_pipeline.py with a dummy session ID.
  3. Prints the output at each step:
       - Classification result (ALLOWED / BLOCKED_*)
       - Top-K table names retrieved from Pinecone
       - Generated T-SQL query
       - Number of rows returned from the database
       - Full summary text from the LLM

WHEN TO USE THIS SCRIPT:
  - After ingesting schemas: verify that test queries return the correct tables.
  - After changing prompt templates: verify SQL quality improved.
  - When debugging "no results" or "wrong table" issues without frontend noise.
  - To quickly benchmark pipeline speed (logs timestamps at each step).

RUN WITH:
  cd backend
  python scripts/test_pipeline.py
  # or with a custom query:
  python scripts/test_pipeline.py "show me all active drivers"

Imports: services/query_pipeline
"""