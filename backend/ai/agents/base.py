"""
Base Agent Class for the E-Commerce Multi-Agent System.

Every specialised agent (Product, Order, Shipping, Customer) extends
FoundryBaseAgent.  The class handles:
  - One-time creation of an Azure AI Foundry agent via the SDK
  - Automatic deletion of any stale agent with the same name on startup
    (prevents agent accumulation in the portal across server restarts)
  - Thread-safe, non-blocking execution via run_in_executor so the
    synchronous SDK call never blocks the uvicorn async event loop
  - Cleanup (deletion) on graceful shutdown
"""
import asyncio
import json
from typing import List, Dict, Optional
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import AgentThreadCreationOptions, ThreadMessageOptions, ToolSet, FunctionTool, MessageRole
from azure.identity import DefaultAzureCredential
from ai.tools.executors import get_callable_functions


class FoundryBaseAgent:
    """Base class for all Azure AI Foundry agents in this system."""

    def __init__(self, name: str, instructions: str, tools: List[Dict], project_endpoint: str, model_deployment: str):
        self.name = name
        self.instructions = instructions
        self.tools = tools
        self.project_endpoint = project_endpoint
        self.model_deployment = model_deployment
        self.agent_id = None        # Set after successful initialize()
        self.agents_client = None   # Azure AI Foundry SDK client
        self.toolset = None         # FunctionTool registry used by the SDK

    async def initialize(self):
        """Create this agent in Azure AI Foundry.

        Before creating, any existing agent with the same name is deleted so
        server hot-reloads never leave stale agents in the portal.
        Raises an exception if the Foundry call fails.
        """
        try:
            credential = DefaultAzureCredential()
            self.agents_client = AgentsClient(
                endpoint=self.project_endpoint,
                credential=credential
            )

            # Delete stale agents from previous runs that share this name.
            try:
                for existing in self.agents_client.list_agents():
                    if existing.name == self.name:
                        self.agents_client.delete_agent(agent_id=existing.id)
            except Exception:
                pass  # Non-fatal — proceed to create even if list/delete fails.

            # Build the FunctionTool registry from this agent's declared tool names.
            tool_names = [t["function"]["name"] for t in self.tools if t.get("type") == "function"]
            callable_funcs = get_callable_functions(tool_names)

            if callable_funcs:
                self.toolset = ToolSet()
                self.toolset.add(FunctionTool(callable_funcs))
                # Enable automatic tool-call dispatch inside the SDK run loop.
                self.agents_client.enable_auto_function_calls(self.toolset)

            agent = self.agents_client.create_agent(
                model=self.model_deployment,
                name=self.name,
                instructions=self.instructions,
                tools=self.toolset.definitions if self.toolset else None
            )
            self.agent_id = agent.id
            print(f"✓ Agent '{self.name}' initialized (ID: {self.agent_id})")

        except Exception as e:
            raise Exception(f"Failed to initialize agent '{self.name}': {str(e)}")

    def _run_sync(self, message: str):
        """Blocking SDK call that creates a thread, posts the message, and
        processes the run (including any auto-dispatched tool calls) to
        completion.

        This method is intended to run inside a ThreadPoolExecutor (see
        ``run()`` below) — never call it directly from async code.
        """
        return self.agents_client.create_thread_and_process_run(
            agent_id=self.agent_id,
            thread=AgentThreadCreationOptions(
                messages=[ThreadMessageOptions(role="user", content=message)]
            ),
            toolset=self.toolset,
        )

    async def run(self, message: str) -> str:
        """Send a message to this agent and return its text response.

        Why run_in_executor?
        ``create_thread_and_process_run`` is a synchronous blocking SDK call.
        When the agent's tools make HTTP callbacks back to the same FastAPI
        server (e.g. GET /products/PROD-001), those requests must be served
        by the uvicorn event loop.  Calling the blocking SDK method directly
        on the event-loop thread would deadlock the server — the loop is
        blocked waiting for the SDK, but the SDK is waiting for HTTP responses
        that the blocked loop can't serve.

        Offloading to a thread pool keeps the event loop free to handle the
        incoming tool-call HTTP requests.
        """
        if not self.agent_id:
            await self.initialize()

        try:
            loop = asyncio.get_running_loop()
            run = await loop.run_in_executor(None, self._run_sync, message)

            if run.status == "completed":
                # The SDK returns messages newest-first; the first assistant
                # message is the final response.
                messages = self.agents_client.messages.list(thread_id=run.thread_id)
                for msg in messages:
                    if msg.role == "assistant":
                        for content_item in msg.content:
                            if hasattr(content_item, 'text'):
                                return content_item.text.value

            return f"Agent completed with status: {run.status}"

        except Exception as e:
            return f"Error in agent '{self.name}': {str(e)}"

    async def cleanup(self):
        """Delete this agent from Azure AI Foundry and reset local state.

        Called during graceful shutdown so agents don't accumulate in the
        portal across server restarts.
        """
        if self.agent_id and self.agents_client:
            try:
                self.agents_client.delete_agent(agent_id=self.agent_id)
                self.agent_id = None
                print(f"✓ Agent '{self.name}' deleted")
            except Exception as e:
                print(f"✗ Failed to delete agent '{self.name}': {e}")
