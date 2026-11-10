import { useCallback } from "react";
import { useAuth } from "../../Auth";
import { notifyAnnouncementRead } from "../events";
import { UserAnnouncementsAPI } from "../../../services/announcements";
import { useAnnouncementRequest } from "./useAnnouncementRequest";

export function useMarkAnnouncementRead() {
  const { run, pending, error } = useAnnouncementRequest();
  const { user } = useAuth();
  const markRead = useCallback(
    async (id: string) => {
      const recipient = await run((token) =>
        UserAnnouncementsAPI.markRead(token, id),
      );
      if (user) notifyAnnouncementRead(id, user.uid);
      return recipient;
    },
    [run, user],
  );
  return { markRead, pending, error };
}
