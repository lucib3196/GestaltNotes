import mermaid, { type MermaidConfig } from "mermaid";
import { useEffect, useId, useState } from "react";

let renderQueue: Promise<void> = Promise.resolve();

export type FlowchartOptions = Pick<
  NonNullable<MermaidConfig["flowchart"]>,
  "useMaxWidth" | "nodeSpacing" | "rankSpacing" | "padding" | "curve"
>;

type MermaidResult =
  | { status: "loading"; drawing: null; error: null }
  | { status: "ready"; drawing: string; error: null }
  | { status: "error"; drawing: null; error: string };

export default function useGetMermaidDiagram(
  code: string,
  {
    useMaxWidth = false,
    nodeSpacing = 30,
    rankSpacing = 50,
    padding = 20,
    curve = "basis",
  }: FlowchartOptions = {},
): MermaidResult {
  const id = useId().replace(/[^a-zA-Z0-9]/g, "");
  const [result, setResult] = useState<MermaidResult>({
    status: "loading",
    drawing: null,
    error: null,
  });

  useEffect(() => {
    let cancelled = false;
    setResult({ status: "loading", drawing: null, error: null });

    if (!code.trim()) {
      setResult({
        status: "error",
        drawing: null,
        error: "No Mermaid code provided.",
      });
      return;
    }

    renderQueue = renderQueue.then(async () => {
      if (cancelled) return;

      try {
        mermaid.initialize({
          startOnLoad: false,
          securityLevel: "strict",
          suppressErrorRendering: true,
          theme:
            document.documentElement.dataset.theme === "light"
              ? "default"
              : "dark",
          themeVariables: {
            fontSize: "10px",
          },
          flowchart: {
            htmlLabels: true,
            useMaxWidth,
            nodeSpacing,
            rankSpacing,
            padding,
            curve,
          },
        });

        const { svg } = await mermaid.render(`mermaid${id}`, code);

        if (!cancelled) {
          setResult({ status: "ready", drawing: svg, error: null });
        }
      } catch (error) {
        if (!cancelled) {
          setResult({
            status: "error",
            drawing: null,
            error:
              error instanceof Error
                ? error.message
                : "Failed to render Mermaid diagram.",
          });
        }
      }
    });

    return () => {
      cancelled = true;
    };
  }, [code, id, useMaxWidth, nodeSpacing, rankSpacing, padding, curve]);

  return result;
}
