import { useCallback } from "react";
import { AnnouncementManagementAPI } from "../../../services/announcements";
import { useAnnouncementQuery } from "./useAnnouncementQuery";

export function useManagedAnnouncements() {
  const query = useAnnouncementQuery(AnnouncementManagementAPI.list);
  return { ...query, announcements: query.data ?? [] };
}

export function useManagedAnnouncement(id: string | null) {
  const load = useCallback(
    (token: string, signal: AbortSignal) =>
      AnnouncementManagementAPI.get(token, id!, signal),
    [id],
  );
  return useAnnouncementQuery(load, Boolean(id));
}

export function useAnnouncementRecipients(id: string | null) {
  const load = useCallback(
    (token: string, signal: AbortSignal) =>
      AnnouncementManagementAPI.listRecipients(token, id!, signal),
    [id],
  );
  return useAnnouncementQuery(load, Boolean(id));
}
