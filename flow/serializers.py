from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.exceptions import ValidationError as DRFValidationError

from flow.models import Component, Flow


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        depth = 10
        fields = "__all__"

    def save(self, **kwargs) -> None:  # type: ignore
        """Ensure that save() errors are returned as user errors instead of internal errors."""
        try:
            return super().save(**kwargs)
        except ValidationError as e:
            raise DRFValidationError({"object_id": str(e.messages[0])})


class FlowSerializer(serializers.ModelSerializer):
    start_component = ComponentSerializer()

    class Meta:
        model = Flow
        fields = ["bot", "start_component"]


class ContentTypeSerializer(serializers.ModelSerializer):
    schema = serializers.SerializerMethodField()
    path = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def get_schema(self, obj: ContentType) -> dict:
        model_class = obj.model_class()
        if model_class is None:
            return {}

        schema = {
            field.name: {
                "type": field.get_internal_type(),
                "required": not field.null and not field.blank,
            }
            for field in model_class._meta.fields
            if field.name != "telegramcomponent_ptr"
            and field.name != "timestamp"
            and field.name != "id"
        }
        return schema

    def get_path(self, obj: ContentType) -> str:
        request = self.context.get("request")  # Get the request from context
        base_url = request.build_absolute_uri("/")[:-1] if request else ""  # Get host
        slugified_name = slugify(obj.name)  # Convert name to a URL-safe slug

        return f"{base_url}/component/{slugified_name}/"

    def get_description(self, obj: ContentType) -> str:
        return obj.model_class().__doc__

    class Meta:
        model = ContentType
        fields = ["id", "name", "description", "path", "schema"]
