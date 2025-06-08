from aiogram.enums import ContentType
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from component.telegram.urls import urlpatterns as telegram_urls
from component.views import (
    CodeComponentSet,
    ContentTypeListView,
    MarkupSet,
    OnCallbackQuerySet,
    OnMessageSet,
    SchemaListView,
    SetStateSet,
    SwitchComponentSet,
)

router = DefaultRouter()
router.register(r"on-message", OnMessageSet, basename="on-message")
router.register(r"set-state", SetStateSet, basename="set-state")
router.register(r"on-callback-query", OnCallbackQuerySet, basename="on-callback-query")
router.register(r"switch-component", SwitchComponentSet, basename="switch-component")
router.register(r"code-component", CodeComponentSet, basename="code-component")
router.register(r"markup", MarkupSet, basename="markup")

urlpatterns = (
    [
        path("content-type/", ContentTypeListView.as_view(), name="contenttypes"),
        path("schema/", SchemaListView.as_view(), name="contenttypes"),
    ]
    + telegram_urls
    + router.urls
)
