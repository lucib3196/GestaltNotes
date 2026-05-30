import type { ToolMessage } from "langchain";

// Tools that are specific and we want to render and get some sorth of output from
export type ToolName = "retrieve_me116_lecture" | "generate_mcq";
export const TOOL_NAMES: ToolName[] = [
  "retrieve_me116_lecture",
  "generate_mcq",
] as const;
export const TOOL_POLICY: Record<
  ToolName,
  "replace" | "append" | "replace_and_push"
> = {
  retrieve_me116_lecture: "replace_and_push",
  generate_mcq: "append",
};

// The render preview is a generic where it takes in a payload
export type RenderPreviewProps<TPayload> = {
  payload: TPayload;
  // Logic to handle submission
  onApprove?: (payload: TPayload) => void;
  // Cancel request
  onCancel?: () => void;
  // Loading and error statte
  loading: boolean;
  error?: string;
};

// Execution takes in in a payload and additional context may be needed such as user toke
export type ToolExecuteContext = {
  token?: string;
  threadId: string | null;
  request_id?: string | null;
};
type ToolExecuteArgs<TPayload> = {
  payload: TPayload;
  ctx?: ToolExecuteContext;
};
export type ToolExecute<TPayload> = (
  args: ToolExecuteArgs<TPayload>,
) => Promise<void>;
// Tools must have a parser, a preview component and optionally an execute
export type ToolDefinition<TPayload> = {
  parse: (msg: ToolMessage) => TPayload;
  Preview: React.ComponentType<RenderPreviewProps<TPayload>>;
  execute?: ToolExecute<TPayload>;
};
export type ToolDefinitions = Record<ToolName, ToolDefinition<any>>;
