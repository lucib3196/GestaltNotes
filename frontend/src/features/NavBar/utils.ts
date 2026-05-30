import type { User } from "firebase/auth";
import type { ValidRole } from "../../services";
import type { NavigationItem } from "./types";

export function canAccessRoute(
  nav: NavigationItem,
  user: User | null,
  userRole: ValidRole[] // Actual role of the user
): boolean {

  if (nav.requiresAuth && !user) return false;


  // Route has role restrictions
  if (nav.allowedRoles && nav.allowedRoles.length > 0) {
    if (!userRole) return false;
    return nav.allowedRoles.some((role) => userRole.includes(role));
  }
  // Public OR only requires login
  return true;
}
