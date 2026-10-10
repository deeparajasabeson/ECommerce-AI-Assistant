from fastapi import APIRouter, HTTPException, Depends, Query
from app.data.repositories import get_shipping_repo
from app.data.shipping_repository import ShippingRepository

router = APIRouter(
    prefix="/shipping",
    tags=["shipping"]
)

@router.get("/rates")
def get_shipping_rates(
    zip_code: str = Query(..., description="Destination ZIP code"),
    weight: float = Query(..., description="Package weight in pounds"),
    repo: ShippingRepository = Depends(get_shipping_repo),
):
    """
    Get shipping rate estimates.
    """
    rates = []
    for rate_type, rate_info in rates_map.items():
        weight_surcharge = max(0, (weight - 5) * 1.5)
        rates.append(
            {
                "type": rate_type,
                "name": rate_info["name"],
                "cost": round(rate_info["cost"] + weight_surcharge, 2),
                "estimated_days": rate_info["days"],
                "carrier": "FastShip Logistics"
            }
        )
    return {
        "destination": zip_code,
        "weight": weight,
        "rates": rates
    }


@router.get("/track/{tracking_number}")
def track_shipment(
    tracking_number: str,
    repo: ShippingRepository = Depends(get_shipping_repo),
):
    """
    Track a shipment by its tracking number.
    """
    info = repo.get_tracking_info(tracking_number)
    if not info:
        raise HTTPException(status_code=404, 
                            detail="Tracking number not found")
    return info

@router.post("/track")
def track_shipment_post(
    tracking_number: str,
    repo: ShippingRepository = Depends(get_shipping_repo),
):
    """
    
    """
    info = repo.get_tracking_info(tracking_number)
    if not info:
        raise HTTPException(status_code=404, 
                            detail="Tracking number not found")
    return info