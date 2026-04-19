from datetime import datetime

from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    product_id: int
    rating: int = Field(ge=1, le=5)
    comment: str | None = None


class ReviewOut(BaseModel):
    id: int
    product_id: int
    customer_id: int
    rating: int
    comment: str | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
