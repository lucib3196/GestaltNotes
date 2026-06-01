import { ChatSession } from "../features/Chat";
import { useState } from "react";
import { GiHamburgerMenu } from "react-icons/gi";

import { ChatSideBar } from "../features/Chat";
import { Group, Panel, Separator, usePanelRef } from "react-resizable-panels";
import StarterView from "../features/ConversationStarters/components/StarterView";
import { TabButton } from "../components/Button";
import { WorkspaceItemsCarousel } from "../features/Tools";
import WorkspaceInfo from "../features/Tools/components/WorkspaceInfo";
import { useWorkspaceStore } from "../features/Tools/instance/store";
export type SectionTab = "resource" | "practice" | "final_review" | "info";


export function ResourceSection() {
    const workspaceItems = useWorkspaceStore((s) => s.workspaceItems);
    const currentTab = useWorkspaceStore((s)=>s.currentSection)
    const setTab = useWorkspaceStore((s)=>s.setCurrentSection)

    const sources = workspaceItems.filter(
        (v) => v.tool === "retrieve_me116_lecture",
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
    const [showResources, setShowResources] = useState<boolean>(true);

    const rightPanelRef = usePanelRef();

    return (
        <div className="h-[calc(90vh-1rem)] w-full p-2 sm:p-3">
            <Group className="h-8-10">


                <ChatSideBar />

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
