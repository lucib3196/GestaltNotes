import api from "../config/api";
type NoteResponse =
  | { type: "pdf"; blob: Blob }
  | { type: "text"; text: string }
  | { type: "json"; data: any }
  | { type: "error"; error: string };

export default class NotesAPI {
  private static readonly base = "/notes";

  static async getNotes(): Promise<string[]> {
    const response = await api.get(this.base);
    return response.data;
  }

  static async getTestNote(): Promise<NoteResponse> {
    try {
      const response = await api.get(`${this.base}/test`, {
        responseType: "blob",
        validateStatus: () => true, // allow manual handling
      });
      const contentType = response.headers["content-type"];
      if (contentType.includes("application/pdf")) {
        return { type: "pdf", blob: response.data };
      }
      if (contentType.includes("text/plain")) {
        const text = await response.data.text();
        return { type: "text", text };
      }
      if (contentType.includes("application/json")) {
        const text = await response.data.text();
        const json = JSON.parse(text);
        return { type: "json", data: json };
      }
      return { type: "error", error: "Unsupported content type" };
    } catch (err: any) {
      return {
        type: "error",
        error: err.message || "Request failed",
      };
    }
  }
}
