import json
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from workouts.models import Characteristics
from workouts.serializers import CharacteristicsSerializer
from django.contrib.auth.models import User


class GetCharacteristicsTest(TestCase):

    def setUp(self):
        user = User.objects.create(username="nerd")
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        Characteristics.objects.create(
            id=2, date="2019-03-25", week=1, time="21:00:00",
            toughness=5, awakeness=5, anxiety=5, soreness=5, enthusiasm=5
        )
        Characteristics.objects.create(
            id=3, date="2019-03-26", week=1, time="21:00:00",
            toughness=2, awakeness=2, anxiety=2, soreness=2, enthusiasm=2
        )
        Characteristics.objects.create(
            id=4, date="2019-03-27", week=1, time="21:00:00",
            toughness=3, awakeness=4, anxiety=4, soreness=5, enthusiasm=8
        )
        Characteristics.objects.create(
            id=5, date="2019-03-28", week=1, time="21:00:00",
            toughness=1, awakeness=4, anxiety=2, soreness=5, enthusiasm=9
        )

    def test_get_characteristics_by_date(self):
        response = self.client.get(reverse('workouts:date_characteristics', kwargs={'date':'25032019'}))
        characterisitics_data = Characteristics.objects.filter(date="2019-03-25").values()
        serializer = CharacteristicsSerializer(characterisitics_data, many=True)
        self.assertEqual(response.data[0]['date'], serializer.data[0]['date'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_characteristics_by_invalid_datetype(self):
        response = self.client.get(reverse('workouts:date_characteristics', kwargs={'date':'999'}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_characteristics_by_invalid_date(self):
        response = self.client.get(reverse('workouts:date_characteristics', kwargs={'date':'22032019'}))
        characterisitics_data = Characteristics.objects.filter(date="2019-03-22").values()
        serializer = CharacteristicsSerializer(characterisitics_data, many=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_no_auth_token(self):
        self.no_auth_user = User.objects.create(username="notoken")
        self.no_auth_client = APIClient()
        response = self.no_auth_client.get(reverse('workouts:date_characteristics', kwargs={'date':'25032019'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
