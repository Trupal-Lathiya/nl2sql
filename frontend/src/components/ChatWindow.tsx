/**
 * components/ChatWindow.tsx — Main Chat Content Area
 * ===================================================
 *
 * The central column of the app. Contains the scrollable message history
 * and the fixed input bar at the bottom.
 *
 * LAYOUT STRUCTURE:
 *   flex-col, height 100%, overflow hidden at the container level.
 *   Message list area: flex-1, overflow-y auto (scrolls independently).
 *   Input bar: fixed to bottom via flex layout or sticky positioning.
 *
 * FOUR RESPONSIBILITIES:
 *
 *   1. WELCOME SCREEN (empty state)
 *      When messages.length === 0, renders a centered welcome message with
 *      2-3 example queries so new users know what to type.
 *      Example: "Try: 'Show me all active drivers'"
 *
 *   2. MESSAGE LIST
 *      Maps messages array -> one <MessageBubble key={m.id} message={m} /> each.
 *      A dummy <div ref={bottomRef} /> sits after the last message as a scroll target.
 *
 *   3. AUTO-SCROLL TO BOTTOM
 *      useEffect watches messages array length.
 *      On change: bottomRef.current?.scrollIntoView({ behavior: "smooth" })
 *      This keeps the newest message visible without the user manually scrolling.
 *
 *   4. CHAT INPUT
 *      Renders <ChatInput onSend={onSendMessage} isStreaming={isStreaming} />
 *      isStreaming prop disables the input while a query is in progress.
 *
 * Props:
 *   messages: ChatMessage[]
 *   isStreaming: boolean
 *   onSendMessage: (query: string) => void
 * Depends on: MessageBubble.tsx, ChatInput.tsx, types/index.ts
 */