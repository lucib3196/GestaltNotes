import React from "react";
import clsx from "clsx";
import { RiChatNewLine } from "react-icons/ri";
import { useEffect, useRef } from "react";

type ChatContainerVariant = "demo" | "main";
type Sizes = "sm" | "med" | "lg";

const Variants: Record<ChatContainerVariant, string> = {
  demo:
    "relative flex flex-col overflow-hidden rounded-xl border border-border bg-surface text-text shadow-soft backdrop-blur",
  main:
    "relative mx-auto flex flex-col overflow-hidden rounded-xl border border-border bg-surface-strong p-4 text-text shadow-soft backdrop-blur",
};

const SizeClasses: Record<Sizes, string> = {
  sm: "h-[360px] w-full max-w-md",
  med: "h-[560px] w-full max-w-3xl",
  lg: "h-[760px] w-full max-w-5xl",
};

interface ChatContainerProps {
  input: React.ReactNode;
  children: React.ReactNode;
  variant?: ChatContainerVariant;
  size?: Sizes;
  onNewChat?: () => void;
  scrollTrigger?: number;
}

export default function ChatContainer({
  input,
  children,
  variant = "main",
  size = "med",
  onNewChat,
  scrollTrigger = 0,
}: ChatContainerProps) {
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  }, [scrollTrigger]);

  return (
    <section className={clsx(Variants[variant], SizeClasses[size])}>
      <div className="mb-3 flex items-center justify-between border-b border-border pb-3">
        <p className="text-xs font-medium uppercase tracking-[0.18em] text-text-soft">
          Conversation
        </p>
        {onNewChat ? (
          <button
            type="button"
            onClick={onNewChat}
            aria-label="Start new chat"
            title="New chat"
            className="inline-flex h-10 w-10 items-center justify-center rounded-md border border-border bg-surface text-text-muted transition-all duration-base ease-base hover:border-border-strong hover:bg-surface-muted hover:text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60"
          >
            <RiChatNewLine size={19} />
          </button>
        ) : null}
      </div>

      <div className="flex flex-1 flex-col gap-4 overflow-y-auto pr-1 scroll-smooth sm:pr-2">
        {children}
        <div ref={bottomRef} />
      </div>

      <div className="mt-3 border-t border-border pt-3">{input}</div>
    </section>
  );
}
