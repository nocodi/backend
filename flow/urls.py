from django.urls import include, path
from rest_framework.routers import DefaultRouter

from flow.views import ComponentViewSet, FlowViewSet

router = DefaultRouter()

router.register(r"flow", FlowViewSet)
router.register(r"component", ComponentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
