import { useEffect, useRef } from "react";
import  { type ChatMessage } from "../types/chat";

type ChatMessagesProps = {
  messages: ChatMessage[];
  showRoutingInfo: boolean;
  isLoading: boolean;
  /** Called when the user clicks a suggestion chip in the empty state. */
  onSuggestionClick?: (text: string) => void;
};

// Shown in the empty state to give users quick starting-point queries.
const SUGGESTIONS = [
  "Show me product PROD-001",
  "What's the status of order ORD-001?",
  "Track shipment SHP-001",
  "Show customer CUST-001 profile",
];

export function ChatMessages({ messages, showRoutingInfo, isLoading, onSuggestionClick }: ChatMessagesProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  // Scroll to the bottom whenever a new message or the loading indicator appears.
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  if (messages.length === 0 && !isLoading) {
    // Empty state — centered welcome screen with suggestion chips.
    return (
      <section className="flex flex-1 flex-col items-center justify-center gap-6 overflow-auto px-4">
        <div className="text-center">
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-brand-500 to-violet-600 text-3xl shadow-lg">
            🤖
          </div>
          <h3 className="text-xl font-semibold text-white">How can I help you?</h3>
          <p className="mt-1 text-sm text-slate-400">
            Ask about products, orders, shipping, or your account.
          </p>
        </div>
        {/* Quick-start suggestion chips */}
        <div className="grid grid-cols-1 gap-2 sm:grid-cols-2 w-full max-w-lg">
          {SUGGESTIONS.map((s) => (
            <button
              key={s}
              type="button"
              onClick={() => onSuggestionClick?.(s)}
              className="rounded-xl border border-slate-700/60 bg-surface-800/60 px-4 py-3 text-left text-sm text-slate-300 transition hover:border-brand-500/50 hover:bg-surface-700/60 hover:text-white"
            >
              {s}
            </button>
          ))}
        </div>
      </section>
    );
  }

  return (
    <section className="flex min-h-0 flex-1 flex-col gap-4 overflow-auto px-4 py-4">
      {messages.map((message, index) => (
        /*
         * Row direction flips per role:
         *   user      → flex-row-reverse  (avatar right, bubble right-aligned)
         *   assistant → flex-row          (avatar left,  bubble left-aligned)
         */
        <div
          key={`${message.role}-${index}`}
          className={`message-enter flex gap-3 ${message.role === "user" ? "flex-row-reverse" : "flex-row"}`}
        >
          {/* Avatar circle */}
          <div
            className={`flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-xl text-sm shadow-md ${
              message.role === "user"
                ? "bg-gradient-to-br from-brand-500 to-violet-600"
                : "bg-gradient-to-br from-slate-700 to-slate-800 border border-slate-600"
            }`}
          >
            {message.role === "user" ? "👤" : "🤖"}
          </div>

          {/* Bubble + optional routing badge */}
          <div className={`flex max-w-[75%] flex-col gap-1.5 ${message.role === "user" ? "items-end" : "items-start"}`}>
            <span className="text-xs text-slate-500">
              {message.role === "user" ? "You" : message.agent ?? "Assistant"}
            </span>
            <div
              className={`rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                message.role === "user"
                  // User: brand gradient, top-right corner squared to hug the avatar side
                  ? "rounded-tr-sm bg-gradient-to-br from-brand-500 to-brand-600 text-white shadow-lg shadow-brand-500/20"
                  // Assistant: dark card, top-left corner squared
                  : "rounded-tl-sm border border-slate-700/60 bg-surface-800 text-slate-200 shadow-md"
              }`}
            >
              <p className="whitespace-pre-wrap">{message.content}</p>
            </div>

            {/* Routing info pill — only shown when the setting is enabled */}
            {message.agent && showRoutingInfo && (
              <div className="flex items-center gap-1.5 rounded-full border border-sky-500/30 bg-sky-500/10 px-3 py-1 text-xs text-sky-400">
                <span className="h-1.5 w-1.5 rounded-full bg-sky-400" />
                Routed to {message.agent}
              </div>
            )}
          </div>
        </div>
      ))}

      {/* Animated typing indicator shown while the API request is in-flight */}
      {isLoading && (
        <div className="message-enter flex gap-3">
          <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-xl border border-slate-600 bg-gradient-to-br from-slate-700 to-slate-800 text-sm shadow-md">
            🤖
          </div>
          <div className="flex flex-col gap-1.5 items-start">
            <span className="text-xs text-slate-500">Assistant</span>
            <div className="rounded-2xl rounded-tl-sm border border-slate-700/60 bg-surface-800 px-5 py-4 shadow-md">
              {/* Three bouncing dots — animation defined in index.css (.typing-dot) */}
              <div className="flex items-center gap-1.5">
                <span className="typing-dot h-2 w-2 rounded-full bg-brand-400" />
                <span className="typing-dot h-2 w-2 rounded-full bg-brand-400" />
                <span className="typing-dot h-2 w-2 rounded-full bg-brand-400" />
              </div>
            </div>
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </section>
  );
}
