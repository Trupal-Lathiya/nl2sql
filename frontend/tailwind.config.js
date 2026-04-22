/**
 * tailwind.config.js — Tailwind CSS Theme Configuration
 * ======================================================
 *
 * Configures Tailwind to purge unused CSS in production and extends the
 * default theme with the project's custom color palette.
 *
 * CONTENT PATHS:
 *   ["./index.html", "./src/**\/*.{ts,tsx}"]
 *   Tailwind scans these files for class name strings at build time.
 *   Any class used in these files is kept; all others are removed from the
 *   production CSS bundle (tree-shaking = tiny CSS output).
 *
 * THEME EXTENSIONS (custom colors matching design spec):
 *   These let you write Tailwind classes like bg-app-bg, text-text-primary, etc.
 *
 *   app-bg:       "#0e1117"   — Main application background
 *   card-bg:      "#1e1e2e"   — Message bubbles, sidebar, panels
 *   card-border:  "#2a2a3d"   — All border colors
 *   text-primary: "#e2e8f0"   — Main readable text
 *   text-muted:   "#94a3b8"   — Secondary text, placeholders, labels
 *   text-dim:     "#475569"   — Timestamps, footers, very secondary text
 *   accent:       "#2563eb"   — Buttons, user bubble, links
 *   accent-hover: "#1d4ed8"   — Hover state for accent elements
 *   divider:      "#1e293b"   — Horizontal rule / separator lines
 */