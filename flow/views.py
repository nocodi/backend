from rest_framework.viewsets import ModelViewSet

from flow.models import Component, Flow
from flow.serializers import ComponentSerializer, FlowSerializer


class FlowViewSet(ModelViewSet):
    serializer_class = FlowSerializer
    queryset = Flow.objects.all()


class ComponentViewSet(ModelViewSet):
    serializer_class = ComponentSerializer
    queryset = Component.objects.all()
