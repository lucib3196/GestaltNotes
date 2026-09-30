export interface Course {
  id: string;
  name: string;
  discipline: string | null;
  description: string | null;
  owner_id: string;
  storage_prefix: string | null;
}

export interface CourseCreate {
  name: string;
  discipline?: string | null;
  description?: string | null;
}

export interface CourseUpdate {
  name?: string | null;
  discipline?: string | null;
  description?: string | null;
}

export interface CourseDelete {
  success: boolean;
  info: string;
}

export type CourseContentType =
  | "lecture"
  | "notes"
  | "assignment"
  | "exam"
  | "quiz"
  | "textbook"
  | "handout"
  | "syllabus"
  | "reference"
  | "other";

export interface CourseNote {
  id: string;
  course_id: string;
  file_id: string;
  title: string;
  resource_type: CourseContentType;
  download_url: string | null;
}

export interface CourseNoteDelete {
  success: boolean;
  info: string;
}
