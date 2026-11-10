import { BrowserRouter, Routes, Route } from "react-router-dom";
import { HomePage, MyAccount } from "./pages";
import {
  AuthPage,
  PasswordResetGuard,
  RoleRedirect,
  UnauthorizedPage,
} from "./features/Auth";
import { Navigate } from "react-router-dom";
import AppLayout from "./layout/AppLayout";
import { CourseDetails } from "./features/CourseDetails";
import CourseManagement from "./features/CourseManagement/CourseManagement";
import ChatPage from "./features/Chat/ChatWorkspace";
import {
  AnnouncementDashboard,
  AnnouncementInbox,
} from "./features/announcements";
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
            <Route path="/annoucements" element={<AnnouncementInbox />} />
            <Route element={<RoleRedirect allow={["admin"]} />}>
              <Route
                path="/admin"
                element={<Navigate to="/admin/announcements" replace />}
              />
              <Route
                path="/admin/announcements"
                element={<AnnouncementDashboard />}
              />
            </Route>
            {/* Student Only Roots */}
            <Route
              element={
                <RoleRedirect allow={["admin", "educator", "student"]} />
              }
            >
              <Route path="/chat" element={<ChatPage />} />
              {/* <Route path="/my_content" element={<MyGeneratedContentPage />} />
              <Route path="/lecture" element={<LectureNotes />} />
              <Route path="/homework" element={<HomeworkNotes />} /> */}
            </Route>

            <Route element={<RoleRedirect allow={["educator"]} />}>
              <Route
                path="/educator"
                element={<Navigate to="/educator/courses" replace />}
              />

              <Route path="/educator/courses" element={<CourseManagement />} />
              <Route
                path="/educator/courses/:courseId"
                element={<CourseDetails />}
              />
            </Route>
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
