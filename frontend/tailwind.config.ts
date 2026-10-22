import type { Config } from "tailwindcss";

export default {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        crimson: "rgb(var(--crimson-rgb) / <alpha-value>)",
        crimsonDeep: "rgb(var(--crimson-deep-rgb) / <alpha-value>)",
        darkSlate: "rgb(var(--dark-slate-rgb) / <alpha-value>)",
        stormyTeal: "rgb(var(--stormy-teal-rgb) / <alpha-value>)",
        pacificCyan: "rgb(var(--pacific-cyan-rgb) / <alpha-value>)",
        turquoise: "rgb(var(--turquoise-rgb) / <alpha-value>)",

        canvas: "rgb(var(--canvas-rgb) / <alpha-value>)",
        panel: "rgb(var(--panel-rgb) / <alpha-value>)",
        card: "rgb(var(--card-rgb) / <alpha-value>)",
        cardHover: "rgb(var(--card-hover-rgb) / <alpha-value>)",
        elev: "rgb(var(--elev-rgb) / <alpha-value>)",
        rule: "rgb(var(--border-rgb) / <alpha-value>)",
        ruleHighlight: "rgb(var(--turquoise-rgb) / 0.5)",

        primary: "rgb(var(--pacific-cyan-rgb) / <alpha-value>)",
        primaryHover: "rgb(var(--pacific-cyan-rgb) / 0.85)",
        alpha: "rgb(var(--turquoise-rgb) / <alpha-value>)",
        friction: "rgb(var(--crimson-rgb) / <alpha-value>)",

        accentNet: "rgb(var(--accent-net-rgb) / <alpha-value>)",
        accentGross: "rgb(var(--accent-gross-rgb) / <alpha-value>)",
        accentFriction: "rgb(var(--accent-friction-rgb) / <alpha-value>)",

        inkText: "rgb(var(--text-primary-rgb) / <alpha-value>)",
        mutedText: "rgb(var(--text-muted-rgb) / <alpha-value>)",
        tertiaryText: "rgb(var(--text-tertiary-rgb) / <alpha-value>)",
      },
      fontFamily: {
        sans: ["var(--font-geist-sans)", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["var(--font-geist-mono)", "ui-monospace", "SFMono-Regular", "monospace"],
        serif: ["var(--font-instrument)", "Georgia", "serif"],
      },
      fontSize: {
        display: ["var(--t-display)", { lineHeight: "0.88", letterSpacing: "-0.035em" }],
        h1: ["var(--t-h1)", { lineHeight: "0.95", letterSpacing: "-0.03em" }],
        h2: ["var(--t-h2)", { lineHeight: "1.06", letterSpacing: "-0.022em" }],
        h3: ["var(--t-h3)", { lineHeight: "1.18", letterSpacing: "-0.018em" }],
        lead: ["var(--t-lead)", { lineHeight: "1.55", letterSpacing: "-0.012em" }],
        label: ["var(--t-label)", { lineHeight: "1.3", letterSpacing: "0.09em" }],
      },
      borderRadius: {
        DEFAULT: "0.5rem",
        sm: "0.375rem",
        md: "0.625rem",
        lg: "0.875rem",
        xl: "1rem",
        "2xl": "1.25rem",
        "3xl": "1.5rem",
      },
      boxShadow: {
        xs: "0 1px 2px rgb(var(--shadow-tint) / var(--shadow-alpha))",
        card: "0 1px 2px rgb(var(--shadow-tint) / 0.28), 0 8px 28px rgb(var(--shadow-tint) / 0.28)",
        lift: "0 2px 6px rgb(var(--shadow-tint) / 0.32), 0 18px 48px rgb(var(--shadow-tint) / 0.38)",
        glow: "0 0 0 1px rgb(var(--turquoise-rgb) / 0.35), 0 12px 40px rgb(var(--turquoise-rgb) / 0.14)",
        panel: "inset 0 1px 0 rgb(255 255 255 / 0.03)",
      },
      transitionTimingFunction: {
        out: "cubic-bezier(0.16, 1, 0.3, 1)",
        inOut: "cubic-bezier(0.76, 0, 0.24, 1)",
        back: "cubic-bezier(0.34, 1.56, 0.64, 1)",
      },
      transitionDuration: {
        micro: "150ms",
        small: "250ms",
        medium: "400ms",
        large: "700ms",
      },
      keyframes: {
        marquee: {
          from: { transform: "translateX(0)" },
          to: { transform: "translateX(-50%)" },
        },
        glowPulse: {
          "0%, 100%": { opacity: "0.5", transform: "scale(1)" },
          "50%": { opacity: "0.8", transform: "scale(1.06)" },
        },
        riseIn: {
          from: { opacity: "0", transform: "translateY(16px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
      },
      animation: {
        marquee: "marquee 42s linear infinite",
        glowPulse: "glowPulse 9s ease-in-out infinite",
        riseIn: "riseIn 0.55s cubic-bezier(0.16, 1, 0.3, 1) both",
      },
      backgroundImage: {
        "gradient-main": "linear-gradient(135deg, #28464bff 0%, #326771ff 50%, #2c8c99ff 100%)",
        "gradient-banner":
          "linear-gradient(90deg, #931621 0%, #28464b 34%, #326771 58%, #2c8c99 80%, #42d9c8 100%)",
        "gradient-signal":
          "linear-gradient(90deg, rgb(var(--turquoise-rgb)) 0%, rgb(var(--pacific-cyan-rgb)) 100%)",
      },
    },
  },
  plugins: [],
} satisfies Config;
