from rest_framework import serializers

from component.models import *
from component.telegram.serializers import ModelSerializerCustom


class IfComponentSerializer(ModelSerializerCustom):
    class Meta:
        model = IfComponent
        depth = 1
        exclude = ["component_type"]


class SwitchComponentSerializer(ModelSerializerCustom):
    class Meta:
        model = SwitchComponent
        depth = 1
        exclude = ["component_type"]


class CodeComponentSerializer(ModelSerializerCustom):
    class Meta:
        model = CodeComponent
        depth = 1
        exclude = ["component_type"]


class OnMessageSerializer(ModelSerializerCustom):
    class Meta:
        model = OnMessage
        depth = 1
        exclude = ["component_type"]
