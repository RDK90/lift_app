import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from workouts.models import Characteristics
from workouts.serializers import CharacteristicsSerializer

# initialize the APIClient app
client = Client()

class DeleteCharacteristicsTest(TestCase):

    def setUp(self):
        self.valid_characteristics = Characteristics.objects.create(
            date="2019-06-09", week=8, time="20:45", toughness=7,
            awakeness=7, anxiety=2, soreness=2, enthusiasm=5
        )
        self.invalid_characteristics = Characteristics.objects.create(
            date="2019-07-09", week=8, time="20:45", toughness=7,
            awakeness=7, anxiety=2, soreness=2, enthusiasm=5
        )

    def test_delete_characteristics_by_date(self):
        response = client.delete(
            reverse("workouts:date_characteristics", kwargs={"date":"06092019"})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_characteristics_by_invalid_date(self):
        response = client.delete(
            reverse("workouts:date_characteristics", kwargs={"date":"999"})
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    