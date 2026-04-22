"""
scripts/extract_schema.py — Auto-Extract Schema from SQL Server
===============================================================

RUN THIS to automatically generate schema_metadata.json from your live database.
This saves you from having to manually write schema descriptions for every table.

WHAT IT DOES:
  1. Connects to SQL Server using credentials from .env (via config.py).
  2. Queries INFORMATION_SCHEMA.COLUMNS to get all tables, columns, and data types.
  3. Queries INFORMATION_SCHEMA.TABLE_CONSTRAINTS + KEY_COLUMN_USAGE to find:
       - Which columns are PRIMARY KEYs
       - Which columns are FOREIGN KEYs and what table/column they reference
  4. For each table, builds a structured text description in this exact format:

       Table: Driver
       Description: Stores records for Driver
       Columns:
       - DriverId (int) [PRIMARY KEY]
       - DriverName (varchar)
       - DriverGroupId (int)
       Relationships:
       - DriverGroupId -> DriverGroup.DriverGroupId

  5. Saves the complete list to data/schema_metadata.json.

WHY THE FORMAT MATTERS:
  The "Relationships:" section (format: "Column -> Table.Column") is specifically
  parsed by query_pipeline.py in Step 3 using regex to auto-fetch FK-linked tables.
  If you write schemas manually, use this EXACT format for FK relationships or
  Step 3 auto-fetch will not work correctly.

RUN WITH:
  cd backend
  python scripts/extract_schema.py

After running, verify the JSON output looks correct, then run ingest_schema.py.
Imports: pyodbc, config, json
"""