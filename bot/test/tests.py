import unittest
from io import BytesIO

from django.core.files.base import ContentFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image
from rest_framework import status

from bot.models import Bot
from component.models import CodeComponent, Component, Markup, OnMessage, SetState
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
        send_message_comp = SendMessage.objects.create(
            bot=self.bot,
            chat_id=".from_user.id",
            text="Hello, World!",
            position_x=1,
            position_y=1,
            previous_component=on_message_component,
        )
        send1 = SendMessage.objects.create(
            bot=self.bot,
            chat_id=".from_user.id",
            text="Bye World",
            position_x=1,
            position_y=1,
            previous_component=on_message_component,
        )

        send_3 = SendMessage.objects.create(
            bot=self.bot,
            chat_id=".from_user.id",
            text="Button clicked!",
            position_x=1,
            position_y=1,
        )
        send_4 = SendMessage.objects.create(
            bot=self.bot,
            chat_id=".from_user.id",
            text="Button clicked 2",
            position_x=1,
            position_y=1,
            previous_component=send_3,
        )

        Markup.objects.create(
            parent_component=send1,
            markup_type=Markup.MarkupType.InlineKeyboard,
            buttons=[
                [{"value": "Button 1"}, {"value": "Button 2"}],
                [{"value": "Button 3"}, {"value": "Button 4"}],
                [{"value": "Button 5", "next_component": send_3.id}],
            ],
        )

        image = Image.new("RGB", (100, 100), color="blue")
        image_io = BytesIO()
        image.save(image_io, "PNG")
        image_content = ContentFile(image_io.getvalue(), "test.png")
        # photo_component = SendPhoto.objects.create(
        #     bot=self.bot,
        #     chat_id=".from_user.id",
        #     photo=image_content,
        #     position_x=1,
        #     position_y=1,
        #     previous_component=on_message_component,
        # )

        SetState.objects.create(
            bot=self.bot,
            state="state",
            position_x=1,
            position_y=1,
            previous_component=on_message_component,
        )

        on_state_component = OnMessage.objects.create(
            bot=self.bot,
            state="state",
            position_x=1,
            position_y=1,
        )

        send2 = SendMessage.objects.create(
            bot=self.bot,
            chat_id=".from_user.id",
            text="State set",
            position_x=1,
            position_y=1,
            previous_component=on_state_component,
        )

        CodeComponent.objects.create(
            bot=self.bot,
            code="print('Hello, World!')",
            position_x=1,
            position_y=1,
            previous_component=send2,
        )

        send_5 = SendMessage.objects.create(
            bot=self.bot,
            chat_id=".from_user.id",
            text="Button 3 clicked from text button",
            position_x=1,
            position_y=1,
        )

        Markup.objects.create(
            parent_component=send_5,
            markup_type=Markup.MarkupType.ReplyKeyboard,
            buttons=[
                [{"value": "Button 1"}, {"value": "Button 2"}],
                [{"value": "Button 3", "next_component": send_5.id}],
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
