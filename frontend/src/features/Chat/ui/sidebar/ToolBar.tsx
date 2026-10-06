import type { ReactNode } from "react";
import { NewChatButton } from "../buttons/ChatActions";

export default function ToolBar({
  collapsed = false,
  children,
}: {
  collapsed?: boolean;
  children?: ReactNode;
}) {
  return (
    <div
      className={
        collapsed
          ? "flex flex-col items-center gap-2"
          : "flex flex-col gap-2 border-b border-border pb-3"
      }
    >
      <NewChatButton variant={collapsed ? "icon" : "full"} />
      {children}
    </div>
  );
}
