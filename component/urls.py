
from rest_framework.routers import DefaultRouter

from component.telegram.urls import urlpatterns as telegram_urls
from component.views import (
    CodeComponentSet,
    IfComponentSet,
    OnCallbackQuerySet,
    OnMessageSet,
    SwitchComponentSet,
)

router = DefaultRouter()
router.register(r"on-message", OnMessageSet, basename="on-message")
router.register(r"on-callback-query", OnCallbackQuerySet, basename="on-callback-query")
router.register(r"if-component", IfComponentSet, basename="if-component")
router.register(r"switch-component", SwitchComponentSet, basename="switch-component")
router.register(r"code-component", CodeComponentSet, basename="code-component")

urlpatterns = [] + telegram_urls + router.urls
