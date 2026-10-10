from fastapi import APIRouter, Depends, HTTPException
from app.data.customer_repository import CustomerRepository
from app.data.repositories import get_customer_repo
from app.models.customer import RedeemPointsRequest
from app.models import customer
from pydantic import BaseModel

router = APIRouter(
    prefix="/customers",
    tags=["customers"]
)

_LOYALTY_TIERS = [(2000, "Gold"), (1000, "Silver"), (500, "Bronze")]

def _get_loyalty_tier(points: int) -> str:
    for threshold, tier in _LOYALTY_TIERS:
        if points >= threshold:
            return tier
    return "Bronze"

@router.get("/{customer_id}")
def get_customer(
    customer_id: str,
    repo: CustomerRepository = Depends(get_customer_repo)
):
    """
    Get customer account information.
    """
    customer = repo.get(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")    
    return customer

@router.get("/{customer_id}/loyalty")
def get_loyalty_points(
    customer_id: str,
    repo: CustomerRepository = Depends(get_customer_repo)
):
    """
    Get Customer loyalty points balance.
    """
    customer = repo.get(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    tier = _get_loyalty_tier(customer["loyalty_points"])
    points_to_next = (
        max(0, 1000 - (customer["loyalty_points"] % 1000))
        if customer["loyalty_points"] < 2000
        else 0
    )
    return {
        "customer_id": customer_id,
        "customer_name": customer["name"],
        "loyalty_points": customer["loyalty_points"],
        "tier": tier,
        "points_to_next_tier": points_to_next,
        "rewards_value": round(customer["loyalty_points"] * 0.01, 2),
    }

@router.post("/{customer_id}/redeem")
def redeem_loyalty_points(
    customer_id: str,
    request: RedeemPointsRequest,
    repo: CustomerRepository = Depends(get_customer_repo)
):
    """Redeem customer loyalty points."""
    customer = repo.get(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    points = request.points

    if points <= 0:
        raise HTTPException(status_code=400, detail="Points to redeem must be greater than zero")

    if customer["loyalty_points"] < points:
        raise HTTPException(
            status_code=400, 
            detail=(
                   f"Insufficient points."
                   f"Available: {customer['loyalty_points']}, Requested: {points}"
            ),
        )

    new_balance = customer["loyalty_points"] - points
    repo.update_loyalty_points(customer_id, new_balance)

    return {
        "message": "Points redeemed successfully",
        "customer_id": customer_id,
        "points_redeemed": points,
        "discount_value": round(points * 0.01, 2),
        "remaining_points": new_balance
    }