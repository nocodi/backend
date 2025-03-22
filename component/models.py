from django.contrib.postgres.fields import ArrayField
from django.db import models


class TelegramComponent(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass


class SendMessage(TelegramComponent):
    """Use this method to send text messages. On success, the sent Message is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    text = models.CharField(
        null=False,
        blank=False,
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


class ForwardMessage(TelegramComponent):
    """Use this method to forward messages of any kind. Service messages and messages with protected content can't be forwarded. On success, the sent Message is returned."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    from_chat_id = models.CharField(
        null=False,
        blank=False,
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
        null=False,
        blank=False,
        help_text="Message identifier in the chat specified in from_chat_id",
    )


class ForwardMessages(TelegramComponent):
    """Use this method to forward multiple messages of any kind. If some of the specified messages can't be found or forwarded, they are skipped. Service messages and messages with protected content can't be forwarded. Album grouping is kept for forwarded messages. On success, an array of MessageId of the sent messages is returned."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    from_chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the chat where the original messages were sent (or channel username in the format @channelusername)",
    )
    message_ids = ArrayField(
        models.IntegerField(),
        default=list,
        null=False,
        blank=False,
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


class CopyMessage(TelegramComponent):
    """Use this method to copy messages of any kind. Service messages, paid media messages, giveaway messages, giveaway winners messages, and invoice messages can't be copied. A quiz poll can be copied only if the value of the field correct_option_id is known to the bot. The method is analogous to the method forwardMessage, but the copied message doesn't have a link to the original message. Returns the MessageId of the sent message on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    from_chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the chat where the original message was sent (or channel username in the format @channelusername)",
    )
    message_id = models.IntegerField(
        null=False,
        blank=False,
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


class CopyMessages(TelegramComponent):
    """Use this method to copy messages of any kind. If some of the specified messages can't be found or copied, they are skipped. Service messages, paid media messages, giveaway messages, giveaway winners messages, and invoice messages can't be copied. A quiz poll can be copied only if the value of the field correct_option_id is known to the bot. The method is analogous to the method forwardMessages, but the copied messages don't have a link to the original message. Album grouping is kept for copied messages. On success, an array of MessageId of the sent messages is returned."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    from_chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the chat where the original messages were sent (or channel username in the format @channelusername)",
    )
    message_ids = ArrayField(
        models.IntegerField(),
        default=list,
        null=False,
        blank=False,
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


class SendPhoto(TelegramComponent):
    """Use this method to send photos. On success, the sent Message is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
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


class SendDocument(TelegramComponent):
    """Use this method to send general files. On success, the sent Message is returned. Bots can currently send files of any type of up to 50 MB in size, this limit may be changed in the future."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
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


class SendVideo(TelegramComponent):
    """Use this method to send video files, Telegram clients support MPEG4 videos (other formats may be sent as Document). On success, the sent Message is returned. Bots can currently send video files of up to 50 MB in size, this limit may be changed in the future."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    duration = models.IntegerField(
        null=True,
        blank=True,
        help_text="Duration of sent video in seconds",
    )
    width = models.IntegerField(null=True, blank=True, help_text="Video width")
    height = models.IntegerField(null=True, blank=True, help_text="Video height")
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


class SendAnimation(TelegramComponent):
    """Use this method to send animation files (GIF or H.264/MPEG-4 AVC video without sound). On success, the sent Message is returned. Bots can currently send animation files of up to 50 MB in size, this limit may be changed in the future."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    duration = models.IntegerField(
        null=True,
        blank=True,
        help_text="Duration of sent animation in seconds",
    )
    width = models.IntegerField(null=True, blank=True, help_text="Animation width")
    height = models.IntegerField(null=True, blank=True, help_text="Animation height")
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


class SendVoice(TelegramComponent):
    """Use this method to send audio files, if you want Telegram clients to display the file as a playable voice message. For this to work, your audio must be in an .OGG file encoded with OPUS, or in .MP3 format, or in .M4A format (other formats may be sent as Audio or Document). On success, the sent Message is returned. Bots can currently send voice messages of up to 50 MB in size, this limit may be changed in the future."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
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


