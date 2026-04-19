from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class RiderApplication(BaseModel):
    email: EmailStr
    full_name: str
    phone: str
    aadhaar_last_four: str = Field(min_length=4, max_length=4, pattern=r"^\d{4}$")
    reason_to_join: str = Field(min_length=10)


class RiderVerifyRequest(BaseModel):
    rider_id: int
    approve: bool = True


class RiderPublic(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    phone: str
    status: str
    application_reason: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class RiderTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
