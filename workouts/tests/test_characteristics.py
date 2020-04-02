import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from workouts.models import Characteristics
from workouts.serializers import CharacteristicsSerializer


class TestCharacteristics(TestCase):

	def setUp(self):
		user = User.objects.create(username="nerd")
		self.client = APIClient()
		self.client.force_authenticate(user=user)

		# Create data in Characteristics table to test GET methods
		Characteristics.objects.create(
			date="2019-03-25", week=1, time="21:00:00",
			toughness=5, awakeness=5, anxiety=5, soreness=5, enthusiasm=5
		)
		Characteristics.objects.create(
			date="2019-03-26", week=1, time="21:00:00",
			toughness=2, awakeness=2, anxiety=2, soreness=2, enthusiasm=2
		)
		Characteristics.objects.create(
			date="2019-03-27", week=1, time="21:00:00",
			toughness=3, awakeness=4, anxiety=4, soreness=5, enthusiasm=8
		)
		Characteristics.objects.create(
			date="2019-03-28", week=1, time="21:00:00",
			toughness=1, awakeness=4, anxiety=2, soreness=5, enthusiasm=9
		)

		# Create Characteristics objects to delete to test DELETE methods
		self.valid_characteristics = Characteristics.objects.create(
			date="2019-06-09", week=8, time="20:45", toughness=7,
			awakeness=7, anxiety=2, soreness=2, enthusiasm=5
		)
		self.invalid_characteristics = Characteristics.objects.create(
			date="2019-07-09", week=8, time="20:45", toughness=7,
			awakeness=7, anxiety=2, soreness=2, enthusiasm=5
		)

		# Create input data to test PUT/POST methods
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
			"time": "20:45",
			"toughness": 5,
			"awakeness": 5,
			"anxiety": 5,
			"soreness": 5,
			"enthusiasm": 5
		}

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

	def test_get_characteristics_no_auth_token(self):
		self.no_auth_user = User.objects.create(username="notoken")
		self.no_auth_client = APIClient()
		response = self.no_auth_client.get(reverse('workouts:date_characteristics', kwargs={'date':'25032019'}))
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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

	def test_post_characteristics_no_auth_token(self):
		self.no_auth_user = User.objects.create(username="notoken")
		self.no_auth_client = APIClient()
		response = self.no_auth_client.post(
			reverse("workouts:date_characteristics", kwargs={"date": "06092019"}),
			data=json.dumps(self.valid_payload),
			content_type="application/json"
		)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_put_characteristics_by_date(self):
		response = self.client.put(
			reverse("workouts:date_characteristics", kwargs={"date": "06092019"}),
			data=json.dumps(self.valid_payload),
			content_type="application/json"
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_put_characteristics_by_invalid_date(self):
		response = self.client.put(
			reverse("workouts:date_characteristics", kwargs={"date": "999"}),
			data=json.dumps(self.invalid_payload),
			content_type="application/json"
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_put_characteristics_by_invalid_payload(self):
		response = self.client.put(
			reverse("workouts:date_characteristics", kwargs={"date": "07062019"}),
			data=json.dumps(self.invalid_payload),
			content_type="application/json"
		)
		self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
	
	def test_put_characteristics_no_auth_token(self):
		self.no_auth_user = User.objects.create(username="notoken")
		self.no_auth_client = APIClient()
		response = self.no_auth_client.put(
			reverse("workouts:date_characteristics", kwargs={"date": "06092019"}),
			data=json.dumps(self.valid_payload),
			content_type="application/json"
		)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_delete_characteristics_by_date(self):
		response = self.client.delete(
			reverse("workouts:date_characteristics", kwargs={"date":"06092019"})
		)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
	
	def test_delete_characteristics_by_invalid_date(self):
		response = self.client.delete(
			reverse("workouts:date_characteristics", kwargs={"date":"999"})
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_delete_characteristics_no_auth_token(self):
		self.no_auth_user = User.objects.create(username="notoken")
		self.no_auth_client = APIClient()
		response = self.no_auth_client.delete(
			reverse("workouts:date_characteristics", kwargs={"date":"06092019"})
		)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def tearDown(self):
		User.objects.filter(username="nerd").delete()
		Characteristics.objects.filter(
			date="2019-03-25", week=1, time="21:00:00",
			toughness=5, awakeness=5, anxiety=5, soreness=5, enthusiasm=5
		).delete()
		Characteristics.objects.filter(
			date="2019-03-25", week=1, time="21:00:00",
		 	toughness=5, awakeness=5, anxiety=5, soreness=5, enthusiasm=5
		).delete()
		Characteristics.objects.filter(
			date="2019-03-26", week=1, time="21:00:00",
			toughness=2, awakeness=2, anxiety=2, soreness=2, enthusiasm=2
		).delete()
		Characteristics.objects.filter(
			date="2019-03-27", week=1, time="21:00:00",
			toughness=3, awakeness=4, anxiety=4, soreness=5, enthusiasm=8
		).delete()
		Characteristics.objects.filter(
			date="2019-03-28", week=1, time="21:00:00",
			toughness=1, awakeness=4, anxiety=2, soreness=5, enthusiasm=9
		).delete()
		Characteristics.objects.filter(
			date="2019-06-09", week=8, time="20:45", toughness=7,
			awakeness=7, anxiety=2, soreness=2, enthusiasm=5
		).delete()
		Characteristics.objects.filter(
			date="2019-07-09", week=8, time="20:45", toughness=7,
			awakeness=7, anxiety=2, soreness=2, enthusiasm=5
		).delete()