class SendVideoNote(TelegramComponent):
    """As of v.4.0, Telegram clients support rounded square MPEG4 videos of up to 1 minute long. Use this method to send video messages. On success, the sent Message is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
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


class SendPaidMedia(TelegramComponent):
    """Use this method to send paid media. On success, the sent Message is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername). If the chat is a channel, all Telegram Star proceeds from this media will be credited to the chat's balance. Otherwise, they will be credited to the bot's balance.",
    )
    star_count = models.IntegerField(
        null=False,
        blank=False,
        help_text="The number of Telegram Stars that must be paid to buy access to the media; 1-2500",
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


class SendMediaGroup(TelegramComponent):
    """Use this method to send a group of photos, videos, documents or audios as an album. Documents and audio files can be only grouped in an album with messages of the same type. On success, an array of Messages that were sent is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=False,
        blank=False,
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


class SendLocation(TelegramComponent):
    """Use this method to send point on the map. On success, the sent Message is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    latitude = models.FloatField(
        null=False,
        blank=False,
        help_text="Latitude of the location",
    )
    longitude = models.FloatField(
        null=False,
        blank=False,
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


class SendVenue(TelegramComponent):
    """Use this method to send information about a venue. On success, the sent Message is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    latitude = models.FloatField(
        null=False,
        blank=False,
        help_text="Latitude of the venue",
    )
    longitude = models.FloatField(
        null=False,
        blank=False,
        help_text="Longitude of the venue",
    )
    title = models.CharField(null=False, blank=False, help_text="Name of the venue")
    address = models.CharField(
        null=False,
        blank=False,
        help_text="Address of the venue",
    )
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


class SendContact(TelegramComponent):
    """Use this method to send phone contacts. On success, the sent Message is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    phone_number = models.CharField(
        null=False,
        blank=False,
        help_text="Contact's phone number",
    )
    first_name = models.CharField(
        null=False,
        blank=False,
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


class SendPoll(TelegramComponent):
    """Use this method to send a native poll. On success, the sent Message is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    question = models.CharField(
        null=False,
        blank=False,
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


class SendDice(TelegramComponent):
    """Use this method to send an animated emoji that will display a random value. On success, the sent Message is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=False,
        blank=False,
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


class SetMessageReaction(TelegramComponent):
    """Use this method to change the chosen reactions on a message. Service messages of some types can't be reacted to. Automatically forwarded messages from a channel to its discussion group have the same available reactions as messages in the channel. Bots can't use paid reactions. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="Identifier of the target message. If the message belongs to a media group, the reaction is set to the first non-deleted message in the group instead.",
    )
    is_big = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to set the reaction with a big animation",
    )


class GetUserProfilePhotos(TelegramComponent):
    """Use this method to get a list of profile pictures for a user. Returns a UserProfilePhotos object."""

    user_id = models.IntegerField(
        null=False,
        blank=False,
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


class SetUserEmojiStatus(TelegramComponent):
    """Changes the emoji status for a given user that previously allowed the bot to manage their emoji status via the Mini App method requestEmojiStatusAccess. Returns True on success."""

    user_id = models.IntegerField(
        null=False,
        blank=False,
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


class GetFile(TelegramComponent):
    """Use this method to get basic information about a file and prepare it for downloading. For the moment, bots can download files of up to 20MB in size. On success, a File object is returned. The file can then be downloaded via the link https://api.telegram.org/file/bot<token>/<file_path>, where <file_path> is taken from the response. It is guaranteed that the link will be valid for at least 1 hour. When the link expires, a new one can be requested by calling getFile again."""

    file_id = models.CharField(
        null=False,
        blank=False,
        help_text="File identifier to get information about",
    )


class BanChatMember(TelegramComponent):
    """Use this method to ban a user in a group, a supergroup or a channel. In the case of supergroups and channels, the user will not be able to return to the chat on their own using invite links, etc., unless unbanned first. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target group or username of the target supergroup or channel (in the format @channelusername)",
    )
    user_id = models.IntegerField(
        null=False,
        blank=False,
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


class UnbanChatMember(TelegramComponent):
    """Use this method to unban a previously banned user in a supergroup or channel. The user will not return to the group or channel automatically, but will be able to join via link, etc. The bot must be an administrator for this to work. By default, this method guarantees that after the call the user is not a member of the chat, but will be able to join it. So if the user is a member of the chat they will also be removed from the chat. If you don't want this, use the parameter only_if_banned. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target group or username of the target supergroup or channel (in the format @channelusername)",
    )
    user_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="Unique identifier of the target user",
    )
    only_if_banned = models.BooleanField(
        null=True,
        blank=True,
        help_text="Do nothing if the user is not banned",
    )


class RestrictChatMember(TelegramComponent):
    """Use this method to restrict a user in a supergroup. The bot must be an administrator in the supergroup for this to work and must have the appropriate administrator rights. Pass True for all permissions to lift restrictions from a user. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )
    user_id = models.IntegerField(
        null=False,
        blank=False,
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


class PromoteChatMember(TelegramComponent):
    """Use this method to promote or demote a user in a supergroup or a channel. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Pass False for all boolean parameters to demote a user. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    user_id = models.IntegerField(
        null=False,
        blank=False,
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


class SetChatAdministratorCustomTitle(TelegramComponent):
    """Use this method to set a custom title for an administrator in a supergroup promoted by the bot. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )
    user_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="Unique identifier of the target user",
    )
    custom_title = models.CharField(
        null=False,
        blank=False,
        max_length=16,
        help_text="New custom title for the administrator; 0-16 characters, emoji are not allowed",
    )


class BanChatSenderChat(TelegramComponent):
    """Use this method to ban a channel chat in a supergroup or a channel. Until the chat is unbanned, the owner of the banned chat won't be able to send messages on behalf of any of their channels. The bot must be an administrator in the supergroup or channel for this to work and must have the appropriate administrator rights. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    sender_chat_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="Unique identifier of the target sender chat",
    )


class UnbanChatSenderChat(TelegramComponent):
    """Use this method to unban a previously banned channel chat in a supergroup or channel. The bot must be an administrator for this to work and must have the appropriate administrator rights. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    sender_chat_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="Unique identifier of the target sender chat",
    )


class SetChatPermissions(TelegramComponent):
    """Use this method to set default chat permissions for all members. The bot must be an administrator in the group or a supergroup for this to work and must have the can_restrict_members administrator rights. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )
    use_independent_chat_permissions = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if chat permissions are set independently. Otherwise, the can_send_other_messages and can_add_web_page_previews permissions will imply the can_send_messages, can_send_audios, can_send_documents, can_send_photos, can_send_videos, can_send_video_notes, and can_send_voice_notes permissions; the can_send_polls permission will imply the can_send_messages permission.",
    )


