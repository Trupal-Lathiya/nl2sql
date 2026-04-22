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

import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from services.database_service import get_connection


def extract():
    print("Connecting to SQL Server...")
    conn = get_connection()
    cursor = conn.cursor()

    print("Reading columns...")
    cursor.execute("""
        SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, IS_NULLABLE
        FROM INFORMATION_SCHEMA.COLUMNS
        ORDER BY TABLE_NAME, ORDINAL_POSITION
    """)
    cols_raw = cursor.fetchall()

    print("Reading primary keys...")
    cursor.execute("""
        SELECT KCU.TABLE_NAME, KCU.COLUMN_NAME
        FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS TC
        JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE KCU
          ON TC.CONSTRAINT_NAME = KCU.CONSTRAINT_NAME
        WHERE TC.CONSTRAINT_TYPE = 'PRIMARY KEY'
    """)
    pks = {(r[0], r[1]) for r in cursor.fetchall()}

    print("Reading foreign keys...")
    cursor.execute("""
        SELECT
            KCU.TABLE_NAME,
            KCU.COLUMN_NAME,
            RCU.TABLE_NAME  AS REF_TABLE,
            RCU.COLUMN_NAME AS REF_COL
        FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS RC
        JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE KCU
          ON RC.CONSTRAINT_NAME = KCU.CONSTRAINT_NAME
        JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE RCU
          ON RC.UNIQUE_CONSTRAINT_NAME = RCU.CONSTRAINT_NAME
    """)
    fks = {}
    for row in cursor.fetchall():
        fks.setdefault(row[0], []).append((row[1], row[2], row[3]))

    conn.close()

    # Group by table
    tables = {}
    for table, col, dtype, nullable in cols_raw:
        tables.setdefault(table, []).append((col, dtype, nullable))

    results = []
    for table, columns in tables.items():
        lines = [
            f"Table: {table}",
            f"Description: Stores records for {table}",
            "Columns:",
        ]
        for col, dtype, nullable in columns:
            pk_flag  = " [PRIMARY KEY]" if (table, col) in pks else ""
            null_tag = " (nullable)"    if nullable == "YES" else ""
            lines.append(f"- {col}: {dtype}{pk_flag}{null_tag}")

        if table in fks:
            lines.append("Relationships:")
            for col, ref_table, ref_col in fks[table]:
                lines.append(f"- {col} → {ref_table}.{ref_col}")

        results.append({"id": table, "text": "\n".join(lines)})

    os.makedirs(os.path.dirname(config.SCHEMA_METADATA_PATH), exist_ok=True)
    with open(config.SCHEMA_METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"✅ Extracted {len(results)} tables → {config.SCHEMA_METADATA_PATH}")


if __name__ == "__main__":
    extract()