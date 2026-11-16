export interface PromptCreate {
  title: string;
  description?: string | null;
  content: string;
}

export interface Prompt extends PromptCreate {
  id: string;
  user_id: string;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export interface PromptSummary {
  id: string;
  title: string;
  description: string | null;
}

export interface PromptUpdate {
  title: string;
  description?: string | null;
  content?: string;
}

export interface PromptListOptions {
  offset?: number;
  limit?: number;
  order?: "asc" | "desc";
  sort?: "updated" | "created";
}
