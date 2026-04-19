from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ChatSessionCreate(BaseModel):
    title: str | None = None


class ChatSessionOut(BaseModel):
    id: int
    customer_id: int | None
    title: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class MessageIn(BaseModel):
    content: str = Field(min_length=1, max_length=4000)


class MessageOut(BaseModel):
    id: int
    session_id: int
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class HandoffCard(BaseModel):
    type: Literal["handoff"] = "handoff"
    support_phone: str
    region: str
    message: str


class ChatTurnResponse(BaseModel):
    user_message: MessageOut
    assistant_message: MessageOut
    handoff: HandoffCard | None = None
