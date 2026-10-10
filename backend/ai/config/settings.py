"""
Configuration for E-Commerce Multi-Agent System
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Azure AI Foundry Configuration
AZURE_AI_FOUNDRY_ENDPOINT = os.getenv("AZURE_AI_FOUNDRY_ENDPOINT")
AZURE_AI_MODEL_DEPLOYMENT = os.getenv("AZURE_AI_MODEL_DEPLOYMENT", "gpt-5-mini")

# E-Commerce API Endpoints (local server on port 8000)
ECOMMERCE_API_BASE_URL = os.getenv("ECOMMERCE_API_BASE_URL", "http://localhost:8000")
ORDERS_API_URL = f"{ECOMMERCE_API_BASE_URL}/orders"
PRODUCTS_API_URL = f"{ECOMMERCE_API_BASE_URL}/products"
SHIPPING_API_URL = f"{ECOMMERCE_API_BASE_URL}/shipping"
PAYMENTS_API_URL = f"{ECOMMERCE_API_BASE_URL}/payments"
CUSTOMERS_API_URL = f"{ECOMMERCE_API_BASE_URL}/customers"

# API Authentication (if needed)
API_KEY = os.getenv("ECOMMERCE_API_KEY", "mock-api-key")
API_HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
