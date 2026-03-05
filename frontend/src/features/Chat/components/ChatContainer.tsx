import React from "react";
import clsx from "clsx";
import { MathJax } from "better-react-mathjax";

type ChatContainerProps = React.ButtonHTMLAttributes<HTMLDivElement> & {
  children?: React.ReactNode;
};

export default function ChatContainer({
  children,
  ...rest
}: ChatContainerProps) {
  return (
    <MathJax className="h-full">
      <div
        className={clsx(
          "flex flex-col grow  bg-gray-100 border rounded-lg shadow-md overflow-y-auto overflow-x-hidden",
          rest.className,
        )}
      >
        {children ?? ""}
      </div>
    </MathJax>
  );
}
