import { Button } from "../Button";

type ChatInputProps = {
    value: string;
    setValue: (val: string) => void;
    onSubmit: () => void;
};

export default function ChatInput({
    value,
    setValue,
    onSubmit,
}: ChatInputProps) {
    return (
        <div className="
      flex items-end gap-3
      p-3
      border border-slate-200
      rounded-xl
      bg-white
      shadow-sm
    ">
            <textarea
                className="
          flex-1
          resize-none
          rounded-lg
          border border-slate-300
          px-3 py-2
          text-sm
          focus:outline-none
          focus:ring-2
          focus:ring-blue-500
          focus:border-blue-500
        "
                rows={1}
                placeholder="Type your message..."
                value={value}
                onChange={(e) => setValue(e.target.value)}
            />

            <Button
                onClick={onSubmit}
                className="
          px-4 py-2
          text-sm
          rounded-lg
          hover:border-blue-500 
          hover:border-2
        "
            >
                Send
            </Button>
        </div>
    );
}
