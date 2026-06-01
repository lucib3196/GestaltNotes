import type { ReactNode } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';



export default function Markdown({ children }: { children: ReactNode | null }) {
  if (!children) return null;

  if (typeof children !== "string") {
    return <div className="markdown-content text-text">{children}</div>;
  }


  return (
    <div className="markdown-content container text-text">
      <ReactMarkdown rehypePlugins={[[rehypeKatex, { throwOnError: false, strict: "ignore", }]]} remarkPlugins={[remarkGfm, remarkMath]}>{children}</ReactMarkdown>
    </div>
  );
}
