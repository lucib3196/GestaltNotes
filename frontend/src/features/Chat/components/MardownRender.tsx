import type { ReactNode } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function Markdown({ children }: { children: ReactNode | null }) {
  if (!children) return null;

  if (typeof children !== "string") {
    return <div className="markdown-content text-text">{children}</div>;
  }

  return (
    <div className="markdown-content container text-text">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{children}</ReactMarkdown>
    </div>
  );
}
