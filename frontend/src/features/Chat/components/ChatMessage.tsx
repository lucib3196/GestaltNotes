
import type { MessageType } from "../instance";
import Markdown from "./MardownRender";
import { formatArgs } from "../utils";
import { normalizeContent } from "../utils";
import type {
    ChatBubbleRender,
    HumanBubbleProps,
    AIMessageBubbleProps,
    ToolBubbleProps,
} from "../instance/types";
import { cleanChildren } from "../utils";

const ChatBubbleBase =
    "my-2 max-w-[88%] rounded-xl px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap shadow-soft";

const ChatBubbleStyles: Record<MessageType, string> = {
    ai: `${ChatBubbleBase} self-start border border-border bg-surface text-text`,
    human: `${ChatBubbleBase} self-end border border-border-strong bg-surface-strong text-text`,
    tool: `${ChatBubbleBase} self-start border border-accent/35 bg-surface-muted text-text`,
};

function renderBubbleContent(model: ChatBubbleRender) {
    if (model.bubble === "ai") {
        const hasToolCalls = !!model.msg.tool_calls?.length;


        if (hasToolCalls && model.showTools !== false) {
            return (
                <div className="space-y-2">
                    <div className="text-[11px] uppercase tracking-[0.16em] text-text-soft">Tool calls</div>
                    {model.msg.tool_calls!.map((toolCall, index) => (
                        <details
                            key={`${toolCall.name}-${index}`}
                            className="rounded-md border border-border bg-surface-muted p-2"
                        >
                            <summary className="cursor-pointer text-sm font-medium text-text transition-colors hover:text-accent">
                                {toolCall.name}
                            </summary>
                            <pre className="mt-2 overflow-x-auto rounded-md border border-border bg-code p-2 text-xs text-text-muted">
                                {formatArgs(toolCall.args)}
                            </pre>
                        </details>
                    ))}
                </div>
            );
        }
        return cleanChildren(normalizeContent(model.msg.content));
    }

    if (model.bubble === "tool") {
        return (
            <div className="space-y-1">
                <div className="text-[11px] uppercase tracking-[0.16em] text-accent">Tool response</div>
                <div className="font-medium">{model.msg.name ?? "unknown_tool"}</div>
                <div>{cleanChildren(normalizeContent(model.msg.content))}</div>
            </div>
        );
    }

    return cleanChildren(normalizeContent(model.msg.content));
}

export function HumanBubble({ msg, type = "human" }: HumanBubbleProps) {
    const content = renderBubbleContent({ bubble: "human", msg });

    return (
        <div className={ChatBubbleStyles[type]}>
            {typeof content === "string" || content == null ? <Markdown>{content}</Markdown> : <>{content}</>}
        </div>
    );
}

export function AIBubble({
    msg,
    type = "ai",
    showTools = false,
}: AIMessageBubbleProps) {
    const content = renderBubbleContent({ bubble: "ai", msg, showTools })
    if (!content) return
    return (
        <div className={ChatBubbleStyles[type]}>
            <Markdown>{content}</Markdown>
        </div>
    );
}

export function ToolMessageBubble({ msg, type = "tool" }: ToolBubbleProps) {
    return <div className={ChatBubbleStyles[type]}>{renderBubbleContent({ bubble: "tool", msg })}</div>;
}
