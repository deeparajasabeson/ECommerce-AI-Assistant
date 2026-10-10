"""
Product Agent - Handles product search, details, and inventory
"""
from .base import FoundryBaseAgent
from ai.tools.definitions import (
    SEARCH_PRODUCTS_TOOL,
    GET_PRODUCT_DETAILS_TOOL,
    CHECK_INVENTORY_TOOL
)


class ProductAgent(FoundryBaseAgent):
    """Agent specialized in product catalog operations"""

    def __init__(self, project_endpoint: str, model_deployment: str):
        instructions = """You are a Product Specialist for an e-commerce platform.
        
Your responsibilities:
- Help customers search for products in our catalog
- Provide detailed product information including prices, descriptions, and specifications
- Check product availability and inventory status
- Recommend similar or alternative products when needed

Use the available tools to access real-time product data from our API.
Be helpful, accurate, and provide complete information.
If a product is out of stock, suggest alternatives if possible."""

        tools = [
            SEARCH_PRODUCTS_TOOL,
            GET_PRODUCT_DETAILS_TOOL,
            CHECK_INVENTORY_TOOL
        ]

        super().__init__(
            name="ProductAgent",
            instructions=instructions,
            tools=tools,
            project_endpoint=project_endpoint,
            model_deployment=model_deployment
        )