class ExportChatInviteLink(TelegramComponent):
    """Use this method to generate a new primary invite link for a chat; any previously generated primary link is revoked. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns the new invite link as String on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )


class CreateChatInviteLink(TelegramComponent):
    """Use this method to create an additional invite link for a chat. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. The link can be revoked using the method revokeChatInviteLink. Returns the new invite link as ChatInviteLink object."""

    chat_id = models.CharField(
        null=False,
        blank=False,
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


class EditChatInviteLink(TelegramComponent):
    """Use this method to edit a non-primary invite link created by the bot. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns the edited invite link as a ChatInviteLink object."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    invite_link = models.CharField(
        null=False,
        blank=False,
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


class CreateChatSubscriptionInviteLink(TelegramComponent):
    """Use this method to create a subscription invite link for a channel chat. The bot must have the can_invite_users administrator rights. The link can be edited using the method editChatSubscriptionInviteLink or revoked using the method revokeChatInviteLink. Returns the new invite link as a ChatInviteLink object."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target channel chat or username of the target channel (in the format @channelusername)",
    )
    name = models.CharField(
        null=True,
        blank=True,
        max_length=32,
        help_text="Invite link name; 0-32 characters",
    )
    subscription_period = models.IntegerField(
        null=False,
        blank=False,
        help_text="The number of seconds the subscription will be active for before the next payment. Currently, it must always be 2592000 (30 days).",
    )
    subscription_price = models.IntegerField(
        null=False,
        blank=False,
        help_text="The amount of Telegram Stars a user must pay initially and after each subsequent subscription period to be a member of the chat; 1-2500",
    )


class EditChatSubscriptionInviteLink(TelegramComponent):
    """Use this method to edit a subscription invite link created by the bot. The bot must have the can_invite_users administrator rights. Returns the edited invite link as a ChatInviteLink object."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    invite_link = models.CharField(
        null=False,
        blank=False,
        help_text="The invite link to edit",
    )
    name = models.CharField(
        null=True,
        blank=True,
        max_length=32,
        help_text="Invite link name; 0-32 characters",
    )


class RevokeChatInviteLink(TelegramComponent):
    """Use this method to revoke an invite link created by the bot. If the primary link is revoked, a new link is automatically generated. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns the revoked invite link as ChatInviteLink object."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier of the target chat or username of the target channel (in the format @channelusername)",
    )
    invite_link = models.CharField(
        null=False,
        blank=False,
        help_text="The invite link to revoke",
    )


class ApproveChatJoinRequest(TelegramComponent):
    """Use this method to approve a chat join request. The bot must be an administrator in the chat for this to work and must have the can_invite_users administrator right. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    user_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="Unique identifier of the target user",
    )


class DeclineChatJoinRequest(TelegramComponent):
    """Use this method to decline a chat join request. The bot must be an administrator in the chat for this to work and must have the can_invite_users administrator right. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    user_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="Unique identifier of the target user",
    )


class SetChatPhoto(TelegramComponent):
    """Use this method to set a new profile photo for the chat. Photos can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )


class DeleteChatPhoto(TelegramComponent):
    """Use this method to delete a chat photo. Photos can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )


class SetChatTitle(TelegramComponent):
    """Use this method to change the title of a chat. Titles can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    title = models.CharField(
        null=False,
        blank=False,
        max_length=128,
        help_text="New chat title, 1-128 characters",
    )


class SetChatDescription(TelegramComponent):
    """Use this method to change the description of a group, a supergroup or a channel. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    description = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text="New chat description, 0-255 characters",
    )


class PinChatMessage(TelegramComponent):
    """Use this method to add a message to the list of pinned messages in a chat. If the chat is not a private chat, the bot must be an administrator in the chat for this to work and must have the 'can_pin_messages' administrator right in a supergroup or 'can_edit_messages' administrator right in a channel. Returns True on success."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be pinned",
    )
    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="Identifier of a message to pin",
    )
    disable_notification = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True if it is not necessary to send a notification to all chat members about the new pinned message. Notifications are always disabled in channels and private chats.",
    )


