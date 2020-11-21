import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from workouts.models import PlanVersionTwo, Profile
from workouts.serializers import PlanSerializer

class TestPlansVersionTwo(TestCase):

	def setUp(self):
		test_user = User.objects.create(username="nerd")
		self.user = Profile.objects.create(user=test_user)
		self.client = APIClient()
		self.client.force_authenticate(user=test_user)

		PlanVersionTwo.objects.create(
			user=self.user, date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
			set_number=1, reps=8, weight=20, rep_category="Warm up"
		)
		PlanVersionTwo.objects.create(
			user=self.user, date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
			set_number=2, reps=4, weight=70, rep_category="Work"
		)
		PlanVersionTwo.objects.create(
			user=self.user, date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
			set_number=3, reps=4, weight=110, rep_category="Work"
		)
		PlanVersionTwo.objects.create(
			user=self.user, date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
			set_number=4, reps=4, weight=120, rep_category="Work"
		)

		self.valid_payload = {
			"date": "16092019",
			"workout": [
				{
					"exercise_category": "T1",
					"exercise": "Squat",
					"set_number": 1,
					"reps": 4,
					"weight": 60,
					"rep_category": "Warm up"
				},
				{
					"exercise_category": "T1",
					"exercise": "Squat",
					"set_number": 1,
					"reps": 4,
					"weight": 90,
					"rep_category": "Warm up"
				}
			]
		}

		self.invalid_payload = {
			"date": "999",
			"workout": [
				{
					"exercise_category": "T1",
					"exercise": "Squat",
					"set_number": 1,
					"reps": 4,
					"weight": 60,
					"rep_category": "Warm up"
				},
				{
					"exercise_category": "T1",
					"exercise": "Squat",
					"set_number": 1,
					"reps": 4,
					"weight": 90,
					"rep_category": "Warm up"
				}
			]
		}

	def test_get_all_plans(self):
		response = self.client.get(reverse('workouts:all_plans_v2'))
		plan_data = PlanVersionTwo.objects.all()
		serializer = PlanSerializer(plan_data, many=True)
		self.assertEqual(response.data[0]['date'], serializer.data[0]['date'])
		self.assertEqual(response.status_code, status.HTTP_200_OK)