import { type Message, type ToolMessage } from "@langchain/langgraph-sdk";
import { MessageBaseStyle, type MessageType } from "./config";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import clsx from "clsx";

import { ToolInvocation, ToolBubble } from "./Tools";
import { MessageStyle } from "./config";

type ChatMessageProps = {
    id?: number | string;
    message: Message;

}

export default function ChatMessage({ message, id, }: ChatMessageProps) {
    if (message.type === "ai" && message.tool_calls?.length) {
        return (
            <>
                {message.tool_calls.map((tool, idx) => (
                    <ToolInvocation key={idx} name={tool.name} args={tool.args} />
                ))}
            </>
        );
    }

    if (message.type === "tool") {

        return <ToolBubble message={message as ToolMessage} />;
    }

    return (
        <div
            key={message.id ?? id}
            className={clsx(
                MessageStyle[message.type as MessageType],
                MessageBaseStyle,
            )}
        >
            <Markdown remarkPlugins={[remarkGfm]}>{String(message.content)}</Markdown>
        </div>
    );
}
