import { Outlet } from "react-router-dom";
import NavBar from "../features/NavBar/NavBar";
import type { NavigationItem } from "../features/NavBar/types";
const navigationItems: NavigationItem[] = [
    { label: "Home", to: "/", type: "route" },
];

export default function AppLayout() {
    return (
        <div className="min-h-screen bg-bg text-text">
            <NavBar items={navigationItems} />

            <main className="mx-auto max-w-7xl px-4 py-6 ">
                <Outlet />
            </main>
        </div>
    );
}