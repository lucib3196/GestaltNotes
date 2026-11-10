import type { NavigationItem } from "./types";
export const navigationItems: NavigationItem[] = [
  { label: "Home", to: "/", type: "route" },
  { label: "Chat", to: "/chat", type: "route" },
  {
    label: "Admin",
    to: "/admin",
    type: "route",
    requiresAuth: true,
    allowedRoles: ["admin"],
  },

];
