from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError as DRFValidationError

from flow.models import Component, Flow


class FlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flow
        fields = "__all__"


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ["id", "model"]


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        # depth = 1
        fields = "__all__"

    def save(self, **kwargs) -> None:  # type: ignore
        """Ensure that save() errors are returned as user errors instead of internal errors."""
        try:
            return super().save(**kwargs)
        except ValidationError as e:
            print(e)
            raise DRFValidationError({"object_id": str(e.messages[0])})
