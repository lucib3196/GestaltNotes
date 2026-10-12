import type { FlowDiagram } from "./schema";

export const assessmentLabels = {
  strength: "Demonstrated strength",
  needs_practice: "Needs practice",
  insufficient_evidence: "Not enough evidence",
};

function textColor(hex: string): string {
  const channels = [1, 3, 5].map((offset) => {
    const value = parseInt(hex.slice(offset, offset + 2), 16) / 255;
    return value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
  });
  const luminance =
    channels[0] * 0.2126 + channels[1] * 0.7152 + channels[2] * 0.0722;
  return luminance > 0.179 ? "#000000" : "#FFFFFF";
}

function quoteLabel(value: string): string {
  return `"${value
    .replace(/&/g, "&amp;")
    .replace(/"/g, "&quot;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\r?\n/g, " ")}"`;
}

export function toMermaid(diagram: FlowDiagram): string {
  const ids = new Map(
    diagram.nodes.map((node, index) => [node.id, `node${index}`]),
  );
  return [
    `flowchart ${diagram.direction}`,
    ...diagram.nodes.map((node) => {
      const label = node.assessment
        ? `${node.label} — ${assessmentLabels[node.assessment]}`
        : node.label;
      return `${ids.get(node.id)}[${quoteLabel(label)}]`;
    }),
    ...diagram.edges.map((edge) => {
      const label = edge.label ? `|${quoteLabel(edge.label)}|` : "";
      return `${ids.get(edge.source)} -->${label} ${ids.get(edge.target)}`;
    }),
    ...diagram.nodes
      .filter((node) => node.color)
      .map(
        (node) =>
          `style ${ids.get(node.id)} fill:${node.color},stroke:${node.color},color:${textColor(node.color!)}`,
      ),
    ...diagram.edges.flatMap((edge, index) =>
      edge.color
        ? [`linkStyle ${index} stroke:${edge.color},stroke-width:2px`]
        : [],
    ),
  ].join("\n");
}
