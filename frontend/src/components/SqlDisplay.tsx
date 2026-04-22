/**
 * components/SqlDisplay.tsx — Collapsible SQL Query & Tables Viewer
 * ==================================================================
 *
 * Shows the generated T-SQL and the list of Pinecone-retrieved tables.
 * Rendered inside an assistant bubble when status === "done".
 * Collapsed by default to keep the UI clean — user expands if curious.
 *
 * INTERACTION:
 *   Click the header row "🧾 View Generated SQL" to toggle open/close.
 *   A chevron icon (▼/▲) rotates to indicate the collapsed/expanded state.
 *   Smooth height transition via CSS max-height animation or Tailwind transition.
 *
 * EXPANDED CONTENT — two sections:
 *
 *   1. SQL CODE BLOCK
 *      <pre> element with:
 *        Font:       monospace (font-mono)
 *        Background: #0e1117 (app background — darker than bubble for contrast)
 *        Padding:    12px
 *        Border:     1px solid #2a2a3d
 *        Border radius: 8px
 *        Overflow-x: auto (long queries scroll horizontally, no line wrap)
 *      Plain text SQL — no syntax highlighting library needed.
 *
 *   2. TABLES USED SECTION
 *      Header: "📋 Tables used from Pinecone"
 *      Renders each table name in retrievedTables as a small chip/badge.
 *      Chip style: bg #0e1117, border #2a2a3d, text #94a3b8, rounded, text-xs.
 *      These are the tables the semantic search returned as most relevant.
 *      Useful for debugging incorrect SQL — if wrong tables listed, improve schemas.
 *
 * STATE: isExpanded: boolean, toggled by click handler.
 *
 * Props:
 *   sql: string
 *   retrievedTables: string[]
 */