from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.auth import decode_token
from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.database import get_db
from app.users.customer.models import Customer
from app.users.rider.models import Rider
from app.users.shop_owner.models import ShopOwner

security = HTTPBearer(auto_error=False)


def _payload(creds: HTTPAuthorizationCredentials | None) -> dict:
    if creds is None or not creds.credentials:
        raise UnauthorizedError("Missing bearer token")
    try:
        return decode_token(creds.credentials)
    except ValueError:
        raise UnauthorizedError("Invalid or expired token") from None


def get_current_shop_owner(
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    db: Session = Depends(get_db),
) -> ShopOwner:
    payload = _payload(creds)
    if payload.get("role") != "shop_owner":
        raise ForbiddenError("Token is not for a shop owner")
    owner = db.get(ShopOwner, int(payload["sub"]))
    if not owner:
        raise UnauthorizedError("Shop owner not found")
    return owner


def get_current_customer(
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    db: Session = Depends(get_db),
) -> Customer:
    payload = _payload(creds)
    if payload.get("role") != "customer":
        raise ForbiddenError("Token is not for a customer")
    customer = db.get(Customer, int(payload["sub"]))
    if not customer:
        raise UnauthorizedError("Customer not found")
    return customer


def get_optional_customer(
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    db: Session = Depends(get_db),
) -> Customer | None:
    if creds is None or not creds.credentials:
        return None
    try:
        payload = decode_token(creds.credentials)
    except ValueError:
        return None
    if payload.get("role") != "customer":
        return None
    return db.get(Customer, int(payload["sub"]))


def get_current_rider(
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    db: Session = Depends(get_db),
) -> Rider:
    payload = _payload(creds)
    if payload.get("role") != "rider":
        raise ForbiddenError("Token is not for a rider")
    rider = db.get(Rider, int(payload["sub"]))
    if not rider:
        raise UnauthorizedError("Rider not found")
    return rider
