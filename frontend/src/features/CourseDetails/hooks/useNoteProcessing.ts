import { useEffect, useRef, useState } from "react";
import { useStartLectureProcessing } from "../../../hooks/processing";
import { useAuth } from "../../Auth";
import type { CourseNoteOverview } from "../../../services/courses";
import {
  LectureRunsAPI,
  type LectureProcessingStatus,
} from "../../../services/processing";
import {
  activeRun,
  getDisplayStatus,
  isProcessingBusy,
} from "../materials/processingStatus";

export type RefreshNote = (note: CourseNoteOverview) => Promise<CourseNoteOverview>;

type PollResult = {
  courseId: string;
  noteId: string;
  taskId: string;
  processing: LectureProcessingStatus;
};

type PollError = {
  courseId: string;
  noteId: string;
  taskId: string;
  message: string;
};

export function useNoteProcessing(
  note: CourseNoteOverview,
  onRefresh: RefreshNote,
) {
  const { user } = useAuth();
  const { startProcessing, task, loading: starting, error: startError } =
    useStartLectureProcessing();
  const [polled, setPolled] = useState<PollResult | null>(null);
  const [pollError, setPollError] = useState<PollError | null>(null);
  const [attempt, setAttempt] = useState(0);
  const [refreshingTaskId, setRefreshingTaskId] = useState<string | null>(null);
  const startLock = useRef(false);
  const noteRef = useRef(note);
  useEffect(() => {
    noteRef.current = note;
  }, [note]);

  const startedTask = task?.course_id === note.course_id && task.note_id === note.id
    ? task
    : null;
  const latest = note.processing.latest_run;
  const taskId = startedTask?.task_id ??
    (!note.processing.has_succeeded && activeRun(latest?.status)
      ? latest?.celery_task_id ?? null
      : null);
  const currentPoll = polled?.courseId === note.course_id &&
    polled.noteId === note.id && polled.taskId === taskId ? polled : null;
  const processing = currentPoll?.processing ?? note.processing;
  // The worker creates the run after dispatch. Ignore an older run until
  // the newly accepted task appears in this note's scoped status response.
  const awaitingRun = startedTask !== null &&
    processing.latest_run?.celery_task_id !== startedTask.task_id;
  const currentRun = awaitingRun ? null : processing.latest_run;
  const processed = !awaitingRun &&
    (processing.has_succeeded || currentRun?.status === "SUCCESS");
  const refreshing = taskId !== null && refreshingTaskId === taskId;
  const currentError = pollError?.courseId === note.course_id &&
    pollError.noteId === note.id && pollError.taskId === taskId
    ? pollError.message : null;
  const displayNote = {
    ...note,
    processing: {
      ...processing,
      has_succeeded: processed,
      latest_run: currentRun,
    },
  };
  const status = getDisplayStatus(
    displayNote,
    starting,
    awaitingRun ? "PENDING" : currentRun?.status,
    refreshing,
  );
  const busy = isProcessingBusy(status);

  const handleProcessing = async () => {
    if (startLock.current || busy || processed || !processing.can_process) return;
    startLock.current = true;
    setPollError(null);
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
    const controller = new AbortController();
    const courseId = note.course_id;
    const noteId = note.id;
    const pollingTaskId = taskId;

    async function poll() {
      try {
        if (!user) throw new Error("You must be signed in to check processing.");
        const token = await user.getIdToken();
        if (!active) return;
        const response = await LectureRunsAPI.getStatus(
          token, courseId, noteId, controller.signal,
        );
        if (!active) return;
        setPollError(null);
        setPolled({ courseId, noteId, taskId: pollingTaskId, processing: response });
        const run = response.latest_run;
        const finished = run?.celery_task_id === pollingTaskId &&
          ["SUCCESS", "FAILURE", "REVOKED"].includes(run.status);
        if (finished) {
          setRefreshingTaskId(pollingTaskId);
          try {
            await onRefresh(noteRef.current);
          } catch {
            if (active) setPollError({
              courseId, noteId, taskId: pollingTaskId,
              message: "Couldn’t refresh the processing result. Check again.",
            });
          } finally {
            if (active) setRefreshingTaskId(null);
          }
          return;
        }
        timer = setTimeout(() => void poll(), 2_000);
      } catch {
        if (active) setPollError({
          courseId, noteId, taskId: pollingTaskId,
          message: "Couldn’t check progress. Processing may still be running.",
        });
      }
    }
    void poll();
    return () => {
      active = false;
      controller.abort();
      clearTimeout(timer);
    };
  }, [taskId, note.course_id, note.id, user, onRefresh, attempt]);

  const requestError = currentError;
  const taskError = processed ? null :
    (startError?.message ?? (status === "failed"
      ? currentRun?.error_message ?? "Processing failed. You can try again."
      : null));

  return {
    status,
    stage: currentRun?.stage,
    errorMessage: taskError,
    actions: {
      processed,
      busy: starting || refreshing || (!requestError && busy),
      canProcess: processing.can_process,
      failed: status === "failed",
      requestError,
      taskError,
      onProcess: () => void handleProcessing(),
      onCheck: () => setAttempt((value) => value + 1),
    },
  };
}
