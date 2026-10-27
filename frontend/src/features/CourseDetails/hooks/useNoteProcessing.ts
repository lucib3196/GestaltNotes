import { useEffect, useRef, useState } from "react";
import {
  useProcessingTaskStatus,
  useStartLectureProcessing,
} from "../../../hooks/processing";
import type { CourseNoteOverview } from "../../../services/courses";
import {
  activeRun,
  getDisplayStatus,
  isProcessingBusy,
} from "../materials/processingStatus";

export type RefreshNote = (note: CourseNoteOverview) => Promise<CourseNoteOverview>;

export function useNoteProcessing(
  note: CourseNoteOverview,
  onRefresh: RefreshNote,
) {
  const {
    startProcessing,
    task,
    loading: starting,
    error: startError,
  } = useStartLectureProcessing();
  const {
    checkStatus,
    taskStatus,
    error: statusError,
  } = useProcessingTaskStatus();
  const [attempt, setAttempt] = useState(0);
  const [refreshingTaskId, setRefreshingTaskId] = useState<string | null>(null);
  const [refreshError, setRefreshError] = useState<string | null>(null);
  const startLock = useRef(false);
  const noteRef = useRef(note);
  useEffect(() => {
    noteRef.current = note;
  }, [note]);

  const processed = note.processing.has_succeeded;
  const latest = note.processing.latest_run;
  const taskId = processed
    ? null
    : (task?.task_id ??
      (activeRun(latest?.status) ? latest?.celery_task_id : null));
  const refreshing = taskId !== null && refreshingTaskId === taskId;
  const currentTask = taskStatus?.task_id === taskId ? taskStatus : null;
  const taskState =
    currentTask?.status ?? (task?.task_id && taskId ? "PENDING" : undefined);
  const status = getDisplayStatus(note, starting, taskState, refreshing);
  const busy = isProcessingBusy(status);

  const handleProcessing = async () => {
    if (startLock.current || busy || processed || !note.processing.can_process)
      return;
    startLock.current = true;
    setRefreshError(null);
    try {
      await startProcessing(note.course_id, note.id);
    } catch {
      // The start hook exposes the request error below the action.
    } finally {
      startLock.current = false;
    }
  };

  useEffect(() => {
    if (!taskId) return;
    let active = true;
    let timer: ReturnType<typeof setTimeout> | undefined;
    async function poll() {
      try {
        const response = await checkStatus(taskId!);
        if (!active) return;
        const finished = ["SUCCESS", "FAILURE", "REVOKED"].includes(
          response.status,
        );
        if (finished) {
          setRefreshingTaskId(taskId!);
          setRefreshError(null);
          try {
            const updated = await onRefresh(noteRef.current);
            if (!active) return;
            // Celery completion and the persisted run can briefly disagree.
            if (
              response.status === "SUCCESS" &&
              !updated.processing.has_succeeded &&
              activeRun(updated.processing.latest_run?.status)
            ) {
              timer = setTimeout(() => void poll(), 2_000);
            }
          } catch {
            if (active)
              setRefreshError(
                "Couldn’t refresh the processing result. Check again.",
              );
          } finally {
            if (active) setRefreshingTaskId(null);
          }
          return;
        }
        timer = setTimeout(() => void poll(), 2_000);
      } catch {
        // A status request failure stops polling until Check again is clicked.
      }
    }
    void poll();
    return () => {
      active = false;
      clearTimeout(timer);
    };
  }, [taskId, checkStatus, onRefresh, attempt]);

  const requestError = processed
    ? null
    : statusError
      ? "Couldn’t check progress. Processing may still be running."
      : refreshError;
  const taskError = processed
    ? null
    : (startError?.message ??
      (status === "failed"
        ? (currentTask?.error ??
          latest?.error_message ??
          "Processing failed. You can try again.")
        : null));

  return {
    status,
    actions: {
      processed,
      busy: starting || refreshing || (!requestError && busy),
      canProcess: note.processing.can_process,
      failed: status === "failed",
      requestError,
      taskError,
      onProcess: () => void handleProcessing(),
      onCheck: () => setAttempt((value) => value + 1),
    },
  };
}
