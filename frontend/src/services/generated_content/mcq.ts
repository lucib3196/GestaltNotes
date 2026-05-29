import type { AxiosError } from "axios";
import type {
  GeneratedContentSaveRequest,
  MCQDB,
  MultipleChoiceQuestion,
} from "./types";
import { api } from "../../config";

export default class MCQ {
  private static readonly base = "generated_content/mcq";

  private static withAuth(token?: string | null) {
    return token
      ? { headers: { Authorization: `Bearer ${token}` } }
      : undefined;
  }

  private static extractErrorMessage(error: unknown, fallback: string): string {
    const axiosError = error as AxiosError<{ detail?: string }>;
    return axiosError?.response?.data?.detail || axiosError?.message || fallback;
  }

  static async saveQuestions(
    data: GeneratedContentSaveRequest,
    token?: string,
  ): Promise<MCQDB[]> {
    if (!data.thread_id) {
      throw new Error("Cannot save content without thread id");
    }
    try {
      const response = await api.post(
        `${this.base}/v1`,
        data,
        this.withAuth(token),
      );
      return response.data;
    } catch (error) {
      const message = this.extractErrorMessage(
        error,
        "Failed to save generated MCQs",
      );
      throw new Error(message);
    }
  }

  static async getAllQuestions(token?: string): Promise<MCQDB[]> {
    try {
      const response = await api.get(
        `${this.base}/v1/all`,
        this.withAuth(token),
      );
      return response.data;
    } catch (error) {
      const message = this.extractErrorMessage(
        error,
        "Failed to retrieve generated MCQs",
      );
      throw new Error(message);
    }
  }

  static async getAllQuizzes(token?: string): Promise<MultipleChoiceQuestion[]> {
    try {
      const response = await api.get(
        `${this.base}/v1/all/quiz`,
        this.withAuth(token),
      );
      return response.data;
    } catch (error) {
      const message = this.extractErrorMessage(
        error,
        "Failed to retrieve generated quizzes",
      );
      throw new Error(message);
    }
  }
}
