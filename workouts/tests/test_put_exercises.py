import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from workouts.models import Training
from workouts.serializers import TrainingSerializer

# initialize the APIClient app
client = Client()

class PutExercisesTest(TestCase):

    def setUp(self):
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

    def test_put_exercise_by_name(self):
        response = client.put(
            reverse("workouts:name_exercises", kwargs={"exercise_name": self.valid_payload["exercise"]}),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_put_invalid_exercise_by_name(self):
        response = client.put(
            reverse("workouts:name_exercises", kwargs={"exercise_name": self.invalid_payload["exercise"]}),
            data=json.dumps(self.invalid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_invalid_data_exercise_by_name(self):
        response = client.put(
            reverse("workouts:name_exercises", kwargs={"exercise_name": self.valid_payload["exercise"]}),
            data=json.dumps({"random": "stuff"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)