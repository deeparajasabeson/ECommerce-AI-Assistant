import React, { FormEvent, KeyboardEvent, useRef } from "react";

type ChatInputProps = {
  prompt: string;
  canSend: boolean;
  disabled: boolean;
  onChange: (value: string) => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
};

export function ChatInput({ prompt, canSend, disabled, onChange, onSubmit }: ChatInputProps) {
  const formRef = useRef<HTMLFormElement>(null);

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (canSend) formRef.current?.requestSubmit();
    }
  }

  /** Grow the textarea to fit its content, up to the max-height set in CSS. */
  function handleResize(e: React.FormEvent<HTMLTextAreaElement>) {
    const el = e.currentTarget;
    el.style.height = "auto";
    el.style.height = `${el.scrollHeight}px`;
  }

  return (
    <form
      ref={formRef}
      onSubmit={onSubmit}
      className="relative flex items-end gap-2 rounded-2xl border border-slate-700/60 bg-surface-800 px-4 py-3 shadow-xl ring-1 ring-transparent transition-all focus-within:border-brand-500/50 focus-within:ring-brand-500/20"
    >
      <textarea
        rows={1}
        value={prompt}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        onInput={handleResize}
        placeholder="Ask about products, orders, shipping, or your account…"
        disabled={disabled}
        className="flex-1 resize-none bg-transparent text-sm text-slate-100 placeholder-slate-500 outline-none disabled:opacity-50"
        style={{ maxHeight: "8rem", overflowY: "auto" }}
      />

      <button
        type="submit"
        disabled={!canSend}
        title="Send (Enter)"
        className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-xl bg-brand-500 text-white shadow-md transition-all hover:bg-brand-600 disabled:cursor-not-allowed disabled:opacity-30 disabled:shadow-none"
      >
        <svg className="h-4 w-4 translate-x-px" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
        </svg>
      </button>
    </form>
  );
}
