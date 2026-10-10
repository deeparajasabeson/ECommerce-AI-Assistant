import { FormEvent, useMemo, useState } from "react";

import { ChatInput } from "./components/ChatInput";
import { ChatMessages } from "./components/ChatMessages";
import { Sidebar } from "./components/Sidebar";
import { agentCapabilities } from "./constants/agentCapabilities";
import { sendChatQuery } from "./services/chatService";
import type { ChatMessage } from "./types/chat";

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [prompt, setPrompt] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [showRoutingInfo, setShowRoutingInfo] = useState(true);
  const [error, setError] = useState<string | null>(null);
  // Controls whether the sidebar is fully expanded (w-72) or collapsed to
  // a narrow icon rail (w-14). Both states remain in the DOM — no overlay.
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // Only truthy when there is typed text AND no request is in-flight.
  const canSend = useMemo(() => prompt.trim().length > 0 && !isLoading, [prompt, isLoading]);

  const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const normalizedPrompt = prompt.trim();
    if (!normalizedPrompt || isLoading) return;

    setError(null);
    setPrompt("");
    setIsLoading(true);
    // Optimistically append the user message before the API responds.
    setMessages((prev) => [...prev, { role: "user", content: normalizedPrompt }]);

    try {
      const data = await sendChatQuery(normalizedPrompt);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.response, agent: data.agent },
      ]);
    } catch (requestError) {
      const message =
        requestError instanceof Error
          ? requestError.message
          : "Unexpected error while calling assistant.";
      setError(message);
      // Still append an error bubble so the conversation history is intact.
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: `❌ Error: ${message}` },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen overflow-hidden bg-surface-950">
      {/*
        Sidebar wrapper: animates its width between 288px (expanded) and 56px
        (icon rail) so the main area naturally fills the reclaimed space.
        Both panels are always rendered; CSS opacity + pointer-events control
        which one is visible at any given width.
      */}
      <div
        className={`flex-shrink-0 transition-all duration-300 ease-in-out ${
          sidebarOpen ? "w-72" : "w-14"
        }`}
      >
        <Sidebar
          isOpen={sidebarOpen}
          onToggle={() => setSidebarOpen((v) => !v)}
          showRoutingInfo={showRoutingInfo}
          onToggleRoutingInfo={setShowRoutingInfo}
          onClearChat={() => { setMessages([]); setError(null); }}
          capabilities={agentCapabilities}
        />
      </div>

      {/* Main chat area — min-w-0 prevents flex overflow when sidebar is wide */}
      <main className="flex min-w-0 flex-1 flex-col overflow-hidden bg-surface-950">
        {/* Top bar */}
        <header className="flex flex-shrink-0 items-center justify-between border-b border-slate-800 px-5 py-3">
          <div>
            <h1 className="text-base font-bold text-white leading-tight">🛍️ E-Commerce AI Assistant</h1>
            <p className="text-xs text-slate-500">Powered by Azure AI Foundry · Multi-Agent System</p>
          </div>
          <div className="hidden items-center gap-1.5 rounded-full border border-slate-700/50 bg-surface-800 px-3 py-1.5 text-xs text-slate-400 sm:flex">
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-400" />
            4 agents online
          </div>
        </header>

        {/* Scrollable message list — flex-1 so it fills all remaining vertical space */}
        <ChatMessages
          messages={messages}
          showRoutingInfo={showRoutingInfo}
          isLoading={isLoading}
          onSuggestionClick={setPrompt}
        />

        {/* Non-fatal error banner shown above the input when a request fails */}
        {error && (
          <div className="mx-4 mb-2 flex items-center gap-2 rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-400">
            <svg className="h-4 w-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            {error}
          </div>
        )}

        {/* Sticky input bar — flex-shrink-0 keeps it pinned at the bottom */}
        <div className="flex-shrink-0 border-t border-slate-800 px-4 py-4">
          <ChatInput
            prompt={prompt}
            canSend={canSend}
            disabled={isLoading}
            onChange={setPrompt}
            onSubmit={onSubmit}
          />
          <p className="mt-2 text-center text-xs text-slate-600">
            Press Enter to send · Shift+Enter for new line
          </p>
        </div>
      </main>
    </div>
  );
}

export default App;
