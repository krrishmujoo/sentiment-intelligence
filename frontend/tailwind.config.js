/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        canvas: {
          DEFAULT: "#FAFAFA",
          dark: "#0B0D10",
        },
        surface: {
          DEFAULT: "#FFFFFF",
          alt: "#F2F3F5",
          dark: "#14161A",
          "dark-alt": "#1B1E23",
        },
        ink: {
          DEFAULT: "#14161A",
          soft: "#5B5F68",
          faint: "#8A8D95",
          dark: "#F2F3F5",
          "dark-soft": "#A3A7B0",
        },
        line: {
          DEFAULT: "#E4E5E9",
          dark: "#262A31",
        },
        signal: {
          DEFAULT: "#3454D1",
          soft: "#E9EDFB",
          dark: "#6B85F0",
        },
        positive: {
          DEFAULT: "#1F8A5F",
          soft: "#E5F3EC",
          dark: "#3FB37F",
        },
        neutral: {
          DEFAULT: "#8A6D1F",
          soft: "#F5EFE0",
          dark: "#D1B15C",
        },
        negative: {
          DEFAULT: "#B23B3B",
          soft: "#FAEAEA",
          dark: "#E06666",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "-apple-system", "Segoe UI", "sans-serif"],
        mono: ["IBM Plex Mono", "ui-monospace", "SFMono-Regular", "monospace"],
      },
      boxShadow: {
        panel: "0 1px 2px rgba(20, 22, 26, 0.04), 0 1px 1px rgba(20,22,26,0.03)",
      },
      animation: {
        "fade-in": "fadeIn 200ms ease-out",
        "slide-up": "slideUp 220ms cubic-bezier(0.16, 1, 0.3, 1)",
      },
      keyframes: {
        fadeIn: { from: { opacity: 0 }, to: { opacity: 1 } },
        slideUp: {
          from: { opacity: 0, transform: "translateY(6px)" },
          to: { opacity: 1, transform: "translateY(0)" },
        },
      },
    },
  },
  plugins: [],
};
