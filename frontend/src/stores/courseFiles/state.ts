import type { CourseContentType } from "../../services/courses";

export type PendingUpload = {
  id: string;
  file: File;
  resourceType: CourseContentType;
};

export type CourseFileState = {
  items: PendingUpload[];
  previewID: string | null;
  uploading: boolean;
  error: string | null;
};

export type CourseFileActions = {
  addFiles: (files: File[]) => void;
  removeFile: (id: string) => void;
  updateResourceType: (id: string, type: CourseContentType) => void;

};

export type CourseFileStore = CourseFileState & CourseFileActions;
