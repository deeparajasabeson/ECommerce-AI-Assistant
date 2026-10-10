import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from app.data.order_repository import OrderRepository
from app.data.customer_repository import CustomerRepository
from app.data.product_repository import ProductRepository

from app.data.repositories import get_order_repo, get_customer_repo, get_product_repo
from app.models.order import CreateOrderRequest

router = APIRouter( 
    prefix="/orders",
    tags=["orders"]
)

@router.get("")
def list_orders(
    customer_id: Optional[str] = Query(None, description="Filter by customer ID"),
    status: Optional[str] = Query(None, description="Filter by order status"),
    limit: Optional[int] = Query(10, description="Maximum number of results"),
    repo: OrderRepository = Depends(get_order_repo)
):
    """
    List orders with optional filters.
    """
    results = repo.get_all(customer_id=customer_id, status=status, limit=limit)
    return {"count": len(results), "orders": results}


@router.get("/{order_id}")
def get_order(
    order_id: str,
    repo: OrderRepository = Depends(get_order_repo)
):
    """
    Get Order status and details.
    """
    order = repo.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("")
def create_order(
    request: CreateOrderRequest,
    repo: OrderRepository = Depends(get_order_repo),
    customer_repo: CustomerRepository = Depends(get_customer_repo),
    product_repo: ProductRepository = Depends(get_product_repo)
):
    """
    Create a new order.
    """
    customer = customer_repo.get(request.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    order_items: list[dict] = []
    total_amount = 0.0

    for item in request.items:
        product = product_repo.get(item.product_id)
        if not product:
            raise HTTPException(
                status_code=404, 
                detail=f"Product {item.product_id} not found"
            )
        if not product["in_stock"] or product["stock_quantity"] < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Product {item.product_id} not available in requested quantity", 
            )
        order_items.append(
            {
                "product_id": item.product_id,
                "product_name": product["name"],
                "quantity": item.quantity,
                "price": product["price"]
            }
        )
        total_amount += product["price"] * item.quantity
    
    new_order = order_repo.create(
        order_id=order_id,
        customer_id=request.cutomer_id,
        items=order_items,
        total_amount=round(total_amount, 2),
        shipping_address=request.shipping_address.model_dump(),
    )
    return {"message": "Order created successfully", "order": new_order}

@router.post("/{order_id}/cancel")
def cancel_order(
    order_id: str,
    reason: Optional[str] = None,
    repo: OrderRepository = Depends(get_order_repo)
):
    """
    Cancel an existing order.
    """
    order = repo.get(order_id)
    if not order:
        raise HTTPException(
            status_code=404, 
            detail="Order not found"
        )
    if order["status"] in {"shipped", "delivered", "cancelled"}:
        raise HTTPException(
            status_code=400, 
            detail="Can not cancel order with status: {order['status']}",
        )

    repo.update_status(order_id, "cancelled")
    return{
        "message": "Order cancelled successfully",
        "order_id": order_id,
        "status": "cancelled",
        "reason": reason or "Customer request",       
    }
