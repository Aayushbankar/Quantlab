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
        // User's Exact Palette Tokens
        crimson: "rgb(var(--crimson-rgb) / <alpha-value>)",
        darkSlate: "rgb(var(--dark-slate-rgb) / <alpha-value>)",
        stormyTeal: "rgb(var(--stormy-teal-rgb) / <alpha-value>)",
        pacificCyan: "rgb(var(--pacific-cyan-rgb) / <alpha-value>)",
        turquoise: "rgb(var(--turquoise-rgb) / <alpha-value>)",
        
        // Semantic Application Aliases
        canvas: "rgb(var(--canvas-rgb) / <alpha-value>)",
        panel: "rgb(var(--panel-rgb) / <alpha-value>)",
        card: "rgb(var(--card-rgb) / <alpha-value>)",
        cardHover: "rgb(var(--card-hover-rgb) / <alpha-value>)",
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
      },
      backgroundImage: {
        'gradient-main': 'linear-gradient(135deg, #28464bff 0%, #326771ff 50%, #2c8c99ff 100%)',
        'gradient-banner': 'linear-gradient(90deg, #931621ff 0%, #28464bff 25%, #326771ff 50%, #2c8c99ff 75%, #42d9c8ff 100%)',
      }
    },
  },
  plugins: [],
} satisfies Config;
