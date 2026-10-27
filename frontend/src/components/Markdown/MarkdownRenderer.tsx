import type { ReactNode } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import remarkMath from "remark-math";
import rehypeMathjax from "rehype-mathjax";

export default function MarkdownRenderer({
  children,
}: {
  children: ReactNode | null;
}) {
  if (!children) return null;

  if (typeof children !== "string") {
    return <div className="chat-markdown text-text">{children}</div>;
  }

  return (
     <div className="chat-markdown min-w-0 text-text">
    <ReactMarkdown
      remarkPlugins={[remarkGfm, remarkMath]}
      rehypePlugins={[rehypeMathjax]}
    >
      {children}
    </ReactMarkdown>
  </div>
  );
}
