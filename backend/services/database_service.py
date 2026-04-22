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


import config


def get_connection():
    import pyodbc
    conn_str = (
        f"DRIVER={{{config.DB_DRIVER}}};"
        f"SERVER={config.DB_SERVER};"
        f"DATABASE={config.DB_NAME};"
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)


def test_connection() -> dict:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        conn.close()
        return {"status": "success", "version": version}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def execute_query(sql: str) -> dict:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        raw_rows = cursor.fetchall()
        rows = []
        for row in raw_rows:
            serialized = []
            for cell in row:
                if cell is None:
                    serialized.append(None)
                elif isinstance(cell, (int, float, bool)):
                    serialized.append(cell)
                else:
                    serialized.append(str(cell))
            rows.append(serialized)
        conn.close()
        return {"status": "success", "columns": columns, "rows": rows}
    except Exception as e:
        try:
            import pyodbc as _pyodbc
            if isinstance(e, _pyodbc.Error) and e.args:
                state = str(e.args[0])
                msg = str(e.args[1]) if len(e.args) > 1 else str(e)
                if state == "42000":
                    return {"status": "error", "message": f"SQL syntax error: {msg}"}
                elif state == "42S02":
                    return {"status": "error", "message": f"Table not found: {msg}"}
                elif state == "42S22":
                    return {"status": "error", "message": f"Column not found: {msg}"}
                else:
                    return {"status": "error", "message": f"Database error [{state}]: {msg}"}
        except Exception:
            pass
        return {"status": "error", "message": f"Database error: {str(e)}"}