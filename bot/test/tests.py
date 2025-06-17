from django.test import TestCase
from django.urls import reverse
from PIL import Image
from rest_framework import status

from bot.models import Bot
from component.models import (
    CodeComponent,
    Component,
    Markup,
    OnMessage,
    SetState,
    SwitchComponent,
)
from component.telegram.models import SendMessage, SendPhoto
from iam.models import IamUser
from iam.utils import create_token_for_iamuser

# Create your tests here.


class CodeTest(TestCase):

    def setUp(self):
        # a simple bot with a code component
        self.user = IamUser.objects.create()

        self.bot = Bot.objects.create(
            name="Test Bot",
            token="1367633212:iEF26FkkrLfyWsjhwlxlslyM4bUxviGmDKWvqV2d",
            description="Test bot for testing",
            user=self.user,
        )
        on_message_component = OnMessage.objects.create(
            bot=self.bot,
            position_x=1,
            position_y=1,
            component_type=Component.ComponentType.TRIGGER,
            text="/start",
        )
        send_message_start = SendMessage.objects.create(
            bot=self.bot,
            chat_id=".from_user.id",
            text="Hello welcome to the bot",
            position_x=1,
            position_y=1,
            previous_component=on_message_component,
        )
        CodeComponent.objects.create(
            bot=self.bot,
            code="print('This is log message to validate code')",
            position_x=1,
            position_y=1,
            previous_component=on_message_component,
        )

        send_support = SendMessage.objects.create(
            bot=self.bot,
            chat_id=".from_user.id",
            text="Send your message then i want to send to admin",
            position_x=1,
            position_y=1,
        )
        SetState.objects.create(
            bot=self.bot,
            state="support",
            position_x=1,
            position_y=1,
            previous_component=send_support,
        )

        send_message_help = SendMessage.objects.create(
            bot=self.bot,
            chat_id=".from_user.id",
            text="This is test help message",
            position_x=1,
            position_y=1,
        )

        send_message_accept_terms = SendMessage.objects.create(
            bot=self.bot,
            chat_id=".from_user.id",
            text="Some text to accept terms and conditions... Do you accept?, send Yes or No",
            position_x=1,
            position_y=1,
        )
        SetState.objects.create(
            bot=self.bot,
            state="accept_terms",
            position_x=1,
            position_y=1,
            previous_component=send_message_accept_terms,
        )

        Markup.objects.create(
            parent_component=send_message_start,
            markup_type=Markup.MarkupType.ReplyKeyboard,
            buttons=[
                [{"value": "Help", "next_component": send_message_help.id}],
                [
                    {
                        "value": "Accept terms and conditions",
                        "next_component": send_message_accept_terms.id,
                    },
                ],
                [{"value": "Support", "next_component": send_support.id}],
            ],
        )

        handle_support = OnMessage.objects.create(
            bot=self.bot,
            state="support",
            position_x=1,
            position_y=1,
        )
        send_message_to_admin = SendMessage.objects.create(
            bot=self.bot,
            chat_id="693259126",
            text="text send from user",
            position_x=1,
            position_y=1,
            previous_component=handle_support,
        )
        send_message_to_user = SendMessage.objects.create(
            bot=self.bot,
            chat_id=".from_user.id",
            text="your message send to admin",
            position_x=1,
            position_y=1,
            previous_component=send_message_to_admin,
        )

        handle_accept_terms = OnMessage.objects.create(
            bot=self.bot,
            state="accept_terms",
            position_x=1,
            position_y=1,
        )
        send_message_accept_terms_yes = SendMessage.objects.create(
            bot=self.bot,
            chat_id=".from_user.id",
            text="You accepted terms and conditions, send your phone number start with +98",
            position_x=1,
            position_y=1,
        )

        send_message_accept_terms_no = SendMessage.objects.create(
            bot=self.bot,
            chat_id=".from_user.id",
            text="You did not accept terms and conditions",
            position_x=1,
            position_y=1,
        )

        SwitchComponent.objects.create(
            bot=self.bot,
            position_x=1,
            position_y=1,
            previous_component=handle_accept_terms,
            expression=".text",
            values=["Yes", "No"],
            next_components=[
                send_message_accept_terms_yes.id,
                send_message_accept_terms_no.id,
            ],
        )

        phone_number_hanndle = OnMessage.objects.create(
            bot=self.bot,
            regex=True,
            text="^\\+98\\d+$",
            position_x=1,
            position_y=1,
        )
        send_message_phone_number = SendMessage.objects.create(
            bot=self.bot,
            chat_id=".from_user.id",
            text="Is your phone number correct?",
            position_x=1,
            position_y=1,
            previous_component=phone_number_hanndle,
        )
        phone_number_handle_yes_no = SendMessage.objects.create(
            bot=self.bot,
            chat_id=".from_user.id",
            text=".text",
            position_x=1,
            position_y=1,
            previous_component=phone_number_hanndle,
        )

        handle_yes = SendMessage.objects.create(
            bot=self.bot,
            chat_id=".from_user.id",
            text="OK, thanks",
            position_x=1,
            position_y=1,
        )

        handle_no = SendMessage.objects.create(
            bot=self.bot,
            chat_id=".from_user.id",
            text="OK, you lose..., send /start to start again",
            position_x=1,
            position_y=1,
        )

        Markup.objects.create(
            parent_component=phone_number_handle_yes_no,
            markup_type=Markup.MarkupType.InlineKeyboard,
            buttons=[
                [{"value": "Yes", "next_component": handle_yes.id}],
                [{"value": "No", "next_component": handle_no.id}],
            ],
        )

    def test_create_bot(self):
        token = create_token_for_iamuser(self.user.id)
        url = reverse("bot:generate-code", args=[self.bot.id])
        response = self.client.get(
            url,
            headers={
                "Authorization": token,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        # print(response.content.decode())
        with open("code_1.py", "w") as f:
            f.write(response.content.decode())
