import { ChatSession } from "../features/Chat";
import { useState } from "react";
import { GiHamburgerMenu } from "react-icons/gi";
import { ChatProvider } from "../features/Chat/instance";
import { ChatSidebar } from "../features/Chat/ui/sidebar";
import { Group, Panel, Separator, usePanelRef } from "react-resizable-panels";
import StarterView from "../features/ConversationStarters/components/StarterView";
import { TabButton } from "../components/Button";
import { WorkspaceItemsCarousel } from "../features/Tools";
import WorkspaceInfo from "../features/Tools/components/WorkspaceInfo";
import { useWorkspaceStore } from "../features/Tools/instance/store";
export type SectionTab = "resource" | "practice" | "final_review" | "info";

export function ResourceSection() {
  const workspaceItems = useWorkspaceStore((s) => s.workspaceItems);
  const currentTab = useWorkspaceStore((s) => s.currentSection);
  const setTab = useWorkspaceStore((s) => s.setCurrentSection);

  const sources = workspaceItems.filter(
    (v) => v.tool === "retrieve_me116_lecture" || "retrieve_me116_homework",
  );

  const practice = workspaceItems.filter((v) => v.tool === "generate_mcq");

  return (
    <section className="flex h-full min-h-0 flex-col rounded-lg  p-3">
      <div className="mb-3 flex gap-2">
        <TabButton
          onClick={() => setTab("info")}
          active={currentTab === "info"}
        >
          Info
        </TabButton>
        <TabButton
          onClick={() => setTab("resource")}
          active={currentTab === "resource"}
        >
          Resource
        </TabButton>
        <TabButton
          onClick={() => setTab("practice")}
          active={currentTab === "practice"}
        >
          Practice
        </TabButton>
        <TabButton
          onClick={() => setTab("final_review")}
          active={currentTab === "final_review"}
        >
          Final Review Outline
        </TabButton>
      </div>

      <div className="h-full rounded-md p-3 text-sm text-text">
        {currentTab === "practice" && (
          <WorkspaceItemsCarousel
            items={practice}
            sectionLabel="Practice"
            itemLabel="Question Set"
            emptyLabel="No practice questions yet."
            variant="accent"
          />
        )}

        {currentTab === "resource" && (
          <WorkspaceItemsCarousel
            items={sources}
            sectionLabel="Resources"
            itemLabel="Resource"
            emptyLabel="No resources available yet."
            variant="subtle"
          />
        )}
        {currentTab === "final_review" && <StarterView />}
        {currentTab === "info" && <WorkspaceInfo />}
      </div>
    </section>
  );
}

export default function ChatPage() {
  return (
    <section id="chat-page" className="flex min-h-0 flex-1 overflow-hidden">
      <ChatProvider>
        <ChatSidebar />
        <div className="flex h-full min-h-0 min-w-0 flex-1 flex-col">
          <ChatSession />
        </div>
      </ChatProvider>
    </section>
  );
}
