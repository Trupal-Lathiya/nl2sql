"""
scripts/test_db.py — Database Connection Test Utility
=====================================================

A simple diagnostic script to verify your SQL Server connection is working
BEFORE starting the full application. Run this first if you're having
connection issues to isolate whether the problem is the DB config or the app.

WHAT IT DOES:
  1. Calls database_service.test_connection()
  2. Prints success message (with SQL Server version string) or a clear error message.
  3. Exit code 0 = success, 1 = failure.

COMMON FAILURE REASONS AND HOW TO FIX THEM:
  - Wrong DB_SERVER in .env      -> Check instance name (e.g. "localhost\\SQLEXPRESS")
  - ODBC Driver 17 not installed -> Download from Microsoft's website
  - SQL Server not running       -> Start the SQL Server service
  - Wrong DB_NAME                -> Database doesn't exist or is misspelled
  - Windows Auth not enabled     -> Enable or switch to SQL Server authentication

RUN WITH:
  cd backend
  python scripts/test_db.py

Imports: services/database_service
"""