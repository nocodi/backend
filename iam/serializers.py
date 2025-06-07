from rest_framework import serializers

from iam.models import IamUser


class SignupRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = IamUser
        fields = ["email", "password"]


class SignupResponseSerializer(serializers.Serializer):
    request_id = serializers.UUIDField()


class IamUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = IamUser
        fields = [
            "email",
            "password",
            "created_at",
            "updated_at",
        ]


class SignupVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    request_id = serializers.UUIDField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class LoginOTPSendRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class LoginOTPSendResponseSerializer(serializers.Serializer):
    request_id = serializers.UUIDField()


class LoginOTPVerifyResponseSerializer(serializers.Serializer):
    request_id = serializers.UUIDField()
    otp = serializers.CharField()


class LoginResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    is_first_login = serializers.BooleanField()
