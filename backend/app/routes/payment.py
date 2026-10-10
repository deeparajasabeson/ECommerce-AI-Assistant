from typing import Optional
from fastapi import APIRouter, Depends, HTTPException

from app.data.order_repository import OrderRepository
from app.data.repositories import get_order_repo
from app.models.payment import ProcessPaymentRequest

router = APIRouter(
    prefix="/payments",
    tags=["payments"]
)

@router.post("/process")
def process_payment(
    request: ProcessPaymentRequest,
    repo: OrderRepository = Depends(get_order_repo),
):
    """
    Record payment information (mock - COD only).
    """
    if not repo.get(request.order_id):
        raise HTTPException(
            status_code=404, 
            detail="Order not found")
    return {
        "message": "Payment information recorded",
        "payment_method": "Cash On Delivery (COD)",
        "order_id": request.order_id,
        "amount": request.amount,
        "status": "pending",
        "note": (
            "Payment will be collected upon delivery."
            "This is a mock API -- actual payments are handled offline."
        ),
    }

@router.post("/{payment_id}/refund")
def refund_payment(
    payment_id: str,
    amount: Optional[float] = None
):
    """
        Process a refund (mock).
    """
    return { 
        "message": "Refund processed successfully",
        "payment_id": payment_id,
        "refund_amount": amount or 0.0,
        "status": "refunded",
        "note": "This is a mock refund.  Actual refunds are handled through customer service.",
    }
