import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "./context";
import ProtectedRoute from "./components/ProtectedRoute";
import EducatorPage from "./features/EducatorPage/EducatorPage";
import AuthPage from "./features/UserAuth/components/AuthPage";
import NavBar from "./components/NavBar/NavBar";
import { Section } from "./components/Section";
import { Chat } from "./features/Chat";

function UnauthorizedPage() {
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

function RoleRedirect() {
    const { user, role, loading } = useAuth();

    if (loading) return <div className="flex items-center justify-center py-20">Loading...</div>;
    if (!user) return <Navigate to="/login" replace />;
    if (role === "student") return <Navigate to="/student" replace />;
    if (role === "educator") return <Navigate to="/educator" replace />;
    return <Navigate to="/unauthorized" replace />;
}

function StudentPage() {
    return (
        <>
            <NavBar />
            <Section>
                <Chat />
            </Section>
        </>
    );
}

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<AuthPage />} />
                <Route path="/unauthorized" element={<UnauthorizedPage />} />
                <Route
                    path="/student"
                    element={
                        <ProtectedRoute requiredRole="student">
                            <StudentPage />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/educator"
                    element={
                        <ProtectedRoute requiredRole="educator">
                            <EducatorPage />
                        </ProtectedRoute>
                    }
                />
                <Route path="*" element={<RoleRedirect />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;