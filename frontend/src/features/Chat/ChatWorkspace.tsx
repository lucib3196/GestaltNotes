import { ChatProvider } from "./instance";
import { ChatSidebar } from "./ui/sidebar";
import ChatSession from "./session/ChatSession";
import { useFetchCourseVectorstore } from "./hooks/useFetchCourseVectorstores";

export default function ChatPage() {
  const { configs } = useFetchCourseVectorstore();
  console.log("Configs", configs);
  return (
    <section id="chat-page" className="flex min-h-0 flex-1 overflow-hidden">
      <ChatProvider>
        <ChatSidebar />
        <div className="flex h-full min-h-0 min-w-0 flex-1 flex-col">
          <div>Settings</div>
          <ChatSession />
        </div>
      </ChatProvider>
    </section>
  );
}
