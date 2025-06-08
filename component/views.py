from django.db.models import QuerySet
from rest_framework.generics import ListAPIView

from bot.permissions import IsBotOwner
from component.serializers import *
from component.telegram.views import ModelViewSetCustom
from iam.permissions import IsLoginedPermission


class SwitchComponentSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SwitchComponentSerializer
    queryset = SwitchComponent.objects.all()


class CodeComponentSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = CodeComponentSerializer
    queryset = CodeComponent.objects.all()


class SetStateSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = SetStateSerializer
    queryset = SetState.objects.all()


class OnMessageSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = OnMessageSerializer
    queryset = OnMessage.objects.all()


class ContentTypeListView(ListAPIView):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    queryset = ContentType.objects.filter(
        Q(app_label="component") & ~Q(model="component") & ~Q(model="keyboard"),
    )
    serializer_class = ContentTypeSerializer


class SchemaListView(ListAPIView):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = ComponentSerializer
    queryset = Component.objects.all()

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(bot=self.kwargs.get("bot"))


class MarkupSet(ModelViewSetCustom):
    permission_classes = [IsLoginedPermission, IsBotOwner]
    serializer_class = MarkupSerializer
    queryset = Markup.objects.all()
