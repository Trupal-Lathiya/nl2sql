/**
 * vite.config.ts — Vite Development Server & Build Configuration
 * ===============================================================
 *
 * Configures the Vite toolchain for local development and production builds.
 *
 * KEY SETTINGS:
 *
 *   plugins: [react()]
 *     Enables the Vite React plugin which:
 *       - Transforms JSX/TSX files using the React 17+ automatic runtime
 *       - Enables React Fast Refresh (hot reload that preserves component state)
 *
 *   server.port: 5173
 *     Dev server port (default). Change if 5173 is occupied.
 *
 *   server.proxy (optional — not required if backend has CORS):
 *     "/api" -> "http://localhost:8000"
 *     If you ever remove CORS middleware from the FastAPI backend, add a proxy
 *     here so the browser thinks all requests go to the same origin.
 *     Currently not needed since backend has CORS enabled for all origins.
 *
 * PRODUCTION BUILD:
 *   npm run build -> runs tsc (type check) then vite build
 *   Output: dist/ folder with index.html + hashed JS/CSS bundles
 *   Serve with: any static file server (nginx, serve, Vercel, etc.)
 */