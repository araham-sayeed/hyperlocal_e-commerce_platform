from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    user_role: Literal["customer", "shop_owner", "rider"]
    user_ref: str = Field(min_length=3, max_length=255)
    issue_description: str = Field(min_length=10)


class TicketOut(BaseModel):
    id: int
    user_role: str
    user_ref: str
    issue_description: str
    status: str
    assigned_phone: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class FAQOut(BaseModel):
    id: int
    question: str
    answer: str
    region: str | None

    model_config = {"from_attributes": True}


class ContactOut(BaseModel):
    area_name: str
    support_phone: str
