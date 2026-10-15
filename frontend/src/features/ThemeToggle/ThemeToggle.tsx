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
                "relative inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-full p-1 sm:w-19",
                "bg-surface text-text-muted hover:bg-surface-muted",
                "sm:border sm:border-border sm:shadow-soft sm:hover:border-border-strong",
                "transition-colors duration-300",
                "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60",
            ].join(" ")}
        >
            <span className="text-lg sm:hidden" aria-hidden="true">
                {isDark ? <MdLightMode /> : <MdDarkMode />}
            </span>
            <span
                aria-hidden="true"
                className={[
                    "absolute left-1 hidden h-8 w-8 rounded-full bg-accent shadow-md sm:block",
                    "transition-transform duration-300 ease-out motion-reduce:transition-none",
                    isDark ? "translate-x-9" : "translate-x-0",
                ].join(" ")}
            />
            <span
                aria-hidden="true"
                className="relative z-10 hidden w-full items-center justify-between px-1.5 text-base sm:flex"
            >
                <MdLightMode
                    className={isDark ? "text-text-soft" : "text-white"}
                />
                <MdDarkMode
                    className={isDark ? "text-white" : "text-text-soft"}
                />
            </span>
        </button>
    );
}
