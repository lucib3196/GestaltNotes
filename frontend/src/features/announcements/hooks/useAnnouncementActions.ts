import { useMemo } from "react";
import {
  AnnouncementManagementAPI as api,
  type AnnouncementCreate,
  type AnnouncementRole,
  type AnnouncementUpdate,
} from "../../../services/announcements";
import { useAnnouncementRequest } from "./useAnnouncementRequest";

export function useAnnouncementActions() {
  const { run, pending, error } = useAnnouncementRequest();
  const actions = useMemo(
    () => ({
      create: (data: AnnouncementCreate) =>
        run((token) => api.create(token, data)),
      update: (id: string, data: AnnouncementUpdate) =>
        run((token) => api.update(token, id, data)),
      deleteAnnouncement: (id: string) => run((token) => api.delete(token, id)),
      publish: (id: string) => run((token) => api.publish(token, id)),
      publishToAll: (id: string, roles?: readonly AnnouncementRole[]) =>
        run((token) => api.publishToAll(token, id, roles)),
      addRecipients: (id: string, userIds: string[]) =>
        run((token) => api.addRecipients(token, id, userIds)),
      removeRecipients: (id: string, userIds: string[]) =>
        run((token) => api.removeRecipients(token, id, userIds)),
    }),
    [run],
  );
  return { ...actions, pending, error };
}
