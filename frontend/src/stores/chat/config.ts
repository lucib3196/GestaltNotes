import { z } from "zod";

export const ConfigSchema = z.object({
  model_provider: z.literal("google_genai").default("google_genai"),
  model: z
    .enum([
      "gemini-3.5-flash",
      "gemini-2.5-flash",
      "gemini-2.5-flash-lite",
      "gemini-2.5-pro",
    ])
    .default("gemini-3.5-flash"),
  course_collection_name: z.string().trim().min(1).nullish(),
  embedding_model: z.string().trim().min(1).nullish(),
  course_name: z.string().nullish(),
});

export type ConfigSchema = z.infer<typeof ConfigSchema>;

export const chatModelOptions = [
  { value: "gemini-3.5-flash", label: "3.5 Flash" },
  { value: "gemini-2.5-flash", label: "2.5 Flash" },
  { value: "gemini-2.5-flash-lite", label: "2.5 Flash Lite" },
  { value: "gemini-2.5-pro", label: "2.5 Pro" },
] satisfies { value: ConfigSchema["model"]; label: string }[];
