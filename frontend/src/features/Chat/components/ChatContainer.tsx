import React from "react";
import clsx from "clsx";
import { useEffect, useRef } from "react";

type ChatContainerVariant = "demo" | "main";
type Sizes = "sm" | "med" | "lg";

const Variants: Record<ChatContainerVariant, string> = {
  demo:
    "relative flex flex-col overflow-hidden rounded-xl bg-surface text-text backdrop-blur",
  main:
    "relative mx-auto flex flex-col overflow-hidden rounded-xl bg-surface-strong p-4 text-text backdrop-blur",
};

const SizeClasses: Record<Sizes, string> = {
  sm: "h-[360px] w-full max-w-md",
  med: "h-[560px] w-full max-w-3xl",
  lg: "h-[760px] w-full max-w-5xl",
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
        bordered ? "border border-border shadow-soft" : "border-0 shadow-none",
      )}
    >
      <div className="flex flex-1 flex-col gap-4 overflow-y-auto pr-1 scroll-smooth scrollbar-hide sm:pr-2">
        {children}
        <div ref={bottomRef} />
      </div>

      {starters ? <div className="mt-3">{starters}</div> : null}
      <div className="mt-3  pt-3">{input}</div>
    </section>
  );
}
