/**
 * types/index.ts — Shared TypeScript Type Definitions
 * ====================================================
 *
 * Central location for all TypeScript interfaces and types used across
 * React components and hooks. Importing from here (not defining inline)
 * prevents type drift between files — one definition, used everywhere.
 *
 * TYPES DEFINED:
 *
 *   ChatMessage
 *     Represents one message in the chat UI. Both user messages and
 *     assistant responses are ChatMessage objects.
 *
 *     Key fields:
 *       id            — UUID used as React key prop and for targeting updates
 *       role          — "user" | "assistant" (determines which bubble to render)
 *       content       — Summary text (builds up chunk by chunk during streaming)
 *       timestamp     — ISO string, formatted in the bubble as "2:34 PM"
 *       status        — "pending" | "streaming" | "done" | "error"
 *                       "pending"   = waiting for first SSE event (loading dots)
 *                       "streaming" = receiving summary chunks (partial text)
 *                       "done"      = all data received (full table + SQL + summary)
 *                       "error"     = pipeline returned an error (red message)
 *       sql           — The T-SQL that was generated (shown in SqlDisplay)
 *       retrievedTables — Table names found by Pinecone search (shown in SqlDisplay)
 *       columns       — Column names from the DB result
 *       rows          — 2D array of result data (shown in ResultsTable)
 *       totalRowCount — Total rows from DB (may differ from rows.length if > 10)
 *       csvPath       — Server path to CSV file if rows > 10
 *       errorMessage  — Human-readable error text when status === "error"
 *
 *   StreamEvent
 *     Represents one SSE message received from GET /query/stream.
 *     The "event" discriminator field determines which other fields are present:
 *       "status"        -> message: string  (e.g. "Generating SQL...")
 *       "sql_ready"     -> sql: string, tables: string[]
 *       "row_data"      -> columns: string[], rows: any[][], total: number
 *       "summary_chunk" -> chunk: string  (append to message content)
 *       "done"          -> csv_path: string | null
 *       "error"         -> message: string  (display in red)
 *
 * Used by: useChat.ts, useStream.ts, ChatWindow.tsx, MessageBubble.tsx,
 *          ResultsTable.tsx, SqlDisplay.tsx, StreamingSummary.tsx
 */