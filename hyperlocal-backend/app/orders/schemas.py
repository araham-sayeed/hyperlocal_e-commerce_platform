from datetime import datetime

from pydantic import BaseModel, Field


class OrderLineIn(BaseModel):
    product_id: int
    quantity: int = Field(ge=1, le=99)


class OrderCreate(BaseModel):
    shop_owner_id: int
    lines: list[OrderLineIn] = Field(min_length=1)
    delivery_latitude: float | None = None
    delivery_longitude: float | None = None


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float

    model_config = {"from_attributes": True}


class OrderOut(BaseModel):
    id: int
    customer_id: int
    shop_owner_id: int
    status: str
    total_amount: float
    delivery_latitude: float | None
    delivery_longitude: float | None
    created_at: datetime
    items: list[OrderItemOut]

    model_config = {"from_attributes": True}
