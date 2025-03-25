from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class LivenessViewTests(TestCase):

    def test_liveness_check(self):
        response = self.client.get(reverse("liveness"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_local_cache_check(self):
        response = self.client.get(reverse("schema"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.has_header("X-Local-Cache"))

        response = self.client.get(reverse("schema"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.headers.get("X-Local-Cache"), "HIT")
