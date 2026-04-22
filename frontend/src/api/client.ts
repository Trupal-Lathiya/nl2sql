/**
 * api/client.ts — HTTP API Client Functions
 * ==========================================
 *
 * Centralizes all HTTP communication with the FastAPI backend.
 * Components and hooks import from here instead of calling fetch() directly.
 * This makes it easy to: change the base URL, add auth headers, or mock for tests.
 *
 * BASE_URL: "http://localhost:8000"
 *   Change this for staging/production deployment.
 *
 * FUNCTIONS EXPORTED:
 *
 *   sendQuery(query, sessionId) -> Promise<QueryResponse>
 *     POST /query with JSON body {natural_language_query, session_id}.
 *     Returns the full non-streaming response.
 *     Not used by the main chat UI (which uses streaming), but available
 *     for testing or as a simple fallback mode.
 *
 *   openStream(query, sessionId) -> EventSource
 *     Creates and returns an EventSource pointing to GET /query/stream.
 *     URL: BASE_URL + "/query/stream?session_id=" + id + "&query=" + encodedQuery
 *     The caller (useStream.ts) attaches onmessage and onerror handlers to it.
 *     Note: EventSource does NOT support custom headers or request bodies.
 *
 *   clearMemory(sessionId) -> Promise<void>
 *     DELETE /query/memory?session_id=xxx
 *     Clears server-side session conversation memory.
 *     Called when the user clicks "Clear Chat" in the Sidebar.
 *     No response body expected — just checks for ok status.
 */