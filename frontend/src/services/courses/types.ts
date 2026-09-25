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
