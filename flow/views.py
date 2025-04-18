from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, QuerySet
from django.db.models.fields.files import FileField
from django.forms import model_to_dict
from requests import RequestException, post
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from bot.models import Bot
from bot.permissions import IsBotOwner
from flow.models import Component, Flow
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
        component = self.get_object()
        related_model_instance = component.content_type.model_class().objects.get(
            id=component.object_id,
        )
        raw_data = model_to_dict(related_model_instance)

        excluded_keys = {"nobe", "id", "component_ptr", "component_ptr_id", "time"}
        data = {}
        files = {}

        for field_name, value in raw_data.items():
            if field_name in excluded_keys or value is None:
                continue
            field_object = related_model_instance._meta.get_field(field_name)
            if isinstance(field_object, FileField):
                file_field = getattr(related_model_instance, field_name)
                if file_field and file_field.name:
                    file_path = file_field.path
                    files[field_name] = open(file_path, "rb")
            else:
                data[field_name] = value

        bot_token = Bot.objects.get(id=bot).token
        telegram_api_url = f"https://tapi.bale.ai/bot{bot_token}/{related_model_instance.__class__.__name__}"

        try:
            response = post(telegram_api_url, data=data, files=files)
            response.raise_for_status()
        except RequestException as e:
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
        Q(app_label="component") & ~Q(model="telegramcomponent"),
    )
    serializer_class = ContentTypeSerializer
