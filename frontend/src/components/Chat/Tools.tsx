import { type ToolMessage } from "@langchain/langgraph-sdk";
import clsx from "clsx";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { parseToolResult } from "./utils";
import { useState } from "react";
import { Button } from "../Button";
import { MessageBaseStyle, MessageStyle } from "./config";
type ToolBubbleProps = {
    message: ToolMessage;
};

export function ToolBubble({ message }: ToolBubbleProps) {
    const [showToolResult, setShowToolResult] = useState<boolean>(false)
    const parsed = parseToolResult(message);

    return (
        <div
            className={clsx(MessageBaseStyle, MessageStyle["invokation"], "self-start")}

        >
            <div className="flex flex-row justify-between">
                <div className="text-xs font-semibold text-amber-700 mb-1">
                    Tool Result
                </div>
                <Button size="sm" onClick={() => setShowToolResult(prev => !prev)}>Show Tool Call</Button>
            </div>
            {showToolResult && parsed.content &&  <Markdown remarkPlugins={[remarkGfm]}>{parsed.content}</Markdown>}

        </div>
    );
}

export function ToolInvocation({
    name,
    args,
}: {
    name: string;
    args: unknown;
}) {
    const [showToolResult, setShowToolResult] = useState<boolean>(false);
    return (
        <div
            className={clsx(MessageBaseStyle, MessageStyle["invokation"], "self-start")}
        >
            <div className="flex flex-row justify-between">
                <div className="font-semibold text-indigo-700 mb-1">
                    🔧 Tool Call: {name}

                </div>
                <Button size="sm" onClick={() => setShowToolResult(prev => !prev)}>Show Tool Call</Button>
            </div>
            {showToolResult && <pre className="whitespace-pre-wrap wrap-break-word text-indigo-800">
                {JSON.stringify(args, null, 2)}
            </pre>}

        </div>
    );
}
