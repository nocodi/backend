from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework import status

from rest_framework.views import APIView
from iam.serializers import SignupSerializer


class Login(APIView):
    def post(self, request: Request):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


class Signup(APIView):
    def post(self, request: Request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data={"message": "User created successfully, go to verify email"}
        )


class Getme(APIView):
    def post(self, request: Request):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
