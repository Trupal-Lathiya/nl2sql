/**
 * components/ChatInput.tsx — User Message Input Bar
 * ==================================================
 *
 * The text input area fixed at the bottom of the chat window. Users type
 * their natural language database questions here and submit them.
 *
 * VISUAL STRUCTURE:
 *   Container: full width, padding, background #1e1e2e, top border #2a2a3d
 *   Inner row:  [text input (flex-1)] [Send button]
 *
 * INPUT ELEMENT:
 *   type="text" (single-line — not textarea, queries are usually one line)
 *   Placeholder: "Ask a question about your database..."
 *   autoFocus: true (user can type immediately without clicking)
 *   Background:  transparent (inherits container bg)
 *   Text color:  #e2e8f0
 *   Focus ring:  none (remove default browser outline, use custom if desired)
 *   Disabled:    when isStreaming === true (prevent sending while processing)
 *
 * SEND BUTTON:
 *   Label:    "Send" or send arrow icon (->)
 *   Style:    bg #2563eb, hover #1d4ed8, text white, rounded, px-4 py-2
 *   Disabled: when isStreaming === true OR inputValue.trim() === ""
 *   Disabled style: bg #475569, cursor-not-allowed
 *
 * INTERACTION BEHAVIORS:
 *   Submit on Enter key (without Shift) via onKeyDown handler.
 *   Submit on Send button click.
 *   After submit: clear inputValue to "" immediately.
 *   Trim whitespace before checking empty or sending.
 *   Do nothing (no API call) if trimmed value is empty.
 *
 * STATE:
 *   inputValue: string  — controlled input value
 *
 * Props:
 *   onSend: (query: string) => void
 *   isStreaming: boolean
 */