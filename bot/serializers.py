from rest_framework import serializers

from bot.models import Bot


class MyBotsResponseSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Bot
        fields = ["id", "name", "description", "created_at", "user", "token"]


class CreateBotRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ["name", "description", "token"]


class CreateBotResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ["id", "name", "description", "created_at", "token"]
