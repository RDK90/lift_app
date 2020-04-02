import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from workouts.views import login


class LoginTest(TestCase):

    def setUp(self):
        user = User.objects.create_user(username="nerd", password="password")
        self.client = APIClient()

        self.valid_payload = {
            "username": "nerd",
            "password": "password"
        }

        self.invalid_credentials = {
            "username": "nerd",
            "password": "nerdpass"
        }

        self.invalid_payload = {
            "username": "nerd",
        }

    def test_login(self):
        response = self.client.post(
            reverse("workouts:login"),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_login_credentials(self):
        response = self.client.post(
            reverse("workouts:login"),
            data=json.dumps(self.invalid_credentials),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_login_payload(self):
        response = self.client.post(
            reverse("workouts:login"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
