import api from "../../config/api";
import type {
  Announcement,
  AnnouncementRole,
  AnnouncementAudiencePreview,
  AnnouncementCreate,
  AnnouncementRecipient,
  AnnouncementUpdate,
} from "./types";

const base = "/admin/announcements";
const path = (id: string) => `${base}/${encodeURIComponent(id)}`;
const config = (token: string, signal?: AbortSignal) => ({
  headers: { Authorization: `Bearer ${token}` },
  signal,
});

function audienceParams(roles?: readonly AnnouncementRole[]) {
  if (roles?.length === 0)
    throw new Error("Select at least one audience role.");
  const params = new URLSearchParams();
  roles?.forEach((role) => params.append("roles", role));
  return params;
}

export class AnnouncementManagementAPI {
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
    return (await api.get<Announcement>(path(id), config(token, signal))).data;
  }

  static async create(
    token: string,
    data: AnnouncementCreate,
  ): Promise<Announcement> {
    return (await api.post<Announcement>(`${base}/`, data, config(token))).data;
  }

  static async update(
    token: string,
    id: string,
    data: AnnouncementUpdate,
  ): Promise<Announcement> {
    return (await api.patch<Announcement>(path(id), data, config(token))).data;
  }

  static async delete(token: string, id: string): Promise<void> {
    await api.delete(path(id), config(token));
  }

  static async previewAudience(
    token: string,
    id: string,
    signal?: AbortSignal,
    roles?: readonly AnnouncementRole[],
  ): Promise<AnnouncementAudiencePreview> {
    return (
      await api.get<AnnouncementAudiencePreview>(
        `${path(id)}/audience-preview`,
        { ...config(token, signal), params: audienceParams(roles) },
      )
    ).data;
  }

  static async publish(token: string, id: string): Promise<Announcement> {
    return (
      await api.post<Announcement>(
        `${path(id)}/publish`,
        undefined,
        config(token),
      )
    ).data;
  }

  static async publishToAll(
    token: string,
    id: string,
    roles?: readonly AnnouncementRole[],
  ): Promise<Announcement> {
    return (
      await api.post<Announcement>(`${path(id)}/publish-to-all`, undefined, {
        ...config(token),
        params: audienceParams(roles),
      })
    ).data;
  }

  static async listRecipients(
    token: string,
    id: string,
    signal?: AbortSignal,
  ): Promise<AnnouncementRecipient[]> {
    return (
      await api.get<AnnouncementRecipient[]>(
        `${path(id)}/recipients`,
        config(token, signal),
      )
    ).data;
  }

  static async addRecipients(
    token: string,
    id: string,
    userIds: string[],
  ): Promise<AnnouncementRecipient[]> {
    return (
      await api.post<AnnouncementRecipient[]>(
        `${path(id)}/recipients`,
        { user_ids: userIds },
        config(token),
      )
    ).data;
  }

  static async removeRecipients(
    token: string,
    id: string,
    userIds: string[],
  ): Promise<void> {
    await api.delete(`${path(id)}/recipients`, {
      ...config(token),
      data: { user_ids: userIds },
    });
  }
}
