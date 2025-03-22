from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from flow.models import Component, Flow
from flow.serializers import ComponentSerializer, ContentTypeSerializer, FlowSerializer


class FlowViewSet(ModelViewSet):
    serializer_class = FlowSerializer
    queryset = Flow.objects.all()


class ComponentViewSet(ModelViewSet):
    serializer_class = ComponentSerializer
    queryset = Component.objects.all()


class ContentTypeListView(ListAPIView):
    queryset = ContentType.objects.filter(
        Q(app_label="component") & ~Q(model="telegramcomponent"),
    )
    serializer_class = ContentTypeSerializer
