import { BrowserRouter, Routes, Route } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";
import StudentPage from "./features/StudentPage/StudentPage";
import EducatorPage from "./features/EducatorPage/EducatorPage";
import AuthPage from "./features/UserAuth/components/AuthPage";
import UnauthorizedPage from "./features/UserAuth/components/UnauthorizedPage";
import RoleRedirect from "./features/UserAuth/components/RoleRedirect";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<AuthPage />} />
                <Route path="/unauthorized" element={<UnauthorizedPage />} />
                <Route
                    path="/student"
                    element={
                        <ProtectedRoute requiredRoles={["student"]}>
                            <StudentPage />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/educator"
                    element={
                        <ProtectedRoute requiredRoles={["educator"]}>
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