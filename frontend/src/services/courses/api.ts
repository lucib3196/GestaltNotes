import api from "../../config/api";
import type { Course, CourseCreate, CourseDelete, CourseUpdate } from "./types";

const base = "/courses";

function authHeaders(token: string) {
  return {
    Authorization: `Bearer ${token}`,
  };
}

export class CoursesAPI {
  static async createCourse(token: string, data: CourseCreate): Promise<Course> {
    const res = await api.post<Course>(`${base}/`, data, {
      headers: authHeaders(token),
    });
    return res.data;
  }

  static async listOwnedCourses(token: string): Promise<Course[]> {
    const res = await api.get<Course[]>(`${base}/`, {
      headers: authHeaders(token),
    });
    return res.data;
  }

  static async getProfCourses(token: string): Promise<Course[]> {
    const res = await api.get<Course[]>(`${base}/get_prof_courses`, {
      headers: authHeaders(token),
    });
    return res.data;
  }

  static async getCourse(token: string, courseId: string): Promise<Course> {
    const res = await api.get<Course>(`${base}/${courseId}`, {
      headers: authHeaders(token),
    });
    return res.data;
  }

  static async updateCourse(
    token: string,
    courseId: string,
    data: CourseUpdate,
  ): Promise<Course> {
    const res = await api.patch<Course>(`${base}/${courseId}`, data, {
      headers: authHeaders(token),
    });
    return res.data;
  }

  static async deleteCourse(token: string, courseId: string): Promise<CourseDelete> {
    const res = await api.delete<CourseDelete>(`${base}/${courseId}`, {
      headers: authHeaders(token),
    });
    return res.data;
  }
}
