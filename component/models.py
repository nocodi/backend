from typing import Any

from component.telegram.models import *


class SwitchComponent(Component):
    """Use this method to create a switch component. Returns True on success."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.type = Component.ComponentType.CONDITIONAL
        self.component_type = Component.ComponentType.CONDITIONAL

    expression = models.CharField(max_length=1024, help_text="Expression to evaluate")
    values = ArrayField(
        models.CharField(max_length=1024),
        help_text="Values to evaluate",
    )
    next_components = ArrayField(models.IntegerField())

    # class Meta:
    #     constraints = [
    #         models.CheckConstraint(
    #             condition=models.Q(
    #                 models.functions.Length("next_components")
    #                 == models.functions.Length("values"),
    #             ),
    #             name="check_next_components_length",
    #         ),
    #     ]

    def generate_code(self) -> str:
        dict_key = ""
        code = [
            f"async def {self.code_function_name}(message: Message, **kwargs):",
            f"    value = message{self.expression}",
            f"    match value:",
        ]
        for i in range(len(self.values)):
            value = self.values[i]
            next_component = self.next_components[i]
            code += [
                f"        case {value}:",
                f"            await {next_component.code_function_name}(message, **kwargs)",
            ]
        return code

    @property
    def required_fields(self) -> list:
        return ["expression", "values"]


class CodeComponent(Component):
    """Use this method to create a code component. Returns True on success."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.type = Component.ComponentType.CODE
        self.component_type = Component.ComponentType.CODE

    code = models.TextField(help_text="Code to execute", null=True, blank=True)

    @property
    def required_fields(self) -> list:
        return ["code"]

    def _format_code_component(self, underlying_object) -> list[str]:
        try:
            import black

            formatted_code = black.format_str(underlying_object.code, mode=black.Mode())
            return [f"    {formatted_code}"]
        except Exception as e:
            return [
                f"    # Original code failed black formatting: {str(e)}",
                f"    # {underlying_object.code}",
                "    pass",
            ]

    def generate_code(self) -> str:
        code = [
            f"async def {self.code_function_name}(message: Message, **kwargs):",
            *self._format_code_component(self),
        ]
        return "\n".join(code)


class SetState(Component):
    """Use this method to set a state. Returns True on success."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.type = Component.ComponentType.STATE
        self.component_type = Component.ComponentType.STATE

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
                assert isinstance(button, dict)
                assert "value" in button
                assert isinstance(button["value"], str)

    def get_callback_data(self, cell: str) -> str:
        value = cell.get("value").replace(" ", "_")
        return f"{self.parent_component.id}-{value}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.validate()
        super().save(*args, **kwargs)

    def _get_markup_config(self) -> tuple[str, str, str]:
        """Returns the configuration for the markup type."""
        match self.markup_type:
            case self.MarkupType.ReplyKeyboard:
                return (
                    "ReplyKeyboardMarkup",
                    "KeyboardButton",
                    "resize_keyboard=True, one_time_keyboard=False, keyboard",
                )
            case self.MarkupType.InlineKeyboard:
                return "InlineKeyboardMarkup", "InlineKeyboardButton", "inline_keyboard"
            case _:
                raise NotImplementedError(f"Unknown markup {self.markup_type}")

    def _generate_button_args(self, cell: dict) -> dict:
        """Generates the arguments for a button."""
        args = {"text": cell["value"]}
        if self.markup_type == self.MarkupType.InlineKeyboard:
            args["callback_data"] = self.get_callback_data(cell)
        return args

    def _generate_button_code(self, button_class: str, args: dict) -> str:
        """Generates the code for a single button."""
        button_lines = [f"{button_class}("]
        for k, v in args.items():
            button_lines.append(f'    {k} = "{v}",')
        button_lines.append("),")
        return "\n".join(button_lines)

    def _generate_callback_handlers(self, cell: dict) -> tuple[list[str], list[str]]:
        """Generates callback handlers for a cell if needed."""
        base_code = []
        callback_code = []

        first_next_component = cell.get("next_component")
        if not first_next_component:
            return base_code, callback_code

        object = (
            Component.objects.get(id=first_next_component)
            .component_content_type.model_class()
            .objects.get(pk=first_next_component)
        )

        if self.markup_type == self.MarkupType.InlineKeyboard:
            callback_code.extend(
                [
                    f"@dp.callback_query(lambda callback_query: callback_query.data == '{self.get_callback_data(cell)}')",
                    f"async def test(callback_query: CallbackQuery, **kwargs):"
                    f"    await {object.code_function_name}(callback_query, **kwargs)",
                ],
            )
        else:
            callback_code.extend(
                [
                    f"@dp.message(F.text == '{cell['value']}')",
                    f"async def test(message: Message, **kwargs):"
                    f"    await {object.code_function_name}(message, **kwargs)",
                ],
            )
        for next_component in Component.objects.get(
            id=first_next_component,
        ).get_all_next_components():
            object = next_component.component_content_type.model_class().objects.get(
                pk=next_component.pk,
            )
            base_code.append(object.generate_code())

        return base_code, callback_code

    def generate_code(self) -> tuple[str, list[str]]:
        """Generates the keyboard markup code and callback handlers."""
        base_code = []
        callback_code = []

        keyword_class, button_class, variable_name = self._get_markup_config()

        keyboard_rows = []
        for row in self.buttons:
            row_buttons = []
            for cell in row:
                cell_base_code, cell_callback_code = self._generate_callback_handlers(
                    cell,
                )
                base_code.extend(cell_base_code)
                callback_code.extend(cell_callback_code)

                button_args = self._generate_button_args(cell)
                row_buttons.append(
                    self._generate_button_code(button_class, button_args),
                )

            keyboard_rows.append("[\n" + "".join(row_buttons) + "\n]")

        keyboard_buttons = "[\n" + ",\n".join(keyboard_rows) + "\n]"
        keyboard = f"{keyword_class}({variable_name} = {keyboard_buttons})"

        callback_code.append("\n\n")
        base_code.extend(callback_code)
        return keyboard, "\n".join(base_code)
