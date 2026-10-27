import type { ReactNode } from "react";
import { NewChatButton } from "./NewChatButton";

export type ChatSidebarToolbarProps = {
  collapsed?: boolean;
  children?: ReactNode;
};

export default function ChatSidebarToolbar({
  collapsed = false,
  children,
}: ChatSidebarToolbarProps) {
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
