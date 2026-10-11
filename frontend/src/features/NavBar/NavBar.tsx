import { useAuth } from "../Auth";
import type { NavigationItem, DropDownNavRoute, Base } from "./types";
import clsx from "clsx";
import { canAccessRoute } from "./utils";
import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
  Menu,
  MenuButton,
  MenuItem,
  MenuItems,
} from "@headlessui/react";
import { Bars3Icon, XMarkIcon } from "@heroicons/react/24/outline";
import { ChevronDownIcon } from "@heroicons/react/20/solid";
import { Link, NavLink } from "react-router-dom";
import { ThemeToggle } from "../ThemeToggle";
interface NavBarProps {
  items: NavigationItem[];
}

function routePillClassName(isActive: boolean) {
  return clsx(
    "inline-flex items-center rounded-full px-3 py-1.5 text-sm font-medium transition-all duration-200",
    "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/50",
    isActive
      ? "bg-surface-strong text-text shadow-sm"
      : "text-text-muted hover:bg-surface-muted hover:text-text",
  );
}

function RoutePill({ to, label }: Base) {
  return (
    <NavLink to={to} className={({ isActive }) => routePillClassName(isActive)}>
      {label}
    </NavLink>
  );
}

function DropDownNav({ nav }: { nav: DropDownNavRoute }) {
  return (
    <Menu as="div" className="relative">
      <MenuButton
        className={clsx(
          "inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-sm font-medium",
          "text-text-muted transition-all duration-200 hover:bg-surface-muted hover:text-text",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/50",
        )}
      >
        <span>{nav.label}</span>
        <ChevronDownIcon className="h-4 w-4" />
      </MenuButton>

      <MenuItems
        anchor="bottom start"
        className={clsx(
          "z-50 mt-2 w-56 rounded-xl border border-border bg-surface-strong p-1.5 shadow-soft backdrop-blur-xl",
          "focus:outline-none",
        )}
      >
        {nav.items.map((child) => (
          <MenuItem key={child.to}>
            {({ focus }) => (
              <Link
                to={child.to}
                className={clsx(
                  "block rounded-xl px-3 py-2 text-sm transition-colors",
                  focus ? "bg-surface-strong text-text" : "text-text-muted"
                )}
              >
                {child.label}
              </Link>
            )}
          </MenuItem>
        ))}
      </MenuItems>
    </Menu>
  );
}

export default function NavBar({ items }: NavBarProps) {
  const { user, userData, logout } = useAuth();
  const role = userData?.roles ?? [];
  const visibleItems = items.filter((item) => canAccessRoute(item, user, role));

  return (
    <Disclosure
      as="nav"
      className={clsx(
        "sticky top-0 z-40 shrink-0 border-b border-border/80 bg-surface/90 text-text backdrop-blur-xl",
        "supports-backdrop-filter:bg-surface/70",
      )}
    >
      <div className="mx-auto flex h-10 max-w-7xl items-center px-3 sm:px-6 lg:px-8">
        <div className="md:hidden">
          <DisclosureButton
            className={clsx(
              "group inline-flex items-center justify-center rounded-lg p-2 text-text-muted transition",
              "hover:bg-surface-muted hover:text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/50",
            )}
            aria-label="Toggle navigation menu"
          >
            <Bars3Icon className="block h-6 w-6 group-data-open:hidden" />
            <XMarkIcon className="hidden h-6 w-6 group-data-open:block" />
          </DisclosureButton>
        </div>

        <div className="hidden md:block">
          <nav className="flex items-center gap-1" aria-label="Primary views">
            {visibleItems.map((item) =>
              item.type === "dropdown" ? (
                <DropDownNav key={item.label} nav={item} />
              ) : (
                <RoutePill key={item.to} to={item.to} label={item.label} />
              ),
            )}
          </nav>
        </div>

        <div className="ml-auto flex items-center gap-2">
          <ThemeToggle />
          {user ? (
            <>
              <Link
                to="/account"
                className={clsx(
                  "hidden rounded-full px-3 py-1.5 text-sm font-medium text-text-muted transition md:inline-flex",
                  "hover:bg-surface-muted hover:text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/50",
                )}
              >
                My Account
              </Link>
              <button
                type="button"
                onClick={logout}
                className={clsx(
                  "hidden rounded-full border border-border-strong bg-button-secondary px-3 py-1.5 text-sm font-medium text-text transition md:inline-flex",
                  "hover:border-accent/40 hover:text-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/50",
                )}
              >
                Logout
              </button>
            </>
          ) : (
            <Link
              to="/login"
              className={clsx(
                "hidden rounded-full border border-border-strong bg-button-secondary px-3 py-1.5 text-sm font-medium text-text transition md:inline-flex",
                "hover:border-accent/40 hover:text-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/50",
              )}
            >
              Sign Up / Log In
            </Link>
          )}
        </div>
      </div>

      <DisclosurePanel className="max-h-[calc(100dvh-4rem)] overflow-y-auto border-t border-border bg-surface md:hidden">
        <div className="space-y-1 px-3 py-3">
          {visibleItems.map((item) =>
            item.type === "dropdown" ? (
              <div key={item.label} className="py-2">
                <p className="px-3 pb-1 text-xs font-semibold uppercase tracking-wide text-text-soft">
                  {item.label}
                </p>
                {item.items.map((child) => (
                  <DisclosureButton
                    key={child.to}
                    as={Link}
                    to={child.to}
                    className="flex min-h-11 items-center rounded-lg px-3 text-sm font-medium text-text-muted hover:bg-surface-muted hover:text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/50"
                  >
                    {child.label}
                  </DisclosureButton>
                ))}
              </div>
            ) : (
              <DisclosureButton
                key={item.to}
                as={Link}
                to={item.to}
                className="flex min-h-11 items-center rounded-lg px-3 text-sm font-medium text-text-muted hover:bg-surface-muted hover:text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/50"
              >
                {item.label}
              </DisclosureButton>
            ),
          )}
        </div>
        <div className="space-y-1 border-t border-border px-3 py-3">
          {user ? (
            <>
              <DisclosureButton
                as={Link}
                to="/account"
                className="flex min-h-11 items-center rounded-lg px-3 text-sm font-medium text-text-muted hover:bg-surface-muted hover:text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/50"
              >
                My Account
              </DisclosureButton>
              <DisclosureButton
                onClick={() => void logout()}
                className="flex min-h-11 w-full items-center rounded-lg px-3 text-sm font-medium text-text-muted hover:bg-surface-muted hover:text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/50"
              >
                Log out
              </DisclosureButton>
            </>
          ) : (
            <DisclosureButton
              as={Link}
              to="/login"
              className="flex min-h-11 items-center rounded-lg bg-button-secondary px-3 text-sm font-medium text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/50"
            >
              Sign up / Log in
            </DisclosureButton>
          )}
        </div>
      </DisclosurePanel>
    </Disclosure>
  );
}
