import unittest

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

# Create your tests here.


class AuthTest(TestCase):

    def create_user(self, email, send_email_patch):
        url = reverse("iam:signup")
        data = {
            "email": "example@example.com",
            "password": "password",
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.content
        )
        response = response.json()
        self.assertIn("request_id", response)
        request_id = response["request_id"]
        otp_text = send_email_patch.call_args.kwargs["text"]
        otp = otp_text.split(" ")[-1]

        data = {
            "request_id": request_id,
            "otp": otp,
        }

        response = self.client.post(
            path=reverse("iam:signup_verify"),
            data=data,
        )
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED, (response.content))

    @ unittest.mock.patch("iam.integrations.email.email_client.send")
    def test_login(self, send_email_patch):
        email = "example@example.com"
        self.create_user(email, send_email_patch)
