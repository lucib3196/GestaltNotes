import { Navigate } from "react-router-dom";
import { useAuth } from "../context";

interface ProtectedRouteProps {
    children: React.ReactNode;
    requiredRole: string;
}

export default function ProtectedRoute({ children, requiredRole }: ProtectedRouteProps) {
    const { user, role, loading } = useAuth();

    if (loading) {
        return <div className="flex items-center justify-center py-20">Loading...</div>;
    }

    if (!user) {
        return <Navigate to="/login" replace />;
    }

    if (role !== requiredRole) {
        return <Navigate to="/unauthorized" replace />;
    }

    return <>{children}</>;
}