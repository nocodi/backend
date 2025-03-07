from django.test import TestCase
from django.urls import reverse
from rest_framework import status

# Create your tests here.


class AuthTest(TestCase):

    def create_user(self, email):
        url = reverse("iam:signup")
        data = {
            "email": "example@example.com",
            "password": "password",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED, response.content)

    def test_login(self):
        email = "example@example.com"
        self.create_user(email)
