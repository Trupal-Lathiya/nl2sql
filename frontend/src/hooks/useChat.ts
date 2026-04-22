/**
 * hooks/useChat.ts — Chat State Manager (Central Controller)
 * ===========================================================
 *
 * This hook owns ALL chat state and is the central controller for the chat
 * experience. Components only render — this hook handles all the logic.
 *
 * STATE MANAGED:
 *   messages: ChatMessage[]   — The full array of all chat messages (user + assistant)
 *   isStreaming: boolean      — True while any SSE stream is open (disables input)
 *
 * MAIN FUNCTION — sendMessage(query, sessionId):
 *   1. Trims and validates the query (ignores empty input).
 *   2. Adds a user bubble with role="user", content=query, status="done".
 *   3. Adds an assistant placeholder with role="assistant", status="pending".
 *      Saves the placeholder's ID for targeting future updates.
 *   4. Sets isStreaming = true (disables the input box).
 *   5. Opens SSE stream via useStream.ts passing an onEvent callback.
 *   6. The onEvent callback handles each SSE event type:
 *        "status"        -> update currentStep label on the pending bubble
 *        "sql_ready"     -> attach sql + retrievedTables fields to the bubble
 *        "row_data"      -> attach columns, rows, totalRowCount to the bubble
 *        "summary_chunk" -> append chunk to content, set status="streaming"
 *        "done"          -> set status="done", attach csvPath, set isStreaming=false
 *        "error"         -> set status="error", set errorMessage, set isStreaming=false
 *   7. Uses functional setState with message ID targeting to avoid stale closures:
 *        setMessages(prev => prev.map(m => m.id === id ? {...m, ...update} : m))
 *
 * SECONDARY FUNCTION — clearChat(sessionId):
 *   1. Resets messages to [].
 *   2. Calls clearMemory(sessionId) from api/client.ts (DELETE /query/memory).
 *
 * Used by: App.tsx (or ChatWindow.tsx)
 * Depends on: useStream.ts, api/client.ts, types/index.ts
 */