import requests
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, QuerySet
from django.db.models.fields.files import FileField
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from bot.models import Bot
from bot.permissions import IsBotOwner
from component.models import Component
from flow.models import Flow
from flow.serializers import ComponentSerializer, ContentTypeSerializer, FlowSerializer
from iam.permissions import IsLoginedPermission


class FlowViewSet(ModelViewSet):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = FlowSerializer
    queryset = Flow.objects.none()

    def get_queryset(self) -> QuerySet:
        return Flow.objects.filter(bot=self.kwargs.get("bot"))

    def get_serializer_context(self) -> dict:
        context = super().get_serializer_context()
        context["bot"] = self.kwargs.get("bot")
        return context


class ComponentViewSet(ModelViewSet):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = ComponentSerializer
    queryset = Component.objects.none()

    def get_queryset(self) -> QuerySet:
        return Component.objects.filter(bot_id=self.kwargs.get("bot"))

    def get_serializer_context(self) -> dict:
        context = super().get_serializer_context()
        context["bot"] = self.kwargs.get("bot")
        return context

    @action(detail=True, methods=["get"], url_path="run")
    def run(self, request: Request, bot: int, pk: int) -> Response:
        related_model_instance = (
            self.get_object().content_type.get_object_for_this_type()
        )
        reply_markup = related_model_instance.content_type.get_object_for_this_type()

        raw_data = model_to_dict(
            related_model_instance,
            exclude=[
                "id",
                "component_ptr",
                "component_ptr_id",
                "timestamp",
                "object_id",
                "component_type",
                "content_type",
            ],
        )
        data = {}
        files = {}

        for field_name, value in raw_data.items():
            field_object = related_model_instance._meta.get_field(field_name)
            if isinstance(field_object, FileField):
                file_field = getattr(related_model_instance, field_name)
                if file_field and file_field.name:
                    file_path = file_field.path
                    files[field_name] = open(file_path, "rb")
            else:
                data[field_name] = value

        if reply_markup:
            keyboard = model_to_dict(
                reply_markup,
                exclude=["id", "keyboard_ptr", "keyboard", "inline_keyboard"],
            )
            if hasattr(reply_markup, "keyboard"):
                keyboard["keyboard"] = []
                for row in reply_markup.keyboard.all():
                    keyboard["keyboard"].append([row.text])

            elif hasattr(reply_markup, "inline_keyboard"):
                keyboard["inline_keyboard"] = []
                for row in reply_markup.inline_keyboard.all():
                    keyboard["inline_keyboard"].append([model_to_dict(row)])

            data["reply_markup"] = keyboard

        bot_token = Bot.objects.get(id=bot).token
        telegram_api_url = f"{settings.BALE_API_URL}/bot{bot_token}/{related_model_instance.__class__.__name__}"
        try:
            response = requests.post(telegram_api_url, files=files, json=data)
            response.raise_for_status()
        except requests.RequestException as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        finally:
            for f in files.values():
                f.close()
        return Response(response.json(), status=status.HTTP_200_OK)


class ContentTypeListView(ListAPIView):
    queryset = ContentType.objects.filter(
        Q(app_label="component") & ~Q(model="component"),
    )
    serializer_class = ContentTypeSerializer
