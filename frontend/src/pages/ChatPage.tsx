
import { ChatSession } from "../features/Chat"
import { useCallback, useEffect, useRef, useState } from "react";
import { GiHamburgerMenu } from "react-icons/gi";
import { useAuth } from "../context";
import type { Thread } from "../services";
import { useChatContext } from "../features/Chat/instance";
import { RenderToolCalls } from "../features/Chat/tools";
import { ChatSideBar } from "../features/Chat";
import { Group, Panel, Separator, usePanelRef } from "react-resizable-panels";
import type { ThreadUpdate } from "../services/chat/types";

import clsx from "clsx";
type SectionTab = "resource" | "practice" | "final_review";


function ChatSideBarComponent() {
    const { user } = useAuth();
    const [threads, setThreads] = useState<Thread[]>([]);
    const selectedId = useChatContext((s) => s.theadId)
    const setSelectedThread = useChatContext((s) => s.selectThread);
    const getUserThreads = useChatContext((s) => s.getUserThreads);
    const setSessionKey = useChatContext((s) => s.setSessionKey)
    const updateThread = useChatContext((s) => s.updateThread)
    const handleNewChat = async () => {
        setSelectedThread(null, null);
        setSessionKey();
    };

    const loadUserThreads = useCallback(
        async (authToken: string) => {
            const res = await getUserThreads(authToken);

            setThreads(res);
        },
        [getUserThreads],
    );

    const handleThreadUpdate = useCallback(async (id: string, data: ThreadUpdate) => {
        if (!user) return;
        const authToken = await user.getIdToken();
        await updateThread(id, data);
        await loadUserThreads(authToken);
    }, [user, updateThread, loadUserThreads])
    useEffect(() => {
        let isMounted = true;

        const bootstrap = async () => {
            if (!user) return;
            const authToken = await user.getIdToken();
            if (!isMounted) return;
            await loadUserThreads(authToken);
        };

        void bootstrap();

        return () => {
            isMounted = false;
        };
    }, [user, loadUserThreads,]);

    return <div>
        <ChatSideBar chats={threads} activeChatId={selectedId} onSelectChat={setSelectedThread} onNewChat={handleNewChat} onThreadUpdate={handleThreadUpdate} />
    </div>

}




