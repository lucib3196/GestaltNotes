import api from "../../config/api";
import type {
  LectureProcessingStatus,
  ProcessingRun,
  ProcessingTaskStarted,
  ProcessingTaskStatus,
} from "./types";

function requestConfig(token: string, signal?: AbortSignal) {
  return {
    headers: { Authorization: `Bearer ${token}` },
    signal,
  };
}

function notePath(courseId: string, noteId: string) {
  return `/courses/notes/${encodeURIComponent(courseId)}/${encodeURIComponent(noteId)}`;
}

export class LectureRunsAPI {
  static async listRuns(
    token: string,
    courseId: string,
    noteId: string,
    signal?: AbortSignal,
  ): Promise<ProcessingRun[]> {
    const res = await api.get<ProcessingRun[]>(
      `${notePath(courseId, noteId)}/runs`,
      requestConfig(token, signal),
    );
    return res.data;
  }

  static async getRun(
    token: string,
    courseId: string,
    noteId: string,
    runId: string,
    signal?: AbortSignal,
  ): Promise<ProcessingRun> {
    const res = await api.get<ProcessingRun>(
      `${notePath(courseId, noteId)}/runs/${encodeURIComponent(runId)}`,
      requestConfig(token, signal),
    );
    return res.data;
  }

  static async getStatus(
    token: string,
    courseId: string,
    noteId: string,
    signal?: AbortSignal,
  ): Promise<LectureProcessingStatus> {
    const res = await api.get<LectureProcessingStatus>(
      `${notePath(courseId, noteId)}/status`,
      requestConfig(token, signal),
    );
    return res.data;
  }
}

export class ProcessingTasksAPI {
  static async startLecture(
    token: string,
    courseId: string,
    noteId: string,
    signal?: AbortSignal,
  ): Promise<ProcessingTaskStarted> {
    const res = await api.post<ProcessingTaskStarted>(
      `${notePath(courseId, noteId)}/process`,
      undefined,
      requestConfig(token, signal),
    );
    return res.data;
  }

  static async getTaskStatus(
    token: string,
    taskId: string,
    signal?: AbortSignal,
  ): Promise<ProcessingTaskStatus> {
    const res = await api.get<ProcessingTaskStatus>(
      `/tasks/${encodeURIComponent(taskId)}`,
      requestConfig(token, signal),
    );
    return res.data;
  }
}
