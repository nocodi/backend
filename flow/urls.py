from django.urls import include, path
from rest_framework.routers import DefaultRouter

from flow.views import ComponentViewSet, ContentTypeListView, FlowViewSet

router = DefaultRouter()

router.register(r"flow", FlowViewSet)
router.register(r"component", ComponentViewSet)

urlpatterns = [
    path("contenttypes/", ContentTypeListView.as_view(), name="contenttypes"),
    path("", include(router.urls)),
]
