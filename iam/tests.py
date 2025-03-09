import unittest

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

# Create your tests here.


class AuthTest(TestCase):

    def create_user(self, email: str, password: str, send_email_patch):
        url = reverse("iam:signup")
        data = {
            "email": email,
            "password": password,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            response.content,
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
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            (response.content),
        )
        return response.json()["user_id"]

    @unittest.mock.patch("iam.integrations.email.email_client.send")
    def test_login(self, send_email_patch):
        email = "example@example.com"
        password = "password"
        self.create_user(email, password, send_email_patch)

        res = self.client.post(
            path=reverse("iam:login"),
            data={
                "email": email,
                "password": password + "0",
            },
        )
        self.assertEqual(res.status_code, 401, res.content)

        res = self.client.get(
            path=reverse("iam:getme"),
            headers={
                "Authorization": "",
            },
        )
        self.assertEqual(res.status_code, 403, res.content)

        res = self.client.post(
            path=reverse("iam:login"),
            data={
                "email": email,
                "password": password,
            },
        )
        self.assertEqual(res.status_code, 200, res.content)
        self.assertIn("access_token", res.json())
        token = res.json()["access_token"]
        res = self.client.get(
            path=reverse("iam:getme"),
            headers={
                "Authorization": token,
            },
        )
        self.assertEqual(res.status_code, 200, res.content)

    @unittest.mock.patch("iam.integrations.email.email_client.send")
    def test_otp_login(self, send_email_patch):
        email = "example@example.com"
        password = "password"
        self.create_user(email, password, send_email_patch)

        res = self.client.post(
            path=reverse("iam:login_otp_send"),
            data={
                "email": email,
            },
        )
        self.assertEqual(res.status_code, 200, res.content)
        self.assertIn("request_id", res.json())
        request_id = res.json()["request_id"]
        res = self.client.post(
            path=reverse("iam:login_otp_verify"),
            data={
                "request_id": request_id,
                "otp": "000000",
            },
        )
        self.assertEqual(res.status_code, 401, res.content)
        otp_text = send_email_patch.call_args.kwargs["text"]
        otp = otp_text.split(" ")[-1]
        res = self.client.post(
            path=reverse("iam:login_otp_verify"),
            data={
                "request_id": request_id,
                "otp": otp,
            },
        )
        self.assertEqual(res.status_code, 200, res.content)
        self.assertIn("access_token", res.json())
        token = res.json()["access_token"]
        res = self.client.get(
            path=reverse("iam:getme"),
            headers={
                "Authorization": token,
            },
        )
        self.assertEqual(res.status_code, 200, res.content)

    @unittest.mock.patch("iam.integrations.email.email_client.send")
    def test_edit_user(self, email_sender):
        email = "example@example.com"
        password = "password"
        user_id = self.create_user(email, password, email_sender)
        # Login to get token
        res = self.client.post(
            path=reverse("iam:login"),
            data={
                "email": email,
                "password": password,
            },
        )
        self.assertEqual(res.status_code, 200, res.content)
        token = res.json()["access_token"]

        # Update password
        new_password = "new_password"
        res = self.client.put(
            path=reverse("iam:update_password"),
            data={
                "email": email,
                "password": new_password,
            },
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 403, res.content)

        res = self.client.put(
            path=reverse("iam:update_password"),
            data={
                "email": email,
                "password": new_password,
            },
            headers={
                "Authorization": token,
            },
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200, res.content)

        # Try logging in with old password - should fail
        res = self.client.post(
            path=reverse("iam:login"),
            data={
                "email": email,
                "password": password,
            },
        )
        self.assertEqual(res.status_code, 401, res.content)

        # Try logging in with new password - should succeed
        res = self.client.post(
            path=reverse("iam:login"),
            data={
                "email": email,
                "password": new_password,
            },
        )
        self.assertEqual(res.status_code, 200, res.content)
        self.assertIn("access_token", res.json())
