export type PdfSource = {
  id: string;
  path: string;
  url: string;
};

export type LectureArtifact = {
  id?: string;
  metadata: MinimalLecturePayload;
};

export type MinimalArtifactPayload = {
  source_markdown?: string;
  source_pdf?: string;
};

export type MinimalLecturePayload = MinimalArtifactPayload & {
  lecture_title: string;
};

export type MinimalHomeworkPayload = MinimalArtifactPayload & {
  course: string;
  homework: string;
};

export type HomeworkArtifact = {
  id?: string;
  metadata: MinimalHomeworkPayload;
};
