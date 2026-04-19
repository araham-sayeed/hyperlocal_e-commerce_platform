from datetime import datetime

from pydantic import BaseModel, Field


class ReturnCreate(BaseModel):
    order_id: int
    reason: str = Field(min_length=10)


class ReturnOut(BaseModel):
    id: int
    order_id: int
    customer_id: int
    reason: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
