from django.urls import path

from bot.views import MyBot
from iam.views import (
    Getme,
    Login,
    OTPLoginSend,
    OTPLoginVerify,
    Signup,
    UpdatePassword,
    VerifySignup,
)

urlpatterns = [
    path("my-bots/", MyBot.as_view(), name="my_bots"),
]
