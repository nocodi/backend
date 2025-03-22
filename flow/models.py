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
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(app_label="component") & ~Q(model="telegramcomponent"),
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    prev_component = models.ForeignKey(
        "flow.Component",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="next_component",
    )

    position_x = models.FloatField(null=False, blank=False)
    position_y = models.FloatField(null=False, blank=False)

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        """Validate object_id belongs to content_type"""
        if self.object_id is None:
            return
        model_class = self.content_type.model_class()
        if (
            model_class is None
            or not model_class.objects.filter(id=self.object_id).exists()
        ):
            raise ValidationError(
                f"Invalid object_id {self.object_id} for {self.content_type}.",
            )

    def save(self, *args, **kwargs) -> None:  # type: ignore
        self.clean()  # Ensure validation before saving
        super().save(*args, **kwargs)


class Terminal(models.Model):
    name = models.CharField(max_length=255)
    flow = models.ForeignKey("flow.Flow", on_delete=models.CASCADE)
    operations = models.JSONField(default=dict)
    fields = models.JSONField(default=dict)

    def __str__(self) -> str:
        return self.name
