import React from "react";
import clsx from "clsx";
import { useEffect, useRef } from "react";

type ChatContainerVariant = "demo" | "main";
type Sizes = "sm" | "med" | "lg";

const Variants: Record<ChatContainerVariant, string> = {
  demo: "relative flex min-h-0 flex-col overflow-hidden rounded-xl bg-surface text-text backdrop-blur",
  main: "relative mx-auto flex min-h-0 flex-col overflow-hidden rounded-xl bg-surface-strong p-3 text-text sm:p-5 backdrop-blur",
};

const SizeClasses: Record<Sizes, string> = {
  sm: " h-full w-full",
  med: "h-full w-full",
  lg: "h-full w-full",
};

interface ChatContainerProps {
  input: React.ReactNode;
  starters?: React.ReactNode;
  children: React.ReactNode;
  variant?: ChatContainerVariant;
  size?: Sizes;
  scrollTrigger?: number;
  bordered?: boolean;
}

export default function ChatContainer({
  input,
  starters,
  children,
  variant = "main",
  size = "med",
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
    <section
      className={clsx(
        Variants[variant],
        SizeClasses[size],
        bordered ? "border border-border shadow-sm" : "border-0 shadow-none",
      )}
    >
      <div className="flex min-h-0 flex-1 flex-col overflow-y-auto overscroll-contain scrollbar-hide px-1 py-3 sm:px-2">
        {children}
        <div ref={bottomRef} />
      </div>

      {starters ? <div className="shrink-0 border-t border-border pt-3">{starters}</div> : null}
      <div className="mt-3 shrink-0 border-t border-border pt-3">{input}</div>
    </section>
  );
}
