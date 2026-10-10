from datetime import datetime
from pydantic import BaseModel, ConfigDict

class Customer(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: str
    name: str
    email: str
    phone: str
    loyalty_points: int
    member_since: datetime

class RedeemPointsRequest(BaseModel):
    """Request body for POST /customers/{customer_id}/loyalty/redeem.
    customer_id comes from the URL path -- it is intentionally absent here.
    """
    points: int
    