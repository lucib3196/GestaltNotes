import { useEffect, useId, useRef, useState } from "react";
import type { FlowDiagram } from "./schema";
import { toMermaid } from "./toMermaid";
import mermaid from "mermaid";
// Mermaid configuration is global; serialize theme configuration and rendering.
let renderQueue: Promise<void> = Promise.resolve();

export function MermaidDiagram({ data }: { data: FlowDiagram }) {
  const id = useId().replace(/[^a-zA-Z0-9]/g, "");
  const host = useRef<HTMLDivElement>(null);
  const [status, setStatus] = useState<"loading" | "ready" | "error">(
    "loading",
  );

  useEffect(() => {
    let cancelled = false;
    const element = host.current;
    const code = toMermaid(data);

    function draw() {
      renderQueue = renderQueue.then(async () => {
        if (cancelled || !element) return;
        element.replaceChildren();
        setStatus("loading");
        try {
          if (cancelled) return;
          mermaid.initialize({
            startOnLoad: false,
            securityLevel: "strict",
            theme:
              document.documentElement.dataset.theme === "light"
                ? "default"
                : "dark",
            themeVariables: {
    fontSize: "20px",
  },
            flowchart: {  htmlLabels: false,
    useMaxWidth: false,
    nodeSpacing: 30,
    rankSpacing: 70,
    padding: 20, },
          });
          const { svg } = await mermaid.render(`mermaid${id}`, code);
          if (cancelled) return;
          element.innerHTML = svg;
          setStatus("ready");
        } catch {
          if (!cancelled) setStatus("error");
        }
      });
    }

    draw();
    const observer = new MutationObserver(draw);
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["data-theme"],
    });
    return () => {
      cancelled = true;
      observer.disconnect();
      element?.replaceChildren();
    };
  }, [data, id]);

  const descriptions = data.edges.filter((edge) => edge.description);
  const labels = new Map(data.nodes.map((node) => [node.id, node.label]));

  return (
    <section
      aria-label={data.title}
      className="min-w-0 w-full rounded-xl border border-border bg-surface p-3 text-text sm:p-4"
    >
      <h3 className="mb-3 text-sm font-semibold">{data.title}</h3>
      {data.legend.length > 0 && (
        <ul
          aria-label="Diagram color legend"
          className="mb-3 flex flex-wrap gap-x-4 gap-y-2 text-xs text-text-muted"
        >
          {data.legend.map((item, index) => (
            <li key={index} className="flex items-center gap-2">
              <span
                aria-hidden="true"
                className="h-3 w-3 shrink-0 rounded-full"
                style={{ backgroundColor: item.color }}
              />
              {item.label}
            </li>
          ))}
        </ul>
      )}
      {status === "loading" && (
        <p role="status" className="text-sm text-text-soft">
          Rendering diagram…
        </p>
      )}
      {status === "error" && (
        <p role="alert" className="text-sm text-text-muted">
          The diagram could not be displayed.
        </p>
      )}
      <div
        ref={host}
        role="img"
        aria-label={data.title}
        aria-busy={status === "loading"}
        className="[&_svg]:h-auto
    [&_svg]:w-full
    [&_svg]:min-w-[1000px]
    [&_svg]:!max-w-none"
      />
      {descriptions.length > 0 && (
        <details className="mt-3 border-t border-border pt-3">
          <summary className="cursor-pointer text-sm font-medium">
            Relationship details
          </summary>
          <ul className="mt-2 space-y-3 text-sm">
            {descriptions.map((edge, index) => (
              <li key={index}>
                <p className="font-medium">
                  {labels.get(edge.source)} → {labels.get(edge.target)}
                </p>
                <p className="mt-1 text-text-muted">{edge.description}</p>
              </li>
            ))}
          </ul>
        </details>
      )}
    </section>
  );
}
