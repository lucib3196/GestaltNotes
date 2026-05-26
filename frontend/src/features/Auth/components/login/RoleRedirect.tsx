import { Navigate } from "react-router-dom";
import { useAuth } from "../../../../context";

export default function RoleRedirect() {
    const { user, userData, loading } = useAuth();
    const userRoles = userData?.roles
    const isStudent = userRoles?.some((r) => r === "student")
    const isEducator = userRoles?.some((r) => r === "educator")

    if (loading) return <div className="flex items-center justify-center py-20">Loading...</div>;
    if (!user) return <Navigate to="/login" replace />;
    if (isStudent) return <Navigate to="/student" replace />;
    if (isEducator) return <Navigate to="/educator" replace />;
    return <Navigate to="/unauthorized" replace />;
}
