/**
 * postcss.config.js — PostCSS Plugin Pipeline
 * ============================================
 *
 * Required boilerplate for Tailwind CSS to work with Vite.
 * PostCSS processes the raw CSS file (which contains @tailwind directives)
 * and runs it through the plugin chain.
 *
 * PLUGINS (in order):
 *
 *   tailwindcss
 *     Expands @tailwind base, @tailwind components, @tailwind utilities
 *     directives in src/index.css into actual CSS rules based on your
 *     tailwind.config.js theme and the classes used in your components.
 *
 *   autoprefixer
 *     Automatically adds vendor prefixes (-webkit-, -moz-, -ms-) to CSS
 *     properties that need them for cross-browser compatibility.
 *     Example: transform -> -webkit-transform for older Safari versions.
 *
 * This file rarely needs to be modified. It is required infrastructure.
 */