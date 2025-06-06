from typing import List

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Q
from django.forms.models import model_to_dict


class Keyboard(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass


class InlineKeyboardButton(models.Model):
    text = models.CharField(max_length=255, help_text="Text of the button")
    url = models.URLField(
        null=True,
        blank=True,
        help_text="Optional. HTTP or tg:// URL to be opened when the button is pressed. Links tg://user?id=<user_id> can be used to mention a user by their ID without using a username, if this is allowed by their privacy settings.",
    )
    callback_data = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Optional. Data to be sent in a callback query to the bot when the button is pressed, 1-64 bytes",
    )


class InlineKeyboardMarkup(Keyboard):
    inline_keyboard = models.ManyToManyField(
        InlineKeyboardButton,
        related_name="inline_keyboards",
        help_text="Array of button rows, each represented by an Array of InlineKeyboardButton objects",
    )

    def __str__(self) -> str:
        return f"InlineKeyboardMarkup ({self.inline_keyboard.count()} rows)"


class KeyboardButton(models.Model):
    text = models.CharField(max_length=255, help_text="Text of the button")
    request_contact = models.BooleanField(
        default=False,
        help_text="Optional. If True, the user's phone number will be sent as a contact when the button is pressed. Available in private chats only.",
    )
    request_location = models.BooleanField(
        default=False,
        help_text="Optional. If True, the user's current location will be sent when the button is pressed. Available in private chats only.",
    )


class ReplyKeyboardMarkup(Keyboard):
    keyboard = models.ManyToManyField(
        KeyboardButton,
        related_name="reply_keyboards",
        help_text="Array of button rows, each represented by an Array of KeyboardButton objects",
    )
    is_persistent = models.BooleanField(
        default=False,
        help_text="Optional. Requests clients to always show the keyboard when the user opens the chat. Defaults to false, in which case the custom keyboard disappears after one use",
    )
    resize_keyboard = models.BooleanField(
        default=False,
        help_text="Requests clients to resize the keyboard vertically for optimal fit",
    )
    one_time_keyboard = models.BooleanField(
        default=False,
        help_text="Requests clients to hide the keyboard as soon as it's been used",
    )
    input_field_placeholder = models.CharField(
        max_length=255,
        help_text="Optional. The placeholder to be shown in the input field when the keyboard is active; 1-64 characters, 0-words",
    )
    selective = models.BooleanField(
        default=False,
        help_text="Optional. Use this parameter if you want to show the keyboard to specific users only. Targets: 1) users that are @mentioned in the text of the Message object; 2) if the bot's message is a reply to a message in the same chat and forum topic, sender of the original message.",
    )

    def __str__(self) -> str:
        return f"ReplyKeyboardMarkup ({self.keyboard.count()} rows)"


class ReplyKeyboardRemove(Keyboard):
    remove_keyboard = models.BooleanField(
        default=True,
        help_text="Requests clients to remove the custom keyboard (user will not be able to summon this keyboard; if you want to hide the keyboard from sight but keep it accessible, use one_time_keyboard in ReplyKeyboardMarkup)",
    )
    selective = models.BooleanField(
        default=False,
        help_text="Use this parameter if you want to remove the keyboard for specific users only",
    )

    def __str__(self) -> str:
        return "ReplyKeyboardRemove"


class ForceReply(Keyboard):
    force_reply = models.BooleanField(
        default=True,
        help_text="Shows reply interface to the user, as if they manually selected the bot's message and tapped 'Reply'",
    )
    input_field_placeholder = models.CharField(
        max_length=64,
        help_text="Optional. The placeholder to be shown in the input field when the reply is active; 1-64 characters",
    )
    selective = models.BooleanField(
        default=False,
        help_text="Use this parameter if you want to force reply from specific users only",
    )

    def __str__(self) -> str:
        return "ForceReply"


class Component(models.Model):
    class ComponentType(models.TextChoices):
        TELEGRAM = "TELEGRAM", "Telegram API Component"
        TRIGGER = "TRIGGER", "Trigger Component"
        CONDITIONAL = "CONDITIONAL", "Conditional Component"
        CODE = "CODE", "Code Component"

    component_type = models.CharField(
        max_length=20,
        choices=ComponentType.choices,
        default=ComponentType.TELEGRAM,
        help_text="Type of the component",
    )

    def save(self, *args: list, **kwargs: dict) -> None:
        """Automatically sets content type"""
        if self.pk is None:
            self.component_content_type = ContentType.objects.get(
                model=self.__class__.__name__.lower(),
            )
        super().save(*args, **kwargs)

    component_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    component_name = models.CharField(
        max_length=255,
        null=True,
    )  # in order to not interfere with some component 'name' field, I added redundant 'component'

    bot = models.ForeignKey("bot.Bot", on_delete=models.CASCADE)

    previous_component = models.ForeignKey(
        "Component",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="next_component",
    )

    position_x = models.FloatField(null=False, blank=False)
    position_y = models.FloatField(null=False, blank=False)

    def __str__(self) -> str:
        return self.component_name or "Empty Component"

    class Meta:
        pass

    @property
    def code_function_name(self) -> str:  # -> name of the function in generated code
        return f"{self.__class__.__name__.lower()}_{self.pk}"

    def _get_file_params(self, underlying_object) -> str:
        """Extract file parameters from the underlying object."""
        file_params = ""
        for field in underlying_object._meta.get_fields():
            if isinstance(field, models.FileField):
                file_instance = getattr(underlying_object, field.name)
                if file_instance and hasattr(file_instance, "url"):
                    full_url = f"{settings.SITE_URL}{file_instance.url}"
                    file_params = f"{field.name}='{full_url}'"
                    setattr(underlying_object, field.name, None)
        return file_params

    def _get_method_name(self, class_name: str) -> str:
        """Convert class name to method name format."""
        method = ""
        for c in class_name:
            if c.isupper():
                method += "_"
            method += c.lower()
        return method.lstrip("_")

    def _generate_keyboard_code(self, keyboard) -> list[str]:
        """Generate code for keyboard markup."""
        if not isinstance(keyboard, InlineKeyboardMarkup):
            return []

        code = ["    builder = InlineKeyboardBuilder()"]
        for k in keyboard.inline_keyboard.all():
            code.append(
                f"    builder.button(text='{k.text}', callback_data='{k.callback_data}')",
            )
        code.append("    keyboard = builder.as_markup()")
        return code

    def _format_code_component(self, underlying_object) -> list[str]:
        """Format code component using black formatter."""
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

    def _get_component_params(
        self,
        underlying_object,
        keyboard,
        file_params: str,
    ) -> str:
        """Generate parameter string for the component."""
        excluded_fields = {
            "id",
            "component_ptr",
            "component_ptr_id",
            "timestamp",
            "object_id",
            "component_type",
            "content_type",
            "component_content_type",
            "bot",
            "component_name",
            "previous_component",
            "position_x",
            "position_y",
        }

        component_data = model_to_dict(underlying_object, exclude=excluded_fields)
        param_strings = []

        for k, v in component_data.items():
            if v:
                if isinstance(v, str):
                    param_strings.append(
                        f"{k}=input_data{v}" if v.startswith(".") else f"{k}='{v}'",
                    )
                else:
                    param_strings.append(f"{k}={v}")

        if keyboard:
            param_strings.append("reply_markup=keyboard")
        if file_params:
            param_strings.append(file_params)

        return ", ".join(param_strings)

    def generate_code(self) -> str:
        """Generate code for the telegram component."""
        if self.component_type != Component.ComponentType.TELEGRAM:
            raise NotImplementedError

        underlying_object = self.component_content_type.model_class().objects.get(
            pk=self.pk,
        )
        file_params = self._get_file_params(underlying_object)
        method = self._get_method_name(underlying_object.__class__.__name__)

        code = [
            f"async def {underlying_object.code_function_name}(input_data: Message, **kwargs):",
        ]

        # Handle code component
        if underlying_object.__class__.__name__ == "CodeComponent":
            code.extend(self._format_code_component(underlying_object))
            return "\n".join(code)

        keyboard = None
        if underlying_object.markup.exists():
            markup = underlying_object.markup
            match markup.markup_type:
                case markup.MarkupType.ReplyKeyboard:
                    keyword_class = "ReplyKeyboardMarkup"
                    button_class = "KeyboardButton"
                case markup.MarkupType.InlineKeyboard:
                    keyword_class = "InlineKeyboardMarkup"
                    button_class = "InlineKeyboardButton"
                case _:
                    raise NotImplementedError(f"Unknown markup {markup.markup_type}")
            keyboard_buttons = "["
            for row in markup.buttons:
                keyboard_buttons += "[\n"

                for cell in row:
                    args = {"text": cell}
                    if markup.markup_type == Markup.MarkupType.InlineKeyboard:
                        args["callback_data"] = markup.get_callback_data(cell)

                    keyboard_buttons += f"{button_class}(\n"
                    for k, v in args.items():
                        keyboard_buttons += f"{k} = {v}\n"
                    keyboard_buttons += f")"

                keyboard_buttons += "]"
            keyboard_buttons += "]"
            keybord = f"{keyword_class}(resize_keyboard=True, one_time_keyboard=False, keyboard = {keyboard_buttons})"

        # Generate parameters and method call
        params_str = self._get_component_params(
            underlying_object,
            keyboard,
            file_params,
        )
        code.append(f"    await bot.{method}({params_str})")

        # Handle next components
        for next_component in underlying_object.next_component.all():
            next_component = (
                next_component.component_content_type.model_class().objects.get(
                    pk=next_component.pk,
                )
            )
            code.append(f"    await {next_component.code_function_name}(input_data, **kwargs)")

        return "\n".join(code)

    def get_all_next_components(self) -> List["Component"]:
        ans = {}
        stack = [self]
        while stack:
            current = stack.pop()
            if current.id not in ans:
                ans[current.id] = current
                for next_component in current.next_component.all():
                    if next_component.id not in ans:
                        stack.append(next_component)
        return list(ans.values())


class SendMessage(Component):
    """Use this method to send text messages. On success, the sent Message is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    text = models.CharField(
        null=True,
        blank=True,
        max_length=4096,
        help_text="Text of the message to be sent, 1-4096 characters after entities parsing",
    )
    parse_mode = models.CharField(
        null=True,
        blank=True,
        help_text="Mode for parsing entities in the message text. See formatting options for more details.",
    )
    disable_notification = models.BooleanField(
        null=True,
        blank=True,
        help_text="Sends the message silently. Users will receive a notification with no sound.",
    )
    protect_content = models.BooleanField(
        null=True,
        blank=True,
        help_text="Protects the contents of the sent message from forwarding and saving",
    )
    allow_paid_broadcast = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance",
    )
    message_effect_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the message effect to be added to the message; for private chats only",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="inlinekeyboardmarkup")
        | Q(model="replykeyboardmarkup")
        | Q(model="replykeyboardremove")
        | Q(model="forcereply"),
        null=True,
        blank=True,
        help_text="Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    @property
    def required_fields(self) -> list:
        return ["chat_id", "text"]


class ForwardMessage(Component):
    """Use this method to forward messages of any kind. Service messages and messages with protected content can't be forwarded. On success, the sent Message is returned."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    from_chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the chat where the original message was sent (or channel username in the format @channelusername)",
    )
    video_start_timestamp = models.IntegerField(
        null=True,
        blank=True,
        help_text="New start timestamp for the forwarded video in the message",
    )
    disable_notification = models.BooleanField(
        null=True,
        blank=True,
        help_text="Sends the message silently. Users will receive a notification with no sound.",
    )
    protect_content = models.BooleanField(
        null=True,
        blank=True,
        help_text="Protects the contents of the forwarded message from forwarding and saving",
    )
    message_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Message identifier in the chat specified in from_chat_id",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "from_chat_id", "message_id"]