class UnpinChatMessage(TelegramComponent):
    """Use this method to remove a message from the list of pinned messages in a chat. If the chat is not a private chat, the bot must be an administrator in the chat for this to work and must have the 'can_pin_messages' administrator right in a supergroup or 'can_edit_messages' administrator right in a channel. Returns True on success."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be unpinned",
    )
    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Identifier of the message to unpin. Required if business_connection_id is specified. If not specified, the most recent pinned message (by sending date) will be unpinned.",
    )


class UnpinAllChatMessages(TelegramComponent):
    """Use this method to clear the list of pinned messages in a chat. If the chat is not a private chat, the bot must be an administrator in the chat for this to work and must have the 'can_pin_messages' administrator right in a supergroup or 'can_edit_messages' administrator right in a channel. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )


class LeaveChat(TelegramComponent):
    """Use this method for your bot to leave a group, supergroup or channel. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)",
    )


class GetChat(TelegramComponent):
    """Use this method to get up-to-date information about the chat. Returns a ChatFullInfo object on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)",
    )


class GetChatAdministrators(TelegramComponent):
    """Use this method to get a list of administrators in a chat, which aren't bots. Returns an Array of ChatMember objects."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)",
    )


class GetChatMemberCount(TelegramComponent):
    """Use this method to get the number of members in a chat. Returns Int on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)",
    )


class GetChatMember(TelegramComponent):
    """Use this method to get information about a member of a chat. The method is only guaranteed to work for other users if the bot is an administrator in the chat. Returns a ChatMember object on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)",
    )
    user_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="Unique identifier of the target user",
    )


class SetChatStickerSet(TelegramComponent):
    """Use this method to set a new group sticker set for a supergroup. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Use the field can_set_sticker_set optionally returned in getChat requests to check if the bot can use this method. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )
    sticker_set_name = models.CharField(
        null=False,
        blank=False,
        help_text="Name of the sticker set to be set as the group sticker set",
    )


class DeleteChatStickerSet(TelegramComponent):
    """Use this method to delete a group sticker set from a supergroup. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Use the field can_set_sticker_set optionally returned in getChat requests to check if the bot can use this method. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )


class CreateForumTopic(TelegramComponent):
    """Use this method to create a topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights. Returns information about the created topic as a ForumTopic object."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )
    name = models.CharField(
        null=False,
        blank=False,
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


class EditForumTopic(TelegramComponent):
    """Use this method to edit name and icon of a topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights, unless it is the creator of the topic. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )
    message_thread_id = models.IntegerField(
        null=False,
        blank=False,
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


class CloseForumTopic(TelegramComponent):
    """Use this method to close an open topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights, unless it is the creator of the topic. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )
    message_thread_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target message thread of the forum topic",
    )


class ReopenForumTopic(TelegramComponent):
    """Use this method to reopen a closed topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights, unless it is the creator of the topic. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )
    message_thread_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target message thread of the forum topic",
    )


class DeleteForumTopic(TelegramComponent):
    """Use this method to delete a forum topic along with all its messages in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_delete_messages administrator rights. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )
    message_thread_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target message thread of the forum topic",
    )


class UnpinAllForumTopicMessages(TelegramComponent):
    """Use this method to clear the list of pinned messages in a forum topic. The bot must be an administrator in the chat for this to work and must have the can_pin_messages administrator right in the supergroup. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )
    message_thread_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target message thread of the forum topic",
    )


class EditGeneralForumTopic(TelegramComponent):
    """Use this method to edit the name of the 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )
    name = models.CharField(
        null=False,
        blank=False,
        max_length=128,
        help_text="New topic name, 1-128 characters",
    )


class CloseGeneralForumTopic(TelegramComponent):
    """Use this method to close an open 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )


class ReopenGeneralForumTopic(TelegramComponent):
    """Use this method to reopen a closed 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights. The topic will be automatically unhidden if it was hidden. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )


class HideGeneralForumTopic(TelegramComponent):
    """Use this method to hide the 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights. The topic will be automatically closed if it was open. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )


class UnhideGeneralForumTopic(TelegramComponent):
    """Use this method to unhide the 'General' topic in a forum supergroup chat. The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )


class UnpinAllGeneralForumTopicMessages(TelegramComponent):
    """Use this method to clear the list of pinned messages in a General forum topic. The bot must be an administrator in the chat for this to work and must have the can_pin_messages administrator right in the supergroup. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)",
    )


class GetUserChatBoosts(TelegramComponent):
    """Use this method to get the list of boosts added to a chat by a user. Requires administrator rights in the chat. Returns a UserChatBoosts object."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the chat or username of the channel (in the format @channelusername)",
    )
    user_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="Unique identifier of the target user",
    )


