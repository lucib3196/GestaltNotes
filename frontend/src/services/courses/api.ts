import api from "../../config/api";
import type {
  Course,
  CourseContentType,
  CourseCreate,
  CourseDelete,
  CourseNote,
  CourseNoteDelete,
  CourseNoteOverview,
  CourseNoteUpdate,
  CourseUpdate,
} from "./types";

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
    const res = await api.get<Course>(`${base}/${encodeURIComponent(courseId)}`, {
      headers: authHeaders(token),
    });
    return res.data;
  }

  static async updateCourse(
    token: string,
    courseId: string,
    data: CourseUpdate,
  ): Promise<Course> {
    const res = await api.patch<Course>(`${base}/${encodeURIComponent(courseId)}`, data, {
      headers: authHeaders(token),
    });
    return res.data;
  }

  static async deleteCourse(token: string, courseId: string): Promise<CourseDelete> {
    const res = await api.delete<CourseDelete>(`${base}/${encodeURIComponent(courseId)}`, {
      headers: authHeaders(token),
    });
    return res.data;
  }

  static async listCourseNotes(
    token: string,
    courseId: string,
  ): Promise<CourseNote[]> {
    const res = await api.get<CourseNote[]>(`${base}/notes/${encodeURIComponent(courseId)}`, {
      headers: authHeaders(token),
    });
    return res.data;
  }

  static async listCourseNoteOverviews(
    token: string,
    courseId: string,
    signal?: AbortSignal,
  ): Promise<CourseNoteOverview[]> {
    const res = await api.get<CourseNoteOverview[]>(
      `${base}/notes/${encodeURIComponent(courseId)}/overview`,
      { headers: authHeaders(token), signal },
    );
    return res.data;
  }

  static async getCourseNoteOverview(
    token: string,
    courseId: string,
    noteId: string,
    signal?: AbortSignal,
  ): Promise<CourseNoteOverview> {
    const res = await api.get<CourseNoteOverview>(
      `${base}/notes/${encodeURIComponent(courseId)}/${encodeURIComponent(noteId)}/overview`,
      { headers: authHeaders(token), signal },
    );
    return res.data;
  }

  static async uploadCourseNote(
    token: string,
    courseId: string,
    file: File,
    resourceType: CourseContentType,
  ): Promise<CourseNote> {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("resource_type", resourceType);

    const res = await api.post<CourseNote>(
      `${base}/notes/${encodeURIComponent(courseId)}`,
      formData,
      {
        headers: authHeaders(token),
      },
    );
    return res.data;
  }

  static async updateCourseNote(
    token: string,
    courseId: string,
    noteId: string,
    data: CourseNoteUpdate,
  ): Promise<CourseNote> {
    const response = await api.put<CourseNote>(
      `${base}/notes/${encodeURIComponent(courseId)}/${encodeURIComponent(noteId)}`, data,
      { headers: authHeaders(token) },
    );
    return response.data;
  }

  static async deleteCourseNote(
    token: string,
    courseId: string,
    noteId: string,
  ): Promise<CourseNoteDelete> {
    const res = await api.delete<CourseNoteDelete>(
      `${base}/notes/${encodeURIComponent(courseId)}/${encodeURIComponent(noteId)}`,
      {
        headers: authHeaders(token),
      },
    );
    return res.data;
  }

  static async streamCourseNote(
    token: string,
    courseId: string,
    noteId: string,
    signal?: AbortSignal,
  ): Promise<Blob> {
    const res = await api.get<Blob>(
      `${base}/notes/${encodeURIComponent(courseId)}/${encodeURIComponent(noteId)}/stream`,
      {
        responseType: "blob",
        signal,
        headers: authHeaders(token),
      },
    );
    return res.data;
  }
}
