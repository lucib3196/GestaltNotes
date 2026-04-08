import { useAuth } from "../../context";
// this is ai generated placeholder page for now
export default function EducatorPage() {
    const { logout } = useAuth();

    return (
        <div className="flex flex-col h-screen">
            <div className="flex justify-between items-center px-6 py-4 border-b">
                <h1 className="text-xl font-semibold">Educator Dashboard</h1>
                <button onClick={logout} className="text-sm text-red-500 hover:underline">
                    Logout
                </button>
            </div>
            <div className="flex flex-col items-center justify-center flex-1 gap-4">
                <h2 className="text-lg font-medium text-slate-700">Welcome, Professor</h2>
                <p className="text-slate-500">Course management and note uploads coming soon.</p>
            </div>
        </div>
    );
}