class ForwardMessages(Component):
    """Use this method to forward multiple messages of any kind. If some of the specified messages can't be found or forwarded, they are skipped. Service messages and messages with protected content can't be forwarded. Album grouping is kept for forwarded messages. On success, an array of MessageId of the sent messages is returned."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    from_chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the chat where the original messages were sent (or channel username in the format @channelusername)",
    )
    message_ids = ArrayField(
        models.IntegerField(),
        default=list,
        null=True,
        blank=True,
        help_text="A JSON-serialized list of 1-100 identifiers of messages in the chat from_chat_id to forward. The identifiers must be specified in a strictly increasing order.",
    )
    disable_notification = models.BooleanField(
        null=True,
        blank=True,
        help_text="Sends the messages silently. Users will receive a notification with no sound.",
    )
    protect_content = models.BooleanField(
        null=True,
        blank=True,
        help_text="Protects the contents of the forwarded messages from forwarding and saving",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "from_chat_id", "message_ids"]


class CopyMessage(Component):
    """Use this method to copy messages of any kind. Service messages, paid media messages, giveaway messages, giveaway winners messages, and invoice messages can't be copied. A quiz poll can be copied only if the value of the field correct_option_id is known to the bot. The method is analogous to the method forwardMessage, but the copied message doesn't have a link to the original message. Returns the MessageId of the sent message on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    from_chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the chat where the original message was sent (or channel username in the format @channelusername)",
    )
    message_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Message identifier in the chat specified in from_chat_id",
    )
    video_start_timestamp = models.IntegerField(
        null=True,
        blank=True,
        help_text="New start timestamp for the copied video in the message",
    )
    caption = models.CharField(
        null=True,
        blank=True,
        max_length=1024,
        help_text="New caption for media, 0-1024 characters after entities parsing. If not specified, the original caption is kept",
    )
    parse_mode = models.CharField(
        null=True,
        blank=True,
        help_text="Mode for parsing entities in the new caption. See formatting options for more details.",
    )
    show_caption_above_media = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True, if the caption must be shown above the message media. Ignored if a new caption isn't specified.",
    )
    disable_notification = models.BooleanField(
        null=True,
        blank=True,
        help_text="Sends the message silently. Users will receive a notification with no sound.",
    )
    protect_content = models.BooleanField(
        null=True,
        blank=True,
        help_text="Protects the contents of the sent message from forwarding and saving",
    )
    allow_paid_broadcast = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="inlinekeyboardmarkup")
        | Q(model="replykeyboardmarkup")
        | Q(model="replykeyboardremove")
        | Q(model="forcereply"),
        null=True,
        blank=True,
        help_text="Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    @property
    def required_fields(self) -> list:
        return ["chat_id", "from_chat_id", "message_id"]


class CopyMessages(Component):
    """Use this method to copy messages of any kind. If some of the specified messages can't be found or copied, they are skipped. Service messages, paid media messages, giveaway messages, giveaway winners messages, and invoice messages can't be copied. A quiz poll can be copied only if the value of the field correct_option_id is known to the bot. The method is analogous to the method forwardMessages, but the copied messages don't have a link to the original message. Album grouping is kept for copied messages. On success, an array of MessageId of the sent messages is returned."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    from_chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the chat where the original messages were sent (or channel username in the format @channelusername)",
    )
    message_ids = ArrayField(
        models.IntegerField(),
        default=list,
        null=True,
        blank=True,
        help_text="A JSON-serialized list of 1-100 identifiers of messages in the chat from_chat_id to copy. The identifiers must be specified in a strictly increasing order.",
    )
    disable_notification = models.BooleanField(
        null=True,
        blank=True,
        help_text="Sends the messages silently. Users will receive a notification with no sound.",
    )
    protect_content = models.BooleanField(
        null=True,
        blank=True,
        help_text="Protects the contents of the sent messages from forwarding and saving",
    )
    remove_caption = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to copy the messages without their captions",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "from_chat_id", "message_ids"]


class SendPhoto(Component):
    """Use this method to send photos. On success, the sent Message is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    photo = models.FileField(
        upload_to="photo/",
        null=True,
        blank=True,
        help_text="Photo to send. Pass a file_id as String to send a photo that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a photo from the Internet, or upload a new photo using multipart/form-data. The photo must be at most 10 MB in size. The photo's width and height must not exceed 10000 in total. Width and height ratio must be at most 20. More information on Sending Files »",
    )
    caption = models.CharField(
        null=True,
        blank=True,
        max_length=1024,
        help_text="Photo caption (may also be used when resending photos by file_id), 0-1024 characters after entities parsing",
    )
    parse_mode = models.CharField(
        null=True,
        blank=True,
        help_text="Mode for parsing entities in the photo caption. See formatting options for more details.",
    )
    show_caption_above_media = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True, if the caption must be shown above the message media",
    )
    has_spoiler = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the photo needs to be covered with a spoiler animation",
    )
    disable_notification = models.BooleanField(
        null=True,
        blank=True,
        help_text="Sends the message silently. Users will receive a notification with no sound.",
    )
    protect_content = models.BooleanField(
        null=True,
        blank=True,
        help_text="Protects the contents of the sent message from forwarding and saving",
    )
    allow_paid_broadcast = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance",
    )
    message_effect_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the message effect to be added to the message; for private chats only",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="inlinekeyboardmarkup")
        | Q(model="replykeyboardmarkup")
        | Q(model="replykeyboardremove")
        | Q(model="forcereply"),
        null=True,
        blank=True,
        help_text="Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    @property
    def required_fields(self) -> list:
        return ["chat_id", "photo"]


class SendDocument(Component):
    """Use this method to send general files. On success, the sent Message is returned. Bots can currently send files of any type of up to 50 MB in size, this limit may be changed in the future."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    document = models.FileField(
        upload_to="document/",
        null=True,
        blank=True,
        help_text="File to send. Pass a file_id as String to send a file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data. More information on Sending Files »",
    )
    thumbnail = models.FileField(
        upload_to="thumbnail/",
        null=True,
        blank=True,
        help_text="Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass “attach://<file_attach_name>” if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files »",
    )
    caption = models.CharField(
        null=True,
        blank=True,
        max_length=1024,
        help_text="Document caption (may also be used when resending documents by file_id), 0-1024 characters after entities parsing",
    )
    parse_mode = models.CharField(
        null=True,
        blank=True,
        help_text="Mode for parsing entities in the document caption. See formatting options for more details.",
    )
    disable_content_type_detection = models.BooleanField(
        null=True,
        blank=True,
        help_text="Disables automatic server-side content type detection for files uploaded using multipart/form-data",
    )
    disable_notification = models.BooleanField(
        null=True,
        blank=True,
        help_text="Sends the message silently. Users will receive a notification with no sound.",
    )
    protect_content = models.BooleanField(
        null=True,
        blank=True,
        help_text="Protects the contents of the sent message from forwarding and saving",
    )
    allow_paid_broadcast = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance",
    )
    message_effect_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the message effect to be added to the message; for private chats only",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="inlinekeyboardmarkup")
        | Q(model="replykeyboardmarkup")
        | Q(model="replykeyboardremove")
        | Q(model="forcereply"),
        null=True,
        blank=True,
        help_text="Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    @property
    def required_fields(self) -> list:
        return ["chat_id", "document"]


class SendVideo(Component):
    """Use this method to send video files, Telegram clients support MPEG4 videos (other formats may be sent as Document). On success, the sent Message is returned. Bots can currently send video files of up to 50 MB in size, this limit may be changed in the future."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    video = models.FileField(
        upload_to="video/",
        null=True,
        blank=True,
        help_text="Video to send. Pass a file_id as String to send a video that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a video from the Internet, or upload a new video using multipart/form-data. More information on Sending Files »",
    )
    duration = models.IntegerField(
        null=True,
        blank=True,
        help_text="Duration of sent video in seconds",
    )
    width = models.IntegerField(null=True, blank=True, help_text="Video width")
    height = models.IntegerField(null=True, blank=True, help_text="Video height")
    thumbnail = models.FileField(
        upload_to="thumbnail/",
        null=True,
        blank=True,
        help_text="Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass “attach://<file_attach_name>” if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files »",
    )
    cover = models.FileField(
        upload_to="cover/",
        null=True,
        blank=True,
        help_text="Cover for the video in the message. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass “attach://<file_attach_name>” to upload a new one using multipart/form-data under <file_attach_name> name. More information on Sending Files »",
    )
    start_timestamp = models.IntegerField(
        null=True,
        blank=True,
        help_text="Start timestamp for the video in the message",
    )
    caption = models.CharField(
        null=True,
        blank=True,
        max_length=1024,
        help_text="Video caption (may also be used when resending videos by file_id), 0-1024 characters after entities parsing",
    )
    parse_mode = models.CharField(
        null=True,
        blank=True,
        help_text="Mode for parsing entities in the video caption. See formatting options for more details.",
    )
    show_caption_above_media = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True, if the caption must be shown above the message media",
    )
    has_spoiler = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the video needs to be covered with a spoiler animation",
    )
    supports_streaming = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the uploaded video is suitable for streaming",
    )
    disable_notification = models.BooleanField(
        null=True,
        blank=True,
        help_text="Sends the message silently. Users will receive a notification with no sound.",
    )
    protect_content = models.BooleanField(
        null=True,
        blank=True,
        help_text="Protects the contents of the sent message from forwarding and saving",
    )
    allow_paid_broadcast = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance",
    )
    message_effect_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the message effect to be added to the message; for private chats only",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="inlinekeyboardmarkup")
        | Q(model="replykeyboardmarkup")
        | Q(model="replykeyboardremove")
        | Q(model="forcereply"),
        null=True,
        blank=True,
        help_text="Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    @property
    def required_fields(self) -> list:
        return ["chat_id", "video"]


class SendAnimation(Component):
    """Use this method to send animation files (GIF or H.264/MPEG-4 AVC video without sound). On success, the sent Message is returned. Bots can currently send animation files of up to 50 MB in size, this limit may be changed in the future."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    animation = models.FileField(
        upload_to="animation/",
        null=True,
        blank=True,
        help_text="Animation to send. Pass a file_id as String to send an animation that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get an animation from the Internet, or upload a new animation using multipart/form-data. More information on Sending Files »",
    )
    duration = models.IntegerField(
        null=True,
        blank=True,
        help_text="Duration of sent animation in seconds",
    )
    width = models.IntegerField(null=True, blank=True, help_text="Animation width")
    height = models.IntegerField(null=True, blank=True, help_text="Animation height")
    thumbnail = models.FileField(
        upload_to="thumbnail/",
        null=True,
        blank=True,
        help_text="Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass “attach://<file_attach_name>” if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files »",
    )
    caption = models.CharField(
        null=True,
        blank=True,
        max_length=1024,
        help_text="Animation caption (may also be used when resending animation by file_id), 0-1024 characters after entities parsing",
    )
    parse_mode = models.CharField(
        null=True,
        blank=True,
        help_text="Mode for parsing entities in the animation caption. See formatting options for more details.",
    )
    show_caption_above_media = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True, if the caption must be shown above the message media",
    )
    has_spoiler = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the animation needs to be covered with a spoiler animation",
    )
    disable_notification = models.BooleanField(
        null=True,
        blank=True,
        help_text="Sends the message silently. Users will receive a notification with no sound.",
    )
    protect_content = models.BooleanField(
        null=True,
        blank=True,
        help_text="Protects the contents of the sent message from forwarding and saving",
    )
    allow_paid_broadcast = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance",
    )
    message_effect_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the message effect to be added to the message; for private chats only",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="inlinekeyboardmarkup")
        | Q(model="replykeyboardmarkup")
        | Q(model="replykeyboardremove")
        | Q(model="forcereply"),
        null=True,
        blank=True,
        help_text="Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    @property
    def required_fields(self) -> list:
        return ["chat_id", "animation"]


class SendVoice(Component):
    """Use this method to send audio files, if you want Telegram clients to display the file as a playable voice message. For this to work, your audio must be in an .OGG file encoded with OPUS, or in .MP3 format, or in .M4A format (other formats may be sent as Audio or Document). On success, the sent Message is returned. Bots can currently send voice messages of up to 50 MB in size, this limit may be changed in the future."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    voice = models.FileField(
        upload_to="voice/",
        null=True,
        blank=True,
        help_text="Audio file to send. Pass a file_id as String to send a file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data. More information on Sending Files »",
    )
    caption = models.CharField(
        null=True,
        blank=True,
        max_length=1024,
        help_text="Voice message caption, 0-1024 characters after entities parsing",
    )
    parse_mode = models.CharField(
        null=True,
        blank=True,
        help_text="Mode for parsing entities in the voice message caption. See formatting options for more details.",
    )
    duration = models.IntegerField(
        null=True,
        blank=True,
        help_text="Duration of the voice message in seconds",
    )
    disable_notification = models.BooleanField(
        null=True,
        blank=True,
        help_text="Sends the message silently. Users will receive a notification with no sound.",
    )
    protect_content = models.BooleanField(
        null=True,
        blank=True,
        help_text="Protects the contents of the sent message from forwarding and saving",
    )
    allow_paid_broadcast = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance",
    )
    message_effect_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the message effect to be added to the message; for private chats only",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="inlinekeyboardmarkup")
        | Q(model="replykeyboardmarkup")
        | Q(model="replykeyboardremove")
        | Q(model="forcereply"),
        null=True,
        blank=True,
        help_text="Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    @property
    def required_fields(self) -> list:
        return ["chat_id", "voice"]


