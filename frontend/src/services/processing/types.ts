export type ProcessingStatus =
  | "PENDING"
  | "RECEIVED"
  | "STARTED"
  | "RETRY"
  | "FAILURE"
  | "SUCCESS"
  | "REVOKED"
  | "PROGRESS";

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
  status: ProcessingStatus;
  stage: ProcessingStage;
  attempt_count: number;
  created_at: string;
  updated_at: string;
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

export type TaskState = ProcessingStatus;

export type JsonValue =
  | string
  | number
  | boolean
  | null
  | JsonValue[]
  | { [key: string]: JsonValue };

export type ProcessingTaskStatus = {
  task_id: string;
  status: TaskState;
  result: JsonValue;
  progress: JsonValue;
  error: string | null;
};
