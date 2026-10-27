import type { CourseNoteOverview } from "../../../services/courses";
import type { ProcessingStatus, TaskState } from "../../../services/processing";

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
  status === "queued" || status === "running" || status === "retrying";

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
      if (activeRun(note.processing.latest_run?.status)) return "checking";
      break;
  }
  switch (note.processing.latest_run?.status) {
    case "queued":
      return "queued";
    case "running":
      return "running";
    case "retrying":
      return "retrying";
    case "failed":
      return "failed";
    case "revoked":
      return "revoked";
    default:
      return "idle";
  }
}

export function isProcessingBusy(status: DisplayStatus): boolean {
  return ["starting", "queued", "running", "retrying", "checking"].includes(
    status,
  );
}
