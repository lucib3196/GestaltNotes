import React from "react";
import clsx from "clsx";
import { useEffect, useRef } from "react";

type ChatContainerVariant = "demo" | "main";

const containerStyles = {
  root: "relative flex h-full min-h-0 min-w-0 w-full   flex-col overflow-hidden  text-text",
  spacing: "p-1 sm:p-3 lg:p-5",
  messages:
    "min-h-0 min-w-0 flex-1 overflow-y-auto overscroll-contain scrollbar-hide px-1 py-2 sm:px-2 sm:py-3",
  starters: "shrink-0 border-t border-border pt-2 sm:pt-3",
  composer: "min-w-0 shrink-0 pt-2 lg:pt-3",
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
