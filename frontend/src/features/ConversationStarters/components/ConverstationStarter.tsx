import { useStarterStore } from "../instance/store";

interface ConversationStartersProps {
  key?: string | number;
  starter: string;
  onSelect: (starter: string) => void;
}
export function Starter({ key, starter, onSelect }: ConversationStartersProps) {
  return (
    <button
      key={key}
      type="button"
      onClick={() => onSelect(starter)}
      className="rounded-full border border-border bg-surface px-5 py-5 text-xs font-medium text-text-muted transition-colors hover:bg-surface-muted hover:text-text disabled:cursor-not-allowed disabled:opacity-50"
      title={starter}
    >
      {starter}
    </button>
  );
}

export default function ConversationStarters({ onSelect }: { onSelect: (val: string) => void }) {
  const currentStarter = useStarterStore((s) => s.selectedState);
  return (
    <div className="flex flex-row">
      {currentStarter?.starters.map((v, key) => (
        <Starter
          key={key}
          starter={v}
          onSelect={onSelect}
        />
      ))}
    </div>
  );
}
