export const MessageBaseStyle = `
  px-4 py-2.5
  my-2
  rounded-2xl
  max-w-[80%]
  text-sm
  leading-relaxed
  break-words
  shadow-sm
  transition-all
  duration-200
  ease-in-out
  animate-[fadeIn_0.2s_ease]
  `;

export type ToolType = "invokation" | "tool_result";
export type MessageType = "ai" | "human" | "tool";

export const MessageStyle: Partial<Record<MessageType | ToolType, string>> = {
  ai: `
    bg-slate-100
    text-slate-900
    self-start
    rounded-bl-md
  `,

  human: `
    bg-blue-600
    text-white
    self-end
    rounded-br-md
    shadow-md
  `,

  tool: `
    bg-amber-50
    text-amber-900
    border border-amber-200
    self-start
  `,

  invokation: `
    bg-indigo-50
    text-indigo-900
    border border-indigo-200
    self-start
    font-mono
    text-xs
  `,

  tool_result: `
    bg-amber-50
    text-amber-900
    border border-amber-200
    self-start
  `,
};