class SendVideoNote(Component):
    """As of v.4.0, Telegram clients support rounded square MPEG4 videos of up to 1 minute long. Use this method to send video messages. On success, the sent Message is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    video_note = models.FileField(
        upload_to="video_note/",
        null=True,
        blank=True,
        help_text="Video note to send. Pass a file_id as String to send a video note that exists on the Telegram servers (recommended) or upload a new video using multipart/form-data. More information on Sending Files ». Sending video notes by a URL is currently unsupported",
    )
    duration = models.IntegerField(
        null=True,
        blank=True,
        help_text="Duration of sent video in seconds",
    )
    length = models.IntegerField(
        null=True,
        blank=True,
        help_text="Video width and height, i.e. diameter of the video message",
    )
    thumbnail = models.FileField(
        upload_to="thumbnail/",
        null=True,
        blank=True,
        help_text="Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass “attach://<file_attach_name>” if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More information on Sending Files »",
    )
    disable_notification = models.BooleanField(
        null=True,
        blank=True,
        help_text="Sends the message silently. Users will receive a notification with no sound.",
    )
    protect_content = models.BooleanField(
        null=True,
        blank=True,
        help_text="Protects the contents of the sent message from forwarding and saving",
    )
    allow_paid_broadcast = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance",
    )
    message_effect_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the message effect to be added to the message; for private chats only",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="inlinekeyboardmarkup")
        | Q(model="replykeyboardmarkup")
        | Q(model="replykeyboardremove")
        | Q(model="forcereply"),
        null=True,
        blank=True,
        help_text="Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    @property
    def required_fields(self) -> list:
        return ["chat_id", "video_note"]


class SendPaidMedia(Component):
    """Use this method to send paid media. On success, the sent Message is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername). If the chat is a channel, all Telegram Star proceeds from this media will be credited to the chat's balance. Otherwise, they will be credited to the bot's balance.",
    )
    star_count = models.IntegerField(
        null=True,
        blank=True,
        help_text="The number of Telegram Stars that must be paid to buy access to the media; 1-10000",
    )
    payload = models.CharField(
        null=True,
        blank=True,
        help_text="Bot-defined paid media payload, 0-128 bytes. This will not be displayed to the user, use it for your internal processes.",
    )
    caption = models.CharField(
        null=True,
        blank=True,
        max_length=1024,
        help_text="Media caption, 0-1024 characters after entities parsing",
    )
    parse_mode = models.CharField(
        null=True,
        blank=True,
        help_text="Mode for parsing entities in the media caption. See formatting options for more details.",
    )
    show_caption_above_media = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True, if the caption must be shown above the message media",
    )
    disable_notification = models.BooleanField(
        null=True,
        blank=True,
        help_text="Sends the message silently. Users will receive a notification with no sound.",
    )
    protect_content = models.BooleanField(
        null=True,
        blank=True,
        help_text="Protects the contents of the sent message from forwarding and saving",
    )
    allow_paid_broadcast = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="inlinekeyboardmarkup")
        | Q(model="replykeyboardmarkup")
        | Q(model="replykeyboardremove")
        | Q(model="forcereply"),
        null=True,
        blank=True,
        help_text="Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    @property
    def required_fields(self) -> list:
        return ["chat_id", "star_count", "media"]


class SendMediaGroup(Component):
    """Use this method to send a group of photos, videos, documents or audios as an album. Documents and audio files can be only grouped in an album with messages of the same type. On success, an array of Messages that were sent is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    disable_notification = models.BooleanField(
        null=True,
        blank=True,
        help_text="Sends messages silently. Users will receive a notification with no sound.",
    )
    protect_content = models.BooleanField(
        null=True,
        blank=True,
        help_text="Protects the contents of the sent messages from forwarding and saving",
    )
    allow_paid_broadcast = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance",
    )
    message_effect_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the message effect to be added to the message; for private chats only",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "media"]


class SendLocation(Component):
    """Use this method to send point on the map. On success, the sent Message is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    latitude = models.FloatField(
        null=True,
        blank=True,
        help_text="Latitude of the location",
    )
    longitude = models.FloatField(
        null=True,
        blank=True,
        help_text="Longitude of the location",
    )
    horizontal_accuracy = models.FloatField(
        null=True,
        blank=True,
        help_text="The radius of uncertainty for the location, measured in meters; 0-1500",
    )
    live_period = models.IntegerField(
        null=True,
        blank=True,
        help_text="Period in seconds during which the location will be updated (see Live Locations, should be between 60 and 86400, or 0x7FFFFFFF for live locations that can be edited indefinitely.",
    )
    heading = models.IntegerField(
        null=True,
        blank=True,
        help_text="For live locations, a direction in which the user is moving, in degrees. Must be between 1 and 360 if specified.",
    )
    proximity_alert_radius = models.IntegerField(
        null=True,
        blank=True,
        help_text="For live locations, a maximum distance for proximity alerts about approaching another chat member, in meters. Must be between 1 and 100000 if specified.",
    )
    disable_notification = models.BooleanField(
        null=True,
        blank=True,
        help_text="Sends the message silently. Users will receive a notification with no sound.",
    )
    protect_content = models.BooleanField(
        null=True,
        blank=True,
        help_text="Protects the contents of the sent message from forwarding and saving",
    )
    allow_paid_broadcast = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance",
    )
    message_effect_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the message effect to be added to the message; for private chats only",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="inlinekeyboardmarkup")
        | Q(model="replykeyboardmarkup")
        | Q(model="replykeyboardremove")
        | Q(model="forcereply"),
        null=True,
        blank=True,
        help_text="Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    @property
    def required_fields(self) -> list:
        return ["chat_id", "latitude", "longitude"]


class SendVenue(Component):
    """Use this method to send information about a venue. On success, the sent Message is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    latitude = models.FloatField(
        null=True,
        blank=True,
        help_text="Latitude of the venue",
    )
    longitude = models.FloatField(
        null=True,
        blank=True,
        help_text="Longitude of the venue",
    )
    title = models.CharField(null=True, blank=True, help_text="Name of the venue")
    address = models.CharField(null=True, blank=True, help_text="Address of the venue")
    foursquare_id = models.CharField(
        null=True,
        blank=True,
        help_text="Foursquare identifier of the venue",
    )
    foursquare_type = models.CharField(
        null=True,
        blank=True,
        help_text="Foursquare type of the venue, if known. (For example, “arts_entertainment/default”, “arts_entertainment/aquarium” or “food/icecream”.)",
    )
    google_place_id = models.CharField(
        null=True,
        blank=True,
        help_text="Google Places identifier of the venue",
    )
    google_place_type = models.CharField(
        null=True,
        blank=True,
        help_text="Google Places type of the venue. (See supported types.)",
    )
    disable_notification = models.BooleanField(
        null=True,
        blank=True,
        help_text="Sends the message silently. Users will receive a notification with no sound.",
    )
    protect_content = models.BooleanField(
        null=True,
        blank=True,
        help_text="Protects the contents of the sent message from forwarding and saving",
    )
    allow_paid_broadcast = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance",
    )
    message_effect_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the message effect to be added to the message; for private chats only",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="inlinekeyboardmarkup")
        | Q(model="replykeyboardmarkup")
        | Q(model="replykeyboardremove")
        | Q(model="forcereply"),
        null=True,
        blank=True,
        help_text="Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    @property
    def required_fields(self) -> list:
        return ["chat_id", "latitude", "longitude", "title", "address"]


class SendContact(Component):
    """Use this method to send phone contacts. On success, the sent Message is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    phone_number = models.CharField(
        null=True,
        blank=True,
        help_text="Contact's phone number",
    )
    first_name = models.CharField(
        null=True,
        blank=True,
        help_text="Contact's first name",
    )
    last_name = models.CharField(null=True, blank=True, help_text="Contact's last name")
    vcard = models.CharField(
        null=True,
        blank=True,
        help_text="Additional data about the contact in the form of a vCard, 0-2048 bytes",
    )
    disable_notification = models.BooleanField(
        null=True,
        blank=True,
        help_text="Sends the message silently. Users will receive a notification with no sound.",
    )
    protect_content = models.BooleanField(
        null=True,
        blank=True,
        help_text="Protects the contents of the sent message from forwarding and saving",
    )
    allow_paid_broadcast = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance",
    )
    message_effect_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the message effect to be added to the message; for private chats only",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="inlinekeyboardmarkup")
        | Q(model="replykeyboardmarkup")
        | Q(model="replykeyboardremove")
        | Q(model="forcereply"),
        null=True,
        blank=True,
        help_text="Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    @property
    def required_fields(self) -> list:
        return ["chat_id", "phone_number", "first_name"]


class SendPoll(Component):
    """Use this method to send a native poll. On success, the sent Message is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    question = models.CharField(
        null=True,
        blank=True,
        max_length=300,
        help_text="Poll question, 1-300 characters",
    )
    question_parse_mode = models.CharField(
        null=True,
        blank=True,
        help_text="Mode for parsing entities in the question. See formatting options for more details. Currently, only custom emoji entities are allowed",
    )
    is_anonymous = models.BooleanField(
        null=True,
        blank=True,
        help_text="True, if the poll needs to be anonymous, defaults to True",
    )
    type = models.CharField(
        null=True,
        blank=True,
        help_text="Poll type, “quiz” or “regular”, defaults to “regular”",
    )
    allows_multiple_answers = models.BooleanField(
        null=True,
        blank=True,
        help_text="True, if the poll allows multiple answers, ignored for polls in quiz mode, defaults to False",
    )
    correct_option_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="0-based identifier of the correct answer option, required for polls in quiz mode",
    )
    explanation = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        help_text="Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style poll, 0-200 characters with at most 2 line feeds after entities parsing",
    )
    explanation_parse_mode = models.CharField(
        null=True,
        blank=True,
        help_text="Mode for parsing entities in the explanation. See formatting options for more details.",
    )
    open_period = models.IntegerField(
        null=True,
        blank=True,
        help_text="Amount of time in seconds the poll will be active after creation, 5-600. Can't be used together with close_date.",
    )
    close_date = models.IntegerField(
        null=True,
        blank=True,
        help_text="Point in time (Unix timestamp) when the poll will be automatically closed. Must be at least 5 and no more than 600 seconds in the future. Can't be used together with open_period.",
    )
    is_closed = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the poll needs to be immediately closed. This can be useful for poll preview.",
    )
    disable_notification = models.BooleanField(
        null=True,
        blank=True,
        help_text="Sends the message silently. Users will receive a notification with no sound.",
    )
    protect_content = models.BooleanField(
        null=True,
        blank=True,
        help_text="Protects the contents of the sent message from forwarding and saving",
    )
    allow_paid_broadcast = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance",
    )
    message_effect_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the message effect to be added to the message; for private chats only",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="inlinekeyboardmarkup")
        | Q(model="replykeyboardmarkup")
        | Q(model="replykeyboardremove")
        | Q(model="forcereply"),
        null=True,
        blank=True,
        help_text="Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    @property
    def required_fields(self) -> list:
        return ["chat_id", "question", "options"]


class SendDice(Component):
    """Use this method to send an animated emoji that will display a random value. On success, the sent Message is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    emoji = models.CharField(
        null=True,
        blank=True,
        help_text="Emoji on which the dice throw animation is based. Currently, must be one of “”, “”, “”, “”, “”, or “”. Dice can have values 1-6 for “”, “” and “”, values 1-5 for “” and “”, and values 1-64 for “”. Defaults to “”",
    )
    disable_notification = models.BooleanField(
        null=True,
        blank=True,
        help_text="Sends the message silently. Users will receive a notification with no sound.",
    )
    protect_content = models.BooleanField(
        null=True,
        blank=True,
        help_text="Protects the contents of the sent message from forwarding",
    )
    allow_paid_broadcast = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance",
    )
    message_effect_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the message effect to be added to the message; for private chats only",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="inlinekeyboardmarkup")
        | Q(model="replykeyboardmarkup")
        | Q(model="replykeyboardremove")
        | Q(model="forcereply"),
        null=True,
        blank=True,
        help_text="Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    @property
    def required_fields(self) -> list:
        return ["chat_id"]


class SetMessageReaction(Component):
    """Use this method to change the chosen reactions on a message. Service messages of some types can't be reacted to. Automatically forwarded messages from a channel to its discussion group have the same available reactions as messages in the channel. Bots can't use paid reactions. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Identifier of the target message. If the message belongs to a media group, the reaction is set to the first non-deleted message in the group instead.",
    )
    is_big = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to set the reaction with a big animation",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "message_id"]


class GetUserProfilePhotos(Component):
    """Use this method to get a list of profile pictures for a user. Returns a UserProfilePhotos object."""

    user_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier of the target user",
    )
    offset = models.IntegerField(
        null=True,
        blank=True,
        help_text="Sequential number of the first photo to be returned. By default, all photos are returned.",
    )
    limit = models.IntegerField(
        null=True,
        blank=True,
        help_text="Limits the number of photos to be retrieved. Values between 1-100 are accepted. Defaults to 100.",
    )

    @property
    def required_fields(self) -> list:
        return ["user_id"]


class SetUserEmojiStatus(Component):
    """Changes the emoji status for a given user that previously allowed the bot to manage their emoji status via the Mini App method requestEmojiStatusAccess. Returns True on success."""

    user_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier of the target user",
    )
    emoji_status_custom_emoji_id = models.CharField(
        null=True,
        blank=True,
        help_text="Custom emoji identifier of the emoji status to set. Pass an empty string to remove the status.",
    )
    emoji_status_expiration_date = models.IntegerField(
        null=True,
        blank=True,
        help_text="Expiration date of the emoji status, if any",
    )

    @property
    def required_fields(self) -> list:
        return ["user_id"]


class GetFile(Component):
    """Use this method to get basic information about a file and prepare it for downloading. For the moment, bots can download files of up to 20MB in size. On success, a File object is returned. The file can then be downloaded via the link https://api.telegram.org/file/bot<token>/<file_path>, where <file_path> is taken from the response. It is guaranteed that the link will be valid for at least 1 hour. When the link expires, a new one can be requested by calling getFile again."""

    file_id = models.CharField(
        null=True,
        blank=True,
        help_text="File identifier to get information about",
    )

    @property
    def required_fields(self) -> list:
        return ["file_id"]


