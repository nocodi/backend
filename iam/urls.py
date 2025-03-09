from django.urls import path

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
    path("signup/", Signup.as_view(), name="signup"),
    path("signup/verify/", VerifySignup.as_view(), name="signup_verify"),
    path("login/pasword", Login.as_view(), name="login"),
    path("login/otp/send", OTPLoginSend.as_view(), name="login_otp_send"),
    path("login/otp/verify", OTPLoginVerify.as_view(), name="login_otp_verify"),
    path("getme/", Getme.as_view(), name="getme"),
    path("update/password", UpdatePassword.as_view(), name="update_password"),
]
