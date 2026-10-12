import { z } from "zod";

const hexColor = z.string().regex(/^#[0-9a-fA-F]{6}$/);

export const flowDiagramSchema = z.object({
  title: z.string(),
  direction: z.enum(["LR", "TD"]).default("TD"),
  legend: z.array(z.object({ label: z.string(), color: hexColor })).default([]),
  nodes: z.array(z.object({
    id: z.string(),
    label: z.string(),
    color: hexColor.nullable().optional(),
    assessment: z.enum(["strength", "needs_practice", "insufficient_evidence"]).nullable().optional(),
  })).min(1),
  edges: z.array(z.object({
    source: z.string(),
    target: z.string(),
    label: z.string().nullable().optional(),
    description: z.string().nullable().optional(),
    color: hexColor.nullable().optional(),
  })).default([]),
}).superRefine((diagram, ctx) => {
  const ids = new Set(diagram.nodes.map((node) => node.id));
  if (ids.size !== diagram.nodes.length) {
    ctx.addIssue({ code: "custom", message: "Node IDs must be unique." });
  }
  if (diagram.edges.some((edge) => !ids.has(edge.source) || !ids.has(edge.target))) {
    ctx.addIssue({ code: "custom", message: "Unknown relationship node." });
  }
});

export type FlowDiagram = z.infer<typeof flowDiagramSchema>;
