from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.core.rate_limiter import limiter
from app.database import get_db
from app.dependencies import get_current_customer
from app.users.customer.models import Customer
from app.users.customer.schemas import (
    CustomerProfile,
    CustomerProfileUpdate,
    CustomerTokenResponse,
    SendOtpRequest,
    VerifyOtpRequest,
)
from app.users.customer import service

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/otp/send")
@limiter.limit("5/minute")
def send_otp(request: Request, body: SendOtpRequest, db: Session = Depends(get_db)):
    return service.send_otp(db, body.phone)


@router.post("/otp/verify", response_model=CustomerTokenResponse)
@limiter.limit("15/minute")
def verify_otp(request: Request, body: VerifyOtpRequest, db: Session = Depends(get_db)):
    token = service.verify_otp(db, body.phone, body.code)
    return CustomerTokenResponse(access_token=token)


@router.get("/me", response_model=CustomerProfile)
def me_customer(customer: Customer = Depends(get_current_customer)):
    return customer


@router.patch("/me", response_model=CustomerProfile)
def patch_me_customer(
    body: CustomerProfileUpdate,
    customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    return service.update_profile(db, customer, body)
