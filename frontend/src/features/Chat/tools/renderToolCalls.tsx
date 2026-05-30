import type { ToolName } from "./types";
import { useAuth } from "../../../context";
import type { BaseMessage } from "langchain";
import { isToolMessage } from "./utils";
import { tools } from "./tools";
import { useState, useMemo } from "react";
import { useRef } from "react";
import { useChatContext } from "../instance";

// This is meant to only render the tool call once it is succesful
export default function RenderToolCalls({ msg }: { msg: BaseMessage }) {
    const { user } = useAuth();
    const threadId = useChatContext((s) => s.theadId);
    const requestIdRef = useRef<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string>();
    const [dismissed, setDismissed] = useState(false);

    // Basics checks
    const isTool = isToolMessage(msg);
    const toolName = isTool ? msg.name : undefined;
    const tool =
        toolName && toolName in tools ? tools[toolName as ToolName] : null;

    const payload = useMemo(() => {
        if (!isTool || !tool) return null;
        try {
            return tool.parse(msg);
        } catch {
            return null;
        }
    }, [isTool, tool, msg]);

    // Double check and ensure that it is valid
    if (!isTool) return null;
    if (msg.status === "error") return null;
    if (!tool) return null;
    if (!payload || dismissed) return null;

    const onApprove = async (approvedPayload: unknown) => {
        setError(undefined);
        setLoading(true);
        try {
            // Eventually add better logic to handle this properly
            if (!tool.execute) return;
            // if (!threadId) throw new Error("Cannot execute tool without thread id")
            await tool.execute({
                payload: approvedPayload,
                ctx: {
                    token: await user?.getIdToken(),
                    threadId: threadId,
                    request_id: requestIdRef.current,
                },
            });
            requestIdRef.current = null;
            // setDismissed(true); // optional: hide after success
        } catch (e) {
            setError(e instanceof Error ? e.message : "Failed to execute tool");
        } finally {
            setLoading(false);
        }
    };
    const onCancel = () => setDismissed(true);
    const Preview = tool.Preview;
    if (!dismissed)
        return (
            <Preview
                payload={payload}
                onApprove={onApprove}
                onCancel={onCancel}
                loading={loading}
                error={error}
            />
        );
    return null;
}