class BanChatMember(Component):
    """Use this method to ban a user in a group, a supergroup or a channel. In the case of supergroups and channels, the user will not be able to return to the chat on their own using invite links, etc., unless unbanned first. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target group or username of the target supergroup or channel (in the format @channelusername)",
    )
    user_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier of the target user",
    )
    until_date = models.IntegerField(
        null=True,
        blank=True,
        help_text="Date when the user will be unbanned; Unix time. If user is banned for more than 366 days or less than 30 seconds from the current time they are considered to be banned forever. Applied for supergroups and channels only.",
    )
    revoke_messages = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to delete all messages from the chat for the user that is being removed. If False, the user will be able to see messages in the group that were sent before the user was removed. Always True for supergroups and channels.",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "user_id"]


class UnbanChatMember(Component):
    """Use this method to unban a previously banned user in a supergroup or channel. The user will not return to the group or channel automatically, but will be able to join via link, etc. The bot must be an administrator for this to work. By default, this method guarantees that after the call the user is not a member of the chat, but will be able to join it. So if the user is a member of the chat they will also be removed from the chat. If you don't want this, use the parameter only_if_banned. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target group or username of the target supergroup or channel (in the format @channelusername)",
    )
    user_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier of the target user",
    )
    only_if_banned = models.BooleanField(
        null=True,
        blank=True,
        help_text="Do nothing if the user is not banned",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "user_id"]


class RestrictChatMember(Component):
    """Use this method to restrict a user in a supergroup. The bot must be an administrator in the supergroup for this to work and must have the appropriate administrator rights. Pass True for all permissions to lift restrictions from a user. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )
    user_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier of the target user",
    )
    use_independent_chat_permissions = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if chat permissions are set independently. Otherwise, the can_send_other_messages and can_add_web_page_previews permissions will imply the can_send_messages, can_send_audios, can_send_documents, can_send_photos, can_send_videos, can_send_video_notes, and can_send_voice_notes permissions; the can_send_polls permission will imply the can_send_messages permission.",
    )
    until_date = models.IntegerField(
        null=True,
        blank=True,
        help_text="Date when restrictions will be lifted for the user; Unix time. If user is restricted for more than 366 days or less than 30 seconds from the current time, they are considered to be restricted forever",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "user_id", "permissions"]


class PromoteChatMember(Component):
    """Use this method to promote or demote a user in a supergroup or a channel. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Pass False for all boolean parameters to demote a user. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    user_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier of the target user",
    )
    is_anonymous = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the administrator's presence in the chat is hidden",
    )
    can_manage_chat = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the administrator can access the chat event log, get boost list, see hidden supergroup and channel members, report spam messages and ignore slow mode. Implied by any other administrator privilege.",
    )
    can_delete_messages = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the administrator can delete messages of other users",
    )
    can_manage_video_chats = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the administrator can manage video chats",
    )
    can_restrict_members = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the administrator can restrict, ban or unban chat members, or access supergroup statistics",
    )
    can_promote_members = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the administrator can add new administrators with a subset of their own privileges or demote administrators that they have promoted, directly or indirectly (promoted by administrators that were appointed by him)",
    )
    can_change_info = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the administrator can change chat title, photo and other settings",
    )
    can_invite_users = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the administrator can invite new users to the chat",
    )
    can_post_stories = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the administrator can post stories to the chat",
    )
    can_edit_stories = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the administrator can edit stories posted by other users, post stories to the chat page, pin chat stories, and access the chat's story archive",
    )
    can_delete_stories = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the administrator can delete stories posted by other users",
    )
    can_post_messages = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the administrator can post messages in the channel, or access channel statistics; for channels only",
    )
    can_edit_messages = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the administrator can edit messages of other users and can pin messages; for channels only",
    )
    can_pin_messages = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the administrator can pin messages; for supergroups only",
    )
    can_manage_topics = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the user is allowed to create, rename, close, and reopen forum topics; for supergroups only",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "user_id"]


class SetChatAdministratorCustomTitle(Component):
    """Use this method to set a custom title for an administrator in a supergroup promoted by the bot. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )
    user_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier of the target user",
    )
    custom_title = models.CharField(
        null=True,
        blank=True,
        max_length=16,
        help_text="New custom title for the administrator; 0-16 characters, emoji are not allowed",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "user_id", "custom_title"]


class BanChatSenderChat(Component):
    """Use this method to ban a channel chat in a supergroup or a channel. Until the chat is unbanned, the owner of the banned chat won't be able to send messages on behalf of any of their channels. The bot must be an administrator in the supergroup or channel for this to work and must have the appropriate administrator rights. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    sender_chat_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier of the target sender chat",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "sender_chat_id"]


class UnbanChatSenderChat(Component):
    """Use this method to unban a previously banned channel chat in a supergroup or channel. The bot must be an administrator for this to work and must have the appropriate administrator rights. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    sender_chat_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier of the target sender chat",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "sender_chat_id"]


class SetChatPermissions(Component):
    """Use this method to set default chat permissions for all members. The bot must be an administrator in the group or a supergroup for this to work and must have the can_restrict_members administrator rights. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )
    use_independent_chat_permissions = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if chat permissions are set independently. Otherwise, the can_send_other_messages and can_add_web_page_previews permissions will imply the can_send_messages, can_send_audios, can_send_documents, can_send_photos, can_send_videos, can_send_video_notes, and can_send_voice_notes permissions; the can_send_polls permission will imply the can_send_messages permission.",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "permissions"]


class ExportChatInviteLink(Component):
    """Use this method to generate a new primary invite link for a chat; any previously generated primary link is revoked. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns the new invite link as String on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id"]


class CreateChatInviteLink(Component):
    """Use this method to create an additional invite link for a chat. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. The link can be revoked using the method revokeChatInviteLink. Returns the new invite link as ChatInviteLink object."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    name = models.CharField(
        null=True,
        blank=True,
        max_length=32,
        help_text="Invite link name; 0-32 characters",
    )
    expire_date = models.IntegerField(
        null=True,
        blank=True,
        help_text="Point in time (Unix timestamp) when the link will expire",
    )
    member_limit = models.IntegerField(
        null=True,
        blank=True,
        help_text="The maximum number of users that can be members of the chat simultaneously after joining the chat via this invite link; 1-99999",
    )
    creates_join_request = models.BooleanField(
        null=True,
        blank=True,
        help_text="True, if users joining the chat via the link need to be approved by chat administrators. If True, member_limit can't be specified",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id"]


class EditChatInviteLink(Component):
    """Use this method to edit a non-primary invite link created by the bot. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns the edited invite link as a ChatInviteLink object."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    invite_link = models.CharField(
        null=True,
        blank=True,
        help_text="The invite link to edit",
    )
    name = models.CharField(
        null=True,
        blank=True,
        max_length=32,
        help_text="Invite link name; 0-32 characters",
    )
    expire_date = models.IntegerField(
        null=True,
        blank=True,
        help_text="Point in time (Unix timestamp) when the link will expire",
    )
    member_limit = models.IntegerField(
        null=True,
        blank=True,
        help_text="The maximum number of users that can be members of the chat simultaneously after joining the chat via this invite link; 1-99999",
    )
    creates_join_request = models.BooleanField(
        null=True,
        blank=True,
        help_text="True, if users joining the chat via the link need to be approved by chat administrators. If True, member_limit can't be specified",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "invite_link"]


class CreateChatSubscriptionInviteLink(Component):
    """Use this method to create a subscription invite link for a channel chat. The bot must have the can_invite_users administrator rights. The link can be edited using the method editChatSubscriptionInviteLink or revoked using the method revokeChatInviteLink. Returns the new invite link as a ChatInviteLink object."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target channel chat or username of the target channel (in the format @channelusername)",
    )
    name = models.CharField(
        null=True,
        blank=True,
        max_length=32,
        help_text="Invite link name; 0-32 characters",
    )
    subscription_period = models.IntegerField(
        null=True,
        blank=True,
        help_text="The number of seconds the subscription will be active for before the next payment. Currently, it must always be 2592000 (30 days).",
    )
    subscription_price = models.IntegerField(
        null=True,
        blank=True,
        help_text="The amount of Telegram Stars a user must pay initially and after each subsequent subscription period to be a member of the chat; 1-10000",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "subscription_period", "subscription_price"]


class EditChatSubscriptionInviteLink(Component):
    """Use this method to edit a subscription invite link created by the bot. The bot must have the can_invite_users administrator rights. Returns the edited invite link as a ChatInviteLink object."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    invite_link = models.CharField(
        null=True,
        blank=True,
        help_text="The invite link to edit",
    )
    name = models.CharField(
        null=True,
        blank=True,
        max_length=32,
        help_text="Invite link name; 0-32 characters",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "invite_link"]


class RevokeChatInviteLink(Component):
    """Use this method to revoke an invite link created by the bot. If the primary link is revoked, a new link is automatically generated. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns the revoked invite link as ChatInviteLink object."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the target chat or username of the target channel (in the format @channelusername)",
    )
    invite_link = models.CharField(
        null=True,
        blank=True,
        help_text="The invite link to revoke",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "invite_link"]


class ApproveChatJoinRequest(Component):
    """Use this method to approve a chat join request. The bot must be an administrator in the chat for this to work and must have the can_invite_users administrator right. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    user_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier of the target user",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "user_id"]


class DeclineChatJoinRequest(Component):
    """Use this method to decline a chat join request. The bot must be an administrator in the chat for this to work and must have the can_invite_users administrator right. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    user_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier of the target user",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "user_id"]


class SetChatPhoto(Component):
    """Use this method to set a new profile photo for the chat. Photos can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "photo"]


class DeleteChatPhoto(Component):
    """Use this method to delete a chat photo. Photos can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id"]


class SetChatTitle(Component):
    """Use this method to change the title of a chat. Titles can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    title = models.CharField(
        null=True,
        blank=True,
        max_length=128,
        help_text="New chat title, 1-128 characters",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "title"]


class SetChatDescription(Component):
    """Use this method to change the description of a group, a supergroup or a channel. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    description = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text="New chat description, 0-255 characters",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id"]


class PinChatMessage(Component):
    """Use this method to add a message to the list of pinned messages in a chat. If the chat is not a private chat, the bot must be an administrator in the chat for this to work and must have the 'can_pin_messages' administrator right in a supergroup or 'can_edit_messages' administrator right in a channel. Returns True on success."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be pinned",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Identifier of a message to pin",
    )
    disable_notification = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if it is not necessary to send a notification to all chat members about the new pinned message. Notifications are always disabled in channels and private chats.",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "message_id"]


class UnpinChatMessage(Component):
    """Use this method to remove a message from the list of pinned messages in a chat. If the chat is not a private chat, the bot must be an administrator in the chat for this to work and must have the 'can_pin_messages' administrator right in a supergroup or 'can_edit_messages' administrator right in a channel. Returns True on success."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be unpinned",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Identifier of the message to unpin. Required if business_connection_id is specified. If not specified, the most recent pinned message (by sending date) will be unpinned.",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id"]


class UnpinAllChatMessages(Component):
    """Use this method to clear the list of pinned messages in a chat. If the chat is not a private chat, the bot must be an administrator in the chat for this to work and must have the 'can_pin_messages' administrator right in a supergroup or 'can_edit_messages' administrator right in a channel. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id"]


class LeaveChat(Component):
    """Use this method for your bot to leave a group, supergroup or channel. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id"]


class GetChat(Component):
    """Use this method to get up-to-date information about the chat. Returns a ChatFullInfo object on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id"]


class GetChatAdministrators(Component):
    """Use this method to get a list of administrators in a chat, which aren't bots. Returns an Array of ChatMember objects."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id"]


class GetChatMemberCount(Component):
    """Use this method to get the number of members in a chat. Returns Int on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id"]


class GetChatMember(Component):
    """Use this method to get information about a member of a chat. The method is only guaranteed to work for other users if the bot is an administrator in the chat. Returns a ChatMember object on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)",
    )
    user_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier of the target user",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "user_id"]


class SetChatStickerSet(Component):
    """Use this method to set a new group sticker set for a supergroup. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Use the field can_set_sticker_set optionally returned in getChat requests to check if the bot can use this method. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )
    sticker_set_name = models.CharField(
        null=True,
        blank=True,
        help_text="Name of the sticker set to be set as the group sticker set",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "sticker_set_name"]


class DeleteChatStickerSet(Component):
    """Use this method to delete a group sticker set from a supergroup. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Use the field can_set_sticker_set optionally returned in getChat requests to check if the bot can use this method. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id"]


