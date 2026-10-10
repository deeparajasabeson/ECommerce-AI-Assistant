from typing import Optional
from pydantic import BaseModel

class Product(BaseModel):
    """The model representing a product."""
    id: str
    name: str
    category: str
    price: float
    description: str
    in_stock: bool
    stock_quantity: int
    rating: float
    image_url: Optional[str] = None