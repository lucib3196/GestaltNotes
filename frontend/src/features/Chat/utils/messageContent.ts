export function extractMessageContent(content: unknown): string | unknown[] {
  if (typeof content === "string") return content;
  if (Array.isArray(content)) return content;
  return String(content ?? "");
}
