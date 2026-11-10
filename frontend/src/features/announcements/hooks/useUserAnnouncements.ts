import { useCallback, useEffect } from "react";
import { useAuth } from "../../Auth";
import { ANNOUNCEMENT_READ_EVENT, type AnnouncementReadEvent } from "../events";
import { UserAnnouncementsAPI } from "../../../services/announcements";
import { useAnnouncementQuery } from "./useAnnouncementQuery";

export function useUserAnnouncements(enabled = true) {
  const query = useAnnouncementQuery(UserAnnouncementsAPI.list, enabled);
  return { ...query, announcements: query.data ?? [] };
}

export function useUnreadAnnouncements() {
  const query = useAnnouncementQuery(UserAnnouncementsAPI.listUnread);
  return { ...query, announcements: query.data ?? [] };
}

export function useUserAnnouncement(id: string | null) {
  const load = useCallback(
    (token: string, signal: AbortSignal) =>
      UserAnnouncementsAPI.get(token, id!, signal),
    [id],
  );
  return useAnnouncementQuery(load, Boolean(id));
}

export function useAnnouncementHistory(page: number) {
  const load = useCallback(
    (token: string, signal: AbortSignal) =>
      UserAnnouncementsAPI.history(token, (page - 1) * 5, signal),
    [page],
  );
  const query = useAnnouncementQuery(load);
  const { user } = useAuth();
  const { refetch } = query;
  useEffect(() => {
    function onRead(event: Event) {
      if ((event as AnnouncementReadEvent).detail.uid === user?.uid)
        void refetch();
    }
    window.addEventListener(ANNOUNCEMENT_READ_EVENT, onRead);
    return () => window.removeEventListener(ANNOUNCEMENT_READ_EVENT, onRead);
  }, [user?.uid, refetch]);
  return query;
}