export function ResourceSection() {
    const [activeTab, setActiveTab] = useState<SectionTab>("resource");
    const [practiceIndex, setPracticeIndex] = useState(0);

    const workspaceItems = useChatContext((s) => s.workspaceItems);

    const sources = workspaceItems.filter((v) => v.tool === "retrieve_me116_lecture");
    const practice = workspaceItems.filter((v) => v.tool === "generate_mcq");

    const practiceCount = practice.length;
    const hasPractice = practiceCount > 0;
    const clampedPracticeIndex = hasPractice ? Math.min(practiceIndex, practiceCount - 1) : 0;
    const currentPracticeItem = hasPractice ? practice[clampedPracticeIndex] : null;

    useEffect(() => {
        if (!hasPractice) {
            setPracticeIndex(0);
            return;
        }
        if (practiceIndex > practiceCount - 1) {
            setPracticeIndex(practiceCount - 1);
        }
    }, [hasPractice, practiceCount, practiceIndex]);

    const goPrevPractice = () => {
        setPracticeIndex((prev) => Math.max(0, prev - 1));
    };

    const goNextPractice = () => {
        setPracticeIndex((prev) => Math.min(practiceCount - 1, prev + 1));
    };

    return (
        <section className="flex h-full min-h-0 flex-col rounded-lg  p-3">
            <div className="mb-3 flex gap-2">
                <button
                    type="button"
                    onClick={() => setActiveTab("resource")}
                    className={clsx(
                        "rounded-md px-3 py-1.5 text-sm transition-colors",
                        activeTab === "resource"
                            ? "bg-accent text-bg"
                            : "bg-surface-muted text-text-muted hover:text-text"
                    )}
                >
                    Resource
                </button>
                <button
                    type="button"
                    onClick={() => setActiveTab("practice")}
                    className={clsx(
                        "rounded-md px-3 py-1.5 text-sm transition-colors",
                        activeTab === "practice"
                            ? "bg-accent text-bg"
                            : "bg-surface-muted text-text-muted hover:text-text"
                    )}
                >
                    Practice
                </button>
            </div>

            <div className="h-full rounded-md p-3 text-sm text-text">
                {activeTab === "resource" ? (
                    <div className="h-full space-y-3 overflow-y-auto pr-1">
                        {sources.length === 0 ? (
                            <p className="text-text-soft">No resources yet.</p>
                        ) : (
                            sources.map((v) => <RenderToolCalls key={v.id} msg={v.rawMsg} />)
                        )}
                    </div>
                ) : (
                    <div className="flex h-[72vh] flex-col">
                        <div className="mb-3 flex items-center justify-between border-b border-border pb-2">
                            <p className="text-xs uppercase tracking-wide text-text-soft">
                                {hasPractice ? `Question Set ${clampedPracticeIndex + 1} of ${practiceCount}` : "Practice"}
                            </p>
                            <div className="flex items-center gap-2">
                                <button
                                    type="button"
                                    onClick={goPrevPractice}
                                    disabled={!hasPractice || clampedPracticeIndex === 0}
                                    className="rounded-md border border-border bg-surface px-2.5 py-1 text-xs text-text-muted transition-colors hover:border-border-strong hover:text-text disabled:cursor-not-allowed disabled:opacity-40"
                                >
                                    Prev
                                </button>
                                <button
                                    type="button"
                                    onClick={goNextPractice}
                                    disabled={!hasPractice || clampedPracticeIndex === practiceCount - 1}
                                    className="rounded-md border border-border bg-surface px-2.5 py-1 text-xs text-text-muted transition-colors hover:border-border-strong hover:text-text disabled:cursor-not-allowed disabled:opacity-40"
                                >
                                    Next
                                </button>
                            </div>
                        </div>

                        <div className="min-h-0 flex-1 overflow-y-auto pr-1">
                            {!currentPracticeItem ? (
                                <p className="text-text-soft">No practice questions yet.</p>
                            ) : (
                                <RenderToolCalls key={currentPracticeItem.id} msg={currentPracticeItem.rawMsg} />
                            )}
                        </div>
                    </div>
                )}
            </div>
        </section>
    );
}
export default function ChatPage() {
    const { user } = useAuth();


    const [token, setToken] = useState<string>("");
    const [showSideBar, setShowSideBar] = useState<boolean>(true);
    const [showResources, setShowResources] = useState<boolean>(true);

    const leftPanelRef = usePanelRef()
    const rightPanelRef = usePanelRef()

    useEffect(() => {
        const getToken = async () => {
            if (!user) return;
            const t = await user?.getIdToken()
            setToken(t)
        }
        getToken()
    }, [user])
    return (
        <div className="h-[calc(100vh-1rem)] w-full p-2 sm:p-3">
            <Group className="h-full">
                <Panel
                    panelRef={leftPanelRef}
                    id="chat-panel"
                    collapsible
                    collapsedSize={100}

                    defaultSize={20}
                    onResize={() => setShowSideBar(true)}
                    className="min-h-0 overflow-hidden rounded-lg bg-surface-strong p-2"
                >
                    <button
                        type="button"
                        aria-label={showSideBar ? "Collapse sidebar" : "Expand sidebar"}
                        onClick={() => {
                            if (showSideBar) {
                                leftPanelRef.current?.collapse();
                                setShowSideBar(false);
                                return;
                            }
                            leftPanelRef.current?.expand();
                            setShowSideBar(true);
                        }}
                        className="mb-2 inline-flex h-9 w-9 items-center justify-center rounded-md bg-surface text-text-muted transition-colors hover:bg-surface-muted hover:text-text"
                    >
                        <GiHamburgerMenu />
                    </button>

                    {showSideBar ? <ChatSideBarComponent /> : null}
                </Panel>

                <Separator className="mx-2 w-2 bg-border   rounded-full hover:bg-blue-500" />

                <Panel id="chat-main" minSize={40} defaultSize={52} className="min-h-0 overflow-hidden rounded-lg bg-surface-strong">
                    <ChatSession token={token}></ChatSession>
                </Panel>

                <Separator className="mx-2 w-2 bg-border   rounded-full hover:bg-blue-500" />

                <Panel
                    panelRef={rightPanelRef}
                    id="chat-resources"
                    collapsible
                    collapsedSize={100}
                    minSize={18}
                    defaultSize={28}
                    className="min-h-0 overflow-hidden rounded-lg bg-surface-strong p-2 scrollbar-hide"
                    onResize={() => setShowResources(true)}
                >
                    <button
                        type="button"
                        aria-label={showResources ? "Collapse resources" : "Expand resources"}
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
