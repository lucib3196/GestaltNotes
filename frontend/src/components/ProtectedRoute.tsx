import { Navigate } from "react-router-dom";
import { useAuth } from "../context";
import type { ValidRole } from "../services";

interface ProtectedRouteProps {
    children: React.ReactNode;
    requiredRoles: ValidRole[];
}

export default function ProtectedRoute({ children, requiredRoles }: ProtectedRouteProps) {
    const { user, userData, loading } = useAuth();
    if (loading) {
        return <div className="flex items-center justify-center py-20">Loading...</div>;
    }

    if (!user) {
        return <Navigate to="/login" replace />;
    }
    const userRoles = userData?.roles

    if (!requiredRoles.some((r) => userRoles?.includes(r))) {
        return <Navigate to="/unauthorized" replace />;
    }

    return <>{children}</>;
}