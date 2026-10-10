import type { AgentCapability } from "../types/chat";

export const agentCapabilities: AgentCapability[] = [
  {
    title: "Product Agent",
    icon: "🛒",
    cardColor: "from-violet-500/20 to-purple-500/20 border-violet-500/30",
    badgeColor: "bg-violet-500/15 hover:bg-violet-500/30 border-violet-500/20",
    details: ["Search products", "Get product details", "Check inventory", "Price information"],
  },
  {
    title: "Order Agent",
    icon: "📦",
    cardColor: "from-amber-500/20 to-orange-500/20 border-amber-500/30",
    badgeColor: "bg-amber-500/15 hover:bg-amber-500/30 border-amber-500/20",
    details: ["Check order status", "Create new orders", "Cancel orders", "Order history"],
  },
  {
    title: "Shipping Agent",
    icon: "🚚",
    cardColor: "from-sky-500/20 to-cyan-500/20 border-sky-500/30",
    badgeColor: "bg-sky-500/15 hover:bg-sky-500/30 border-sky-500/20",
    details: ["Track shipments", "Get shipping rates", "Delivery estimates", "Carrier information"],
  },
  {
    title: "Customer Agent",
    icon: "👤",
    cardColor: "from-emerald-500/20 to-teal-500/20 border-emerald-500/30",
    badgeColor: "bg-emerald-500/15 hover:bg-emerald-500/30 border-emerald-500/20",
    details: ["Account information", "Loyalty points", "Redeem rewards", "Customer profile"],
  },
];
