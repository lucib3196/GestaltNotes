import { useAuth } from "../../../context";

export default function UnauthorizedPage() {
    const { logout } = useAuth();
    return (
        <div className="flex flex-col items-center justify-center py-20 gap-4">
            <h2 className="text-xl font-semibold text-slate-800">Unauthorized</h2>
            <p className="text-slate-500">You don't have access to this page.</p>
            <button onClick={logout} className="text-sm text-red-500 hover:underline">
                Logout
            </button>
        </div>
    );
}