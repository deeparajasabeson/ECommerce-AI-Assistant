export type Role = "user" | "assistant";

export type ChatMessage = {
  role: Role;
  content: string;
  agent?: string;
};

export type ChatApiResponse = {
  response: string;
  agent: string;
};

export type ChatErrorPayload = {
  detail?: string;
};

export type AgentCapability = {
  title: string;
  details: string[];
  /** Emoji icon shown in both expanded and collapsed sidebar views */
  icon: string;
  /** Tailwind gradient + border classes for the expanded agent card */
  cardColor: string;
  /** Tailwind bg + hover + border classes for the collapsed icon button */
  badgeColor: string;
};
