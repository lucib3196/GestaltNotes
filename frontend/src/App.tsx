import { BrowserRouter, Routes, Route } from "react-router-dom";
import { HomePage, ChatPage, MyAccount } from "./pages";
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
                    <Route path="/" element={<HomePage />} />
                    <Route path="/login" element={<AuthPage />} />
                    <Route path="/account" element={<MyAccount />} />
                    <Route path="/unauthorized" element={<UnauthorizedPage />} />

                    {/* Student Only Roots */}
                    <Route element={<RoleRedirect allow={["admin", "educator", "student"]} />}>
                        <Route path="/chat" element={<ChatPage />} />
                    </Route>

                    <Route element={<RoleRedirect allow={["educator"]} />}>
                        <Route path="/educator" element={<EducatorPage />} />
                    </Route>


                    <Route path="*" element={<Navigate to="/" replace />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}

export default App;
