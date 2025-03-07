import json
import uuid

from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from iam.integrations.email import email_client
from iam.serializers import SignupSerializer, SignupVerifySerializer
from iam.models import IamUser
from iam.utils import create_token_for_iamuser, generate_otp
from utils.redis import redis_client


class Login(APIView):
    def post(self, request: Request):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


class Signup(APIView):
    def post(self, request: Request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        otp = generate_otp(length=6)
        redis_data = {"email": data["email"],
                      "password": data["password"], "otp": otp}
        redis_data = json.dumps(redis_data)
        signup_id = str(uuid.uuid4())
        redis_client.set(f"signup::{signup_id}", redis_data, ex=120)

        email_client.send(
            target=data["email"],
            subject="Your OTP for signup",
            text=f"Your OTP is {otp}",
        )

        return Response(status=status.HTTP_201_CREATED, data={"request_id": signup_id})


class VerifySignup(APIView):
    def post(self, request: Request):
        serialzier = SignupVerifySerializer(data=request.data)
        serialzier.is_valid(raise_exception=True)
        redis_key = f"signup::{serialzier.validated_data['request_id']}"
        if redis_data := redis_client.get(redis_key):
            redis_data = json.loads(redis_data)
            if serialzier.validated_data["otp"] == redis_data["otp"]:

                user_id = IamUser.objects.create(
                    email=redis_data["email"], password=redis_data["password"]
                ).id
                return Response(
                    status=status.HTTP_201_CREATED,
                    data={
                        "access_token": create_token_for_iamuser(
                            user_id=user_id,
                        ),
                    },
                )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class Getme(APIView):
    def post(self, request: Request):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
