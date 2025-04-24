from typing import Any

from component.telegram.models import *


class IfComponent(Component):
    """Use this method to create a conditional component. Returns True on success."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.type = Component.ComponentType.CONDITIONAL

    class Condition(models.TextChoices):
        Equal = "Equal"
        Contains = "Contains"
        Greater = "Greater"
        GreaterEqual = "GreaterEqual"

    expression = models.CharField(max_length=1024, help_text="Expression to evaluate")
    condition = models.CharField(
        max_length=40,
        choices=Condition.choices,
        help_text="Condition to evaluate",
    )
    is_reverse = models.BooleanField(default=False, help_text="Is reverse?")


class SwitchComponent(Component):
    """Use this method to create a switch component. Returns True on success."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.type = Component.ComponentType.CONDITIONAL

    expression = models.CharField(max_length=1024, help_text="Expression to evaluate")
    values = ArrayField(
        models.CharField(max_length=1024),
        help_text="Values to evaluate",
    )


class CodeComponent(Component):
    """Use this method to create a code component. Returns True on success."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.type = Component.ComponentType.CODE

    code = models.TextField(help_text="Code to execute", null=False, blank=False)


class OnMessage(Component):
    """Trigger component that executes when a text message is received."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.type = Component.ComponentType.TRIGGER
        self.component_type = Component.ComponentType.TRIGGER

    text = models.CharField(
        null=True,
        blank=True,
        max_length=4096,
        help_text="Optional text pattern to match against incoming messages. If not specified, matches any text message.",
    )
    regex = models.BooleanField(
        default=False,
        help_text="Whether to treat the text pattern as a regular expression",
    )
    case_sensitive = models.BooleanField(
        default=False,
        help_text="Whether the text matching should be case sensitive",
    )


class OnCallbackQuery(Component):
    """Trigger component that executes when a callback query is received."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.type = Component.ComponentType.TRIGGER

    data = models.CharField(
        null=True,
        blank=True,
        max_length=64,
        help_text="Optional callback data pattern to match against incoming callback queries. If not specified, matches any callback query.",
    )
    regex = models.BooleanField(
        default=False,
        help_text="Whether to treat the data pattern as a regular expression",
    )
    case_sensitive = models.BooleanField(
        default=False,
        help_text="Whether the data matching should be case sensitive",
    )
