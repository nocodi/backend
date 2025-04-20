from rest_framework.viewsets import ModelViewSet

from component.serializers import *


class IfComponentSet(ModelViewSet):
    serializer_class = IfComponentSerializer
    queryset = IfComponent.objects.all()


class SwitchComponentSet(ModelViewSet):
    serializer_class = SwitchComponentSerializer
    queryset = SwitchComponent.objects.all()


class CodeComponentSet(ModelViewSet):
    serializer_class = CodeComponent
    queryset = CodeComponent.objects.all()
