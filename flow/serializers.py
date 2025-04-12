from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.exceptions import ValidationError as DRFValidationError

from bot.models import Bot
from flow.models import Component, Flow


class ComponentSerializer(serializers.ModelSerializer):
    content_type = serializers.IntegerField(source="content_type_id")
    next_component = serializers.IntegerField(
        source="next_component_id",
        required=False,
        default=None,
    )

    def validate_object_id(self, value: int) -> int:
        """Validate that the object_id exists and belongs to the given content_type."""
        if value is None:
            return value

        content_type = getattr(
            self.instance,
            "content_type",
            None,
        ) or getattr(self.initial_data, "content_type", None)

        if not content_type:
            raise serializers.ValidationError(
                "content_type is required to validate object_id.",
            )

        try:
            model_class = ContentType.objects.get(id=content_type).model_class()
        except ContentType.DoesNotExist:
            raise serializers.ValidationError("Invalid content_type.")

        if model_class is None or not model_class.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                f"Invalid object_id '{value}' for content_type '{content_type}'.",
            )

        return value

    def validate_next_component(self, value: int) -> int:
        """Validate that next_component is not self and belongs to the same bot."""
        if value is None:
            return value

        # Prevent next_component from being self
        if self.instance and value == self.instance:
            raise serializers.ValidationError(
                "next_component cannot be the same as self.",
            )

        # Get bot from context or instance
        current_bot = getattr(self.instance, "bot", None) or getattr(
            self.initial_data,
            "bot",
            None,
        )
        if not current_bot:
            raise serializers.ValidationError(
                "Bot must be defined to validate next_component.",
            )

        # Ensure the next_component exists and is valid for the given bot
        if not Component.objects.filter(id=value, bot_id=current_bot).exists():
            raise serializers.ValidationError(
                "next_component does not exist in components.",
            )

        return value

    class Meta:
        model = Component
        exclude = ["bot"]

    def create(self, validated_data: dict) -> Component:
        validated_data["bot_id"] = self.context.get("bot")
        return super().create(validated_data)

    def update(self, instance: Component, validated_data: dict) -> Component:
        validated_data.pop("content_type_id", None)
        return super().update(instance, validated_data)


class RecursiveComponentSerializer(serializers.ModelSerializer):
    next_component = serializers.SerializerMethodField()

    class Meta:
        model = Component
        exclude = ["bot"]  # explicitly exclude 'bot'

    def get_next_component(self, obj: Component) -> dict:
        if obj.next_component:
            return RecursiveComponentSerializer(
                obj.next_component,
                context=self.context,
            ).data
        return {}


class FlowSerializer(serializers.ModelSerializer):
    start_component = RecursiveComponentSerializer(read_only=True)
    start = serializers.IntegerField(source="start_component_id", write_only=True)

    class Meta:
        model = Flow
        fields = ["id", "start_component", "start"]

    def create(self, validated_data: dict) -> Flow:
        validated_data["bot_id"] = self.context.get("bot")
        return super().create(validated_data)


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
