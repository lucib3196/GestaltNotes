import type { CourseNoteOverview } from "../../../services/courses";
import type { ProcessingStage, ProcessingStatus, TaskState } from "../../../services/processing";

export type DisplayStatus =
  | "processed"
  | "idle"
  | "starting"
  | "queued"
  | "running"
  | "retrying"
  | "failed"
  | "revoked"
  | "checking";

export const activeRun = (status: ProcessingStatus | null | undefined) =>
  status === "PENDING" || status === "RECEIVED" ||
  status === "STARTED" || status === "PROGRESS" || status === "RETRY";

export function getDisplayStatus(
  note: CourseNoteOverview,
  starting: boolean,
  state: TaskState | undefined,
  refreshing: boolean,
): DisplayStatus {
  if (note.processing.has_succeeded) return "processed";
  if (starting) return "starting";
  if (refreshing) return "checking";
  switch (state) {
    case "PENDING":
    case "RECEIVED":
      return "queued";
    case "STARTED":
    case "PROGRESS":
      return "running";
    case "RETRY":
      return "retrying";
    case "FAILURE":
      return "failed";
    case "REVOKED":
      return "revoked";
    case "SUCCESS":
      return "processed";
  }
  switch (note.processing.latest_run?.status) {
    case "PENDING":
    case "RECEIVED":
      return "queued";
    case "STARTED":
    case "PROGRESS":
      return "running";
    case "RETRY":
      return "retrying";
    case "FAILURE":
      return "failed";
    case "REVOKED":
      return "revoked";
    case "SUCCESS":
      return "processed";
    default:
      return "idle";
  }
}

export function isProcessingBusy(status: DisplayStatus): boolean {
  return ["starting", "queued", "running", "retrying", "checking"].includes(
    status,
  );
}

export const stageLabels: Record<ProcessingStage, string> = {
  validating: "Preparing…",
  downloading: "Downloading document…",
  extracting: "Extracting lecture content…",
  saving_blocks: "Saving notes…",
  building_documents: "Building notes…",
  indexing: "Indexing notes…",
};