class CreateForumTopic(Component):
    """Use this method to create a topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights. Returns information about the created topic as a ForumTopic object."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )
    name = models.CharField(
        null=True,
        blank=True,
        max_length=128,
        help_text="Topic name, 1-128 characters",
    )
    icon_color = models.IntegerField(
        null=True,
        blank=True,
        help_text="Color of the topic icon in RGB format. Currently, must be one of 7322096 (0x6FB9F0), 16766590 (0xFFD67E), 13338331 (0xCB86DB), 9367192 (0x8EEE98), 16749490 (0xFF93B2), or 16478047 (0xFB6F5F)",
    )
    icon_custom_emoji_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the custom emoji shown as the topic icon. Use getForumTopicIconStickers to get all allowed custom emoji identifiers.",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "name"]


class EditForumTopic(Component):
    """Use this method to edit name and icon of a topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights, unless it is the creator of the topic. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread of the forum topic",
    )
    name = models.CharField(
        null=True,
        blank=True,
        max_length=128,
        help_text="New topic name, 0-128 characters. If not specified or empty, the current name of the topic will be kept",
    )
    icon_custom_emoji_id = models.CharField(
        null=True,
        blank=True,
        help_text="New unique identifier of the custom emoji shown as the topic icon. Use getForumTopicIconStickers to get all allowed custom emoji identifiers. Pass an empty string to remove the icon. If not specified, the current icon will be kept",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "message_thread_id"]


class CloseForumTopic(Component):
    """Use this method to close an open topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights, unless it is the creator of the topic. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread of the forum topic",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "message_thread_id"]


class ReopenForumTopic(Component):
    """Use this method to reopen a closed topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights, unless it is the creator of the topic. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread of the forum topic",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "message_thread_id"]


class DeleteForumTopic(Component):
    """Use this method to delete a forum topic along with all its messages in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_delete_messages administrator rights. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread of the forum topic",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "message_thread_id"]


class UnpinAllForumTopicMessages(Component):
    """Use this method to clear the list of pinned messages in a forum topic. The bot must be an administrator in the chat for this to work and must have the can_pin_messages administrator right in the supergroup. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread of the forum topic",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "message_thread_id"]


class EditGeneralForumTopic(Component):
    """Use this method to edit the name of the 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )
    name = models.CharField(
        null=True,
        blank=True,
        max_length=128,
        help_text="New topic name, 1-128 characters",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "name"]


class CloseGeneralForumTopic(Component):
    """Use this method to close an open 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id"]


class ReopenGeneralForumTopic(Component):
    """Use this method to reopen a closed 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights. The topic will be automatically unhidden if it was hidden. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id"]


class HideGeneralForumTopic(Component):
    """Use this method to hide the 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights. The topic will be automatically closed if it was open. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id"]


class UnhideGeneralForumTopic(Component):
    """Use this method to unhide the 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id"]


class UnpinAllGeneralForumTopicMessages(Component):
    """Use this method to clear the list of pinned messages in a General forum topic. The bot must be an administrator in the chat for this to work and must have the can_pin_messages administrator right in the supergroup. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id"]


class GetUserChatBoosts(Component):
    """Use this method to get the list of boosts added to a chat by a user. Requires administrator rights in the chat. Returns a UserChatBoosts object."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the chat or username of the channel (in the format @channelusername)",
    )
    user_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier of the target user",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "user_id"]


class GetBusinessConnection(Component):
    """Use this method to get information about the connection of the bot with a business account. Returns a BusinessConnection object on success."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection",
    )

    @property
    def required_fields(self) -> list:
        return ["business_connection_id"]


class SetMyCommands(Component):
    """Use this method to change the list of the bot's commands. See this manual for more details about bot commands. Returns True on success."""

    language_code = models.CharField(
        null=True,
        blank=True,
        help_text="A two-letter ISO 639-1 language code. If empty, commands will be applied to all users from the given scope, for whose language there are no dedicated commands",
    )

    @property
    def required_fields(self) -> list:
        return ["commands"]


class DeleteMyCommands(Component):
    """Use this method to delete the list of the bot's commands for the given scope and user language. After deletion, higher level commands will be shown to affected users. Returns True on success."""

    language_code = models.CharField(
        null=True,
        blank=True,
        help_text="A two-letter ISO 639-1 language code. If empty, commands will be applied to all users from the given scope, for whose language there are no dedicated commands",
    )

    @property
    def required_fields(self) -> list:
        return []


class GetMyCommands(Component):
    """Use this method to get the current list of the bot's commands for the given scope and user language. Returns an Array of BotCommand objects. If commands aren't set, an empty list is returned."""

    language_code = models.CharField(
        null=True,
        blank=True,
        help_text="A two-letter ISO 639-1 language code or an empty string",
    )

    @property
    def required_fields(self) -> list:
        return []


class SetMyName(Component):
    """Use this method to change the bot's name. Returns True on success."""

    name = models.CharField(
        null=True,
        blank=True,
        max_length=64,
        help_text="New bot name; 0-64 characters. Pass an empty string to remove the dedicated name for the given language.",
    )
    language_code = models.CharField(
        null=True,
        blank=True,
        help_text="A two-letter ISO 639-1 language code. If empty, the name will be shown to all users for whose language there is no dedicated name.",
    )

    @property
    def required_fields(self) -> list:
        return []


class GetMyName(Component):
    """Use this method to get the current bot name for the given user language. Returns BotName on success."""

    language_code = models.CharField(
        null=True,
        blank=True,
        help_text="A two-letter ISO 639-1 language code or an empty string",
    )

    @property
    def required_fields(self) -> list:
        return []


class SetMyDescription(Component):
    """Use this method to change the bot's description, which is shown in the chat with the bot if the chat is empty. Returns True on success."""

    description = models.CharField(
        null=True,
        blank=True,
        max_length=512,
        help_text="New bot description; 0-512 characters. Pass an empty string to remove the dedicated description for the given language.",
    )
    language_code = models.CharField(
        null=True,
        blank=True,
        help_text="A two-letter ISO 639-1 language code. If empty, the description will be applied to all users for whose language there is no dedicated description.",
    )

    @property
    def required_fields(self) -> list:
        return []


class GetMyDescription(Component):
    """Use this method to get the current bot description for the given user language. Returns BotDescription on success."""

    language_code = models.CharField(
        null=True,
        blank=True,
        help_text="A two-letter ISO 639-1 language code or an empty string",
    )

    @property
    def required_fields(self) -> list:
        return []


class SetMyShortDescription(Component):
    """Use this method to change the bot's short description, which is shown on the bot's profile page and is sent together with the link when users share the bot. Returns True on success."""

    short_description = models.CharField(
        null=True,
        blank=True,
        max_length=120,
        help_text="New short description for the bot; 0-120 characters. Pass an empty string to remove the dedicated short description for the given language.",
    )
    language_code = models.CharField(
        null=True,
        blank=True,
        help_text="A two-letter ISO 639-1 language code. If empty, the short description will be applied to all users for whose language there is no dedicated short description.",
    )

    @property
    def required_fields(self) -> list:
        return []


class GetMyShortDescription(Component):
    """Use this method to get the current bot short description for the given user language. Returns BotShortDescription on success."""

    language_code = models.CharField(
        null=True,
        blank=True,
        help_text="A two-letter ISO 639-1 language code or an empty string",
    )

    @property
    def required_fields(self) -> list:
        return []


class SetChatMenuButton(Component):
    """Use this method to change the bot's menu button in a private chat, or the default menu button. Returns True on success."""

    chat_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target private chat. If not specified, default bot's menu button will be changed",
    )

    @property
    def required_fields(self) -> list:
        return []


class GetChatMenuButton(Component):
    """Use this method to get the current value of the bot's menu button in a private chat, or the default menu button. Returns MenuButton on success."""

    chat_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target private chat. If not specified, default bot's menu button will be returned",
    )

    @property
    def required_fields(self) -> list:
        return []


class SetMyDefaultAdministratorRights(Component):
    """Use this method to change the default administrator rights requested by the bot when it's added as an administrator to groups or channels. These rights will be suggested to users, but they are free to modify the list before adding the bot. Returns True on success."""

    for_channels = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to change the default administrator rights of the bot in channels. Otherwise, the default administrator rights of the bot for groups and supergroups will be changed.",
    )

    @property
    def required_fields(self) -> list:
        return []


class GetMyDefaultAdministratorRights(Component):
    """Use this method to get the current default administrator rights of the bot. Returns ChatAdministratorRights on success."""

    for_channels = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to get default administrator rights of the bot in channels. Otherwise, default administrator rights of the bot for groups and supergroups will be returned.",
    )

    @property
    def required_fields(self) -> list:
        return []


class EditMessageText(Component):
    """Use this method to edit text and game messages. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message to be edited was sent",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Required if inline_message_id is not specified. Identifier of the message to edit",
    )
    inline_message_id = models.CharField(
        null=True,
        blank=True,
        help_text="Required if chat_id and message_id are not specified. Identifier of the inline message",
    )
    text = models.CharField(
        null=True,
        blank=True,
        max_length=4096,
        help_text="New text of the message, 1-4096 characters after entities parsing",
    )
    parse_mode = models.CharField(
        null=True,
        blank=True,
        help_text="Mode for parsing entities in the message text. See formatting options for more details.",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="inlinekeyboardmarkup"),
        null=True,
        blank=True,
        help_text="A JSON-serialized object for an inline keyboard.",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    @property
    def required_fields(self) -> list:
        return ["text"]


class EditMessageCaption(Component):
    """Use this method to edit captions of messages. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message to be edited was sent",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Required if inline_message_id is not specified. Identifier of the message to edit",
    )
    inline_message_id = models.CharField(
        null=True,
        blank=True,
        help_text="Required if chat_id and message_id are not specified. Identifier of the inline message",
    )
    caption = models.CharField(
        null=True,
        blank=True,
        max_length=1024,
        help_text="New caption of the message, 0-1024 characters after entities parsing",
    )
    parse_mode = models.CharField(
        null=True,
        blank=True,
        help_text="Mode for parsing entities in the message caption. See formatting options for more details.",
    )
    show_caption_above_media = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True, if the caption must be shown above the message media. Supported only for animation, photo and video messages.",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="inlinekeyboardmarkup"),
        null=True,
        blank=True,
        help_text="A JSON-serialized object for an inline keyboard.",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    @property
    def required_fields(self) -> list:
        return []


class EditMessageMedia(Component):
    """Use this method to edit animation, audio, document, photo, or video messages, or to add media to text messages. If a message is part of a message album, then it can be edited only to an audio for audio albums, only to a document for document albums and to a photo or a video otherwise. When an inline message is edited, a new file can't be uploaded; use a previously uploaded file via its file_id or specify a URL. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message to be edited was sent",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Required if inline_message_id is not specified. Identifier of the message to edit",
    )
    inline_message_id = models.CharField(
        null=True,
        blank=True,
        help_text="Required if chat_id and message_id are not specified. Identifier of the inline message",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="inlinekeyboardmarkup"),
        null=True,
        blank=True,
        help_text="A JSON-serialized object for a new inline keyboard.",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    @property
    def required_fields(self) -> list:
        return ["media"]


class EditMessageLiveLocation(Component):
    """Use this method to edit live location messages. A location can be edited until its live_period expires or editing is explicitly disabled by a call to stopMessageLiveLocation. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message to be edited was sent",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Required if inline_message_id is not specified. Identifier of the message to edit",
    )
    inline_message_id = models.CharField(
        null=True,
        blank=True,
        help_text="Required if chat_id and message_id are not specified. Identifier of the inline message",
    )
    latitude = models.FloatField(
        null=True,
        blank=True,
        help_text="Latitude of new location",
    )
    longitude = models.FloatField(
        null=True,
        blank=True,
        help_text="Longitude of new location",
    )
    live_period = models.IntegerField(
        null=True,
        blank=True,
        help_text="New period in seconds during which the location can be updated, starting from the message send date. If 0x7FFFFFFF is specified, then the location can be updated forever. Otherwise, the new value must not exceed the current live_period by more than a day, and the live location expiration date must remain within the next 90 days. If not specified, then live_period remains unchanged",
    )
    horizontal_accuracy = models.FloatField(
        null=True,
        blank=True,
        help_text="The radius of uncertainty for the location, measured in meters; 0-1500",
    )
    heading = models.IntegerField(
        null=True,
        blank=True,
        help_text="Direction in which the user is moving, in degrees. Must be between 1 and 360 if specified.",
    )
    proximity_alert_radius = models.IntegerField(
        null=True,
        blank=True,
        help_text="The maximum distance for proximity alerts about approaching another chat member, in meters. Must be between 1 and 100000 if specified.",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="inlinekeyboardmarkup"),
        null=True,
        blank=True,
        help_text="A JSON-serialized object for a new inline keyboard.",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    @property
    def required_fields(self) -> list:
        return ["latitude", "longitude"]


