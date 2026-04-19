"""SMS / push (integrate Twilio, FCM in production)."""

import logging

logger = logging.getLogger(__name__)


def send_sms_otp(phone: str, code: str) -> None:
    logger.info("SMS OTP to %s: %s (dev log only)", phone, code)
