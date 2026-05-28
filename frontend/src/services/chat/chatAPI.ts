import api from "../../config/api";
import type {
  Message,
  MessageCreate,
  Thread,
  ThreadCreate,
  ThreadUpdate,
} from "./types";

export default class ChatAPI {
  private static readonly base = "/threads";

  private static withAuth(token?: string|null) {
    return token
      ? { headers: { Authorization: `Bearer ${token}` } }
      : undefined;
  }

  static async createThread(
    data: ThreadCreate,
    token?: string,
  ): Promise<Thread> {
    const response = await api.post(
      `${this.base}/`,
      data,
      this.withAuth(token),
    );
    return response.data;
  }
  static async getThread(
    threadId: string,
    token?: string|null,
  ): Promise<Thread> {
    const response = await api.get(
      `${this.base}/${threadId}`,
      this.withAuth(token),
    );
    return response.data;
  }

  static async updateThread(
    threadId: string,
    data: ThreadUpdate,
    token?: string,
  ): Promise<Thread> {
    const response = await api.put(
      `${this.base}/${threadId}`,
      data,
      this.withAuth(token),
    );
    return response.data;
  }

  static async listMyThreads(token?: string): Promise<Thread[]> {
    const response = await api.get(`${this.base}/`, this.withAuth(token));
    return response.data;
  }

  static async createMessage(
    threadId: string,
    data: MessageCreate,
    token?: string,
  ): Promise<Message> {
    const response = await api.post(
      `${this.base}/${threadId}/messages`,
      data,
      this.withAuth(token),
    );
    return response.data;
  }

  static async getMessages(
    threadId: string,
    token?: string,
  ): Promise<Message[]> {
    const response = await api.get(
      `${this.base}/${threadId}/messages`,
      this.withAuth(token),
    );
    return response.data;
  }
}
