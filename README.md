<!--
README.md — Project Documentation & Setup Guide
================================================

The first file anyone reads when they open the repository. Keep it practical —
step-by-step setup instructions that actually work, not marketing prose.

SECTIONS TO INCLUDE:

  1. WHAT IS NL2SQL (2-3 sentences)
     One-line description + the core user experience (type English, get table).

  2. HOW IT WORKS (brief pipeline summary)
     List the 9 steps in plain English. Optionally include a simple ASCII
     flow diagram: User -> Classifier -> Embedder -> Pinecone -> LLM -> SQL Server -> LLM -> User

  3. PREREQUISITES
     - Python 3.10+
     - Node.js 18+
     - Microsoft SQL Server with ODBC Driver 17 installed
     - Pinecone account (free tier works)
     - Groq API key (free at console.groq.com)

  4. STEP-BY-STEP SETUP
     Step 1: Clone repo, copy .env.example to .env, fill in credentials
     Step 2: pip install -r requirements.txt
     Step 3: python scripts/extract_schema.py  (auto-generate schema JSON)
     Step 4: python scripts/ingest_schema.py   (push schemas to Pinecone)
     Step 5: python scripts/test_db.py         (verify DB connection)
     Step 6: uvicorn app:app --reload --port 8000  (wait for model load log)
     Step 7: cd frontend && npm install && npm run dev

  5. SCHEMA_METADATA.JSON FORMAT
     Show the JSON format with a real example. Explain the Relationships format.

  6. TROUBLESHOOTING
     - "ODBC Driver not found" -> install ODBC Driver 17 from Microsoft
     - "BGE-M3 model stuck" -> wait, it takes 30-60 seconds on first load
     - "Pinecone index not found" -> run ingest_schema.py first
     - "SQL syntax error" -> check GROQ_MODEL is correct in .env
     - CORS errors in browser -> ensure backend is running on port 8000

  7. RE-INGESTING AFTER SCHEMA CHANGES
     Short paragraph: edit schema_metadata.json (or re-run extract_schema.py),
     then re-run ingest_schema.py. Restart the backend.

  8. PROJECT STRUCTURE
     Paste the folder tree from the specification with one-line descriptions.
-->



