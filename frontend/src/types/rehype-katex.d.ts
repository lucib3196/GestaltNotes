declare module "rehype-katex" {
  import type { Root } from "hast";
  import type { Plugin } from "unified";

  export type Options = {
    throwOnError?: boolean;
    errorColor?: string;
    macros?: Record<string, string>;
    strict?: boolean | "ignore" | "warn" | "error";
    inlineMathDoubleDisplay?: boolean;
  };

  const rehypeKatex: Plugin<[Options?], Root>;
  export default rehypeKatex;
}
