from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class ShopOwnerRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str
    shop_name: str
    phone: str
    latitude: float | None = None
    longitude: float | None = None


class ShopOwnerLogin(BaseModel):
    email: EmailStr
    password: str


class ShopOwnerProfile(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    shop_name: str
    phone: str
    latitude: float | None
    longitude: float | None
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class KycSubmit(BaseModel):
    aadhaar_last_four: str = Field(min_length=4, max_length=4, pattern=r"^\d{4}$")
