import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from workouts.models import Plan
from workouts.serializers import PlanSerializer

# initialize the APIClient app
client = Client()

class DeletePlanssTest(TestCase):

    def setUp(self):
        Plan.objects.create(
            id=2, date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=1, reps=8, weight=20, rep_category="Warm up"
        )
        Plan.objects.create(
            id=3, date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=2, reps=4, weight=70, rep_category="Work"
        )
        Plan.objects.create(
            id=4, date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=3, reps=4, weight=110, rep_category="Work"
        )
        Plan.objects.create(
            id=5, date="2019-03-25", exercise_category="T1", exercise="Low Bar Squat",
            set_number=4, reps=4, weight=120, rep_category="Work"
        )

    def test_delete_plan_by_date(self):
        response = client.delete(
            reverse("workouts:date_plans", kwargs={"date":"25032019"})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_plan_by_invalid_date(self):
        response = client.delete(
            reverse("workouts:date_plans", kwargs={"date":"999"})
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
