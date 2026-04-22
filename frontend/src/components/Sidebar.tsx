/**
 * components/Sidebar.tsx — Left Navigation & Info Panel
 * ======================================================
 *
 * Fixed left sidebar (240px wide). Contains app branding, session stats,
 * and the destructive "Clear Chat" action. Does not scroll.
 *
 * LAYOUT (top to bottom, full height):
 *
 *   1. APP HEADER (top, padded)
 *      Primary title:  "NL2SQL" with database icon
 *      Subtitle:       "Natural Language -> SQL" in muted text
 *      Divider line below.
 *
 *   2. SESSION STATS (middle section)
 *      "Messages" label with count badge showing messages.length.
 *      Updates reactively as the user has more conversations.
 *      Styled as a small stat card with muted label and white count number.
 *
 *   3. CLEAR CHAT BUTTON (conditionally rendered)
 *      Only shown when messages.length > 0 (hidden on empty chat — no need to clear nothing).
 *      "🗑️ Clear Chat" — danger/warning style:
 *        Background: transparent, border: #ef4444 (red), text: #ef4444
 *        Hover: bg #ef444420 (red tint)
 *      On click: calls onClearChat(sessionId) which:
 *        - Clears the messages array in useChat.ts
 *        - Calls DELETE /query/memory on the backend
 *
 *   4. FOOTER (pinned to bottom with mt-auto)
 *      "Powered by Pinecone + Groq + SQL Server"
 *      text-xs, text-dim (#475569), centered.
 *
 * STYLING:
 *   Background:   #1e1e2e (slightly lighter than app background)
 *   Right border: 1px solid #2a2a3d
 *   Width:        240px, flex-shrink-0 (never collapses)
 *
 * Props:
 *   messages: ChatMessage[]
 *   sessionId: string
 *   onClearChat: (sessionId: string) => void
 */