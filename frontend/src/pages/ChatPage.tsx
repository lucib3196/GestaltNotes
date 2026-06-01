import { ChatSession } from "../features/Chat";
import { useState } from "react";
import { GiHamburgerMenu } from "react-icons/gi";

import { useChatContext } from "../features/Chat/instance";
import { ChatSideBar } from "../features/Chat";
import { Group, Panel, Separator, usePanelRef } from "react-resizable-panels";
import StarterView from "../features/ConversationStarters/components/StarterView";
import { TabButton } from "../components/Button";
import { WorkspaceItemsCarousel } from "../features/Tools";
type SectionTab = "resource" | "practice" | "final_review";

export function ResourceSection() {
  const [activeTab, setActiveTab] = useState<SectionTab>("resource");

  const workspaceItems = useChatContext((s) => s.workspaceItems);

  const sources = workspaceItems.filter(
    (v) => v.tool === "retrieve_me116_lecture",
  );
  const practice = workspaceItems.filter((v) => v.tool === "generate_mcq");

  return (
    <section className="flex h-full min-h-0 flex-col rounded-lg  p-3">
      <div className="mb-3 flex gap-2">
        <TabButton
          onClick={() => setActiveTab("resource")}
          active={activeTab === "resource"}
        >
          Resource
        </TabButton>
        <TabButton
          onClick={() => setActiveTab("practice")}
          active={activeTab === "practice"}
        >
          Practice
        </TabButton>
        <TabButton
          onClick={() => setActiveTab("final_review")}
          active={activeTab === "final_review"}
        >
          Final Review Outline
        </TabButton>
      </div>

      <div className="h-full rounded-md p-3 text-sm text-text">
        {activeTab === "practice" && (
          <WorkspaceItemsCarousel
            items={practice}
            sectionLabel="Practice"
            itemLabel="Question Set"
            emptyLabel="No practice questions yet."
            variant="accent"
          />
        )}

        {activeTab === "resource" && (
          <WorkspaceItemsCarousel
            items={sources}
            sectionLabel="Resources"
            itemLabel="Resource"
            emptyLabel="No resources available yet."
            variant="subtle"
          />
        )}
        {activeTab === "final_review" && <StarterView />}
      </div>
    </section>
  );
}
// TODO lets imporve the style for the chatside bar where there is collapse version 
export default function ChatPage() {
  const [showSideBar, setShowSideBar] = useState<boolean>(true);
  const [showResources, setShowResources] = useState<boolean>(true);

  const rightPanelRef = usePanelRef();

  return (
    <div className="h-[calc(100vh-1rem)] w-full p-2 sm:p-3">
      <Group className="h-full">
        

        {showSideBar ? <ChatSideBar /> : null}

        <Panel
          id="chat-main"
          minSize={40}
          defaultSize={52}
          className="min-h-0 overflow-hidden rounded-lg bg-surface-strong"
        >
          <ChatSession />
        </Panel>

        <Separator className="mx-2 w-2 bg-border   rounded-full hover:bg-blue-500" />

        <Panel
          panelRef={rightPanelRef}
          id="chat-resources"
          collapsible
          collapsedSize={10}
          minSize={18}
          defaultSize={28}
          className="min-h-0 overflow-hidden rounded-lg bg-surface-strong p-2 scrollbar-hide"
          onResize={() => setShowResources(true)}
        >
          <button
            type="button"
            aria-label={
              showResources ? "Collapse resources" : "Expand resources"
            }
            onClick={() => {
              if (showResources) {
                rightPanelRef.current?.collapse();
                setShowResources(false);
                return;
              }
              rightPanelRef.current?.expand();
              setShowResources(true);
            }}
            className="mb-2 inline-flex h-9 w-9 items-center justify-center rounded-md bg-surface text-text-muted transition-colors hover:bg-surface-muted hover:text-text"
          >
            <GiHamburgerMenu />
          </button>

          {showResources ? <ResourceSection /> : null}
        </Panel>
      </Group>
    </div>
  );
}
