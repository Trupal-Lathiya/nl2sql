"""
services/database_service.py — Microsoft SQL Server Query Executor
==================================================================

This service handles all direct communication with the SQL Server database
using PyODBC (Python ODBC bridge). It is intentionally stateless — it opens
a new connection per query (no connection pool needed for this app's load).

CONNECTION STRING FORMAT:
  DRIVER={ODBC Driver 17 for SQL Server};
  SERVER=localhost\\SQLEXPRESS;
  DATABASE=YourDB;
  Trusted_Connection=yes;   <- Uses Windows Authentication (no username/password)
  Alternatively, use UID= and PWD= for SQL Server authentication.

FUNCTIONS EXPORTED:

  get_connection() -> pyodbc.Connection
    Builds the connection string from config.py values and returns a new
    PyODBC connection. Raises an exception if connection fails (caught upstream).

  test_connection() -> dict
    Opens a connection, runs "SELECT @@VERSION" to get SQL Server version.
    Returns {"status": "success", "version": "..."} or {"status": "error", ...}
    Used by scripts/test_db.py to verify credentials are correct.

  execute_query(sql: str) -> dict
    Opens a connection, executes the given SQL, fetches ALL rows.
    Returns {"status": "success", "columns": [...], "rows": [[...], ...]}

    IMPORTANT — ODBC Error Mapping:
      Instead of returning raw ODBC error strings (unreadable to users), maps
      known SQLSTATE codes to friendly messages:
        "42000" -> "SQL syntax error: ..."
        "42S02" -> "Table not found: ..."
        "42S22" -> "Column not found: ..."
        other   -> "Database error: ..."
      This mapping is in the except block for pyodbc.Error.

Used by: query_pipeline.py (Step 7), scripts/test_db.py
"""