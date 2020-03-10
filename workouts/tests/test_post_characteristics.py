import json
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.urls import reverse
from workouts.models import Characteristics
from workouts.serializers import CharacteristicsSerializer

class PostCharacteristicsTest(TestCase):

    def setUp(self):
        user = User.objects.create(username="nerd")
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        self.valid_payload = {
            "date": "06092019",
            "week": 7,
            "time": "20:45",
            "toughness": 5,
            "awakeness": 5,
            "anxiety": 5,
            "soreness": 5,
            "enthusiasm": 5
        }
        
        self.invalid_payload = {
            "date":"999",
            "week": 7,
            "time": "20:45:00",
            "toughness": 5,
            "awakeness": 5,
            "anxiety": 5,
            "soreness": 5,
            "enthusiasm": 5
        }

    def test_post_characteristics_by_date(self):
        response = self.client.post(
            reverse("workouts:date_characteristics", kwargs={"date": "06092019"}),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_characteristics_by_invalid_payload(self):
        response = self.client.post(
            reverse("workouts:date_characteristics", kwargs={"date": "06092019"}),
            data=json.dumps(self.invalid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_post_characteristics_by_invalid_date(self):
        response = self.client.post(
            reverse("workouts:date_characteristics", kwargs={"date": "999"}),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_auth_token(self):
        self.no_auth_user = User.objects.create(username="notoken")
        self.no_auth_client = APIClient()
        response = self.no_auth_client.post(
            reverse("workouts:date_characteristics", kwargs={"date": "06092019"}),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
