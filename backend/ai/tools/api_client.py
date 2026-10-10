"""
E-Commerce API Client
Simple, async HTTP client using httpx for all API operations.
"""
import httpx
from typing import Dict, List, Optional

try:
    from config import (
        ORDERS_API_URL,
        PRODUCTS_API_URL,
        SHIPPING_API_URL,
        PAYMENTS_API_URL,
        CUSTOMERS_API_URL,
        API_HEADERS
    )
except ImportError:
    ORDERS_API_URL = "http://localhost:8000/orders"
    PRODUCTS_API_URL = "http://localhost:8000/products"
    SHIPPING_API_URL = "http://localhost:8000/shipping"
    PAYMENTS_API_URL = "http://localhost:8000/payments"
    CUSTOMERS_API_URL = "http://localhost:8000/customers"
    API_HEADERS = {"Content-Type": "application/json"}


class ECommerceAPIClient:
    """
    Async HTTP client for the e-commerce API.
    Uses httpx for automatic connection pooling and HTTP/2 support.
    """

    def __init__(self, timeout: float = 30.0):
        self.timeout = timeout

    async def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                return await client.request(method, url, headers=API_HEADERS, **kwargs)
            except httpx.RequestError as e:
                print(f"Request error: {e}")
                raise

    # ===== Product APIs =====
    async def search_products(self, query: str, category: Optional[str] = None) -> List[Dict]:
        """Search products by name or category. GET /products/search?q={query}&category={category}"""
        params = {"q": query}
        if category:
            params["category"] = category
        try:
            response = await self._request("GET", f"{PRODUCTS_API_URL}/search", params=params)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return []
            else:
                print(f"API Error: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error searching products: {e}")
            return []

    async def get_product_details(self, product_id: str) -> Optional[Dict]:
        """Get detailed product information. GET /products/{product_id}"""
        try:
            response = await self._request("GET", f"{PRODUCTS_API_URL}/{product_id}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                print(f"API Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error getting product details: {e}")
            return None

    async def check_inventory(self, product_id: str) -> Dict:
        """Check inventory availability. GET /products/{product_id}/inventory"""
        try:
            response = await self._request("GET", f"{PRODUCTS_API_URL}/{product_id}/inventory")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return {"available": False, "stock": 0, "product_id": product_id, "message": "Product not found"}
            else:
                print(f"API Error: {response.status_code}")
                return {"available": False, "stock": 0, "message": "API error"}
        except Exception as e:
            print(f"Error checking inventory: {e}")
            return {"available": False, "stock": 0, "message": str(e)}

    # ===== Order APIs =====
    async def get_order_status(self, order_id: str) -> Optional[Dict]:
        """Get order status and details. GET /orders/{order_id}"""
        try:
            response = await self._request("GET", f"{ORDERS_API_URL}/{order_id}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                print(f"API Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error getting order status: {e}")
            return None

    async def create_order(self, customer_id: str, items: List[Dict], total: float) -> Dict:
        """Create a new order. POST /orders"""
        payload = {"customer_id": customer_id, "items": items, "total": total}
        try:
            response = await self._request("POST", ORDERS_API_URL, json=payload)
            if response.status_code in [200, 201]:
                return response.json()
            else:
                error_text = response.text
                print(f"API Error: {response.status_code} - {error_text}")
                return {"success": False, "message": f"Failed to create order: {error_text}"}
        except Exception as e:
            print(f"Error creating order: {e}")
            return {"success": False, "message": str(e)}

    async def cancel_order(self, order_id: str) -> Dict:
        """Cancel an order. POST /orders/{order_id}/cancel"""
        try:
            response = await self._request("POST", f"{ORDERS_API_URL}/{order_id}/cancel")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return {"success": False, "message": "Order not found"}
            elif response.status_code == 400:
                error_data = response.json()
                return {"success": False, "message": error_data.get("message", "Cannot cancel order")}
            else:
                print(f"API Error: {response.status_code}")
                return {"success": False, "message": "API error"}
        except Exception as e:
            print(f"Error cancelling order: {e}")
            return {"success": False, "message": str(e)}

    # ===== Shipping APIs =====
    async def get_shipping_rates(self, postal_code: str, weight: float = 5.0) -> Dict:
        """Get available shipping rates. GET /shipping/rates?zip_code={postal_code}&weight={weight}"""
        try:
            response = await self._request(
                "GET",
                f"{SHIPPING_API_URL}/rates",
                params={"zip_code": postal_code, "weight": weight}
            )
            if response.status_code == 200:
                return response.json().get("rates", {})
            else:
                print(f"API Error: {response.status_code}")
                return {
                    "standard": {"cost": 5.99, "days": "5-7"},
                    "express": {"cost": 15.99, "days": "2-3"},
                    "overnight": {"cost": 29.99, "days": "1"},
                }
        except Exception as e:
            print(f"Error getting shipping rates: {e}")
            return {
                "standard": {"cost": 5.99, "days": "5-7"},
                "express": {"cost": 15.99, "days": "2-3"},
            }

    async def track_shipment(self, tracking_number: str) -> Dict:
        """Track a shipment. GET /shipping/track/{tracking_number}"""
        try:
            response = await self._request("GET", f"{SHIPPING_API_URL}/track/{tracking_number}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return {"tracking_number": tracking_number, "status": "not_found", "message": "Tracking number not found"}
            else:
                print(f"API Error: {response.status_code}")
                return {"tracking_number": tracking_number, "status": "error", "message": "Unable to track shipment"}
        except Exception as e:
            print(f"Error tracking shipment: {e}")
            return {"tracking_number": tracking_number, "status": "error", "message": str(e)}

    # ===== Customer APIs =====
    async def get_customer_info(self, customer_id: str) -> Optional[Dict]:
        """Get customer information. GET /customers/{customer_id}"""
        try:
            response = await self._request("GET", f"{CUSTOMERS_API_URL}/{customer_id}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                print(f"API Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error getting customer info: {e}")
            return None

    async def get_loyalty_points(self, customer_id: str) -> Dict:
        """Get customer loyalty points. GET /customers/{customer_id}/loyalty"""
        try:
            response = await self._request("GET", f"{CUSTOMERS_API_URL}/{customer_id}/loyalty")
            if response.status_code == 200:
                data = response.json()
                data["found"] = True
                return data
            elif response.status_code == 404:
                return {"customer_id": customer_id, "points": 0, "tier": "None", "found": False}
            else:
                print(f"API Error: {response.status_code}")
                return {"customer_id": customer_id, "points": 0, "tier": "Unknown", "found": False}
        except Exception as e:
            print(f"Error getting loyalty points: {e}")
            return {"customer_id": customer_id, "points": 0, "tier": "Error", "found": False}

    async def redeem_points(self, customer_id: str, points: int) -> Dict:
        """Redeem loyalty points. POST /customers/{customer_id}/loyalty/redeem"""
        payload = {"points": points}
        try:
            response = await self._request(
                "POST",
                f"{CUSTOMERS_API_URL}/{customer_id}/loyalty/redeem",
                json=payload
            )
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                error_data = response.json()
                return {"success": False, "message": error_data.get("message", "Insufficient points")}
            elif response.status_code == 404:
                return {"success": False, "message": "Customer not found"}
            else:
                print(f"API Error: {response.status_code}")
                return {"success": False, "message": "API error"}
        except Exception as e:
            print(f"Error redeeming points: {e}")
            return {"success": False, "message": str(e)}

    # ===== Payment APIs =====
    async def process_payment(self, order_id: str, payment_method: str, amount: float) -> Dict:
        """Process payment for an order. POST /payments/process"""
        payload = {"order_id": order_id, "payment_method": payment_method, "amount": amount, "currency": "USD"}
        try:
            response = await self._request("POST", f"{PAYMENTS_API_URL}/process", json=payload)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                error_data = response.json()
                return {"success": False, "message": error_data.get("message", "Payment failed"), "order_id": order_id}
            else:
                print(f"API Error: {response.status_code}")
                return {"success": False, "message": "Payment processing error", "order_id": order_id}
        except Exception as e:
            print(f"Error processing payment: {e}")
            return {"success": False, "message": str(e), "order_id": order_id}


api_client = ECommerceAPIClient()
