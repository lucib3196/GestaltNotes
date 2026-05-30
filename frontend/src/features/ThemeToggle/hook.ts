import { useEffect, useState } from "react";

type Theme = "dark" | "light";

export default function useTheme() {
  const [theme, setTheme] = useState<Theme>("dark");

  useEffect(() => {
    const saved = localStorage.getItem("theme");
    const next = saved === "light" || saved === "dark" ? saved : "dark";
    document.documentElement.dataset.theme = next;
    setTheme(next);
  }, []);

  function toggleTheme() {
    setTheme((current) => {
      const next = current === "dark" ? "light" : "dark";
      document.documentElement.dataset.theme = next;
      localStorage.setItem("theme", next);
      return next;
    });
  }

  return { theme, toggleTheme };
}
