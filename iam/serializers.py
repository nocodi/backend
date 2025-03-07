from rest_framework import serializers

from iam.models import IamUser


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = IamUser
        fields = ["email", "password"]


class SignupVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    request_id = serializers.UUIDField()
