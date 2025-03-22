from django.apps import apps
from django.contrib import admin

from component.models import SendMessage, SendPhoto, TelegramComponent

app = apps.get_app_config("component")

# for model_name, model in app.models.items():
#     admin.site.register(model)


admin.site.register(TelegramComponent)
admin.site.register(SendMessage)
admin.site.register(SendPhoto)
