import { Navigate } from "react-router-dom";
import { useAuth } from "../../../context";

export default function RoleRedirect() {
    const { user, role, loading } = useAuth();

    if (loading) return <div className="flex items-center justify-center py-20">Loading...</div>;
    if (!user) return <Navigate to="/login" replace />;
    if (role === "student") return <Navigate to="/student" replace />;
    if (role === "educator") return <Navigate to="/educator" replace />;
    return <Navigate to="/unauthorized" replace />;
}