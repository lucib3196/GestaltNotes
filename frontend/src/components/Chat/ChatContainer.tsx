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
    <MathJax>
      <div
        className={clsx(
          "flex flex-col w-200 h-150 bg-gray-100 border rounded-lg shadow-md overflow-hidden",
          rest.className,
        )}
      >
        {children ?? ""}
      </div>
    </MathJax>
  );
}
