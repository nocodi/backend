from django.apps import apps
from django.contrib import admin

from component.models import (
    CodeComponent,
    Markup,
    OnMessage,
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
admin.site.register(AddStickerToSet)
admin.site.register(CodeComponent)
admin.site.register(Markup)
