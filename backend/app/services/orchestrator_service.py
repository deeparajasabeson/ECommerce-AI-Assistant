import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

_project_root = Path(__file__).resolve().parents[3]
_ai_dir = _project_root / "ai"

# Add ai/ to sys.path so its packages are importable from here.
if str(_ai_dir) not in sys.path:
    sys.path.insert(0, str(_ai_dir))

# Load .env files in priority order: project root first, then ai/.
# Variables set earlier take precedence (load_dotenv doesn't overwrite by default).
for _dotenv_path in [_project_root / ".env", _ai_dir / ".env"]:
    if _dotenv_path.exists():
        load_dotenv(_dotenv_path)

from ai.agents import CustomerAgent, OrderAgent, ProductAgent, ShippingAgent
from ai.orchestrator import IntelligentOrchestrator

_orchestrator: IntelligentOrchestrator | None = None
_orchestrator_lock = asyncio.Lock()

# Maps each agent to the signal strings used to identify it in responses/queries.
_AGENT_LABELS: list[tuple[str, list[str], list[str]]] = [
    (
        "Product Agent 🛒",
        ["ProductAgent", "[Product Agent", "[ProductAgent"],
        ["product", "price", "stock", "inventory", "search"],
    ),
    (
        "Order Agent 📦",
        ["OrderAgent", "[Order Agent", "[OrderAgent"],
        ["order", "purchase", "buy", "cancel"],
    ),
    (
        "Shipping Agent 🚚",
        ["ShippingAgent", "[Shipping Agent", "[ShippingAgent"],
        ["shipping", "delivery", "ship", "track"],
    ),
    (
        "Customer Agent 👤",
        ["CustomerAgent", "[Customer Agent", "[CustomerAgent"],
        ["customer", "account", "loyalty", "points", "reward"],
    ),
]


def _read_orchestrator_config() -> tuple[str, str]:
    """Read Azure endpoint and model deployment from environment variables.

    Raises RuntimeError when the required endpoint is missing so the server
    fails fast with a clear message instead of a cryptic SDK error later.
    """
    endpoint = os.getenv("AZURE_AI_FOUNDRY_ENDPOINT")
    if not endpoint:
        raise RuntimeError(
            "AZURE_AI_FOUNDRY_ENDPOINT is not set. "
            "Set it as an environment variable or in .env "
            "(project root or ai/.env)."
        )
    model_deployment = os.getenv("AZURE_AI_MODEL_DEPLOYMENT", "gpt-5-mini")
    return endpoint, model_deployment


def detect_agent_name(query: str, response: str) -> str:
    """Identify which agent handled a query from the response text and query keywords.

    Checks response signals first (more reliable), then falls back to query keywords.
    Returns a human-readable label with emoji, e.g. "Product Agent 🛒".
    """
    query_lower = query.lower()
    for label, response_signals, query_signals in _AGENT_LABELS:
        if any(signal in response for signal in response_signals):
            return label
        if any(signal in query_lower for signal in query_signals):
            return label
    return "Multi-Agent System"


async def _build_and_initialize_orchestrator() -> IntelligentOrchestrator:
    """Instantiate all four agents and the routing agent, then start them."""
    project_endpoint, model_deployment = _read_orchestrator_config()
    agents = [
        ProductAgent(project_endpoint, model_deployment),
        OrderAgent(project_endpoint, model_deployment),
        ShippingAgent(project_endpoint, model_deployment),
        CustomerAgent(project_endpoint, model_deployment),
    ]
    orchestrator = IntelligentOrchestrator(
        agents,
        endpoint=project_endpoint,
        model=model_deployment,
        use_azure_ad=True,
    )
    await orchestrator.initialize_all_agents()
    return orchestrator


async def get_orchestrator() -> IntelligentOrchestrator:
    """Return the shared orchestrator singleton, creating it on first call.

    Uses an asyncio Lock for thread-safe lazy initialisation — the orchestrator
    is expensive to build (creates 5 Azure AI agents) so it's created once and
    reused for the lifetime of the server process.
    """
    global _orchestrator
    if _orchestrator is not None:
        return _orchestrator

    async with _orchestrator_lock:
        if _orchestrator is None:
            _orchestrator = await _build_and_initialize_orchestrator()
    return _orchestrator


async def route_user_query(query: str) -> tuple[str, str]:
    """Route a user query through the multi-agent system.

    Returns a (response_text, agent_label) tuple where agent_label is the
    human-readable name of the agent that handled the request.
    """
    orchestrator = await get_orchestrator()
    response = await orchestrator.route_query_with_collaboration(query)
    return response, detect_agent_name(query, response)
