from django.apps import apps
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from iam.models import IamUser


class Flow(models.Model):
    bot = models.ForeignKey("bot.Bot", on_delete=models.CASCADE)
    start_component = models.ForeignKey("flow.Component", on_delete=models.CASCADE)


BOT_MODELS = [
    (model_name, model_name)
    for model_name in apps.get_app_config("component").models.keys()
]


class Component(models.Model):
    name = models.CharField(max_length=255)
    bot = models.ForeignKey("bot.Bot", on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(app_label="component") & ~Q(model="telegramcomponent"),
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    next_component = models.ForeignKey(
        "flow.Component",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="nextcomponent",
    )

    position_x = models.FloatField(null=False, blank=False)
    position_y = models.FloatField(null=False, blank=False)

    def __str__(self) -> str:
        return self.name


class Terminal(models.Model):
    name = models.CharField(max_length=255)
    flow = models.ForeignKey("flow.Flow", on_delete=models.CASCADE)
    operations = models.JSONField(default=dict)
    fields = models.JSONField(default=dict)

    def __str__(self) -> str:
        return self.name
