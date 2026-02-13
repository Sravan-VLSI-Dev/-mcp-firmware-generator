/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx}", "./public/index.html"],
  theme: {
    extend: {
      colors: {
        ink: {
          900: "#0b0f14",
          800: "#111827",
          700: "#1f2937",
          600: "#374151"
        },
        core: {
          500: "#4f46e5",
          400: "#6366f1",
          300: "#818cf8"
        },
        signal: {
          500: "#22d3ee",
          400: "#38bdf8",
          300: "#7dd3fc"
        },
        grid: {
          500: "#1f2937",
          400: "#334155"
        }
      },
      fontFamily: {
        sans: ["Space Grotesk", "system-ui", "sans-serif"],
        mono: ["IBM Plex Mono", "ui-monospace", "SFMono-Regular", "Menlo", "monospace"]
      },
      boxShadow: {
        core: "0 30px 80px rgba(15, 23, 42, 0.55)",
        signal: "0 0 30px rgba(34, 211, 238, 0.35)"
      },
      backgroundImage: {
        "radial-fade": "radial-gradient(circle at center, rgba(99,102,241,0.2), transparent 60%)"
      }
    }
  },
  plugins: []
};
