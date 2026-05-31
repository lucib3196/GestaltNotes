import type { NavigationItem } from "./types";
export const navigationItems: NavigationItem[] = [
    { label: "Home", to: "/", type: "route" },
    { label: "Chat", to: "/chat", type: "route" },
    { label: "My Content", to: "/my_content", type: "route" },
    { label: "Lectures", to: "/lecture", type: "route" }
];