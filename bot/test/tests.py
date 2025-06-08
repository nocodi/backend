import unittest
from io import BytesIO

from django.core.files.base import ContentFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image
from rest_framework import status

from bot.models import Bot
from component.models import Component, OnMessage, SetState
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
            chat_id=693259126,
            text="Hello, World!",
            position_x=1,
            position_y=1,
            previous_component=on_message_component,
        )
        SendMessage.objects.create(
            bot=self.bot,
            chat_id=693259126,
            text="Bye World",
            position_x=1,
            position_y=1,
            previous_component=on_message_component,
        )

        image = Image.new("RGB", (100, 100), color="blue")
        image_io = BytesIO()
        image.save(image_io, "PNG")
        image_content = ContentFile(image_io.getvalue(), "test.png")
        SendPhoto.objects.create(
            bot=self.bot,
            chat_id=".chat.id",
            photo=image_content,
            position_x=1,
            position_y=1,
            previous_component=on_message_component,
        )

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

        SendMessage.objects.create(
            bot=self.bot,
            chat_id=693259126,
            text="State set",
            position_x=1,
            position_y=1,
            previous_component=on_state_component,
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
