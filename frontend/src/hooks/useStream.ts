/**
 * hooks/useStream.ts — SSE (Server-Sent Events) Stream Handler
 * =============================================================
 *
 * Abstracts the browser's native EventSource API for consuming the streaming
 * pipeline endpoint. Handles connection setup, message parsing, and cleanup
 * so useChat.ts only needs to worry about event payloads.
 *
 * HOW SERVER-SENT EVENTS (SSE) WORK:
 *   The browser opens a persistent HTTP GET connection to the server.
 *   The server holds the connection open and periodically writes:
 *     "data: {json}\n\n"
 *   Each such block fires an EventSource.onmessage event in the browser.
 *   This is simpler than WebSockets for one-direction (server -> client) streaming.
 *   The browser handles reconnection automatically, but we close manually on "done".
 *
 * FUNCTION EXPORTED:
 *
 *   openStream(query, sessionId, onEvent) -> cleanup function
 *     1. URL-encodes the query: encodeURIComponent(query)
 *     2. Creates: new EventSource(`/query/stream?session_id=${id}&query=${q}`)
 *     3. On each message: JSON.parse(e.data) -> calls onEvent(parsed).
 *     4. On "done" or "error" event: calls es.close() to end the connection.
 *     5. On EventSource.onerror: emits a synthetic error event, closes stream.
 *     6. Returns a cleanup function (() => es.close()) for use in useEffect.
 *
 * WHY QUERY IS A URL PARAM (not POST body):
 *   EventSource only supports GET requests — it cannot send a request body.
 *   This is a browser API limitation, not a design choice.
 *
 * Used by: hooks/useChat.ts
 */