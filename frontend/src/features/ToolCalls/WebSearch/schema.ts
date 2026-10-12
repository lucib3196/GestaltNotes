import { z } from "zod";

export const webSearchSourcesSchema = z.array(
  z.object({
    url: z.string().url().refine(
      (value) => ["http:", "https:"].includes(new URL(value).protocol),
      "Expected an HTTP or HTTPS link",
    ),
    title: z.string().nullable().optional(),
    start_index: z.number().int().nonnegative().nullable().optional(),
    end_index: z.number().int().nonnegative().nullable().optional(),
  }),
);

export type WebSearchSources = z.infer<typeof webSearchSourcesSchema>;
