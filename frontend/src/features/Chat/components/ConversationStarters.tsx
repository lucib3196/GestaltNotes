import type { ConversationStarter } from "../instance/types";

interface ConversationStartersProps {
  starters: ConversationStarter[];
  disabled?: boolean;
  onSelectStarter: (starter: ConversationStarter) => void;
}

export default function ConversationStarters({
  starters,
  disabled = false,
  onSelectStarter,
}: ConversationStartersProps) {
  if (starters.length === 0) return null;

  return (
    <div className="flex flex-wrap items-center gap-2">
      {starters.map((starter) => (
        <button
          key={starter.id}
          type="button"
          disabled={disabled || starter.disabled}
          onClick={() => onSelectStarter(starter)}
          className="rounded-full border border-border bg-surface px-5 py-5 text-xs font-medium text-text-muted transition-colors hover:bg-surface-muted hover:text-text disabled:cursor-not-allowed disabled:opacity-50"
          title={starter.description}
        >
          {starter.label}
        </button>
      ))}
    </div>
  );
}
