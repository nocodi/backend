from django.apps import apps
from django.contrib import admin

from component.models import Component, SendDocument, SendMessage, SendPhoto, SendVideo

app = apps.get_app_config("component")

# for model_name, model in app.models.items():
#     admin.site.register(model)


admin.site.register(Component)
admin.site.register(SendMessage)
admin.site.register(SendPhoto)
admin.site.register(SendVideo)
admin.site.register(SendDocument)
