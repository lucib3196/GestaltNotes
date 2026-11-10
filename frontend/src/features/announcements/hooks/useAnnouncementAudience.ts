import { useCallback } from "react";
import {
  AnnouncementManagementAPI,
  type AnnouncementRole,
} from "../../../services/announcements";
import { useAnnouncementQuery } from "./useAnnouncementQuery";

export function useAnnouncementAudience(
  id: string | null,
  role?: AnnouncementRole,
) {
  const load = useCallback(
    (token: string, signal: AbortSignal) =>
      AnnouncementManagementAPI.previewAudience(
        token,
        id!,
        signal,
        role ? [role] : undefined,
      ),
    [id, role],
  );
  return useAnnouncementQuery(load, Boolean(id));
}
