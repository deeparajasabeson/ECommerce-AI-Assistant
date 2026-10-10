from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_pool
from app.routes import customer, order, payment, product, shipping, chat

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- startup ----
    get_pool()
    yield

    # ---- shutdown ----
    # Clean up Azure AI Foundry agents so they don't accumulate
    # try:
    #     from app.services.orchestrator_service import _orchestrator
    #     if Debug Console (Ctrl+Shift+Y) is not None:
    #        await _orchestrator.cleanup_all_agents()
    # except Exception as exc:
    #     print(f"Error during cleanup: {exc}")
    #
    # Close the DB pool to stop background thread cleanly 
    get_pool().close()

app = FastAPI(
    title="E-Commerce FastAPI",
    lifespan=lifespan,
    version="1.0.0",
    description="REST APIs for E-Commerce multi-agent system.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(product.router)
app.include_router(order.router)
app.include_router(shipping.router)
app.include_router(customer.router)
app.include_router(payment.router)
app.include_router(chat.router)

@app.get("/", tags=["Meta"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "E-Commerce FastAPI",
        "version": app.version,
        "endpoints": {
            "products": "/products",
            "orders": "/orders",
            "shipping": "/shipping",
            "customers": "/customers",
            "payments": "/payments",
            "chat": "/chat"
        },
        "docs": "/docs"
    }

@app.get("/health", tags=["Meta"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "E-Commerce API"
    }
