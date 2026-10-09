import type { MessagePayload } from "../types";
import type { ImagePayload } from "../types/content";

export async function blobURLtoBase64(blobUrl: string): Promise<string> {
  const response = await fetch(blobUrl);
  const blob = await response.blob();
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.readAsDataURL(blob);
    reader.onloadend = () => resolve(reader.result as string);
    reader.onerror = reject;
  });
}


export async function prepareMessage(
  text: string,
  images?: string[],
): Promise<MessagePayload[]> {
  // Append text to send to llm
  const content: MessagePayload[] = [{ type: "text", text }];
  if (images && images.length > 0) {
    const urls = await Promise.all(images.map(async (v) => blobURLtoBase64(v)));
    const imagePayload: ImagePayload[] = urls.map((url) => ({
      type: "image_url",
      image_url: { url },
    }));

    content.push(...imagePayload);
  }
  return content;
}
