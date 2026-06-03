import { BrowserRouter, Routes, Route } from "react-router-dom";
import { HomePage, ChatPage, MyAccount, MyGeneratedContentPage } from "./pages";
import EducatorPage from "./features/EducatorPage/EducatorPage";
import { AuthPage, PasswordResetGuard, RoleRedirect, UnauthorizedPage } from "./features/Auth";
import LectureNotes from "./pages/LectureNotes";
import { Navigate } from "react-router-dom";
import AppLayout from "./layout/AppLayout";
import LectureJson from "./features/Lectures/components/JsonParser";


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

                    <Route element={<PasswordResetGuard />}>
                        {/* Student Only Roots */}
                        <Route element={<RoleRedirect allow={["admin", "educator", "student"]} />}>
                            <Route path="/chat" element={<ChatPage />} />
                            <Route path="/my_content" element={<MyGeneratedContentPage />} />
                            <Route path="/lecture" element={<LectureNotes />} />
                            <Route path="/lecture_test" element={<LectureJson />} />
                        </Route>

                        <Route element={<RoleRedirect allow={["educator"]} />}>
                            <Route path="/educator" element={<EducatorPage />} />
                        </Route>
                    </Route>


                    <Route path="*" element={<Navigate to="/" replace />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}

export default App;
