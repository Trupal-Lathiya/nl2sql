/**
 * components/ResultsTable.tsx — Database Query Results Grid
 * ==========================================================
 *
 * Renders the actual rows returned by the SQL query in a styled data table.
 * Rendered inside an assistant bubble when status === "done".
 *
 * FEATURES:
 *
 *   1. ROW COUNT HEADER
 *      "Showing {rows.length} of {totalRowCount} rows"
 *      If totalRowCount > rows.length, the backend truncated for display
 *      and saved the full result to CSV.
 *
 *   2. DATA TABLE
 *      Wrapped in overflow-x: auto div for horizontal scroll on narrow screens.
 *      Sticky header: position sticky, top 0, background #1e1e2e so it doesn't
 *        disappear when scrolling a tall result set.
 *      Column headers: text-xs, uppercase, text #94a3b8 (muted), border-bottom.
 *      Data rows: alternating row colors (#1e1e2e and a slightly darker shade).
 *      Cell borders: subtle #2a2a3d bottom border.
 *      Text: #e2e8f0, text-sm, padding 8px 12px.
 *
 *   3. CSV DOWNLOAD BUTTON
 *      "⬇️ Download CSV" button — fully client-side, no server round-trip:
 *        const csv = [columns.join(","), ...rows.map(r => r.join(","))].join("\\n")
 *        const blob = new Blob([csv], { type: "text/csv" })
 *        const url = URL.createObjectURL(blob)
 *        anchor.href = url; anchor.download = "results.csv"; anchor.click()
 *      Styled: bg #1e1e2e, border #2a2a3d, hover bg #2a2a3d, text-sm.
 *
 *   4. EMPTY STATE
 *      If rows.length === 0: shows "Query returned no results." centered in muted text.
 *      No empty table rendered.
 *
 * Props:
 *   columns: string[]
 *   rows: any[][]
 *   totalRowCount: number
 */