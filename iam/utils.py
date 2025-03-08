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

    return "Bearer " + jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_token(token: str) -> int:
    payload = jwt.decode(
        jwt=token,
        key=settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM],
    )
    if user_id := payload.get("user_id"):
        return user_id
        
    raise ValueError("payload is not correct, it must contain a user_id field")    

