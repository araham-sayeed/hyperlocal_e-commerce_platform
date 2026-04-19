from sqlalchemy.orm import Session

from app.core.auth import create_access_token
from app.core.exceptions import BadRequestError, NotFoundError
from app.users.rider.models import Rider
from app.users.rider.schemas import RiderApplication
from app.users.rider import verification


def apply_rider(db: Session, data: RiderApplication) -> Rider:
    check = verification.verify_rider_documents(data.aadhaar_last_four, data.reason_to_join)
    if not check.get("ok"):
        raise BadRequestError(check.get("message", "Verification failed"))
    existing = db.query(Rider).filter(Rider.email == str(data.email).lower()).first()
    if existing:
        raise BadRequestError("Email already used")
    rider = Rider(
        email=str(data.email).lower(),
        full_name=data.full_name,
        phone=data.phone,
        status="pending",
        application_reason=data.reason_to_join,
        aadhaar_reference=check.get("reference"),
    )
    db.add(rider)
    db.commit()
    db.refresh(rider)
    return rider


def verify_rider_admin(db: Session, rider_id: int, approve: bool) -> Rider:
    rider = db.get(Rider, rider_id)
    if not rider:
        raise NotFoundError("Rider not found")
    rider.status = "verified" if approve else "rejected"
    db.add(rider)
    db.commit()
    db.refresh(rider)
    return rider


def rider_status(db: Session, rider_id: int) -> Rider:
    rider = db.get(Rider, rider_id)
    if not rider:
        raise NotFoundError("Rider not found")
    return rider


def issue_rider_token_if_verified(db: Session, rider_id: int) -> str:
    rider = db.get(Rider, rider_id)
    if not rider:
        raise NotFoundError("Rider not found")
    if rider.status != "verified":
        raise BadRequestError("Rider is not verified yet")
    return create_access_token(str(rider.id), "rider")
