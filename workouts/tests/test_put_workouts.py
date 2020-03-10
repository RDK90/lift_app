import json
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.urls import reverse
from workouts.models import Training
from workouts.serializers import TrainingSerializer

class PutWorkoutsTest(TestCase):

    def setUp(self):
        user = User.objects.create(username="nerd")
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        self.valid_training = Training.objects.create(
            date="2019-09-16", exercise_category="T1", exercise="Low Bar Squat",
            set_number=1, reps=8, weight=20, rep_category="Warm up"
        )
        self.invalid_training = Training.objects.create(
            date="2019-09-23", exercise_category="T1", exercise="Low Bar Squat",
            set_number=1, reps=8, weight=20, rep_category="Warm up"
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

    def test_put_workout_by_id(self):
        response = self.client.put(
            reverse("workouts:id_workouts", kwargs={"workout_id": self.valid_payload["date"]}),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_invalid_datetype_workout_by_id(self):
        response = self.client.put(
            reverse("workouts:id_workouts", kwargs={"workout_id": self.invalid_payload["date"]}),
            data=json.dumps(self.invalid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_auth_token(self):
        self.no_auth_user = User.objects.create(username="notoken")
        self.no_auth_client = APIClient()
        response = self.no_auth_client.put(
            reverse("workouts:id_workouts", kwargs={"workout_id": self.valid_payload["date"]}),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)