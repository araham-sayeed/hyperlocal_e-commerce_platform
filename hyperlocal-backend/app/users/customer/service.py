import random
import string
from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from app.config import get_settings
from app.core.auth import create_access_token
from app.core.exceptions import BadRequestError, UnauthorizedError
from app.core.notifications import send_sms_otp
from app.users.customer.models import Customer, OtpChallenge
from app.users.customer.schemas import CustomerProfileUpdate


def _generate_code() -> str:
    settings = get_settings()
    if settings.otp_dev_fixed_code:
        return settings.otp_dev_fixed_code
    return "".join(random.choices(string.digits, k=settings.otp_length))


def send_otp(db: Session, phone: str) -> dict:
    settings = get_settings()
    code = _generate_code()
    expires = datetime.now(UTC) + timedelta(seconds=settings.otp_ttl_seconds)
    row = OtpChallenge(phone=phone, code=code, expires_at=expires)
    db.add(row)
    db.commit()
    send_sms_otp(phone, code)
    return {"phone": phone, "expires_in_seconds": settings.otp_ttl_seconds, "dev_hint": "Use code from SMS log or OTP_DEV_FIXED_CODE"}


def verify_otp(db: Session, phone: str, code: str) -> str:
    row = (
        db.query(OtpChallenge)
        .filter(OtpChallenge.phone == phone, OtpChallenge.code == code)
        .order_by(OtpChallenge.id.desc())
        .first()
    )
    if not row:
        raise UnauthorizedError("Invalid or expired OTP")
    exp = row.expires_at
    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=UTC)
    if exp < datetime.now(UTC):
        raise UnauthorizedError("Invalid or expired OTP")
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    if not customer:
        customer = Customer(phone=phone)
        db.add(customer)
        db.commit()
        db.refresh(customer)
    return create_access_token(str(customer.id), "customer")


def update_profile(db: Session, customer: Customer, data: CustomerProfileUpdate) -> Customer:
    if data.email is not None:
        customer.email = str(data.email).lower()
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer
