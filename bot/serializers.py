from rest_framework import serializers


class MyBotResponseSerializer(serializers.Serializer):
    name = serializers.CharField()
