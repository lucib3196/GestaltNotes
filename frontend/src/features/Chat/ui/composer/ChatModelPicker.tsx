import {
  chatModelOptions,
  ConfigSchema,
} from "../../../../stores/chat/config";
import { useChatStore } from "../../instance";

export function ChatModelPicker({ disabled = false }: { disabled?: boolean }) {
  const model = useChatStore((state) => state.config.model);
  const setModel = useChatStore((state) => state.setModel);

  return (
    <select
      aria-label="Chat model"
      title="Choose a Gemini model"
      value={model}
      disabled={disabled}
      onChange={(event) => {
        const result = ConfigSchema.shape.model.safeParse(event.target.value);
        if (result.success) setModel(result.data);
      }}
      className="h-10 min-w-0 max-w-36 rounded-md border border-border bg-surface px-2 text-sm text-text outline-none focus-visible:ring-2 focus-visible:ring-accent/60 disabled:cursor-not-allowed disabled:opacity-50 sm:max-w-44"
    >
      {chatModelOptions.map(({ value, label }) => (
        <option key={value} value={value}>
          Gemini {label}
        </option>
      ))}
    </select>
  );
}
