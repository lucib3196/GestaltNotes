import type { ValidRole } from "../users/types";

export type AnnouncementRole = ValidRole;

export interface Announcement {
  id: string;
  title: string;
  message: string;
  version: string;
  audience_summary: string | null;
  published: boolean;
  created_by_id: string | null;
  created_at: string | null;
  updated_at: string | null;
  published_at: string | null;
}

export interface AnnouncementCreate {
  title: string;
  message: string;
  version: string;
  audience_summary?: string | null;
}

// Publication and ownership are controlled by dedicated backend operations.
export type AnnouncementUpdate = Partial<
  Pick<AnnouncementCreate, "title" | "message" | "version">
>;

export interface AnnouncementRecipient {
  announcement_id: string;
  user_id: string;
  read_at: string | null;
}

export interface AnnouncementHistoryItem {
  announcement: Announcement;
  read_at: string | null;
}

export interface AnnouncementHistoryPage {
  items: AnnouncementHistoryItem[];
  total: number;
  limit: number;
  offset: number;
}

export interface AnnouncementAudiencePreview {
  announcement_id: string;
  published: boolean;
  total_users: number;
  existing_recipients: number;
  new_recipients: number;
  read_recipients: number;
  unread_recipients: number;
  conflicting_recipients: number;
}
