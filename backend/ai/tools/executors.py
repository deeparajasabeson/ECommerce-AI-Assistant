"""
Callable tool executors for E-Commerce agents.

Provides synchronous wrapper functions around the async API client so they can
be registered with Azure AI Foundry's FunctionTool, which calls tools
synchronously during a run.

Each function corresponds to one tool the agents can invoke.  The _run_async
helper bridges the sync/async boundary safely even when called from a thread
that is itself running inside an async executor.
"""
import asyncio
import json
import concurrent.futures
from typing import Dict, Set, Callable

from .api_client import api_client


def _run_async(coro):
    """Run an async coroutine from a synchronous context.

    The FunctionTool callbacks are called synchronously by the SDK, but they
    need to call async httpx methods.  This helper detects whether an event
    loop is already running in the current thread:

    - Loop running → spawn a fresh thread with its own loop (avoids blocking
      the existing loop and prevents a nested-loop RuntimeError).
    - No loop → use asyncio.run() directly (simplest path, e.g. in tests).
    """
    try:
        asyncio.get_running_loop()
        # Already inside an async context; run the coroutine in a separate
        # thread that owns its own fresh event loop.
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(asyncio.run, coro)
            return future.result()
    except RuntimeError:
        # No running loop in this thread — safe to create one.
        return asyncio.run(coro)


# ---------------------------------------------------------------------------
# Product tools
# ---------------------------------------------------------------------------

def search_products(query: str, category: str = None) -> str:
    """
    Search for products by keyword or category in the e-commerce catalog.

    :param query: Search query (product name or keyword)
    :param category: Filter by product category (optional). Values: Electronics, Sports, Home, Clothing
    :return: JSON string of matching products
    """
    result = _run_async(api_client.search_products(query=query, category=category))
    return json.dumps(result, indent=2)


def get_product_details(product_id: str) -> str:
    """
    Get detailed information about a specific product.

    :param product_id: The unique product ID (e.g. PROD-001)
    :return: JSON string of product details, or a not-found message
    """
    result = _run_async(api_client.get_product_details(product_id))
    return json.dumps(result, indent=2) if result else "Product not found"


def check_inventory(product_id: str) -> str:
    """
    Check whether a product is in stock and how many units are available.

    :param product_id: The product ID to check inventory for
    :return: JSON string with available flag, stock count, and availability label
    """
    result = _run_async(api_client.check_inventory(product_id))
    return json.dumps(result, indent=2)


# ---------------------------------------------------------------------------
# Order tools
# ---------------------------------------------------------------------------

def get_order_status(order_id: str) -> str:
    """
    Get the current status and full details of an order.

    :param order_id: The order ID to check (e.g. ORD-001)
    :return: JSON string of order details, or a not-found message
    """
    result = _run_async(api_client.get_order_status(order_id))
    return json.dumps(result, indent=2) if result else "Order not found"


def create_order(customer_id: str, items: str, total: float) -> str:
    """
    Place a new order for a customer.

    :param customer_id: The customer ID placing the order
    :param items: JSON string array of {product_id, quantity} objects
    :param total: Total order amount
    :return: JSON string of the created order
    """
    items_list = json.loads(items) if isinstance(items, str) else items
    result = _run_async(api_client.create_order(customer_id=customer_id, items=items_list, total=total))
    return json.dumps(result, indent=2)


def cancel_order(order_id: str) -> str:
    """
    Cancel an existing order.

    :param order_id: The order ID to cancel
    :return: JSON string with success flag and cancellation details
    """
    result = _run_async(api_client.cancel_order(order_id))
    return json.dumps(result, indent=2)


# ---------------------------------------------------------------------------
# Shipping tools
# ---------------------------------------------------------------------------

def get_shipping_rates(postal_code: str, weight: float = 5.0) -> str:
    """
    Get available shipping rates and estimated delivery times.

    :param postal_code: Destination postal code
    :param weight: Package weight in pounds (default: 5.0)
    :return: JSON string of shipping rate options
    """
    result = _run_async(api_client.get_shipping_rates(postal_code, weight))
    return json.dumps(result, indent=2)


def track_shipment(tracking_number: str) -> str:
    """
    Track a shipment and retrieve its event history.

    :param tracking_number: The shipment tracking number (e.g. SHP-001)
    :return: JSON string with current status, location, and event history
    """
    result = _run_async(api_client.track_shipment(tracking_number))
    return json.dumps(result, indent=2)


# ---------------------------------------------------------------------------
# Customer tools
# ---------------------------------------------------------------------------

def get_customer_info(customer_id: str) -> str:
    """
    Get customer account information and profile.

    :param customer_id: The customer ID (e.g. CUST-001)
    :return: JSON string of customer data, or a not-found message
    """
    result = _run_async(api_client.get_customer_info(customer_id))
    return json.dumps(result, indent=2) if result else "Customer not found"


def get_loyalty_points(customer_id: str) -> str:
    """
    Get a customer's loyalty points balance and tier.

    :param customer_id: The customer ID
    :return: JSON string with points, tier, and rewards value
    """
    result = _run_async(api_client.get_loyalty_points(customer_id))
    return json.dumps(result, indent=2)


def redeem_points(customer_id: str, points: int) -> str:
    """
    Redeem loyalty points for a discount on a future order.

    :param customer_id: The customer ID
    :param points: Number of points to redeem
    :return: JSON string with redemption result and remaining balance
    """
    result = _run_async(api_client.redeem_points(customer_id=customer_id, points=points))
    return json.dumps(result, indent=2)


# ---------------------------------------------------------------------------
# Function registry — maps tool name strings to callables
# ---------------------------------------------------------------------------

# Used by get_callable_functions() to look up the right function when building
# a FunctionTool set for an agent.
CALLABLE_FUNCTIONS: Dict[str, Callable] = {
    "search_products": search_products,
    "get_product_details": get_product_details,
    "check_inventory": check_inventory,
    "get_order_status": get_order_status,
    "create_order": create_order,
    "cancel_order": cancel_order,
    "get_shipping_rates": get_shipping_rates,
    "track_shipment": track_shipment,
    "get_customer_info": get_customer_info,
    "get_loyalty_points": get_loyalty_points,
    "redeem_points": redeem_points,
}


def get_callable_functions(tool_names: list) -> Set[Callable]:
    """Return the set of callable functions matching the given tool name strings.

    Called by FoundryBaseAgent.initialize() to build the FunctionTool set that
    the SDK registers with the agent.  Unknown names are silently ignored.

    :param tool_names: List of function name strings declared in the agent's tool spec
    :return: Set of matching callable functions
    """
    return {CALLABLE_FUNCTIONS[name] for name in tool_names if name in CALLABLE_FUNCTIONS}
