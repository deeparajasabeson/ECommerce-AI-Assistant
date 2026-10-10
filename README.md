# ECommerce-AI-Assistant
This is a chat-based e-commerce assistant. The React frontend sends a customer’s message to a FastAPI backend, where an Azure AI Foundry orchestrator routes it to a specialist agent. Those agents can call the backend’s REST endpoints to retrieve or update store data in PostgreSQL.

<img width="756" height="444" alt="image" src="https://github.com/user-attachments/assets/e3d613c9-7cc7-4ffc-a979-1498cd61f83f" />
<img width="1248" height="321" alt="image" src="https://github.com/user-attachments/assets/7acc236e-33f4-44f0-bb4b-96e5a2e891ea" />

Frontend
The UI is a single-page chat app built with React, TypeScript, and Vite. App.tsx manages the prompt, message history, loading and error states, and sidebar controls. ChatMessages.tsx renders the conversation, routing labels, typing indicator, and starter prompts.

chatService.ts sends { query } to POST /chat, using VITE_API_BASE_URL or http://localhost:8000 by default. It expects { response, agent } and surfaces API errors to the UI. The frontend sends only the current query, not prior messages, so conversation history is displayed in the browser but isn’t provided to the backend as context.
<img width="3822" height="2295" alt="image" src="https://github.com/user-attachments/assets/0b5e6f24-45d4-4040-80b8-5aa116c3edf3" />

Backend and AI
main.py starts the FastAPI app, configures CORS, initializes the database pool, and registers REST routers for products, orders, shipping, customers, payments, and chat. The /health and / endpoints provide basic service information.
The chat route validates the query and calls orchestrator_service.py. That service lazily initializes a shared Azure AI Foundry orchestrator using AZURE_AI_FOUNDRY_ENDPOINT and AZURE_AI_MODEL_DEPLOYMENT (defaulting to gpt-5-mini). The orchestrator classifies the request and routes it to a Product, Order, Shipping, or Customer agent. Azure authentication uses DefaultAzureCredential.

Agents use callable tools from executors.py. Those tools call the backend REST API through an async HTTP client, api_client.py; the synchronous tool callbacks bridge to the async calls. FastAPI routes use repositories and a pooled PostgreSQL connection. schema.sql defines products, customers, orders and order items, shipping rates, and shipment tracking data.

Payment-related pieces are more limited: the router and API client exist, but chat payment questions are currently answered with a fixed Cash on Delivery explanation rather than routed to a dedicated payment agent.

In short: the frontend is the customer-facing chat interface; the backend combines the chat API, AI routing, store REST APIs, and database access.
<img width="2637" height="1551" alt="image" src="https://github.com/user-attachments/assets/02f1d52b-969c-4aff-9cee-97743abd2207" />
<img width="2598" height="1809" alt="image" src="https://github.com/user-attachments/assets/6ae6cd0d-4105-473c-993a-0ea766b8aa89" />
<img width="3801" height="2136" alt="image" src="https://github.com/user-attachments/assets/91688a86-6e41-4843-9f55-8ab9d33f5e4e" />
<img width="3807" height="1830" alt="image" src="https://github.com/user-attachments/assets/6fb41a0c-6763-43c2-8f10-bf5ca77b4544" />
<img width="237" height="759" alt="image" src="https://github.com/user-attachments/assets/ebab312c-939a-4b97-a69f-c399689b5d59" />
<img width="741" height="1029" alt="image" src="https://github.com/user-attachments/assets/610fa845-199d-4bfd-81a7-c46445de7f56" />
<img width="756" height="954" alt="image" src="https://github.com/user-attachments/assets/cb22f953-4459-4f3f-8d8d-430b45b89d70" />
<img width="870" height="816" alt="image" src="https://github.com/user-attachments/assets/d51b3eb7-b5c9-4069-b557-3c484519f0c2" />
<img width="633" height="885" alt="image" src="https://github.com/user-attachments/assets/02e585c0-bffe-4d4f-9d04-dc8625c3f9d7" />




