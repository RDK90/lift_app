import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from workouts.models import Training
from workouts.serializers import TrainingSerializer


class TestExercises(TestCase):

	def setUp(self):
		user = User.objects.create(username="nerd")
		self.client = APIClient()
		self.client.force_authenticate(user=user)

		Training.objects.create(
			date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
			set_number=1, reps=8, weight=20, rep_category="Warm up"
		)
		Training.objects.create(
			date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
			set_number=2, reps=4, weight=70, rep_category="Work"
		)
		Training.objects.create(
			date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
			set_number=3, reps=4, weight=110, rep_category="Work"
		)
		Training.objects.create(
			date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
			set_number=4, reps=4, weight=120, rep_category="Work"
		)

		self.valid_training = Training.objects.create(
			date="2019-09-16", exercise_category="T1", exercise="Low Bar Squat",
			set_number=1, reps=8, weight=20, rep_category="Warm up"
		)
		self.invalid_training = Training.objects.create(
			date="2019-09-23", exercise_category="T1", exercise="Low Bar Squat",
			set_number=1, reps=8, weight=20, rep_category="Warm up"
		)
		self.valid_payload = {
			"exercise": "Low Bar Squat",
			"workout": [
				{
					"exercise_category": "T1",
					"date": "16092019",
					"set_number": 1,
					"reps": 4,
					"weight": 60,
					"rep_category": "Warm up"
				},
				{
					"exercise_category": "T1",
					"date": "16092019",
					"set_number": 1,
					"reps": 4,
					"weight": 90,
					"rep_category": "Warm up"
				}
			]
		}
		self.invalid_payload = {
			"exercise": "Unknown",
			"workout": [
				{
					"exercise_category": "T1",
					"date": "16092019",
					"set_number": 1,
					"reps": 4,
					"weight": 60,
					"rep_category": "Warm up"
				},
				{
					"exercise_category": "T1",
					"date": "16092019",
					"set_number": 1,
					"reps": 4,
					"weight": 90,
					"rep_category": "Warm up"
				}
			]
		}

	def test_get_exercise_by_name(self):
		response = self.client.get(reverse('workouts:name_exercises', kwargs={'exercise_name':'Low Bar Squat'}))
		exercise_data = Training.objects.filter(exercise="Low Bar Squat").values()
		serializer = TrainingSerializer(exercise_data, many=True)
		self.assertEqual(response.data['exercise'], serializer.data[0]['exercise'])
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_get_exercise_by_invalid_name(self):
		response = self.client.get(reverse('workouts:name_exercises', kwargs={'exercise_name':'Unknown Exercise'}))
		exercise_data = Training.objects.filter(exercise="Unknown Exercise").values()
		serializer = TrainingSerializer(exercise_data, many=True)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_get_exercise_no_auth_token(self):
		self.no_auth_user = User.objects.create(username="notoken")
		self.no_auth_client = APIClient()
		response = self.no_auth_client.get(reverse('workouts:name_exercises', kwargs={'exercise_name':'Low Bar Squat'}))
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_put_exercise_by_name(self):
		response = self.client.put(
			reverse("workouts:name_exercises", kwargs={"exercise_name": self.valid_payload["exercise"]}),
			data=json.dumps(self.valid_payload),
			content_type="application/json"
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
	
	def test_put_invalid_exercise_by_name(self):
		response = self.client.put(
			reverse("workouts:name_exercises", kwargs={"exercise_name": self.invalid_payload["exercise"]}),
			data=json.dumps(self.invalid_payload),
			content_type="application/json"
		)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_put_invalid_data_exercise_by_name(self):
		response = self.client.put(
			reverse("workouts:name_exercises", kwargs={"exercise_name": self.valid_payload["exercise"]}),
			data=json.dumps({"random": "stuff"}),
			content_type="application/json"
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_put_exercise_no_auth_token(self):
		self.no_auth_user = User.objects.create(username="notoken")
		self.no_auth_client = APIClient()
		response = self.no_auth_client.put(
			reverse("workouts:name_exercises", kwargs={"exercise_name": self.valid_payload["exercise"]}),
			data=json.dumps(self.valid_payload),
			content_type="application/json"
		)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def tearDown(self):
		User.objects.filter(username="nerd").delete()
		Training.objects.filter(
			date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
			set_number=1, reps=8, weight=20, rep_category="Warm up"
		).delete()
		Training.objects.filter(
			date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
			set_number=2, reps=4, weight=70, rep_category="Work"
		).delete()
		Training.objects.filter(
			date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
			set_number=3, reps=4, weight=110, rep_category="Work"
		).delete()
		Training.objects.filter(
			date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
			set_number=4, reps=4, weight=120, rep_category="Work"
		).delete()
		Training.objects.filter(
			date="2019-09-16", exercise_category="T1", exercise="Low Bar Squat",
			set_number=1, reps=8, weight=20, rep_category="Warm up"
		).delete()
		Training.objects.filter(
			date="2019-09-23", exercise_category="T1", exercise="Low Bar Squat",
			set_number=1, reps=8, weight=20, rep_category="Warm up"
		).delete()
