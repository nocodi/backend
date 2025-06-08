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

    code = models.TextField(help_text="Code to execute", null=True, blank=True)

    @property
    def required_fields(self) -> list:
        return ["code"]


class SetState(Component):
    """Use this method to set a state. Returns True on success."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.type = Component.ComponentType.STATE

    state = models.CharField(
        null=True,
        blank=True,
        max_length=4096,
        help_text="Name of state. Should not contain comma",
    )

    @property
    def required_fields(self) -> list:
        return ["state"]

    def generate_code(self) -> str:

        underlying_object: (
            SetState
        ) = self.component_content_type.model_class().objects.get(
            pk=self.pk,
        )

        code = [
            f"async def {self.code_function_name}(message: Message, **kwargs):",
            f"    await kwargs['state'].set_state('{underlying_object.state}')",
        ]

        for next_component in underlying_object.next_component.all():
            next_component = (
                next_component.component_content_type.model_class().objects.get(
                    pk=next_component.pk,
                )
            )
            code.append(
                f"    await {next_component.code_function_name}(message, **kwargs)",
            )

        return "\n".join(code)


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
    state = models.CharField(
        null=True,
        blank=True,
        max_length=4096,
        help_text="Optional comma separated list of states to match. If not specified, matches any state.",
    )

    def generate_code(self) -> str:

        underlying_object: (
            OnMessage
        ) = self.component_content_type.model_class().objects.get(
            pk=self.pk,
        )
        if underlying_object.next_component.count() == 0:
            return ""

        filters = []
        if underlying_object.text:
            if underlying_object.regex:
                filters.append(f"regexp=re.compile(r'{underlying_object.text})'")
            else:
                filters.append(
                    f"F.text{'.lower()' if underlying_object.case_sensitive else ''} == '{underlying_object.text}'",
                )
        if underlying_object.state:
            state_list = [f"'{s.strip()}'" for s in underlying_object.state.split(",")]
            filters.append(
                f"lambda _, raw_state: raw_state in [{','.join(state_list)}]",
            )

        code = [
            f"@dp.message({','.join(filters)})",
            f"async def {self.code_function_name}(message: Message, **kwargs):",
        ]

        for next_component in underlying_object.next_component.all():
            next_component = (
                next_component.component_content_type.model_class().objects.get(
                    pk=next_component.pk,
                )
            )
            code.append(
                f"    await {next_component.code_function_name}(message, **kwargs)",
            )
        return "\n".join(code)


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


class Markup(models.Model):
    parent_component = models.OneToOneField(
        "component.Component",
        on_delete=models.CASCADE,
        related_name="markup",
    )

    class MarkupType(models.TextChoices):
        InlineKeyboard = "InlineKeyboard"
        ReplyKeyboard = "ReplyKeyboard"

    markup_type = models.CharField(
        max_length=20,
        choices=MarkupType.choices,
        help_text="Markup type",
    )
    buttons = models.JSONField(help_text="Buttons to use")

    def validate(self) -> None:
        buttons = self.buttons
        assert isinstance(buttons, list)
        for row in buttons:
            assert isinstance(row, list)
            for button in row:
                assert isinstance(button, str)

    def get_callback_data(self, cell: str) -> str:
        return f"{self.prent_component.id}-{cell}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.validate()
        super().save(*args, **kwargs)
