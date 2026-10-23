export type ProcessingStatus =
  | "queued"
  | "running"
  | "retrying"
  | "succeeded"
  | "partial"
  | "failed"
  | "revoked";

export type ProcessingStage =
  | "validating"
  | "downloading"
  | "extracting"
  | "saving_blocks"
  | "building_documents"
  | "indexing";

export type ProcessingRun = {
  id: string;
  celery_task_id: string;
  task_type: string;
  status: ProcessingStatus | null;
  stage: ProcessingStage;
  attempt_count: number;
  error_type: string | null;
  error_message: string | null;
};

export type LectureProcessingStatus = {
  has_succeeded: boolean;
  can_process: boolean;
  latest_run: ProcessingRun | null;
};

export type ProcessingTaskStarted = {
  course_id: string;
  note_id: string;
  task_id: string;
  summary: string;
};

export type ProcessingTaskStatus = {
  task_id: string;
  status: string;
  result: unknown;
  progress: unknown;
  error: string | null;
};
