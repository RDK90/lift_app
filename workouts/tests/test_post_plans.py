import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from workouts.models import Plan
from workouts.serializers import PlanSerializer

# initialize the APIClient app
client = Client()

class PostPlansTest(TestCase):

    def setUp(self):
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

    def test_post_plan_by_date(self):
        response = client.post(
            reverse("workouts:date_plans", kwargs={"date":"16092019"}),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_plan_by_invalid_date(self):
        response = client.post(
            reverse("workouts:date_plans", kwargs={"date":"999"}),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_plan_by_invalid_payload(self):
        response = client.post(
            reverse("workouts:date_plans", kwargs={"date":"16092019"}),
            data=json.dumps(self.invalid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)