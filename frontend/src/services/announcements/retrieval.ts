import api from "../../config/api";
import type {
  Announcement,
  AnnouncementHistoryPage,
  AnnouncementRecipient,
} from "./types";

const base = "/announcements";
const config = (token: string, signal?: AbortSignal) => ({
  headers: { Authorization: `Bearer ${token}` },
  signal,
});

export class UserAnnouncementsAPI {
  static async history(
    token: string,
    offset = 0,
    signal?: AbortSignal,
  ): Promise<AnnouncementHistoryPage> {
    return (
      await api.get<AnnouncementHistoryPage>(`${base}/history`, {
        ...config(token, signal),
        params: { limit: 5, offset },
      })
    ).data;
  }

  static async listUnread(
    token: string,
    signal?: AbortSignal,
  ): Promise<Announcement[]> {
    return (
      await api.get<Announcement[]>(`${base}/`, {
        ...config(token, signal),
        params: { unread_only: true },
      })
    ).data;
  }

  static async list(
    token: string,
    signal?: AbortSignal,
  ): Promise<Announcement[]> {
    return (await api.get<Announcement[]>(`${base}/`, config(token, signal)))
      .data;
  }

  static async get(
    token: string,
    id: string,
    signal?: AbortSignal,
  ): Promise<Announcement> {
    return (
      await api.get<Announcement>(
        `${base}/${encodeURIComponent(id)}`,
        config(token, signal),
      )
    ).data;
  }

  static async markRead(
    token: string,
    id: string,
  ): Promise<AnnouncementRecipient> {
    return (
      await api.put<AnnouncementRecipient>(
        `${base}/${encodeURIComponent(id)}/read`,
        undefined,
        config(token),
      )
    ).data;
  }
}
