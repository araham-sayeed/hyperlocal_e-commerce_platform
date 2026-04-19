from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.core.auth import create_access_token
from app.core.rate_limiter import limiter
from app.database import get_db
from app.dependencies import get_current_shop_owner
from app.users.shop_owner.models import ShopOwner
from app.users.shop_owner.schemas import (
    KycSubmit,
    ShopOwnerLogin,
    ShopOwnerProfile,
    ShopOwnerRegister,
    TokenResponse,
)
from app.users.shop_owner import service

router = APIRouter(prefix="/shop-owners", tags=["Shop Owners"])


@router.post("/register", response_model=ShopOwnerProfile)
@limiter.limit("5/minute")
def register_shop_owner(request: Request, payload: ShopOwnerRegister, db: Session = Depends(get_db)):
    owner = service.register_shop_owner(db, payload)
    return owner


@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
def login_shop_owner(request: Request, body: ShopOwnerLogin, db: Session = Depends(get_db)):
    owner = service.authenticate_shop_owner(db, str(body.email), body.password)
    token = create_access_token(str(owner.id), "shop_owner", {"shop_name": owner.shop_name})
    return TokenResponse(access_token=token)


@router.get("/me", response_model=ShopOwnerProfile)
def me_shop_owner(
    owner: ShopOwner = Depends(get_current_shop_owner),
):
    return owner


@router.post("/me/kyc", response_model=ShopOwnerProfile)
def kyc_shop_owner(
    body: KycSubmit,
    owner: ShopOwner = Depends(get_current_shop_owner),
    db: Session = Depends(get_db),
):
    return service.submit_kyc(db, owner, body.aadhaar_last_four)


@router.get("/subscription/tiers")
def subscription_tiers():
    return service.list_subscription_tiers()
