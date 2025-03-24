import json
import logging
import uuid
from typing import Dict

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from iam.integrations.email import email_client
from iam.models import IamUser
from iam.permissions import IsLoginedPermission
from iam.serializers import (
    IamUserSerializer,
    LoginOTPSendRequestSerializer,
    LoginOTPSendResponseSerializer,
    LoginOTPVerifyResponseSerializer,
    LoginResponseSerializer,
    LoginSerializer,
    SignupRequestSerializer,
    SignupResponseSerializer,
    SignupVerifySerializer,
)
from iam.utils import create_token_for_iamuser, generate_otp
from utils.redis import redis_client


class Login(APIView):
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            user = IamUser.objects.get(email=data["email"])
            if user.password == data["password"]:
                return Response(
                    status=status.HTTP_200_OK,
                    data=LoginResponseSerializer(
                        {
                            "access_token": create_token_for_iamuser(
                                user_id=user.id,
                            ),
                        },
                    ).data,
                )
        except IamUser.DoesNotExist:
            pass

        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
            data={"detail": "Invalid credentials"},
        )


class Signup(APIView):
    serializer_class = SignupRequestSerializer

    @extend_schema(
        request=SignupRequestSerializer,
        responses={201: SignupResponseSerializer},
    )
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        otp = generate_otp(length=6)
        redis_data = {
            "email": data["email"],
            "password": data["password"],
            "otp": otp,
        }
        redis_data_str: str = json.dumps(redis_data)
        signup_id = str(uuid.uuid4())
        redis_client.set(f"signup::{signup_id}", redis_data_str, ex=120)

        try:
            email_client.send(
                target=data["email"],
                subject="Your OTP for signup",
                text=f"Your OTP is {otp}",
            )
        except Exception as e:
            print("cant send otp", e)

        return Response(
            status=status.HTTP_201_CREATED,
            data=SignupResponseSerializer({"request_id": signup_id}).data,
        )


class VerifySignup(APIView):
    serializer_class = SignupVerifySerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        redis_key = f"signup::{serializer.validated_data['request_id']}"
        if redis_data := redis_client.get(redis_key):
            redis_data = json.loads(redis_data)

            if serializer.validated_data["otp"] == redis_data["otp"]:
                user_id = IamUser.objects.create(
                    email=redis_data["email"],
                    password=redis_data["password"],
                ).id
                return Response(
                    status=status.HTTP_201_CREATED,
                    data={
                        "user_id": user_id,
                        "access_token": create_token_for_iamuser(
                            user_id=user_id,
                        ),
                    },
                )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class OTPLoginSend(APIView):
    serializer_class = LoginOTPSendRequestSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        otp = generate_otp(length=6)
        request_id = str(uuid.uuid4())
        redis_data = {"email": data["email"], "otp": otp}
        redis_data_str: str = json.dumps(redis_data)
        redis_key = f"login::otp::{request_id}"

        redis_client.set(redis_key, redis_data_str, ex=120)
        try:
            email_client.send(
                target=data["email"],
                subject="Your OTP for login",
                text=f"Your OTP is {otp}",
            )
        except Exception as e:
            print("cant send otp", e)

        return Response(
            status=status.HTTP_200_OK,
            data=LoginOTPSendResponseSerializer(
                {
                    "request_id": request_id,
                    "otp": f"Your OTP is {otp}",
                },
            ).data,
        )


class OTPLoginVerify(APIView):
    serializer_class = LoginOTPVerifyResponseSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        redis_key = f"login::otp::{data['request_id']}"
        if redis_data := redis_client.get(redis_key):
            redis_data = json.loads(redis_data)
            if data["otp"] == redis_data["otp"]:
                user = IamUser.objects.get(email=redis_data["email"])
                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        "access_token": create_token_for_iamuser(
                            user_id=user.id,
                        ),
                    },
                )
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class Getme(APIView):
    permission_classes = [IsLoginedPermission]

    def get(self, request: Request) -> Response:
        return Response(
            data=IamUserSerializer(request.iam_user).data,
            status=status.HTTP_200_OK,
        )


# edit user view using updateAPIView
class UpdatePassword(UpdateAPIView):
    permission_classes = [IsLoginedPermission]
    serializer_class = LoginSerializer
    queryset = IamUser.objects

    def update(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.queryset.filter(id=request.iam_user.id).update(
            password=serializer.validated_data["password"],
        )
        return Response(status=status.HTTP_200_OK)
