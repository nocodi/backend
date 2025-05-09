from django.apps import apps
from django.contrib import admin

from component.models import (
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Keyboard,
    KeyboardButton,
    OnMessage,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    SendDocument,
    SendMessage,
    SendPhoto,
    SendVideo,
)
from component.telegram.models import AddStickerToSet

app = apps.get_app_config("component")

# for model_name, model in app.models.items():
#     admin.site.register(model)

admin.site.register(OnMessage)
admin.site.register(SendMessage)
admin.site.register(SendPhoto)
admin.site.register(SendVideo)
admin.site.register(SendDocument)
admin.site.register(Keyboard)
admin.site.register(KeyboardButton)
admin.site.register(InlineKeyboardButton)
admin.site.register(InlineKeyboardMarkup)
admin.site.register(ReplyKeyboardMarkup)
admin.site.register(ReplyKeyboardRemove)
admin.site.register(ForceReply)
admin.site.register(AddStickerToSet)
