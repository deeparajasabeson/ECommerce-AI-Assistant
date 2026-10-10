from pydantic import BaseModel

class ProcessPaymentRequest(BaseModel):
    """The request body for processing a payment."""
    order_id: str
    payment_method: str
    amount: float