class StopMessageLiveLocation(Component):
    """Use this method to stop updating a live location message before live_period expires. On success, if the message is not an inline message, the edited Message is returned, otherwise True is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message to be edited was sent",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Required if inline_message_id is not specified. Identifier of the message with live location to stop",
    )
    inline_message_id = models.CharField(
        null=True,
        blank=True,
        help_text="Required if chat_id and message_id are not specified. Identifier of the inline message",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="inlinekeyboardmarkup"),
        null=True,
        blank=True,
        help_text="A JSON-serialized object for a new inline keyboard.",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    @property
    def required_fields(self) -> list:
        return []


class EditMessageReplyMarkup(Component):
    """Use this method to edit only the reply markup of messages. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message to be edited was sent",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Required if inline_message_id is not specified. Identifier of the message to edit",
    )
    inline_message_id = models.CharField(
        null=True,
        blank=True,
        help_text="Required if chat_id and message_id are not specified. Identifier of the inline message",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="inlinekeyboardmarkup"),
        null=True,
        blank=True,
        help_text="A JSON-serialized object for an inline keyboard.",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    @property
    def required_fields(self) -> list:
        return []


class StopPoll(Component):
    """Use this method to stop a poll which was sent by the bot. On success, the stopped Poll is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message to be edited was sent",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Identifier of the original message with the poll",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="inlinekeyboardmarkup"),
        null=True,
        blank=True,
        help_text="A JSON-serialized object for a new message inline keyboard.",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    @property
    def required_fields(self) -> list:
        return ["chat_id", "message_id"]


class DeleteMessage(Component):
    """Use this method to delete a message, including service messages, with the following limitations:- A message can only be deleted if it was sent less than 48 hours ago.- Service messages about a supergroup, channel, or forum topic creation can't be deleted.- A dice message in a private chat can only be deleted if it was sent more than 24 hours ago.- Bots can delete outgoing messages in private chats, groups, and supergroups.- Bots can delete incoming messages in private chats.- Bots granted can_post_messages permissions can delete outgoing messages in channels.- If the bot is an administrator of a group, it can delete any message there.- If the bot has can_delete_messages permission in a supergroup or a channel, it can delete any message there.Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Identifier of the message to delete",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "message_id"]


class DeleteMessages(Component):
    """Use this method to delete multiple messages simultaneously. If some of the specified messages can't be found, they are skipped. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_ids = ArrayField(
        models.IntegerField(),
        default=list,
        null=True,
        blank=True,
        help_text="A JSON-serialized list of 1-100 identifiers of messages to delete. See deleteMessage for limitations on which messages can be deleted",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id", "message_ids"]


class SendGift(Component):
    """Sends a gift to the given user or channel chat. The gift can't be converted to Telegram Stars by the receiver. Returns True on success."""

    user_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Required if chat_id is not specified. Unique identifier of the target user who will receive the gift.",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Required if user_id is not specified. Unique identifier for the chat or username of the channel (in the format @channelusername) that will receive the gift.",
    )
    gift_id = models.CharField(
        null=True,
        blank=True,
        help_text="Identifier of the gift",
    )
    pay_for_upgrade = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to pay for the gift upgrade from the bot's balance, thereby making the upgrade free for the receiver",
    )
    text = models.CharField(
        null=True,
        blank=True,
        max_length=128,
        help_text="Text that will be shown along with the gift; 0-128 characters",
    )
    text_parse_mode = models.CharField(
        null=True,
        blank=True,
        help_text="Mode for parsing entities in the text. See formatting options for more details. Entities other than “bold”, “italic”, “underline”, “strikethrough”, “spoiler”, and “custom_emoji” are ignored.",
    )

    @property
    def required_fields(self) -> list:
        return ["gift_id"]


class GiftPremiumSubscription(Component):
    """Gifts a Telegram Premium subscription to the given user. Returns True on success."""

    user_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier of the target user who will receive a Telegram Premium subscription",
    )
    month_count = models.IntegerField(
        null=True,
        blank=True,
        help_text="Number of months the Telegram Premium subscription will be active for the user; must be one of 3, 6, or 12",
    )
    star_count = models.IntegerField(
        null=True,
        blank=True,
        help_text="Number of Telegram Stars to pay for the Telegram Premium subscription; must be 1000 for 3 months, 1500 for 6 months, and 2500 for 12 months",
    )
    text = models.CharField(
        null=True,
        blank=True,
        max_length=128,
        help_text="Text that will be shown along with the service message about the subscription; 0-128 characters",
    )
    text_parse_mode = models.CharField(
        null=True,
        blank=True,
        help_text="Mode for parsing entities in the text. See formatting options for more details. Entities other than “bold”, “italic”, “underline”, “strikethrough”, “spoiler”, and “custom_emoji” are ignored.",
    )

    @property
    def required_fields(self) -> list:
        return ["user_id", "month_count", "star_count"]


class VerifyUser(Component):
    """Verifies a user on behalf of the organization which is represented by the bot. Returns True on success."""

    user_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier of the target user",
    )
    custom_description = models.CharField(
        null=True,
        blank=True,
        max_length=70,
        help_text="Custom description for the verification; 0-70 characters. Must be empty if the organization isn't allowed to provide a custom verification description.",
    )

    @property
    def required_fields(self) -> list:
        return ["user_id"]


class VerifyChat(Component):
    """Verifies a chat on behalf of the organization which is represented by the bot. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    custom_description = models.CharField(
        null=True,
        blank=True,
        max_length=70,
        help_text="Custom description for the verification; 0-70 characters. Must be empty if the organization isn't allowed to provide a custom verification description.",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id"]


class RemoveUserVerification(Component):
    """Removes verification from a user who is currently verified on behalf of the organization represented by the bot. Returns True on success."""

    user_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier of the target user",
    )

    @property
    def required_fields(self) -> list:
        return ["user_id"]


class RemoveChatVerification(Component):
    """Removes verification from a chat that is currently verified on behalf of the organization represented by the bot. Returns True on success."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )

    @property
    def required_fields(self) -> list:
        return ["chat_id"]


class ReadBusinessMessage(Component):
    """Marks incoming message as read on behalf of a business account. Requires the can_read_messages business bot right. Returns True on success."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which to read the message",
    )
    chat_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier of the chat in which the message was received. The chat must have been active in the last 24 hours.",
    )
    message_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier of the message to mark as read",
    )

    @property
    def required_fields(self) -> list:
        return ["business_connection_id", "chat_id", "message_id"]


class DeleteBusinessMessages(Component):
    """Delete messages on behalf of a business account. Requires the can_delete_sent_messages business bot right to delete messages sent by the bot itself, or the can_delete_all_messages business bot right to delete any message. Returns True on success."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which to delete the messages",
    )
    message_ids = ArrayField(
        models.IntegerField(),
        default=list,
        null=True,
        blank=True,
        help_text="A JSON-serialized list of 1-100 identifiers of messages to delete. All messages must be from the same chat. See deleteMessage for limitations on which messages can be deleted",
    )

    @property
    def required_fields(self) -> list:
        return ["business_connection_id", "message_ids"]


class SetBusinessAccountName(Component):
    """Changes the first and last name of a managed business account. Requires the can_change_name business bot right. Returns True on success."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection",
    )
    first_name = models.CharField(
        null=True,
        blank=True,
        max_length=64,
        help_text="The new value of the first name for the business account; 1-64 characters",
    )
    last_name = models.CharField(
        null=True,
        blank=True,
        max_length=64,
        help_text="The new value of the last name for the business account; 0-64 characters",
    )

    @property
    def required_fields(self) -> list:
        return ["business_connection_id", "first_name"]


class SetBusinessAccountUsername(Component):
    """Changes the username of a managed business account. Requires the can_change_username business bot right. Returns True on success."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection",
    )
    username = models.CharField(
        null=True,
        blank=True,
        max_length=32,
        help_text="The new value of the username for the business account; 0-32 characters",
    )

    @property
    def required_fields(self) -> list:
        return ["business_connection_id"]


class SetBusinessAccountBio(Component):
    """Changes the bio of a managed business account. Requires the can_change_bio business bot right. Returns True on success."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection",
    )
    bio = models.CharField(
        null=True,
        blank=True,
        max_length=140,
        help_text="The new value of the bio for the business account; 0-140 characters",
    )

    @property
    def required_fields(self) -> list:
        return ["business_connection_id"]


class SetBusinessAccountProfilePhoto(Component):
    """Changes the profile photo of a managed business account. Requires the can_edit_profile_photo business bot right. Returns True on success."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection",
    )
    is_public = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to set the public photo, which will be visible even if the main photo is hidden by the business account's privacy settings. An account can have only one public photo.",
    )

    @property
    def required_fields(self) -> list:
        return ["business_connection_id", "photo"]


class RemoveBusinessAccountProfilePhoto(Component):
    """Removes the current profile photo of a managed business account. Requires the can_edit_profile_photo business bot right. Returns True on success."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection",
    )
    is_public = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to remove the public photo, which is visible even if the main photo is hidden by the business account's privacy settings. After the main photo is removed, the previous profile photo (if present) becomes the main photo.",
    )

    @property
    def required_fields(self) -> list:
        return ["business_connection_id"]


class SetBusinessAccountGiftSettings(Component):
    """Changes the privacy settings pertaining to incoming gifts in a managed business account. Requires the can_change_gift_settings business bot right. Returns True on success."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection",
    )
    show_gift_button = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True, if a button for sending a gift to the user or by the business account must always be shown in the input field",
    )

    @property
    def required_fields(self) -> list:
        return ["business_connection_id", "show_gift_button", "accepted_gift_types"]


class GetBusinessAccountStarBalance(Component):
    """Returns the amount of Telegram Stars owned by a managed business account. Requires the can_view_gifts_and_stars business bot right. Returns StarAmount on success."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection",
    )

    @property
    def required_fields(self) -> list:
        return ["business_connection_id"]


class TransferBusinessAccountStars(Component):
    """Transfers Telegram Stars from the business account balance to the bot's balance. Requires the can_transfer_stars business bot right. Returns True on success."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection",
    )
    star_count = models.IntegerField(
        null=True,
        blank=True,
        help_text="Number of Telegram Stars to transfer; 1-10000",
    )

    @property
    def required_fields(self) -> list:
        return ["business_connection_id", "star_count"]


class GetBusinessAccountGifts(Component):
    """Returns the gifts received and owned by a managed business account. Requires the can_view_gifts_and_stars business bot right. Returns OwnedGifts on success."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection",
    )
    exclude_unsaved = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to exclude gifts that aren't saved to the account's profile page",
    )
    exclude_saved = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to exclude gifts that are saved to the account's profile page",
    )
    exclude_unlimited = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to exclude gifts that can be purchased an unlimited number of times",
    )
    exclude_limited = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to exclude gifts that can be purchased a limited number of times",
    )
    exclude_unique = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to exclude unique gifts",
    )
    sort_by_price = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to sort results by gift price instead of send date. Sorting is applied before pagination.",
    )
    offset = models.CharField(
        null=True,
        blank=True,
        help_text="Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results",
    )
    limit = models.IntegerField(
        null=True,
        blank=True,
        help_text="The maximum number of gifts to be returned; 1-100. Defaults to 100",
    )

    @property
    def required_fields(self) -> list:
        return ["business_connection_id"]


class ConvertGiftToStars(Component):
    """Converts a given regular gift to Telegram Stars. Requires the can_convert_gifts_to_stars business bot right. Returns True on success."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection",
    )
    owned_gift_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the regular gift that should be converted to Telegram Stars",
    )

    @property
    def required_fields(self) -> list:
        return ["business_connection_id", "owned_gift_id"]


class UpgradeGift(Component):
    """Upgrades a given regular gift to a unique gift. Requires the can_transfer_and_upgrade_gifts business bot right. Additionally requires the can_transfer_stars business bot right if the upgrade is paid. Returns True on success."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection",
    )
    owned_gift_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the regular gift that should be upgraded to a unique one",
    )
    keep_original_details = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to keep the original gift text, sender and receiver in the upgraded gift",
    )
    star_count = models.IntegerField(
        null=True,
        blank=True,
        help_text="The amount of Telegram Stars that will be paid for the upgrade from the business account balance. If gift.prepaid_upgrade_star_count > 0, then pass 0, otherwise, the can_transfer_stars business bot right is required and gift.upgrade_star_count must be passed.",
    )

    @property
    def required_fields(self) -> list:
        return ["business_connection_id", "owned_gift_id"]


class TransferGift(Component):
    """Transfers an owned unique gift to another user. Requires the can_transfer_and_upgrade_gifts business bot right. Requires can_transfer_stars business bot right if the transfer is paid. Returns True on success."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection",
    )
    owned_gift_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the regular gift that should be transferred",
    )
    new_owner_chat_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier of the chat which will own the gift. The chat must be active in the last 24 hours.",
    )
    star_count = models.IntegerField(
        null=True,
        blank=True,
        help_text="The amount of Telegram Stars that will be paid for the transfer from the business account balance. If positive, then the can_transfer_stars business bot right is required.",
    )

    @property
    def required_fields(self) -> list:
        return ["business_connection_id", "owned_gift_id", "new_owner_chat_id"]


