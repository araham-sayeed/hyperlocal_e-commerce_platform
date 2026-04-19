from sqlalchemy.orm import Session

from app.core.auth import hash_password, verify_password
from app.core.exceptions import BadRequestError, UnauthorizedError
from app.users.shop_owner import kyc
from app.users.shop_owner.models import ShopOwner, Subscription
from app.users.shop_owner.schemas import ShopOwnerRegister
from app.users.shop_owner.subscription import SUBSCRIPTION_TIERS


def register_shop_owner(db: Session, data: ShopOwnerRegister) -> ShopOwner:
    existing = db.query(ShopOwner).filter(ShopOwner.email == str(data.email)).first()
    if existing:
        raise BadRequestError("Email already registered")
    owner = ShopOwner(
        email=str(data.email).lower(),
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
        shop_name=data.shop_name,
        phone=data.phone,
        latitude=data.latitude,
        longitude=data.longitude,
    )
    db.add(owner)
    db.flush()
    sub = Subscription(shop_owner_id=owner.id, plan_tier="starter", status="active")
    db.add(sub)
    db.commit()
    db.refresh(owner)
    return owner


def authenticate_shop_owner(db: Session, email: str, password: str) -> ShopOwner:
    owner = db.query(ShopOwner).filter(ShopOwner.email == email.lower()).first()
    if not owner or not verify_password(password, owner.hashed_password):
        raise UnauthorizedError("Invalid email or password")
    return owner


def get_shop_owner(db: Session, owner_id: int) -> ShopOwner | None:
    return db.get(ShopOwner, owner_id)


def submit_kyc(db: Session, owner: ShopOwner, aadhaar_last_four: str) -> ShopOwner:
    result = kyc.verify_aadhaar_stub(aadhaar_last_four, owner.full_name)
    if not result.get("verified"):
        raise BadRequestError(result.get("reason", "KYC failed"))
    owner.aadhaar_reference = result.get("reference")
    db.add(owner)
    db.commit()
    db.refresh(owner)
    return owner


def list_subscription_tiers():
    return SUBSCRIPTION_TIERS
