export type Assistant = {
  id: string;
  label: string;
  description: string | null;
};

export type Attachment = {
  id: string;
  file: File;
};
export type PendingPrompt = {
  id: string;
  text: string;
};
export type RequestStatus = "idle" | "loading" | "success" | "error";