class PostStory(Component):
    """Posts a story on behalf of a managed business account. Requires the can_manage_stories business bot right. Returns Story on success."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection",
    )
    active_period = models.IntegerField(
        null=True,
        blank=True,
        help_text="Period after which the story is moved to the archive, in seconds; must be one of 6 * 3600, 12 * 3600, 86400, or 2 * 86400",
    )
    caption = models.CharField(
        null=True,
        blank=True,
        max_length=2048,
        help_text="Caption of the story, 0-2048 characters after entities parsing",
    )
    parse_mode = models.CharField(
        null=True,
        blank=True,
        help_text="Mode for parsing entities in the story caption. See formatting options for more details.",
    )
    post_to_chat_page = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to keep the story accessible after it expires",
    )
    protect_content = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the content of the story must be protected from forwarding and screenshotting",
    )

    @property
    def required_fields(self) -> list:
        return ["business_connection_id", "content", "active_period"]


class EditStory(Component):
    """Edits a story previously posted by the bot on behalf of a managed business account. Requires the can_manage_stories business bot right. Returns Story on success."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection",
    )
    story_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier of the story to edit",
    )
    caption = models.CharField(
        null=True,
        blank=True,
        max_length=2048,
        help_text="Caption of the story, 0-2048 characters after entities parsing",
    )
    parse_mode = models.CharField(
        null=True,
        blank=True,
        help_text="Mode for parsing entities in the story caption. See formatting options for more details.",
    )

    @property
    def required_fields(self) -> list:
        return ["business_connection_id", "story_id", "content"]


class DeleteStory(Component):
    """Deletes a story previously posted by the bot on behalf of a managed business account. Requires the can_manage_stories business bot right. Returns True on success."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection",
    )
    story_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier of the story to delete",
    )

    @property
    def required_fields(self) -> list:
        return ["business_connection_id", "story_id"]


class SendSticker(Component):
    """Use this method to send static .WEBP, animated .TGS, or video .WEBM stickers. On success, the sent Message is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    sticker = models.FileField(
        upload_to="sticker/",
        null=True,
        blank=True,
        help_text="Sticker to send. Pass a file_id as String to send a file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a .WEBP sticker from the Internet, or upload a new .WEBP, .TGS, or .WEBM sticker using multipart/form-data. More information on Sending Files ». Video and animated stickers can't be sent via an HTTP URL.",
    )
    emoji = models.CharField(
        null=True,
        blank=True,
        help_text="Emoji associated with the sticker; only for just uploaded stickers",
    )
    disable_notification = models.BooleanField(
        null=True,
        blank=True,
        help_text="Sends the message silently. Users will receive a notification with no sound.",
    )
    protect_content = models.BooleanField(
        null=True,
        blank=True,
        help_text="Protects the contents of the sent message from forwarding and saving",
    )
    allow_paid_broadcast = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance",
    )
    message_effect_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the message effect to be added to the message; for private chats only",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="inlinekeyboardmarkup")
        | Q(model="replykeyboardmarkup")
        | Q(model="replykeyboardremove")
        | Q(model="forcereply"),
        null=True,
        blank=True,
        help_text="Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    @property
    def required_fields(self) -> list:
        return ["chat_id", "sticker"]


class GetStickerSet(Component):
    """Use this method to get a sticker set. On success, a StickerSet object is returned."""

    name = models.CharField(null=True, blank=True, help_text="Name of the sticker set")

    @property
    def required_fields(self) -> list:
        return ["name"]


class GetCustomEmojiStickers(Component):
    """Use this method to get information about custom emoji stickers by their identifiers. Returns an Array of Sticker objects."""

    custom_emoji_ids = ArrayField(
        models.CharField(),
        default=list,
        null=True,
        blank=True,
        help_text="A JSON-serialized list of custom emoji identifiers. At most 200 custom emoji identifiers can be specified.",
    )

    @property
    def required_fields(self) -> list:
        return ["custom_emoji_ids"]


class UploadStickerFile(Component):
    """Use this method to upload a file with a sticker for later use in the createNewStickerSet, addStickerToSet, or replaceStickerInSet methods (the file can be used multiple times). Returns the uploaded File on success."""

    user_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="User identifier of sticker file owner",
    )
    sticker_format = models.CharField(
        null=True,
        blank=True,
        help_text="Format of the sticker, must be one of “static”, “animated”, “video”",
    )

    @property
    def required_fields(self) -> list:
        return ["user_id", "sticker", "sticker_format"]


class CreateNewStickerSet(Component):
    """Use this method to create a new sticker set owned by a user. The bot will be able to edit the sticker set thus created. Returns True on success."""

    user_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="User identifier of created sticker set owner",
    )
    name = models.CharField(
        null=True,
        blank=True,
        max_length=64,
        help_text='Short name of sticker set, to be used in t.me/addstickers/ URLs (e.g., animals). Can contain only English letters, digits and underscores. Must begin with a letter, can\'t contain consecutive underscores and must end in "_by_<bot_username>". <bot_username> is case insensitive. 1-64 characters.',
    )
    title = models.CharField(
        null=True,
        blank=True,
        max_length=64,
        help_text="Sticker set title, 1-64 characters",
    )
    sticker_type = models.CharField(
        null=True,
        blank=True,
        help_text="Type of stickers in the set, pass “regular”, “mask”, or “custom_emoji”. By default, a regular sticker set is created.",
    )
    needs_repainting = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if stickers in the sticker set must be repainted to the color of text when used in messages, the accent color if used as emoji status, white on chat photos, or another appropriate color based on context; for custom emoji sticker sets only",
    )

    @property
    def required_fields(self) -> list:
        return ["user_id", "name", "title", "stickers"]


class AddStickerToSet(Component):
    """Use this method to add a new sticker to a set created by the bot. Emoji sticker sets can have up to 200 stickers. Other sticker sets can have up to 120 stickers. Returns True on success."""

    user_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="User identifier of sticker set owner",
    )
    name = models.CharField(null=True, blank=True, help_text="Sticker set name")

    @property
    def required_fields(self) -> list:
        return ["user_id", "name", "sticker"]


class SetStickerPositionInSet(Component):
    """Use this method to move a sticker in a set created by the bot to a specific position. Returns True on success."""

    sticker = models.CharField(
        null=True,
        blank=True,
        help_text="File identifier of the sticker",
    )
    position = models.IntegerField(
        null=True,
        blank=True,
        help_text="New sticker position in the set, zero-based",
    )

    @property
    def required_fields(self) -> list:
        return ["sticker", "position"]


class DeleteStickerFromSet(Component):
    """Use this method to delete a sticker from a set created by the bot. Returns True on success."""

    sticker = models.CharField(
        null=True,
        blank=True,
        help_text="File identifier of the sticker",
    )

    @property
    def required_fields(self) -> list:
        return ["sticker"]


class ReplaceStickerInSet(Component):
    """Use this method to replace an existing sticker in a sticker set with a new one. The method is equivalent to calling deleteStickerFromSet, then addStickerToSet, then setStickerPositionInSet. Returns True on success."""

    user_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="User identifier of the sticker set owner",
    )
    name = models.CharField(null=True, blank=True, help_text="Sticker set name")
    old_sticker = models.CharField(
        null=True,
        blank=True,
        help_text="File identifier of the replaced sticker",
    )

    @property
    def required_fields(self) -> list:
        return ["user_id", "name", "old_sticker", "sticker"]


class SetStickerEmojiList(Component):
    """Use this method to change the list of emoji assigned to a regular or custom emoji sticker. The sticker must belong to a sticker set created by the bot. Returns True on success."""

    sticker = models.CharField(
        null=True,
        blank=True,
        help_text="File identifier of the sticker",
    )
    emoji_list = ArrayField(
        models.CharField(),
        default=list,
        null=True,
        blank=True,
        help_text="A JSON-serialized list of 1-20 emoji associated with the sticker",
    )

    @property
    def required_fields(self) -> list:
        return ["sticker", "emoji_list"]


class SetStickerKeywords(Component):
    """Use this method to change search keywords assigned to a regular or custom emoji sticker. The sticker must belong to a sticker set created by the bot. Returns True on success."""

    sticker = models.CharField(
        null=True,
        blank=True,
        help_text="File identifier of the sticker",
    )
    keywords = ArrayField(
        models.CharField(),
        default=list,
        null=True,
        blank=True,
        help_text="A JSON-serialized list of 0-20 search keywords for the sticker with total length of up to 64 characters",
    )

    @property
    def required_fields(self) -> list:
        return ["sticker"]


class SetStickerMaskPosition(Component):
    """Use this method to change the mask position of a mask sticker. The sticker must belong to a sticker set that was created by the bot. Returns True on success."""

    sticker = models.CharField(
        null=True,
        blank=True,
        help_text="File identifier of the sticker",
    )

    @property
    def required_fields(self) -> list:
        return ["sticker"]


class SetStickerSetTitle(Component):
    """Use this method to set the title of a created sticker set. Returns True on success."""

    name = models.CharField(null=True, blank=True, help_text="Sticker set name")
    title = models.CharField(
        null=True,
        blank=True,
        max_length=64,
        help_text="Sticker set title, 1-64 characters",
    )

    @property
    def required_fields(self) -> list:
        return ["name", "title"]


class SetStickerSetThumbnail(Component):
    """Use this method to set the thumbnail of a regular or mask sticker set. The format of the thumbnail file must match the format of the stickers in the set. Returns True on success."""

    name = models.CharField(null=True, blank=True, help_text="Sticker set name")
    user_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="User identifier of the sticker set owner",
    )
    thumbnail = models.FileField(
        upload_to="thumbnail/",
        null=True,
        blank=True,
        help_text="A .WEBP or .PNG image with the thumbnail, must be up to 128 kilobytes in size and have a width and height of exactly 100px, or a .TGS animation with a thumbnail up to 32 kilobytes in size (see https://core.telegram.org/stickers#animation-requirements for animated sticker technical requirements), or a .WEBM video with the thumbnail up to 32 kilobytes in size; see https://core.telegram.org/stickers#video-requirements for video sticker technical requirements. Pass a file_id as a String to send a file that already exists on the Telegram servers, pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data. More information on Sending Files ». Animated and video sticker set thumbnails can't be uploaded via HTTP URL. If omitted, then the thumbnail is dropped and the first sticker is used as the thumbnail.",
    )
    format = models.CharField(
        null=True,
        blank=True,
        help_text="Format of the thumbnail, must be one of “static” for a .WEBP or .PNG image, “animated” for a .TGS animation, or “video” for a .WEBM video",
    )

    @property
    def required_fields(self) -> list:
        return ["name", "user_id", "format"]


class SetCustomEmojiStickerSetThumbnail(Component):
    """Use this method to set the thumbnail of a custom emoji sticker set. Returns True on success."""

    name = models.CharField(null=True, blank=True, help_text="Sticker set name")
    custom_emoji_id = models.CharField(
        null=True,
        blank=True,
        help_text="Custom emoji identifier of a sticker from the sticker set; pass an empty string to drop the thumbnail and use the first sticker as the thumbnail.",
    )

    @property
    def required_fields(self) -> list:
        return ["name"]


class DeleteStickerSet(Component):
    """Use this method to delete a sticker set that was created by the bot. Returns True on success."""

    name = models.CharField(null=True, blank=True, help_text="Sticker set name")

    @property
    def required_fields(self) -> list:
        return ["name"]


class AnswerInlineQuery(Component):
    """Use this method to send answers to an inline query. On success, True is returned.No more than 50 results per query are allowed."""

    inline_query_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the answered query",
    )
    cache_time = models.IntegerField(
        null=True,
        blank=True,
        help_text="The maximum amount of time in seconds that the result of the inline query may be cached on the server. Defaults to 300.",
    )
    is_personal = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if results may be cached on the server side only for the user that sent the query. By default, results may be returned to any user who sends the same query.",
    )
    next_offset = models.CharField(
        null=True,
        blank=True,
        help_text="Pass the offset that a client should send in the next query with the same text to receive more results. Pass an empty string if there are no more results or if you don't support pagination. Offset length can't exceed 64 bytes.",
    )

    @property
    def required_fields(self) -> list:
        return ["inline_query_id", "results"]


class AnswerWebAppQuery(Component):
    """Use this method to set the result of an interaction with a Web App and send a corresponding message on behalf of the user to the chat from which the query originated. On success, a SentWebAppMessage object is returned."""

    web_app_query_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the query to be answered",
    )

    @property
    def required_fields(self) -> list:
        return ["web_app_query_id", "result"]


class SavePreparedInlineMessage(Component):
    """Stores a message that can be sent by a user of a Mini App. Returns a PreparedInlineMessage object."""

    user_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier of the target user that can use the prepared message",
    )
    allow_user_chats = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the message can be sent to private chats with users",
    )
    allow_bot_chats = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the message can be sent to private chats with bots",
    )
    allow_group_chats = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the message can be sent to group and supergroup chats",
    )
    allow_channel_chats = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the message can be sent to channel chats",
    )

    @property
    def required_fields(self) -> list:
        return ["user_id", "result"]


