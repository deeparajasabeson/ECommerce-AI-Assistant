import type { AgentCapability } from "../types/chat";

type SidebarProps = {
  isOpen: boolean;
  onToggle: () => void;
  showRoutingInfo: boolean;
  onToggleRoutingInfo: (checked: boolean) => void;
  onClearChat: () => void;
  capabilities: AgentCapability[];
};

// Icon, cardColor, and badgeColor are now fields on AgentCapability itself
// (defined in agentCapabilities.ts) so no parallel lookup maps are needed.

export function Sidebar({
  isOpen,
  onToggle,
  showRoutingInfo,
  onToggleRoutingInfo,
  onClearChat,
  capabilities,
}: SidebarProps) {
  return (
    <aside className="relative flex h-full flex-col overflow-hidden border-r border-slate-800 bg-surface-900">
      {/* ── COLLAPSED STRIP ── */}
      <div
        className={`absolute inset-0 flex flex-col items-center py-3 gap-3 transition-opacity duration-200 ${
          isOpen ? "opacity-0 pointer-events-none" : "opacity-100"
        }`}
      >
        {/* Toggle open */}
        <button
          type="button"
          onClick={onToggle}
          title="Open sidebar"
          className="flex h-9 w-9 items-center justify-center rounded-xl text-slate-400 transition hover:bg-surface-800 hover:text-white"
        >
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>

        <div className="h-px w-8 bg-slate-700" />

        {/* Agent icons — use cap.icon and cap.badgeColor from the capability data */}
        {capabilities.map((cap) => (
          <button
            key={cap.title}
            type="button"
            title={cap.title}
            className={`flex h-9 w-9 items-center justify-center rounded-xl border text-lg transition ${cap.badgeColor}`}
          >
            {cap.icon}
          </button>
        ))}

        <div className="flex-1" />

        {/* Status dot */}
        <span className="relative flex h-2.5 w-2.5 mb-1" title="4 agents active">
          <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-60" />
          <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-emerald-500" />
        </span>

        {/* Clear icon */}
        <button
          type="button"
          onClick={onClearChat}
          title="Clear chat"
          className="flex h-9 w-9 items-center justify-center rounded-xl text-slate-500 transition hover:bg-red-500/15 hover:text-red-400"
        >
          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>

      {/* ── EXPANDED PANEL ── */}
      <div
        className={`flex flex-1 flex-col overflow-y-auto transition-opacity duration-200 ${
          isOpen ? "opacity-100" : "opacity-0 pointer-events-none"
        }`}
      >
        {/* Header */}
        <div className="px-4 pt-5 pb-4">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-brand-500 to-violet-600 text-lg shadow-lg glow-brand">
              🤖
            </div>
            <div className="flex-1 min-w-0">
              <h2 className="truncate text-sm font-bold text-white leading-tight">Multi-Agent System</h2>
              <p className="truncate text-xs text-slate-500">AI-powered commerce</p>
            </div>
            {/* Collapse button */}
            <button
              type="button"
              onClick={onToggle}
              title="Collapse sidebar"
              className="flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-lg text-slate-500 transition hover:bg-surface-800 hover:text-slate-300"
            >
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
              </svg>
            </button>
          </div>

          {/* Status badge */}
          <div className="mt-4 flex items-center gap-2 rounded-xl border border-emerald-500/20 bg-emerald-500/10 px-3 py-2">
            <span className="relative flex h-2 w-2 flex-shrink-0">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75" />
              <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-500" />
            </span>
            <div className="min-w-0">
              <p className="truncate text-xs font-medium text-emerald-400">Active · Singleton Pattern</p>
              <p className="truncate text-xs text-slate-500">Shared across requests</p>
            </div>
          </div>
        </div>

        <div className="h-px bg-gradient-to-r from-transparent via-slate-700 to-transparent mx-4" />

        {/* Agents */}
        <div className="flex-1 px-4 py-4">
          <p className="mb-3 text-xs font-semibold tracking-widest text-slate-500 uppercase">
            Available Agents
          </p>
          <div className="space-y-2">
            {capabilities.map((capability) => (
              <details
                key={capability.title}
                className={`group rounded-xl border bg-gradient-to-br ${capability.cardColor} transition-all`}
              >
                <summary className="flex cursor-pointer select-none items-center gap-2 px-3 py-2.5 text-sm font-medium text-slate-200 list-none [&::-webkit-details-marker]:hidden">
                  <span className="text-base">{capability.icon}</span>
                  <span className="flex-1 truncate">{capability.title}</span>
                  <svg
                    className="h-3.5 w-3.5 flex-shrink-0 text-slate-400 transition-transform group-open:rotate-180"
                    fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
                  </svg>
                </summary>
                <ul className="space-y-1 px-4 pb-3 pt-1">
                  {capability.details.map((detail) => (
                    <li key={detail} className="flex items-center gap-1.5 text-xs text-slate-400">
                      <span className="h-1 w-1 flex-shrink-0 rounded-full bg-slate-600" />
                      {detail}
                    </li>
                  ))}
                </ul>
              </details>
            ))}
          </div>
        </div>

        <div className="h-px bg-gradient-to-r from-transparent via-slate-700 to-transparent mx-4" />

        {/* Footer controls */}
        <div className="px-4 py-4 space-y-3">
          {/* Routing toggle */}
          <div className="flex items-center justify-between rounded-xl border border-slate-700/50 bg-surface-800/50 px-3 py-2.5">
            <div className="flex items-center gap-2 min-w-0">
              <span className="text-sm flex-shrink-0">⚙️</span>
              <span className="truncate text-xs font-medium text-slate-300">Show routing info</span>
            </div>
            <button
              type="button"
              role="switch"
              aria-checked={showRoutingInfo}
              onClick={() => onToggleRoutingInfo(!showRoutingInfo)}
              className={`relative ml-2 inline-flex h-5 w-9 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors focus:outline-none ${
                showRoutingInfo ? "bg-brand-500" : "bg-slate-700"
              }`}
            >
              <span
                className={`pointer-events-none inline-block h-4 w-4 transform rounded-full bg-white shadow transition-transform ${
                  showRoutingInfo ? "translate-x-4" : "translate-x-0"
                }`}
              />
            </button>
          </div>

          {/* Clear button */}
          <button
            type="button"
            onClick={onClearChat}
            className="group flex w-full items-center justify-center gap-2 rounded-xl border border-red-500/20 bg-red-500/10 px-4 py-2.5 text-sm font-medium text-red-400 transition-all hover:bg-red-500/20 hover:text-red-300 hover:border-red-500/40"
          >
            <svg className="h-4 w-4 flex-shrink-0 transition-transform group-hover:rotate-12" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Clear Chat History
          </button>
        </div>
      </div>
    </aside>
  );
}
