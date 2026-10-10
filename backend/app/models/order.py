from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

class OrderItemInput(BaseModel):
    """A single line item as supplied by the client when creating an order.
    
    Only product_id and quantity are accepted from the caller; name and price
    are resolved server-side from the product catalogue.
    """
    product_id: str
    quantity: int = Field(default=1, ge=1)

class OrderItem(BaseModel):
    """A fully resolved line item stored in and returned from the database."""
    model_config = ConfigDict(from_attributes=True)

    product_id: str
    product_name: str
    quantity: int = Field(default=1, ge=1)
    price: float

class ShippingAddress(BaseModel):
    """A shipping address associated with an order."""
    model_config = ConfigDict(from_attributes=True)

    street: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"

class Order(BaseModel):
    """A complete order, including line items and shipping address."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    customer_id: str
    items: List[OrderItem]
    total_amount: float
    status: str
    shipping_address: ShippingAddress
    tracking_number: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class CreateOrderRequest(BaseModel):
    """The request body for creating a new order."""
    customer_id: str
    items: List[OrderItemInput]
    shipping_address: ShippingAddress