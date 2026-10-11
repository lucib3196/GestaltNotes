import { Outlet, useLocation } from "react-router-dom";
import clsx from "clsx";
import NavBar from "../features/NavBar/NavBar";
import { navigationItems } from "../features/NavBar";

export default function AppLayout() {
  const isChatPage = useLocation().pathname === "/chat";
  return (
    <div className={clsx("bg-bg text-text", isChatPage ? "flex h-svh flex-col overflow-hidden" : "min-h-screen")}>
      <NavBar items={navigationItems} />

      <main className={clsx("px-2 sm:px-4", isChatPage && "flex min-h-0 flex-1 flex-col overflow-hidden")}>
        <Outlet />
      </main>
    </div>
  );
}
