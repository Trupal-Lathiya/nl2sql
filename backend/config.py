"""
config.py — Centralized Configuration & Environment Variables
=============================================================

This file is the SINGLE SOURCE OF TRUTH for all configuration in the backend.
It reads from the .env file using python-dotenv and exports typed constants
that every other module imports.

WHY THIS EXISTS:
  Instead of every service calling os.getenv() directly (which is error-prone
  and scattered), all services import from here. This makes it easy to:
  - See all config in one place
  - Set default values in one place
  - Change a key name in one place

WHAT IT EXPORTS:
  Database:
    DB_SERVER        — SQL Server host/instance (e.g. "localhost\\SQLEXPRESS")
    DB_NAME          — Database name
    DB_DRIVER        — ODBC driver string (default: "ODBC Driver 17 for SQL Server")

  Pinecone (Vector Database):
    PINECONE_API_KEY    — Secret key for Pinecone API
    PINECONE_INDEX_NAME — Name of the index storing table embeddings (default: "nl2sql-schema")
    PINECONE_CLOUD      — Cloud provider (default: "aws")
    PINECONE_REGION     — Region (default: "us-east-1")

  Embedding Model:
    EMBEDDING_MODEL     — HuggingFace model ID (default: "BAAI/bge-m3")
    EMBEDDING_DIMENSION — Vector size output by the model (default: 1024)

  LLM:
    GROQ_API_KEY  — Secret key for Groq API
    GROQ_MODEL    — Model name (default: "meta-llama/llama-4-scout-17b-16e-instruct")

  Paths:
    SCHEMA_METADATA_PATH — Path to schema_metadata.json used by ingest script

All other modules import these constants instead of calling os.getenv() directly.
"""

import os
from dotenv import load_dotenv

load_dotenv()

DB_SERVER             = os.getenv("DB_SERVER", r"localhost\SQLEXPRESS")
DB_NAME               = os.getenv("DB_NAME", "")
DB_DRIVER             = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")

PINECONE_API_KEY      = os.getenv("PINECONE_API_KEY", "")
PINECONE_INDEX_NAME   = os.getenv("PINECONE_INDEX_NAME", "nl2sql-schema")
PINECONE_CLOUD        = os.getenv("PINECONE_CLOUD", "aws")
PINECONE_REGION       = os.getenv("PINECONE_REGION", "us-east-1")

EMBEDDING_MODEL       = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
EMBEDDING_DIMENSION   = int(os.getenv("EMBEDDING_DIMENSION", "1024"))

GROQ_API_KEY          = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL            = os.getenv("GROQ_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")

SCHEMA_METADATA_PATH  = os.getenv("SCHEMA_METADATA_PATH", "data/schema_metadata.json")
