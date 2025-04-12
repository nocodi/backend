from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, QuerySet
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import ListAPIView
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


class ContentTypeListView(ListAPIView):
    queryset = ContentType.objects.filter(
        Q(app_label="component") & ~Q(model="telegramcomponent"),
    )
    serializer_class = ContentTypeSerializer
