/**
 * App.tsx — Root Application Component
 * =====================================
 *
 * The top-level React component that holds global state and defines layout.
 *
 * RESPONSIBILITIES:
 *
 * 1. SESSION ID GENERATION
 *    Generates a UUID once on mount using crypto.randomUUID() stored in useState.
 *    This ID persists for the browser tab's lifetime and is sent with every query
 *    so the backend associates requests with the correct session memory.
 *    Each new tab = fresh UUID = fresh session = fresh conversation memory.
 *
 * 2. LAYOUT
 *    Renders a flex-row layout filling the full viewport:
 *      [Sidebar — 240px fixed] [ChatWindow — fills remaining width]
 *    Background: #0e1117 (app background from design spec)
 *    Height: 100vh (full viewport height, no scrolling at the root level)
 *
 * 3. PROP PASSING
 *    sessionId flows down to Sidebar and ChatWindow.
 *    Both components need it:
 *      ChatWindow -> useChat.ts -> API calls (session_id query param)
 *      Sidebar -> "Clear Chat" button handler (DELETE /query/memory)
 *
 * Component tree:
 *   App
 *   ├── Sidebar (branding, stats, clear button)
 *   └── ChatWindow (message list + input bar)
 *       ├── MessageBubble[] (one per message)
 *       │   ├── LoadingIndicator (when pending/streaming)
 *       │   ├── StreamingSummary (answer text)
 *       │   ├── SqlDisplay (generated SQL, collapsible)
 *       │   └── ResultsTable (data grid + CSV download)
 *       └── ChatInput (text field + send button)
 */