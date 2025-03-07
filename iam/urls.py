from django.urls import path

from iam.views import Getme, Login, Signup, VerifySignup

urlpatterns = [
    path("signup/", Signup.as_view(), name="signup"),
    path("signup/verify/", VerifySignup.as_view(), name="signup_verify"),
    path("login/", Login.as_view(), name="login"),
    path("getme/", Getme.as_view(), name="getme"),
]
