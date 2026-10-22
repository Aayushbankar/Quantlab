export const THEMES = ["abyss", "vellum", "graphite"] as const;

export type ThemeName = (typeof THEMES)[number];

export const THEME_LABELS: Record<ThemeName, string> = {
  abyss: "Abyss",
  vellum: "Vellum",
  graphite: "Graphite",
};

const STORAGE_KEY = "pramaan_theme";

export function normalizeTheme(value: string | null): ThemeName {
  if (value === "light") return "vellum";
  if (value === "graphite") return "graphite";
  if (value === "vellum") return "vellum";
  return "abyss";
}

export function loadTheme(): ThemeName {
  if (typeof window === "undefined") return "abyss";
  return normalizeTheme(window.localStorage.getItem(STORAGE_KEY));
}

export function applyTheme(theme: ThemeName): void {
  if (typeof document === "undefined") return;
  document.documentElement.setAttribute("data-theme", theme);
  window.localStorage.setItem(STORAGE_KEY, theme);
}

export function nextTheme(current: ThemeName): ThemeName {
  const idx = THEMES.indexOf(current);
  return THEMES[(idx + 1) % THEMES.length];
}

export function applyThemeFromString(value: string): ThemeName {
  const theme = normalizeTheme(value);
  applyTheme(theme);
  return theme;
}