class GetBusinessConnection(TelegramComponent):
    """Use this method to get information about the connection of the bot with a business account. Returns a BusinessConnection object on success."""

    business_connection_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier of the business connection",
    )


class SetMyCommands(TelegramComponent):
    """Use this method to change the list of the bot's commands. See this manual for more details about bot commands. Returns True on success."""

    language_code = models.CharField(
        null=True,
        blank=True,
        help_text="A two-letter ISO 639-1 language code. If empty, commands will be applied to all users from the given scope, for whose language there are no dedicated commands",
    )


class DeleteMyCommands(TelegramComponent):
    """Use this method to delete the list of the bot's commands for the given scope and user language. After deletion, higher level commands will be shown to affected users. Returns True on success."""

    language_code = models.CharField(
        null=True,
        blank=True,
        help_text="A two-letter ISO 639-1 language code. If empty, commands will be applied to all users from the given scope, for whose language there are no dedicated commands",
    )


class GetMyCommands(TelegramComponent):
    """Use this method to get the current list of the bot's commands for the given scope and user language. Returns an Array of BotCommand objects. If commands aren't set, an empty list is returned."""

    language_code = models.CharField(
        null=True,
        blank=True,
        help_text="A two-letter ISO 639-1 language code or an empty string",
    )


class SetMyName(TelegramComponent):
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


class GetMyName(TelegramComponent):
    """Use this method to get the current bot name for the given user language. Returns BotName on success."""

    language_code = models.CharField(
        null=True,
        blank=True,
        help_text="A two-letter ISO 639-1 language code or an empty string",
    )


class SetMyDescription(TelegramComponent):
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


class GetMyDescription(TelegramComponent):
    """Use this method to get the current bot description for the given user language. Returns BotDescription on success."""

    language_code = models.CharField(
        null=True,
        blank=True,
        help_text="A two-letter ISO 639-1 language code or an empty string",
    )


class SetMyShortDescription(TelegramComponent):
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


class GetMyShortDescription(TelegramComponent):
    """Use this method to get the current bot short description for the given user language. Returns BotShortDescription on success."""

    language_code = models.CharField(
        null=True,
        blank=True,
        help_text="A two-letter ISO 639-1 language code or an empty string",
    )


class SetChatMenuButton(TelegramComponent):
    """Use this method to change the bot's menu button in a private chat, or the default menu button. Returns True on success."""

    chat_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target private chat. If not specified, default bot's menu button will be changed",
    )


class GetChatMenuButton(TelegramComponent):
    """Use this method to get the current value of the bot's menu button in a private chat, or the default menu button. Returns MenuButton on success."""

    chat_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target private chat. If not specified, default bot's menu button will be returned",
    )


class SetMyDefaultAdministratorRights(TelegramComponent):
    """Use this method to change the default administrator rights requested by the bot when it's added as an administrator to groups or channels. These rights will be suggested to users, but they are free to modify the list before adding the bot. Returns True on success."""

    for_channels = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to change the default administrator rights of the bot in channels. Otherwise, the default administrator rights of the bot for groups and supergroups will be changed.",
    )


class GetMyDefaultAdministratorRights(TelegramComponent):
    """Use this method to get the current default administrator rights of the bot. Returns ChatAdministratorRights on success."""

    for_channels = models.BooleanField(
        null=True,
        blank=True,
        help_text="Pass True to get default administrator rights of the bot in channels. Otherwise, default administrator rights of the bot for groups and supergroups will be returned.",
    )


class EditMessageText(TelegramComponent):
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
        null=False,
        blank=False,
        max_length=4096,
        help_text="New text of the message, 1-4096 characters after entities parsing",
    )
    parse_mode = models.CharField(
        null=True,
        blank=True,
        help_text="Mode for parsing entities in the message text. See formatting options for more details.",
    )


class EditMessageCaption(TelegramComponent):
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


class EditMessageMedia(TelegramComponent):
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


class EditMessageLiveLocation(TelegramComponent):
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
        null=False,
        blank=False,
        help_text="Latitude of new location",
    )
    longitude = models.FloatField(
        null=False,
        blank=False,
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


class StopMessageLiveLocation(TelegramComponent):
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


class EditMessageReplyMarkup(TelegramComponent):
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


class StopPoll(TelegramComponent):
    """Use this method to stop a poll which was sent by the bot. On success, the stopped Poll is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message to be edited was sent",
    )
    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="Identifier of the original message with the poll",
    )


class DeleteMessage(TelegramComponent):
    """Use this method to delete a message, including service messages, with the following limitations:- A message can only be deleted if it was sent less than 48 hours ago.- Service messages about a supergroup, channel, or forum topic creation can't be deleted.- A dice message in a private chat can only be deleted if it was sent more than 24 hours ago.- Bots can delete outgoing messages in private chats, groups, and supergroups.- Bots can delete incoming messages in private chats.- Bots granted can_post_messages permissions can delete outgoing messages in channels.- If the bot is an administrator of a group, it can delete any message there.- If the bot has can_delete_messages permission in a supergroup or a channel, it can delete any message there.Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="Identifier of the message to delete",
    )


