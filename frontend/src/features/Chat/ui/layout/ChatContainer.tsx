import React from "react";
import clsx from "clsx";
import { useEffect, useRef } from "react";

type ChatContainerVariant = "demo" | "main";

const containerStyles = {
  root: "relative flex h-full min-h-0 min-w-0 w-full flex-col overflow-hidden text-text",
  spacing: "px-3 pb-3 sm:px-6 sm:pb-5 lg:px-8",
  messages:
    "min-h-0 min-w-0 flex-1 overflow-y-auto overscroll-contain scrollbar-hide py-5 sm:py-8",
  starters: "mx-auto w-full max-w-4xl shrink-0 border-t border-border pt-4",
  composer: "mx-auto w-full max-w-4xl  min-w-0 shrink-0 pt-4 sm:pt-5",
};

const variantStyles: Record<ChatContainerVariant, string> = {
  main: "bg-inherit",
  demo: "rounded-xl bg-surface",
};

interface ChatContainerProps {
  input: React.ReactNode;
  starters?: React.ReactNode;
  children: React.ReactNode;
  variant?: ChatContainerVariant;
  className?: string;
  scrollTrigger?: number;
  bordered?: boolean;
}

export default function ChatContainer({
  input,
  starters,
  children,
  variant = "main",
  className,
  scrollTrigger = 0,
  bordered = true,
}: ChatContainerProps) {
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  }, [scrollTrigger]);

  return (
    <div
      className={clsx(
        containerStyles.root,
        containerStyles.spacing,
        variantStyles[variant],
        bordered && "border border-border shadow-sm",
        className,
      )}
    >
      <div id="message-container" className={containerStyles.messages}>
        {children}
        <div ref={bottomRef} aria-hidden="true" />
      </div>

      {starters ? (
        <div id="conversation-starters" className={containerStyles.starters}>
          {starters}
        </div>
      ) : null}

      <div id="input-container" className={containerStyles.composer}>
        {input}
      </div>
    </div>
  );
}
