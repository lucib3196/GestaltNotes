import type { Config } from "tailwindcss";

export default {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "var(--bg)",
        surface: "var(--surface)",
        "surface-strong": "var(--surface-strong)",
        "surface-muted": "var(--surface-muted)",
        border: "var(--border)",
        "border-strong": "var(--border-strong)",
        text: "var(--text)",
        "text-muted": "var(--text-muted)",
        "text-soft": "var(--text-soft)",
        accent: "var(--accent)",
        "accent-strong": "var(--accent-strong)",
        "button-secondary": "var(--button-secondary)",
        code: "var(--code-bg)",
      },
      fontFamily: {
        sans: ["var(--font-sans)"],
        mono: ["var(--font-mono)"],
      },
      borderRadius: {
        xl: "var(--radius-xl)",
        lg: "var(--radius-lg)",
        md: "var(--radius-md)",
      },
      boxShadow: {
        soft: "var(--shadow-soft)",
      },
      transitionTimingFunction: {
        base: "var(--transition-base)",
      },
      transitionDuration: {
        base: "var(--duration-base)",
      },
    },
  },
} satisfies Config;