export type ConversationStarter = {
  id: string;
  label: string;
  message: string;
  description?: string;
  disabled?: boolean;
};

export interface TopicStarter {
  id: string;
  title: string;
  starters: string[];
}