class DeleteMessages(TelegramComponent):
    """Use this method to delete multiple messages simultaneously. If some of the specified messages can't be found, they are skipped. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_ids = ArrayField(
        models.IntegerField(),
        default=list,
        null=False,
        blank=False,
        help_text="A JSON-serialized list of 1-100 identifiers of messages to delete. See deleteMessage for limitations on which messages can be deleted",
    )


class SendSticker(TelegramComponent):
    """Use this method to send static .WEBP, animated .TGS, or video .WEBM stickers. On success, the sent Message is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.CharField(
        null=False,
        blank=False,
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


class GetStickerSet(TelegramComponent):
    """Use this method to get a sticker set. On success, a StickerSet object is returned."""

    name = models.CharField(
        null=False,
        blank=False,
        help_text="Name of the sticker set",
    )


class GetCustomEmojiStickers(TelegramComponent):
    """Use this method to get information about custom emoji stickers by their identifiers. Returns an Array of Sticker objects."""

    custom_emoji_ids = ArrayField(
        models.CharField(),
        default=list,
        null=False,
        blank=False,
        help_text="A JSON-serialized list of custom emoji identifiers. At most 200 custom emoji identifiers can be specified.",
    )


class UploadStickerFile(TelegramComponent):
    """Use this method to upload a file with a sticker for later use in the createNewStickerSet, addStickerToSet, or replaceStickerInSet methods (the file can be used multiple times). Returns the uploaded File on success."""

    user_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="User identifier of sticker file owner",
    )
    sticker_format = models.CharField(
        null=False,
        blank=False,
        help_text="Format of the sticker, must be one of “static”, “animated”, “video”",
    )


class CreateNewStickerSet(TelegramComponent):
    """Use this method to create a new sticker set owned by a user. The bot will be able to edit the sticker set thus created. Returns True on success."""

    user_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="User identifier of created sticker set owner",
    )
    name = models.CharField(
        null=False,
        blank=False,
        max_length=64,
        help_text='Short name of sticker set, to be used in t.me/addstickers/ URLs (e.g., animals). Can contain only English letters, digits and underscores. Must begin with a letter, can\'t contain consecutive underscores and must end in "_by_<bot_username>". <bot_username> is case insensitive. 1-64 characters.',
    )
    title = models.CharField(
        null=False,
        blank=False,
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


class AddStickerToSet(TelegramComponent):
    """Use this method to add a new sticker to a set created by the bot. Emoji sticker sets can have up to 200 stickers. Other sticker sets can have up to 120 stickers. Returns True on success."""

    user_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="User identifier of sticker set owner",
    )
    name = models.CharField(null=False, blank=False, help_text="Sticker set name")


class SetStickerPositionInSet(TelegramComponent):
    """Use this method to move a sticker in a set created by the bot to a specific position. Returns True on success."""

    sticker = models.CharField(
        null=False,
        blank=False,
        help_text="File identifier of the sticker",
    )
    position = models.IntegerField(
        null=False,
        blank=False,
        help_text="New sticker position in the set, zero-based",
    )


class DeleteStickerFromSet(TelegramComponent):
    """Use this method to delete a sticker from a set created by the bot. Returns True on success."""

    sticker = models.CharField(
        null=False,
        blank=False,
        help_text="File identifier of the sticker",
    )


class ReplaceStickerInSet(TelegramComponent):
    """Use this method to replace an existing sticker in a sticker set with a new one. The method is equivalent to calling deleteStickerFromSet, then addStickerToSet, then setStickerPositionInSet. Returns True on success."""

    user_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="User identifier of the sticker set owner",
    )
    name = models.CharField(null=False, blank=False, help_text="Sticker set name")
    old_sticker = models.CharField(
        null=False,
        blank=False,
        help_text="File identifier of the replaced sticker",
    )


class SetStickerEmojiList(TelegramComponent):
    """Use this method to change the list of emoji assigned to a regular or custom emoji sticker. The sticker must belong to a sticker set created by the bot. Returns True on success."""

    sticker = models.CharField(
        null=False,
        blank=False,
        help_text="File identifier of the sticker",
    )
    emoji_list = ArrayField(
        models.CharField(),
        default=list,
        null=False,
        blank=False,
        help_text="A JSON-serialized list of 1-20 emoji associated with the sticker",
    )


class SetStickerKeywords(TelegramComponent):
    """Use this method to change search keywords assigned to a regular or custom emoji sticker. The sticker must belong to a sticker set created by the bot. Returns True on success."""

    sticker = models.CharField(
        null=False,
        blank=False,
        help_text="File identifier of the sticker",
    )
    keywords = ArrayField(
        models.CharField(),
        default=list,
        null=True,
        blank=True,
        help_text="A JSON-serialized list of 0-20 search keywords for the sticker with total length of up to 64 characters",
    )


