import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../../../../context";

export default function PasswordResetGuard() {
    const { user, userData, loading } = useAuth();

    if (loading) {
        return <div className="flex items-center justify-center py-20">Loading...</div>;
    }

    if (!user) {
        return <Navigate to="/login" replace />;
    }

    if (userData?.force_password_reset) {
        return <Navigate to="/login" replace />;
    }

    return <Outlet />;
}
