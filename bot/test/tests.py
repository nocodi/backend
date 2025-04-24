import unittest

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from bot.models import Bot
from component.models import OnMessage
from component.telegram.models import SendMessage
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
        send_message_component = SendMessage.objects.create(
            chat_id=123456789,
            text="Hello, World!",
        )
        on_message_component = OnMessage.objects.create(
            text="Hello",
        )
        print(on_message_component.__dict__)

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