class SetStickerMaskPosition(TelegramComponent):
    """Use this method to change the mask position of a mask sticker. The sticker must belong to a sticker set that was created by the bot. Returns True on success."""

    sticker = models.CharField(
        null=False,
        blank=False,
        help_text="File identifier of the sticker",
    )


class SetStickerSetTitle(TelegramComponent):
    """Use this method to set the title of a created sticker set. Returns True on success."""

    name = models.CharField(null=False, blank=False, help_text="Sticker set name")
    title = models.CharField(
        null=False,
        blank=False,
        max_length=64,
        help_text="Sticker set title, 1-64 characters",
    )


class SetStickerSetThumbnail(TelegramComponent):
    """Use this method to set the thumbnail of a regular or mask sticker set. The format of the thumbnail file must match the format of the stickers in the set. Returns True on success."""

    name = models.CharField(null=False, blank=False, help_text="Sticker set name")
    user_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="User identifier of the sticker set owner",
    )
    format = models.CharField(
        null=False,
        blank=False,
        help_text="Format of the thumbnail, must be one of “static” for a .WEBP or .PNG image, “animated” for a .TGS animation, or “video” for a .WEBM video",
    )


class SetCustomEmojiStickerSetThumbnail(TelegramComponent):
    """Use this method to set the thumbnail of a custom emoji sticker set. Returns True on success."""

    name = models.CharField(null=False, blank=False, help_text="Sticker set name")
    custom_emoji_id = models.CharField(
        null=True,
        blank=True,
        help_text="Custom emoji identifier of a sticker from the sticker set; pass an empty string to drop the thumbnail and use the first sticker as the thumbnail.",
    )


class DeleteStickerSet(TelegramComponent):
    """Use this method to delete a sticker set that was created by the bot. Returns True on success."""

    name = models.CharField(null=False, blank=False, help_text="Sticker set name")


class SendGift(TelegramComponent):
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
        null=False,
        blank=False,
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


class VerifyUser(TelegramComponent):
    """Verifies a user on behalf of the organization which is represented by the bot. Returns True on success."""

    user_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="Unique identifier of the target user",
    )
    custom_description = models.CharField(
        null=True,
        blank=True,
        max_length=70,
        help_text="Custom description for the verification; 0-70 characters. Must be empty if the organization isn't allowed to provide a custom verification description.",
    )


class VerifyChat(TelegramComponent):
    """Verifies a chat on behalf of the organization which is represented by the bot. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    custom_description = models.CharField(
        null=True,
        blank=True,
        max_length=70,
        help_text="Custom description for the verification; 0-70 characters. Must be empty if the organization isn't allowed to provide a custom verification description.",
    )


class RemoveUserVerification(TelegramComponent):
    """Removes verification from a user who is currently verified on behalf of the organization represented by the bot. Returns True on success."""

    user_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="Unique identifier of the target user",
    )


class RemoveChatVerification(TelegramComponent):
    """Removes verification from a chat that is currently verified on behalf of the organization represented by the bot. Returns True on success."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )


class AnswerInlineQuery(TelegramComponent):
    """Use this method to send answers to an inline query. On success, True is returned.No more than 50 results per query are allowed."""

    inline_query_id = models.CharField(
        null=False,
        blank=False,
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


class AnswerWebAppQuery(TelegramComponent):
    """Use this method to set the result of an interaction with a Web App and send a corresponding message on behalf of the user to the chat from which the query originated. On success, a SentWebAppMessage object is returned."""

    web_app_query_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the query to be answered",
    )


