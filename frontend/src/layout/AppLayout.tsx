import { Outlet } from "react-router-dom";
import NavBar from "../features/NavBar/NavBar";
import { navigationItems } from "../features/NavBar";


export default function AppLayout() {
    return (
        <div className="min-h-screen bg-bg text-text">
            <NavBar items={navigationItems} />

            <main className="mx-auto  px-4 py-6 ">
                <Outlet />
            </main>
        </div>
    );
}