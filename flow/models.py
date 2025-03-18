from django.contrib.postgres.fields import ArrayField
from django.db.models import (
    CASCADE,
    CharField,
    FloatField,
    ForeignKey,
    JSONField,
    Model,
)


class Flow(Model):
    start_component = ForeignKey("flow.Component", on_delete=CASCADE)


class Component(Model):
    name = CharField(max_length=255)
    type = ForeignKey("bot.TelegramComponent", on_delete=CASCADE)

    next_component = ForeignKey(
        "flow.Component",
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name="previous_components",
    )
    prev_component = ForeignKey(
        "flow.Component",
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name="next_components",
    )

    position_x = FloatField(null=False, blank=False)
    position_y = FloatField(null=False, blank=False)

    def __str__(self) -> str:
        return self.name


class Terminal(Model):
    name = CharField(max_length=255)
    flow = ForeignKey("flow.Flow", on_delete=CASCADE)
    operations = JSONField(default=dict)
    fields = JSONField(default=dict)

    def __str__(self) -> str:
        return self.name
