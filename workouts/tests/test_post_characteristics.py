import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from workouts.models import Characteristics
from workouts.serializers import CharacteristicsSerializer

# initialize the APIClient app
client = Client()

class PostCharacteristicsTest(TestCase):

    def setUp(self):
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
        response = client.post(
            reverse("workouts:date_characteristics", kwargs={"date": "06092019"}),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_characteristics_by_invalid_payload(self):
        response = client.post(
            reverse("workouts:date_characteristics", kwargs={"date": "06092019"}),
            data=json.dumps(self.invalid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_post_characteristics_by_invalid_date(self):
        response = client.post(
            reverse("workouts:date_characteristics", kwargs={"date": "999"}),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)