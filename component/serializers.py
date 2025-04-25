from rest_framework import serializers

from component.models import *


class IfComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IfComponent
        depth = 1
        fields = "__all__"


class SwitchComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwitchComponent
        depth = 1
        fields = "__all__"


class CodeComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeComponent
        depth = 1
        fields = "__all__"


class OnMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnMessage
        depth = 1
        fields = "__all__"
