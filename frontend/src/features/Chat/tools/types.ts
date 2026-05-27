import type { ToolMessage } from "langchain";

export type ToolExecuteContext = {
  token?: string;
};

type ToolExecuteArgs<TPayload> = {
  payload: TPayload;
  ctx?: ToolExecuteContext;
};
export type ToolExecute<TPayload> = (
  args: ToolExecuteArgs<TPayload>,
) => Promise<void>;
// Tools that are specific and we want to render and get some sorth of output from
export type ToolName = "retrieve_me116_lecture"|"generate_mcq";

export type RenderPreviewProps<TPayload> = {
  payload: TPayload;
  onApprove?: (payload: TPayload) => void;
  onCancel?: () => void;
  loading: boolean;
  error?: string;
};

export type ToolDefinition<TPayload> = {
  parse: (msg: ToolMessage) => TPayload;
  Preview: React.ComponentType<RenderPreviewProps<TPayload>>;
  execute?: ToolExecute<TPayload>;
};

export type ToolDefinitions = Record<ToolName, ToolDefinition<any>>;
