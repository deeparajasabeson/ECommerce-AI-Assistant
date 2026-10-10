"""
Tool schema definitions for E-Commerce agents.
Each constant is the JSON schema dict passed to the Azure AI Foundry agent.
"""

# ===== Product Agent Tools =====
SEARCH_PRODUCTS_TOOL = {
    "type": "function",
    "function": {
        "name": "search_products",
        "description": "Search for products by keyword or category in the e-commerce catalog",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query (product name or keyword)"
                },
                "category": {
                    "type": "string",
                    "description": "Filter by product category (optional)",
                    "enum": ["Electronics", "Sports", "Home", "Clothing"]
                }
            },
            "required": ["query"]
        }
    }
}

GET_PRODUCT_DETAILS_TOOL = {
    "type": "function",
    "function": {
        "name": "get_product_details",
        "description": "Get detailed information about a specific product",
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "string",
                    "description": "The unique product ID"
                }
            },
            "required": ["product_id"]
        }
    }
}

CHECK_INVENTORY_TOOL = {
    "type": "function",
    "function": {
        "name": "check_inventory",
        "description": "Check if a product is in stock and available",
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "string",
                    "description": "The product ID to check inventory for"
                }
            },
            "required": ["product_id"]
        }
    }
}

# ===== Order Agent Tools =====
GET_ORDER_STATUS_TOOL = {
    "type": "function",
    "function": {
        "name": "get_order_status",
        "description": "Get the current status and details of an order",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order ID to check"
                }
            },
            "required": ["order_id"]
        }
    }
}

CREATE_ORDER_TOOL = {
    "type": "function",
    "function": {
        "name": "create_order",
        "description": "Create a new order for a customer",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer ID placing the order"
                },
                "items": {
                    "type": "string",
                    "description": "JSON string of items array with product_id and quantity"
                },
                "total": {
                    "type": "number",
                    "description": "Total order amount"
                }
            },
            "required": ["customer_id", "items", "total"]
        }
    }
}

CANCEL_ORDER_TOOL = {
    "type": "function",
    "function": {
        "name": "cancel_order",
        "description": "Cancel an existing order",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order ID to cancel"
                }
            },
            "required": ["order_id"]
        }
    }
}

# ===== Shipping Agent Tools =====
GET_SHIPPING_RATES_TOOL = {
    "type": "function",
    "function": {
        "name": "get_shipping_rates",
        "description": "Get available shipping rates and delivery times for a shipment",
        "parameters": {
            "type": "object",
            "properties": {
                "postal_code": {
                    "type": "string",
                    "description": "Destination postal code"
                },
                "weight": {
                    "type": "number",
                    "description": "Package weight in pounds (default: 5.0)"
                }
            },
            "required": ["postal_code"]
        }
    }
}

TRACK_SHIPMENT_TOOL = {
    "type": "function",
    "function": {
        "name": "track_shipment",
        "description": "Track a shipment using tracking number",
        "parameters": {
            "type": "object",
            "properties": {
                "tracking_number": {
                    "type": "string",
                    "description": "The shipment tracking number"
                }
            },
            "required": ["tracking_number"]
        }
    }
}

# ===== Customer Agent Tools =====
GET_CUSTOMER_INFO_TOOL = {
    "type": "function",
    "function": {
        "name": "get_customer_info",
        "description": "Get customer account information",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer ID"
                }
            },
            "required": ["customer_id"]
        }
    }
}

GET_LOYALTY_POINTS_TOOL = {
    "type": "function",
    "function": {
        "name": "get_loyalty_points",
        "description": "Get customer loyalty points balance",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer ID"
                }
            },
            "required": ["customer_id"]
        }
    }
}

REDEEM_POINTS_TOOL = {
    "type": "function",
    "function": {
        "name": "redeem_points",
        "description": "Redeem loyalty points for discount",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer ID"
                },
                "points": {
                    "type": "integer",
                    "description": "Number of points to redeem"
                }
            },
            "required": ["customer_id", "points"]
        }
    }
}

# Note: Payment is handled offline/COD — no payment agent tool needed.
