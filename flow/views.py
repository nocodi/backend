from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, QuerySet
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from bot.models import Bot
from flow.models import Component, Flow
from flow.serializers import ComponentSerializer, ContentTypeSerializer, FlowSerializer
from iam.permissions import IsLoginedPermission


class FlowViewSet(ModelViewSet):
    serializer_class = FlowSerializer
    queryset = Flow.objects.all()


class FlowListViewSet(ListAPIView):
    serializer_class = FlowSerializer
    permission_classes = [IsLoginedPermission]

    def get_queryset(self) -> QuerySet:
        bot_id = self.kwargs.get("bot_id")
        if not bot_id:
            raise PermissionDenied("Bot ID is required.")

        try:
            bot = Bot.objects.get(id=bot_id, user=self.request.iam_user)
        except Bot.DoesNotExist:
            raise PermissionDenied("You do not have access to this bot.")

        return Flow.objects.filter(bot=bot)


class ComponentViewSet(ModelViewSet):
    serializer_class = ComponentSerializer
    queryset = Component.objects.all()


class ContentTypeListView(ListAPIView):
    queryset = ContentType.objects.filter(
        Q(app_label="component") & ~Q(model="telegramcomponent"),
    )
    serializer_class = ContentTypeSerializer
