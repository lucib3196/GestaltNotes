export const ANNOUNCEMENT_READ_EVENT = "gestalt:announcement-read";

export type AnnouncementReadEvent = CustomEvent<{
  announcementId: string;
  uid: string;
}>;

export function notifyAnnouncementRead(announcementId: string, uid: string) {
  window.dispatchEvent(
    new CustomEvent(ANNOUNCEMENT_READ_EVENT, {
      detail: { announcementId, uid },
    }),
  );
}
