/**
 * components/MessageBubble.tsx — Individual Chat Message Renderer
 * ================================================================
 *
 * Renders a single chat message. Appearance and content change based on
 * the message's role ("user" | "assistant") and status.
 *
 * USER BUBBLE (role === "user"):
 *   Alignment:    right (justify-end)
 *   Background:   #2563eb (accent blue)
 *   Text color:   white
 *   Border radius: 18px 18px 4px 18px  (flat bottom-right = "sent" style)
 *   Label above:  "You 👤"
 *   Content:      plain text of the user's query
 *
 * ASSISTANT BUBBLE (role === "assistant"):
 *   Alignment:    left (justify-start)
 *   Background:   #1e1e2e
 *   Border:       1px solid #2a2a3d
 *   Text color:   #e2e8f0
 *   Border radius: 18px 18px 18px 4px  (flat bottom-left = "received" style)
 *   Label above:  "NL2SQL"
 *
 *   Content varies by STATUS:
 *     "pending"   -> <LoadingIndicator step={currentStep} />
 *                    Shows animated dots + current pipeline step name
 *     "streaming" -> <StreamingSummary content={content} isStreaming={true} />
 *                    Summary text building up word by word with blinking cursor
 *     "done"      -> <StreamingSummary isStreaming={false} />
 *                    + <SqlDisplay sql={...} retrievedTables={...} />
 *                    + <ResultsTable columns={...} rows={...} total={...} />
 *     "error"     -> Red bordered box with errorMessage text
 *                    Uses text-red-400 and border-red-800 colors
 *
 * TIMESTAMP:
 *   Displayed below each bubble in muted text (#475569).
 *   Formatted as locale time: new Date(message.timestamp).toLocaleTimeString()
 *
 * Props: message: ChatMessage
 * Depends on: LoadingIndicator, StreamingSummary, SqlDisplay, ResultsTable
 */