from django.db.models import QuerySet
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from component.serializers import *
from component.telegram.views import ModelViewSetCustom


class IfComponentSet(ModelViewSetCustom):
    serializer_class = IfComponentSerializer
    queryset = IfComponent.objects.all()


class SwitchComponentSet(ModelViewSetCustom):
    serializer_class = SwitchComponentSerializer
    queryset = SwitchComponent.objects.all()


class CodeComponentSet(ModelViewSetCustom):
    serializer_class = CodeComponent
    queryset = CodeComponent.objects.all()


class OnMessageSet(ModelViewSetCustom):
    serializer_class = OnMessageSerializer
    queryset = OnMessage.objects.all()


class OnCallbackQuerySet(ModelViewSetCustom):
    serializer_class = OnCallbackQuerySerializer
    queryset = OnCallbackQuery.objects.all()


class ContentTypeListView(ListAPIView):
    queryset = ContentType.objects.filter(
        Q(app_label="component") & ~Q(model="component") & ~Q(model="keyboard"),
    )
    serializer_class = ContentTypeSerializer
