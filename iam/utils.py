import math
import random

import jwt
from django.conf import settings
from django.utils import timezone


def generate_otp(length=6):
    digits = "0123456789"
    OTP = ""
    for i in range(length):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


def create_token_for_iamuser(user_id: int) -> str:
    iat = timezone.now().timestamp()
    payload = {
        "iat": iat,
        "exp": iat + settings.JWT_DURATION,
        "user_id": user_id,
    }

    return jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
