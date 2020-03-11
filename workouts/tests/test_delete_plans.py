import json
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from workouts.models import Plan
from workouts.serializers import PlanSerializer
from django.contrib.auth.models import User

class DeletePlanssTest(TestCase):

    def setUp(self):
        user = User.objects.create(username="nerd")
        self.client = APIClient()
        self.client.force_authenticate(user=user)

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
        response = self.client.delete(
            reverse("workouts:date_plans", kwargs={"date":"25032019"})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_plan_by_invalid_date(self):
        response = self.client.delete(
            reverse("workouts:date_plans", kwargs={"date":"999"})
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_auth_token(self):
        self.no_auth_user = User.objects.create(username="notoken")
        self.no_auth_client = APIClient()
        response = self.no_auth_client.delete(
            reverse("workouts:date_plans", kwargs={"date":"25032019"})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
