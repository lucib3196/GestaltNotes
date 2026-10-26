import api from "../../config/api";
import type { Course } from "../courses";
import type {
  CourseEnrollment,
  EnrollmentChatContext,
  EnrollmentStudent,
} from "./types";

const base = "/courses";

function authHeaders(token: string) {
  return { Authorization: `Bearer ${token}` };
}

export class EnrollmentsAPI {
  static async enrollStudent(
    token: string,
    courseId: string,
    studentId: string,
  ): Promise<CourseEnrollment> {
    const res = await api.post<CourseEnrollment>(
      `${base}/${encodeURIComponent(courseId)}/enrollments/${encodeURIComponent(studentId)}`,
      undefined,
      { headers: authHeaders(token) },
    );
    return res.data;
  }

  static async unenrollStudent(
    token: string,
    courseId: string,
    studentId: string,
  ): Promise<void> {
    await api.delete(
      `${base}/${encodeURIComponent(courseId)}/enrollments/${encodeURIComponent(studentId)}`,
      { headers: authHeaders(token) },
    );
  }

  static async listStudents(
    token: string,
    courseId: string,
  ): Promise<EnrollmentStudent[]> {
    const res = await api.get<EnrollmentStudent[]>(
      `${base}/${encodeURIComponent(courseId)}/students`,
      { headers: authHeaders(token) },
    );
    return res.data;
  }

  static async listStudentCourses(token: string): Promise<Course[]> {
    const res = await api.get<Course[]>(`${base}/student/enrollments`, {
      headers: authHeaders(token),
    });
    return res.data;
  }

  static async assertCourseAccess(
    token: string,
    courseId: string,
  ): Promise<Course> {
    const res = await api.get<Course>(
      `${base}/${encodeURIComponent(courseId)}/access`,
      { headers: authHeaders(token) },
    );
    return res.data;
  }

  static async getChatContext(token: string): Promise<EnrollmentChatContext[]> {
    const res = await api.get<EnrollmentChatContext[]>(
      `${base}/student/enrollment/chat-context`,
      { headers: authHeaders(token) },
    );
    return res.data;
  }
}
