import { BrowserRouter, Routes, Route } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";
import StudentPage from "./features/StudentPage/StudentPage";
import EducatorPage from "./features/EducatorPage/EducatorPage";
import { AuthPage, RoleRedirect, UnauthorizedPage } from "./features/Auth";
import AppLayout from "./layout/AppLayout";
function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route element={<AppLayout />}>
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
                </Route>
            </Routes>
        </BrowserRouter>
    );
}

export default App;
