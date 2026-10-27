import type { Course } from "../courses";

export interface CourseEnrollment {
  student_id: string;
  course_id: string;
  enrolled_at: string;
  active: boolean;
}

export interface EnrollmentStudent {
  id: string | null;
  first_name: string | null;
  last_name: string | null;
  username: string | null;
  email: string;
}

export interface CourseVectorStore {
  course_id: string;
  namespace_key: string;
  collection_name: string;
  description: string | null;
  embedding_model: string;
  provider: "astra" | "postgres";
  status: "pending" | "ready" | "failed" | "archieved";
}

export interface CourseChatContext {
  course: Omit<Course, "storage_prefix"> & {
    created_at: string;
    updated_at: string;
  };
  vectorstore: CourseVectorStore | null;
}
