/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#06b6d4",
        "primary-light": "#22d3ee",
        "primary-dark": "#0891b2",
        secondary: "#8b5cf6",
        "secondary-light": "#a78bfa",
        "secondary-dark": "#7c3aed",
        accent: "#ec4899",
        "accent-light": "#f472b6",
        success: "#10b981",
        "success-light": "#6ee7b7",
        warning: "#f59e0b",
        error: "#ef4444",
        "text-primary": "#f1f5f9",
        "text-secondary": "#cbd5e1",
        "text-tertiary": "#94a3b8",
      },
      backgroundColor: {
        glass: "rgba(15, 23, 42, 0.7)",
      },
      borderColor: {
        glass: "rgba(255, 255, 255, 0.1)",
      },
      backdropBlur: {
        glass: "16px",
        "glass-lg": "20px",
      },
      boxShadow: {
        glass: "0 8px 32px rgba(0, 0, 0, 0.3)",
      },
      borderRadius: {
        sm: "6px",
        md: "12px",
        lg: "16px",
        xl: "20px",
      },
    },
  },
  plugins: [],
}
