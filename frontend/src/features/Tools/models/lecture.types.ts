export type MinimalLecturePayload = {
  lecture_title: string;
  source_markdown?: string;
  source_pdf?: string;
};

export type LectureArtifact = {
  id?: string;
  metadata: MinimalLecturePayload;
};
