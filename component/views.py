from django.db.models import QuerySet
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
