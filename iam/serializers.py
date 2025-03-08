from rest_framework import serializers

from iam.models import IamUser


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = IamUser
        fields = ["email", "password"]

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
