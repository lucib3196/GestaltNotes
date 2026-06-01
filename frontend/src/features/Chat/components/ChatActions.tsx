import { useThreadStore } from "../instance/store";

type NewChatButtonVariant = "full" | "icon";

type NewChatButtonProps = {
    variant?: NewChatButtonVariant;
};

export function NewChatButton({ variant = "full" }: NewChatButtonProps) {
    const clearThread = useThreadStore((s) => s.clearThread);

    const sharedProps = {
        type: "button" as const,
        onClick: () => clearThread(),
        "aria-label": "New chat",
    };

    if (variant === "icon") {
        return (
            <button
                {...sharedProps}
                className="flex h-9 w-9 items-center justify-center rounded-md border border-border bg-surface text-text-muted transition-all duration-base ease-base hover:border-border-strong hover:bg-surface-muted hover:text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-5 w-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={1.8}
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M12 4H6a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2v-6M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"
                    />
                </svg>
            </button>
        );
    }

    return (
        <button
            {...sharedProps}
            className="relative flex h-9 w-full items-center rounded-md border border-border bg-surface px-3 text-text-muted transition-all duration-base ease-base hover:border-border-strong hover:bg-surface-muted hover:text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60"
        >
            <svg
                xmlns="http://www.w3.org/2000/svg"
                className="absolute left-3 h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={1.8}
            >
                <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M12 4H6a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2v-6M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"
                />
            </svg>
            <span className="w-full text-center">New Chat</span>
        </button>
    );
}
export default function ChatActions() {
    return (
        <div className="flex w-full flex-row gap-2">
            <NewChatButton variant="full" />
            
        </div>
    );
}
