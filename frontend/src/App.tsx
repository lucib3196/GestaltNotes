import { BrowserRouter, Routes, Route } from "react-router-dom";
import StudentPage from "./features/StudentPage/StudentPage";
import EducatorPage from "./features/EducatorPage/EducatorPage";
import { AuthPage, RoleRedirect, UnauthorizedPage } from "./features/Auth";
import { Navigate } from "react-router-dom";
import AppLayout from "./layout/AppLayout";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route element={<AppLayout />}>
                    {/* General roots */}
                    <Route path="/login" element={<AuthPage />} />
                    <Route path="/unauthorized" element={<UnauthorizedPage />} />

                    {/* Student Only Roots */}
                    <Route element={<RoleRedirect requiredRoles={["admin", "educator", "student"]} />}>
                        <Route path="/student" element={<StudentPage />} />
                    </Route>

                    <Route element={<RoleRedirect requiredRoles={["educator"]} />}>
                        <Route path="/educator" element={<EducatorPage />} />
                    </Route>


                    <Route path="*" element={<Navigate to="/" replace />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}

export default App;
