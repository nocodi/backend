from django.apps import apps
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from iam.models import IamUser


class Flow(models.Model):
    bot = models.ForeignKey("bot.Bot", on_delete=models.CASCADE)
    start_component = models.ForeignKey("component.Component", on_delete=models.CASCADE)


BOT_MODELS = [
    (model_name, model_name)
    for model_name in apps.get_app_config("component").models.keys()
]
