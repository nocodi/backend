from django.utils.text import slugify
from rest_framework import serializers

from component.models import *
from component.telegram.serializers import ModelSerializerCustom


class SwitchComponentSerializer(ModelSerializerCustom):
    class Meta:
        model = SwitchComponent
        exclude = ["bot"]
        read_only_fields = ["component_type"]


class CodeComponentSerializer(ModelSerializerCustom):
    class Meta:
        model = CodeComponent
        exclude = ["bot"]
        read_only_fields = ["component_type"]


class SetStateSerializer(ModelSerializerCustom):
    class Meta:
        model = SetState
        exclude = ["bot"]
        read_only_fields = ["component_type"]


class OnMessageSerializer(ModelSerializerCustom):
    class Meta:
        model = OnMessage
        exclude = ["bot"]
        read_only_fields = ["component_type"]


class OnCallbackQuerySerializer(ModelSerializerCustom):
    class Meta:
        model = OnCallbackQuery
        exclude = ["bot"]
        read_only_fields = ["component_type"]


class ComponentSerializer(serializers.ModelSerializer):
    hover_text = serializers.SerializerMethodField()

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
            "hover_text",
            "reply_markup",
        ]

    reply_markup = serializers.SerializerMethodField(required=False)

    def get_hover_text(self, obj: Component) -> str:
        underlying_object = obj.component_content_type.model_class().objects.get(
            pk=obj.pk,
        )
        for field in underlying_object._meta.get_fields():
            if field.name == "text":
                return underlying_object.text
            elif field.name == "caption":
                return underlying_object.caption
        return ""

    def get_reply_markup(self, obj: Component):
        try:
            markup: Markup = obj.markup.get()
        except:
            return
        return {
            "buttons": markup.buttons,
            "type": markup.markup_type,
        }


class ContentTypeSerializer(serializers.ModelSerializer):
    schema = serializers.SerializerMethodField()
    path = serializers.SerializerMethodField()
    component_type = serializers.SerializerMethodField()
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

    def get_component_type(self, obj: ContentType) -> str:
        model_class = obj.model_class()
        if model_class is not None and hasattr(model_class, "component_type"):
            return model_class().component_type
        return ""

    class Meta:
        model = ContentType
        fields = ["id", "name", "description", "path", "schema", "component_type"]


class MarkupSerializer(ModelSerializerCustom):
    class Meta:
        model = Markup
        fields = "__all__"
        read_only_fields = ["component_type"]