class SendInvoice(Component):
    """Use this method to send invoices. On success, the sent Message is returned."""

    chat_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    title = models.CharField(
        null=True,
        blank=True,
        max_length=32,
        help_text="Product name, 1-32 characters",
    )
    description = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text="Product description, 1-255 characters",
    )
    payload = models.CharField(
        null=True,
        blank=True,
        help_text="Bot-defined invoice payload, 1-128 bytes. This will not be displayed to the user, use it for your internal processes.",
    )
    provider_token = models.CharField(
        null=True,
        blank=True,
        help_text="Payment provider token, obtained via @BotFather. Pass an empty string for payments in Telegram Stars.",
    )
    currency = models.CharField(
        null=True,
        blank=True,
        help_text="Three-letter ISO 4217 currency code, see more on currencies. Pass “XTR” for payments in Telegram Stars.",
    )
    max_tip_amount = models.IntegerField(
        null=True,
        blank=True,
        help_text="The maximum accepted amount for tips in the smallest units of the currency (integer, not float/double). For example, for a maximum tip of US$ 1.45 pass max_tip_amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies). Defaults to 0. Not supported for payments in Telegram Stars.",
    )
    suggested_tip_amounts = ArrayField(
        models.IntegerField(),
        default=list,
        null=True,
        blank=True,
        help_text="A JSON-serialized array of suggested amounts of tips in the smallest units of the currency (integer, not float/double). At most 4 suggested tip amounts can be specified. The suggested tip amounts must be positive, passed in a strictly increased order and must not exceed max_tip_amount.",
    )
    start_parameter = models.CharField(
        null=True,
        blank=True,
        help_text="Unique deep-linking parameter. If left empty, forwarded copies of the sent message will have a Pay button, allowing multiple users to pay directly from the forwarded message, using the same invoice. If non-empty, forwarded copies of the sent message will have a URL button with a deep link to the bot (instead of a Pay button), with the value used as the start parameter",
    )
    provider_data = models.CharField(
        null=True,
        blank=True,
        help_text="JSON-serialized data about the invoice, which will be shared with the payment provider. A detailed description of required fields should be provided by the payment provider.",
    )
    photo_url = models.CharField(
        null=True,
        blank=True,
        help_text="URL of the product photo for the invoice. Can be a photo of the goods or a marketing image for a service. People like it better when they see what they are paying for.",
    )
    photo_size = models.IntegerField(
        null=True,
        blank=True,
        help_text="Photo size in bytes",
    )
    photo_width = models.IntegerField(null=True, blank=True, help_text="Photo width")
    photo_height = models.IntegerField(null=True, blank=True, help_text="Photo height")
    need_name = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if you require the user's full name to complete the order. Ignored for payments in Telegram Stars.",
    )
    need_phone_number = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if you require the user's phone number to complete the order. Ignored for payments in Telegram Stars.",
    )
    need_email = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if you require the user's email address to complete the order. Ignored for payments in Telegram Stars.",
    )
    need_shipping_address = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if you require the user's shipping address to complete the order. Ignored for payments in Telegram Stars.",
    )
    send_phone_number_to_provider = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the user's phone number should be sent to the provider. Ignored for payments in Telegram Stars.",
    )
    send_email_to_provider = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the user's email address should be sent to the provider. Ignored for payments in Telegram Stars.",
    )
    is_flexible = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the final price depends on the shipping method. Ignored for payments in Telegram Stars.",
    )
    disable_notification = models.BooleanField(
        null=True,
        blank=True,
        help_text="Sends the message silently. Users will receive a notification with no sound.",
    )
    protect_content = models.BooleanField(
        null=True,
        blank=True,
        help_text="Protects the contents of the sent message from forwarding and saving",
    )
    allow_paid_broadcast = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance",
    )
    message_effect_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the message effect to be added to the message; for private chats only",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="inlinekeyboardmarkup"),
        null=True,
        blank=True,
        help_text="A JSON-serialized object for an inline keyboard. If empty, one 'Pay total price' button will be shown. If not empty, the first button must be a Pay button.",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    @property
    def required_fields(self) -> list:
        return ["chat_id", "title", "description", "payload", "currency", "prices"]


class CreateInvoiceLink(Component):
    """Use this method to create a link for an invoice. Returns the created invoice link as String on success."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the link will be created. For payments in Telegram Stars only.",
    )
    title = models.CharField(
        null=True,
        blank=True,
        max_length=32,
        help_text="Product name, 1-32 characters",
    )
    description = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text="Product description, 1-255 characters",
    )
    payload = models.CharField(
        null=True,
        blank=True,
        help_text="Bot-defined invoice payload, 1-128 bytes. This will not be displayed to the user, use it for your internal processes.",
    )
    provider_token = models.CharField(
        null=True,
        blank=True,
        help_text="Payment provider token, obtained via @BotFather. Pass an empty string for payments in Telegram Stars.",
    )
    currency = models.CharField(
        null=True,
        blank=True,
        help_text="Three-letter ISO 4217 currency code, see more on currencies. Pass “XTR” for payments in Telegram Stars.",
    )
    subscription_period = models.IntegerField(
        null=True,
        blank=True,
        help_text="The number of seconds the subscription will be active for before the next payment. The currency must be set to “XTR” (Telegram Stars) if the parameter is used. Currently, it must always be 2592000 (30 days) if specified. Any number of subscriptions can be active for a given bot at the same time, including multiple concurrent subscriptions from the same user. Subscription price must no exceed 10000 Telegram Stars.",
    )
    max_tip_amount = models.IntegerField(
        null=True,
        blank=True,
        help_text="The maximum accepted amount for tips in the smallest units of the currency (integer, not float/double). For example, for a maximum tip of US$ 1.45 pass max_tip_amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies). Defaults to 0. Not supported for payments in Telegram Stars.",
    )
    suggested_tip_amounts = ArrayField(
        models.IntegerField(),
        default=list,
        null=True,
        blank=True,
        help_text="A JSON-serialized array of suggested amounts of tips in the smallest units of the currency (integer, not float/double). At most 4 suggested tip amounts can be specified. The suggested tip amounts must be positive, passed in a strictly increased order and must not exceed max_tip_amount.",
    )
    provider_data = models.CharField(
        null=True,
        blank=True,
        help_text="JSON-serialized data about the invoice, which will be shared with the payment provider. A detailed description of required fields should be provided by the payment provider.",
    )
    photo_url = models.CharField(
        null=True,
        blank=True,
        help_text="URL of the product photo for the invoice. Can be a photo of the goods or a marketing image for a service.",
    )
    photo_size = models.IntegerField(
        null=True,
        blank=True,
        help_text="Photo size in bytes",
    )
    photo_width = models.IntegerField(null=True, blank=True, help_text="Photo width")
    photo_height = models.IntegerField(null=True, blank=True, help_text="Photo height")
    need_name = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if you require the user's full name to complete the order. Ignored for payments in Telegram Stars.",
    )
    need_phone_number = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if you require the user's phone number to complete the order. Ignored for payments in Telegram Stars.",
    )
    need_email = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if you require the user's email address to complete the order. Ignored for payments in Telegram Stars.",
    )
    need_shipping_address = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if you require the user's shipping address to complete the order. Ignored for payments in Telegram Stars.",
    )
    send_phone_number_to_provider = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the user's phone number should be sent to the provider. Ignored for payments in Telegram Stars.",
    )
    send_email_to_provider = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the user's email address should be sent to the provider. Ignored for payments in Telegram Stars.",
    )
    is_flexible = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the final price depends on the shipping method. Ignored for payments in Telegram Stars.",
    )

    @property
    def required_fields(self) -> list:
        return ["title", "description", "payload", "currency", "prices"]


class AnswerShippingQuery(Component):
    """If you sent an invoice requesting a shipping address and the parameter is_flexible was specified, the Bot API will send an Update with a shipping_query field to the bot. Use this method to reply to shipping queries. On success, True is returned."""

    shipping_query_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the query to be answered",
    )
    ok = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if delivery to the specified address is possible and False if there are any problems (for example, if delivery to the specified address is not possible)",
    )
    error_message = models.CharField(
        null=True,
        blank=True,
        help_text="Required if ok is False. Error message in human readable form that explains why it is impossible to complete the order (e.g. “Sorry, delivery to your desired address is unavailable”). Telegram will display this message to the user.",
    )

    @property
    def required_fields(self) -> list:
        return ["shipping_query_id", "ok"]


class AnswerPreCheckoutQuery(Component):
    """Once the user has confirmed their payment and shipping details, the Bot API sends the final confirmation in the form of an Update with the field pre_checkout_query. Use this method to respond to such pre-checkout queries. On success, True is returned. Note: The Bot API must receive an answer within 10 seconds after the pre-checkout query was sent."""

    pre_checkout_query_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier for the query to be answered",
    )
    ok = models.BooleanField(
        null=True,
        blank=True,
        help_text="Specify True if everything is alright (goods are available, etc.) and the bot is ready to proceed with the order. Use False if there are any problems.",
    )
    error_message = models.CharField(
        null=True,
        blank=True,
        help_text='Required if ok is False. Error message in human readable form that explains the reason for failure to proceed with the checkout (e.g. "Sorry, somebody just bought the last of our amazing black T-shirts while you were busy filling out your payment details. Please choose a different color or garment!"). Telegram will display this message to the user.',
    )

    @property
    def required_fields(self) -> list:
        return ["pre_checkout_query_id", "ok"]


class GetStarTransactions(Component):
    """Returns the bot's Telegram Star transactions in chronological order. On success, returns a StarTransactions object."""

    offset = models.IntegerField(
        null=True,
        blank=True,
        help_text="Number of transactions to skip in the response",
    )
    limit = models.IntegerField(
        null=True,
        blank=True,
        help_text="The maximum number of transactions to be retrieved. Values between 1-100 are accepted. Defaults to 100.",
    )

    @property
    def required_fields(self) -> list:
        return []


class RefundStarPayment(Component):
    """Refunds a successful payment in Telegram Stars. Returns True on success."""

    user_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Identifier of the user whose payment will be refunded",
    )
    telegram_payment_charge_id = models.CharField(
        null=True,
        blank=True,
        help_text="Telegram payment identifier",
    )

    @property
    def required_fields(self) -> list:
        return ["user_id", "telegram_payment_charge_id"]


class EditUserStarSubscription(Component):
    """Allows the bot to cancel or re-enable extension of a subscription paid in Telegram Stars. Returns True on success."""

    user_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Identifier of the user whose subscription will be edited",
    )
    telegram_payment_charge_id = models.CharField(
        null=True,
        blank=True,
        help_text="Telegram payment identifier for the subscription",
    )
    is_canceled = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to cancel extension of the user subscription; the subscription must be active up to the end of the current subscription period. Pass False to allow the user to re-enable a subscription that was previously canceled by the bot.",
    )

    @property
    def required_fields(self) -> list:
        return ["user_id", "telegram_payment_charge_id", "is_canceled"]


class SendGame(Component):
    """Use this method to send a game. On success, the sent Message is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target chat",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    game_short_name = models.CharField(
        null=True,
        blank=True,
        help_text="Short name of the game, serves as the unique identifier for the game. Set up your games via @BotFather.",
    )
    disable_notification = models.BooleanField(
        null=True,
        blank=True,
        help_text="Sends the message silently. Users will receive a notification with no sound.",
    )
    protect_content = models.BooleanField(
        null=True,
        blank=True,
        help_text="Protects the contents of the sent message from forwarding and saving",
    )
    allow_paid_broadcast = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance",
    )
    message_effect_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the message effect to be added to the message; for private chats only",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="inlinekeyboardmarkup"),
        null=True,
        blank=True,
        help_text="A JSON-serialized object for an inline keyboard. If empty, one 'Play game_title' button will be shown. If not empty, the first button must launch the game.",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_to_main = GenericForeignKey("content_type", "object_id")

    @property
    def required_fields(self) -> list:
        return ["chat_id", "game_short_name"]


class SetGameScore(Component):
    """Use this method to set the score of the specified user in a game message. On success, if the message is not an inline message, the Message is returned, otherwise True is returned. Returns an error, if the new score is not greater than the user's current score in the chat and force is False."""

    user_id = models.IntegerField(null=True, blank=True, help_text="User identifier")
    score = models.IntegerField(
        null=True,
        blank=True,
        help_text="New score, must be non-negative",
    )
    force = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the high score is allowed to decrease. This can be useful when fixing mistakes or banning cheaters",
    )
    disable_edit_message = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if the game message should not be automatically edited to include the current scoreboard",
    )
    chat_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Required if inline_message_id is not specified. Unique identifier for the target chat",
    )
    message_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Required if inline_message_id is not specified. Identifier of the sent message",
    )
    inline_message_id = models.CharField(
        null=True,
        blank=True,
        help_text="Required if chat_id and message_id are not specified. Identifier of the inline message",
    )

    @property
    def required_fields(self) -> list:
        return ["user_id", "score"]
