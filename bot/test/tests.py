from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status

from bot.models import Bot
from bot.test.factory import BotFactory
from iam.test.factory import IamUserFactory
from iam.utils import create_token_for_iamuser

fake = Faker()


class BotTest(TestCase):

    def _get_token(self):
        user = IamUserFactory.create()
        return {
            "Authorization": create_token_for_iamuser(user.id),
        }

    def test_create_bot(self):
        url = reverse("bot:create-bot")
        token = fake.name()
        data = {"name": fake.name(), "description": fake.text(), "token": token}

        response = self.client.post(url, data, headers=self._get_token())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Bot.objects.filter(token=token).exists())

    def test_my_bots(self):
        user = IamUserFactory.create()
        BotFactory.create_batch(3, user=user)

        url = reverse("bot:my-bots")
        response = self.client.get(
            url,
            headers={
                "Authorization": create_token_for_iamuser(user.id),
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
