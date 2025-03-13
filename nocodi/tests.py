from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class LivenessViewTests(TestCase):

    def test_liveness_check(self):
        """Test that liveness check returns 200 OK with correct response"""
        response = self.client.get(reverse("liveness"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"status": "ok"})
