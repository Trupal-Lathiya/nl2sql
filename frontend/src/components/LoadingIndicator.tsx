/**
 * components/LoadingIndicator.tsx — Animated Pipeline Step Indicator
 * ===================================================================
 *
 * Displays an animated loading state with the current pipeline step label.
 * Rendered inside an assistant bubble while status === "pending".
 * The step text updates in real-time as SSE "status" events arrive from the backend.
 *
 * VISUAL DESIGN:
 *   Three dots (●●●) with a staggered pulse animation:
 *     Dot 1: animates at 0ms delay
 *     Dot 2: animates at 150ms delay
 *     Dot 3: animates at 300ms delay
 *   Step text shown to the right of the dots in muted color (#94a3b8).
 *
 * STEP TEXT PROGRESSION (what the user sees):
 *   "Classifying query..."     <- Step 0 classifier running
 *   "Searching schemas..."     <- Steps 1-3 embedding + Pinecone search
 *   "Generating SQL..."        <- Step 5 LLM SQL generation
 *   "Running query..."         <- Step 7 SQL Server execution
 *   "Generating summary..."    <- Step 8 LLM summary starting
 *
 * Each step update comes in as a "status" SSE event and is passed down
 * through MessageBubble as the `step` prop.
 *
 * Props:
 *   step: string — Current status message text from the backend
 *
 * Animation: Tailwind animate-bounce with animation-delay via inline style,
 *            or custom CSS keyframes if more control is needed.
 * Dot color: #2563eb (accent blue)
 */