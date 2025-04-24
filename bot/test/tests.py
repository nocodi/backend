import unittest

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from bot.models import Bot
from component.models import Component, OnMessage
from component.telegram.models import SendMessage
from flow.models import ContentType
from iam.models import IamUser
from iam.utils import create_token_for_iamuser

# Create your tests here.


class CodeTest(TestCase):

    def setUp(self):
        # a simple bot with a code component
        self.user = IamUser.objects.create()

        self.bot = Bot.objects.create(
            name="Test Bot",
            token="123456789:ABCDEF",
            description="Test bot for testing",
            user=self.user,
        )
        on_message_component = OnMessage.objects.create(
            bot=self.bot,
            text="Hello",
            position_x=1,
            position_y=1,
            component_type=Component.ComponentType.TRIGGER,
        )
        send_message_component = SendMessage.objects.create(
            bot=self.bot,
            chat_id=123456789,
            text="Hello, World!",
            position_x=1,
            position_y=1,
            previous_component=on_message_component,
        )

    def test_foo(self):
        token = create_token_for_iamuser(self.user.id)
        url = reverse("bot:generate-code", args=[self.bot.id])
        response = self.client.get(
            url,
            headers={
                "Authorization": token,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        print(response.content.decode())
