import type { ReactNode } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import remarkMath from "remark-math";
import { MathJax } from "better-react-mathjax";
import "katex/dist/katex.min.css";
import rehypeKatex from "rehype-katex";

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
    <MathJax>
      <div className="chat-markdown min-w-0 text-text">
        <ReactMarkdown rehypePlugins={[rehypeKatex]} remarkPlugins={[remarkGfm, remarkMath]}>
          {children}
        </ReactMarkdown>
      </div>
    </MathJax>
  );
}
