import { Navigate, useLocation, Outlet } from "react-router-dom";
import { useAuth } from "../../../../context";
import type { ValidRole } from "../../../../services";
export default function RoleRedirect({ allow }: { allow: ValidRole[] }) {
    const { user, userData, loading,} = useAuth();
    const userRoles = userData?.roles
    const location = useLocation();

    console.log("User roles", userRoles)



    if (loading) return <div className="flex items-center justify-center py-20">Loading...</div>;


    if (!user) return <Navigate to="/login" state={{ from: location }} replace />;
    if (!allow.some((r) => userRoles?.includes(r))) {
        return <Navigate to="/forbidden" replace />;
    }
    return <Outlet />;
}
