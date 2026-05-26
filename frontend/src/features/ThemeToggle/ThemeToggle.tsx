import { MdDarkMode, MdLightMode } from "react-icons/md";
import useTheme from "./hook";

export default function ThemeToggle() {
    const { theme, toggleTheme } = useTheme();
    const isDark = theme === "dark";

    return (
        <button
            id="themeToggle"
            type="button"
            onClick={toggleTheme}
            aria-label={`Switch to ${isDark ? "light" : "dark"} mode`}
            aria-pressed={isDark}
            className={[
                "group relative inline-flex h-10 w-19 items-center rounded-full border p-1",
                "bg-surface border-border shadow-soft",
                "transition-colors duration-300 hover:border-border-strong",
                "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60 focus-visible:ring-offset-2 focus-visible:ring-offset-bg",
            ].join(" ")}
        >
            <span
                className={[
                    "absolute h-8 w-8 rounded-full bg-accent shadow-md",
                    "transition-transform duration-300 ease-out",
                    isDark ? "translate-x-9" : "translate-x-0",
                ].join(" ")}
            />
            <span className="relative z-10 flex w-full items-center justify-between px-1.5 text-base">
                <MdLightMode
                    className={[
                        "transition-colors duration-300",
                        isDark ? "text-text-soft" : "text-white",
                    ].join(" ")}
                />
                <MdDarkMode
                    className={[
                        "transition-colors duration-300",
                        isDark ? "text-white" : "text-text-soft",
                    ].join(" ")}
                />
            </span>
        </button>
    );
}
