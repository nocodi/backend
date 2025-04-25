from django.urls import include, path
from rest_framework.routers import DefaultRouter

from component.telegram.urls import urlpatterns as telegram_urls
from component.views import OnMessageSet

router = DefaultRouter()
router.register(r"on-message", OnMessageSet)

urlpatterns = telegram_urls.copy()
urlpatterns += [
    path("", include(router.urls)),
]
