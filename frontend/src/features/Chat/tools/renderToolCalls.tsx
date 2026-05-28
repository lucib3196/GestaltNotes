import type { ToolName } from "./types";
import { useAuth } from "../../../context";
import type { BaseMessage } from "langchain";
import { isToolMessage } from "./utils";
import { tools } from "./tools";
import { useState, useMemo } from "react";


// This is meant to only render the tool call once it is succesful
export default function RenderToolCalls({ msg }: { msg: BaseMessage }) {
    const { user } = useAuth();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string>();
    const [dismissed, setDismissed] = useState(false);
    const [show, setShow] = useState<boolean>(true)

    // Basics checks
    const isTool = isToolMessage(msg);
    const toolName = isTool ? msg.name : undefined;
    const tool = toolName && toolName in tools ? tools[toolName as ToolName] : null;

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
        console.log("Approving payload", approvedPayload)
        setError(undefined);
        setLoading(true);
        try {
            // Eventually add better logic to handle this properly
            if (!tool.execute) return;
            await tool.execute({
                payload: approvedPayload,
                ctx: { token: await user?.getIdToken() },
            });
            // setDismissed(true); // optional: hide after success
        } catch (e) {
            setError(e instanceof Error ? e.message : "Failed to execute tool");
        } finally {
            setLoading(false);
        }
    };
    const onCancel = () => setDismissed(true);
    const Preview = tool.Preview;
    if (!dismissed) return (




        <Preview
            payload={payload}
            onApprove={onApprove}
            onCancel={onCancel}
            loading={loading}
            error={error}
        />
    )



}
