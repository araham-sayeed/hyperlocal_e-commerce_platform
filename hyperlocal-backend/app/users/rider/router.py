from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.core.rate_limiter import limiter
from app.database import get_db
from app.dependencies import get_current_rider
from app.users.rider.models import Rider
from app.users.rider.schemas import (
    RiderApplication,
    RiderPublic,
    RiderTokenResponse,
    RiderVerifyRequest,
)
from app.users.rider import service

router = APIRouter(prefix="/riders", tags=["Riders"])


@router.post("/apply", response_model=RiderPublic)
@limiter.limit("5/minute")
def apply(request: Request, body: RiderApplication, db: Session = Depends(get_db)):
    return service.apply_rider(db, body)


@router.post("/verify", response_model=RiderPublic)
def verify_rider(body: RiderVerifyRequest, db: Session = Depends(get_db)):
    """Demo admin endpoint — protect with admin auth in production."""
    return service.verify_rider_admin(db, body.rider_id, body.approve)


@router.get("/me/status", response_model=RiderPublic)
def me_rider(rider: Rider = Depends(get_current_rider)):
    return rider


@router.get("/{rider_id}/status", response_model=RiderPublic)
def rider_status(rider_id: int, db: Session = Depends(get_db)):
    return service.rider_status(db, rider_id)


@router.post("/{rider_id}/token", response_model=RiderTokenResponse)
def rider_token(rider_id: int, db: Session = Depends(get_db)):
    token = service.issue_rider_token_if_verified(db, rider_id)
    return RiderTokenResponse(access_token=token)
