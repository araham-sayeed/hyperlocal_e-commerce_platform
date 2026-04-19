from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class SendOtpRequest(BaseModel):
    phone: str = Field(min_length=10, max_length=15)


class VerifyOtpRequest(BaseModel):
    phone: str
    code: str = Field(min_length=4, max_length=8)


class CustomerProfile(BaseModel):
    id: int
    phone: str
    email: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class CustomerTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CustomerProfileUpdate(BaseModel):
    email: EmailStr | None = None
