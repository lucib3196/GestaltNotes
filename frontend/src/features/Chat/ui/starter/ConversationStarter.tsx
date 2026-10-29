import { useChatStore } from "../../instance";

export function ConversationStarter({
  key,
  value,
}: {
  key: string;
  value: string;
}) {
  const setDraftMessage = useChatStore((s) => s.setDraftMessage);
  return (
    <button
      key={key}
      type="button"
      onClick={() => setDraftMessage({ text: value, internal: false })}
      className="rounded-md border border-border bg-surface p-3 text-xs font-medium text-text-muted transition-colors hover:bg-surface-muted hover:text-text disabled:cursor-not-allowed disabled:opacity-50"
    >
      {value}
    </button>
  );
}
