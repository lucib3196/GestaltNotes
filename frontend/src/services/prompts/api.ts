import api from "../../config/api";
import type {
  Prompt,
  PromptCreate,
  PromptListOptions,
  PromptSummary,
  PromptUpdate,
} from "./types";

const base = "/prompts";

function authHeaders(token: string) {
  return { Authorization: `Bearer ${token}` };
}

export class PromptsAPI {
  static async createPrompt(
    token: string,
    data: PromptCreate,
  ): Promise<Prompt> {
    const res = await api.post<Prompt>(`${base}/`, data, {
      headers: authHeaders(token),
    });
    return res.data;
  }

  static async listPrompts(
    token: string,
    options: PromptListOptions = {},
  ): Promise<PromptSummary[]> {
    const res = await api.get<PromptSummary[]>(`${base}/`, {
      headers: authHeaders(token),
      params: options,
    });
    return res.data;
  }

  static async getPrompt(
    token: string,
    promptId: string,
  ): Promise<Prompt> {
    const res = await api.get<Prompt>(
      `${base}/${encodeURIComponent(promptId)}`,
      { headers: authHeaders(token) },
    );
    return res.data;
  }

  static async updatePrompt(
    token: string,
    promptId: string,
    data: PromptUpdate,
  ): Promise<Prompt> {
    const res = await api.put<Prompt>(
      `${base}/${encodeURIComponent(promptId)}`,
      data,
      { headers: authHeaders(token) },
    );
    return res.data;
  }

  static async deletePrompt(
    token: string,
    promptId: string,
  ): Promise<void> {
    await api.delete(`${base}/${encodeURIComponent(promptId)}`, {
      headers: authHeaders(token),
    });
  }
}
