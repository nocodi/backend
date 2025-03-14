from rest_framework import serializers

from iam.models import IamUser


class MyBotResponseSerializer(serializers.Serializer):
    name = serializers.CharField()