class SavePreparedInlineMessage(TelegramComponent):
    """Stores a message that can be sent by a user of a Mini App. Returns a PreparedInlineMessage object."""

    user_id = models.IntegerField(
        null=False,
        blank=False,
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


class SendInvoice(TelegramComponent):
    """Use this method to send invoices. On success, the sent Message is returned."""

    chat_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat or username of the target channel (in the format @channelusername)",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    title = models.CharField(
        null=False,
        blank=False,
        max_length=32,
        help_text="Product name, 1-32 characters",
    )
    description = models.CharField(
        null=False,
        blank=False,
        max_length=255,
        help_text="Product description, 1-255 characters",
    )
    payload = models.CharField(
        null=False,
        blank=False,
        help_text="Bot-defined invoice payload, 1-128 bytes. This will not be displayed to the user, use it for your internal processes.",
    )
    provider_token = models.CharField(
        null=True,
        blank=True,
        help_text="Payment provider token, obtained via @BotFather. Pass an empty string for payments in Telegram Stars.",
    )
    currency = models.CharField(
        null=False,
        blank=False,
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


class CreateInvoiceLink(TelegramComponent):
    """Use this method to create a link for an invoice. Returns the created invoice link as String on success."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the link will be created. For payments in Telegram Stars only.",
    )
    title = models.CharField(
        null=False,
        blank=False,
        max_length=32,
        help_text="Product name, 1-32 characters",
    )
    description = models.CharField(
        null=False,
        blank=False,
        max_length=255,
        help_text="Product description, 1-255 characters",
    )
    payload = models.CharField(
        null=False,
        blank=False,
        help_text="Bot-defined invoice payload, 1-128 bytes. This will not be displayed to the user, use it for your internal processes.",
    )
    provider_token = models.CharField(
        null=True,
        blank=True,
        help_text="Payment provider token, obtained via @BotFather. Pass an empty string for payments in Telegram Stars.",
    )
    currency = models.CharField(
        null=False,
        blank=False,
        help_text="Three-letter ISO 4217 currency code, see more on currencies. Pass “XTR” for payments in Telegram Stars.",
    )
    subscription_period = models.IntegerField(
        null=True,
        blank=True,
        help_text="The number of seconds the subscription will be active for before the next payment. The currency must be set to “XTR” (Telegram Stars) if the parameter is used. Currently, it must always be 2592000 (30 days) if specified. Any number of subscriptions can be active for a given bot at the same time, including multiple concurrent subscriptions from the same user. Subscription price must no exceed 2500 Telegram Stars.",
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


class AnswerShippingQuery(TelegramComponent):
    """If you sent an invoice requesting a shipping address and the parameter is_flexible was specified, the Bot API will send an Update with a shipping_query field to the bot. Use this method to reply to shipping queries. On success, True is returned."""

    shipping_query_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the query to be answered",
    )
    ok = models.BooleanField(
        null=False,
        blank=False,
        help_text="Pass True if delivery to the specified address is possible and False if there are any problems (for example, if delivery to the specified address is not possible)",
    )
    error_message = models.CharField(
        null=True,
        blank=True,
        help_text="Required if ok is False. Error message in human readable form that explains why it is impossible to complete the order (e.g. “Sorry, delivery to your desired address is unavailable”). Telegram will display this message to the user.",
    )


class AnswerPreCheckoutQuery(TelegramComponent):
    """Once the user has confirmed their payment and shipping details, the Bot API sends the final confirmation in the form of an Update with the field pre_checkout_query. Use this method to respond to such pre-checkout queries. On success, True is returned. Note: The Bot API must receive an answer within 10 seconds after the pre-checkout query was sent."""

    pre_checkout_query_id = models.CharField(
        null=False,
        blank=False,
        help_text="Unique identifier for the query to be answered",
    )
    ok = models.BooleanField(
        null=False,
        blank=False,
        help_text="Specify True if everything is alright (goods are available, etc.) and the bot is ready to proceed with the order. Use False if there are any problems.",
    )
    error_message = models.CharField(
        null=True,
        blank=True,
        help_text='Required if ok is False. Error message in human readable form that explains the reason for failure to proceed with the checkout (e.g. "Sorry, somebody just bought the last of our amazing black T-shirts while you were busy filling out your payment details. Please choose a different color or garment!"). Telegram will display this message to the user.',
    )


class GetStarTransactions(TelegramComponent):
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


class RefundStarPayment(TelegramComponent):
    """Refunds a successful payment in Telegram Stars. Returns True on success."""

    user_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="Identifier of the user whose payment will be refunded",
    )
    telegram_payment_charge_id = models.CharField(
        null=False,
        blank=False,
        help_text="Telegram payment identifier",
    )


class EditUserStarSubscription(TelegramComponent):
    """Allows the bot to cancel or re-enable extension of a subscription paid in Telegram Stars. Returns True on success."""

    user_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="Identifier of the user whose subscription will be edited",
    )
    telegram_payment_charge_id = models.CharField(
        null=False,
        blank=False,
        help_text="Telegram payment identifier for the subscription",
    )
    is_canceled = models.BooleanField(
        null=False,
        blank=False,
        help_text="Pass True to cancel extension of the user subscription; the subscription must be active up to the end of the current subscription period. Pass False to allow the user to re-enable a subscription that was previously canceled by the bot.",
    )


class SendGame(TelegramComponent):
    """Use this method to send a game. On success, the sent Message is returned."""

    business_connection_id = models.CharField(
        null=True,
        blank=True,
        help_text="Unique identifier of the business connection on behalf of which the message will be sent",
    )
    chat_id = models.IntegerField(
        null=False,
        blank=False,
        help_text="Unique identifier for the target chat",
    )
    message_thread_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Unique identifier for the target message thread (topic) of the forum; for forum supergroups only",
    )
    game_short_name = models.CharField(
        null=False,
        blank=False,
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


class SetGameScore(TelegramComponent):
    """Use this method to set the score of the specified user in a game message. On success, if the message is not an inline message, the Message is returned, otherwise True is returned. Returns an error, if the new score is not greater than the user's current score in the chat and force is False."""

    user_id = models.IntegerField(null=False, blank=False, help_text="User identifier")
    score = models.IntegerField(
        null=False,
        blank=False,
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
