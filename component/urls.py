from rest_framework.routers import DefaultRouter

from component.telegram.urls import urlpatterns as telegram_urls
from component.views import OnCallbackQuerySet, OnMessageSet

router = DefaultRouter()
router.register(r"on-message", OnMessageSet, basename="on-message")
router.register(r"on-callback-query", OnCallbackQuerySet, basename="on-callback-query")

urlpatterns = [] + telegram_urls + router.urls
