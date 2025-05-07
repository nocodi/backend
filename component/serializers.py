from django.utils.text import slugify
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


class OnCallbackQuerySerializer(ModelSerializerCustom):
    class Meta:
        model = OnCallbackQuery
        depth = 1
        exclude = ["component_type"]


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = [
            "id",
            "component_name",
            "component_type",
            "component_content_type",
            "previous_component",
            "position_y",
            "position_x",
        ]


class ContentTypeSerializer(serializers.ModelSerializer):
    schema = serializers.SerializerMethodField()
    path = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def get_schema(self, obj: ContentType) -> dict:
        model_class = obj.model_class()
        if model_class is None:
            return {}

        required_fields = []
        if hasattr(model_class, "required_fields"):
            required_fields = model_class().required_fields

        schema = {
            field.name: {
                "type": field.get_internal_type(),
                "required": field.name in required_fields,
                "help_text": field.help_text,
                "choices": (
                    [choice[0] for choice in field.choices]
                    if hasattr(field, "choices") and field.choices
                    else None
                ),
                "max_length": (
                    field.max_length if hasattr(field, "max_length") else None
                ),
                "verbose_name": field.verbose_name,
            }
            for field in model_class._meta.fields
            if field.name != "component_ptr"
            and field.name != "timestamp"
            and field.name != "id"
            and field.name != "object_id"
            and field.name != "content_type"
            and field.name != "component_type"
            and field.name != "bot"
            and field.name != "component_content_type"
            and field.name != "previous_component"
            and field.name != "position_x"
            and field.name != "position_y"
            and field.name != "component_name"
        }
        return schema

    def get_path(self, obj: ContentType) -> str:
        request = self.context.get("request")  # Get the request from context
        base_url = request.build_absolute_uri("/")[:-1] if request else ""  # Get host
        slugified_name = slugify(obj.name)  # Convert name to a URL-safe slug
        bot_id = request.parser_context.get("kwargs").get("bot")

        return f"{base_url}/component/{bot_id}/{slugified_name}/"

    def get_description(self, obj: ContentType) -> str:
        return obj.model_class().__doc__

    class Meta:
        model = ContentType
        fields = ["id", "name", "description", "path", "schema"]
